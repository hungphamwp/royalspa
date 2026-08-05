#!/usr/bin/env python3
"""Put Royal Spa's own offers on the lucky wheel, and make them readable.

Two problems in the export, both inherited from the previous brand:

1. The six segment labels still read "VOUCHER 1 TRIỆU" / "VOUCHER GIẢM 200K
   TIỀN MẶT" — Seoul Center's prizes. LadiPage announces the winning label in
   the result popup, so a visitor who spins is told they have won a voucher
   Royal Spa never offered. They are replaced with the three offers the page
   already makes in its own copy (mua 5 tặng 1, mua 10 tặng 3, tư vấn miễn phí),
   each on two opposite segments exactly as the template had it.

2. The wheel's font-size is 0px, so nothing renders and the segments look like
   an unfinished graphic. 11px fits the 42%-wide label track on a 388px wheel.

Idempotent: the new strings are not among the old ones, so re-running is a no-op.
"""
import base64
import os
import re
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "index13c1.html")
WHEEL = "G1761724761034_SPINLUCKY2558"

# old label -> new label. Order round the wheel is preserved, so the three
# prizes still land on alternating segments.
PRIZES = {
    "VOUCHER MUA 1 TẶNG 1": "MUA 5 TẶNG 1",
    "VOUCHER 1 TRIỆU": "MUA 10 TẶNG 3",
    "VOUCHER GIẢM 200K TIỀN MẶT": "TƯ VẤN MIỄN PHÍ",
}

LABEL_RE = re.compile(
    r'(<div class="ladi-spin-lucky-label"[^>]*>)([^<]+)(</div>)')


def main():
    with open(PAGE, encoding="utf-8") as f:
        html = f.read()

    n = 0

    def sub(m):
        nonlocal n
        new = PRIZES.get(m.group(2).strip())
        if not new:
            return m.group(0)
        n += 1
        return m.group(1) + new + m.group(3)

    html = LABEL_RE.sub(sub, html)

    # The markup above is only the server-rendered copy. LadiPage's runtime
    # rebuilds the wheel from `cA` in script_ladipage_run — an array of base64
    # strings, each decoding to "CODE|url-encoded label|url-encoded odds" — and
    # that array is also what the result popup reads. Miss it and the labels
    # revert to Seoul Center's the moment the script runs.
    def recode(m):
        nonlocal c
        try:
            parts = base64.b64decode(m.group(1)).decode().split("|")
        except Exception:                      # noqa: BLE001 - not a cA entry
            return m.group(0)
        if len(parts) != 3:
            return m.group(0)
        new = PRIZES.get(urllib.parse.unquote(parts[1]).strip())
        if not new:
            return m.group(0)
        c += 1
        parts[0] = re.sub(r"[^A-Z0-9]", "", new.upper())[:16] or parts[0]
        parts[1] = urllib.parse.quote(new)
        return '"%s"' % base64.b64encode("|".join(parts).encode()).decode()

    c = 0
    i = html.find('"%s":{' % WHEEL)
    if i != -1:
        j = html.find('"a":"spinlucky"', i)
        end = html.find("}", j) if j != -1 else -1
        if end != -1:
            block = re.sub(r'"([A-Za-z0-9+/]{16,}={0,2})"', recode, html[i:end])
            html = html[:i] + block + html[end:]

    # font-size: 0px -> 11px, only inside this wheel's own rule
    rule = re.compile(r'(#%s > \.ladi-spin-lucky\{[^}]*?font-size:\s*)0px' % WHEEL)
    html, k = rule.subn(r'\g<1>11px', html)

    if not n and not k and not c:
        print("Vòng quay đã chỉnh trước đó — không có gì thay đổi.")
        return

    with open(PAGE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Vòng quay: {n} nhãn HTML, {c} mục cấu hình, {k} lần bật cỡ chữ.")


if __name__ == "__main__":
    main()
