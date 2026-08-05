#!/usr/bin/env python3
"""Re-skin the page from Seoul Center's plum/navy to Royal Spa's gold.

The export's palette is the previous brand's: a crimson-plum primary
(#AD1E46 and eight near-duplicates) plus a navy used for headings. Royal Spa's
identity is the gold of the lotus-crown logo, so every one of those hues is
remapped here.

Each replacement is luminance-matched to the colour it replaces — a dark plum
becomes a dark bronze-gold, a bright accent becomes a bright gold — so text that
was readable on a fill stays readable, and the page's contrast relationships
survive the change untouched.

Idempotent: no output value appears as an input key, so re-running is a no-op.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "index13c1.html")

# old hex -> new hex
MAP = {
    # --- Large fills become champagne, not saturated yellow.
    # A big area of #C9A227 reads as mustard; the same hue desaturated and
    # lightened reads as brushed champagne, which is what "sang trọng" means
    # here. The saturated metal is kept for small accents only.
    "99183d": "c4a46a",   # header bar, footer bar
    "ad1e46": "d0b483",   # primary fill
    "ac1e46": "d0b483",
    "ac1d45": "d0b483",
    "af1f45": "d0b483",
    "b31e45": "d6bb8d",
    "b61e4c": "dec69c",   # lightest large fill

    # --- Small accents keep real metal.
    "ca2b58": "b08d57",   # antique gold
    "c9175d": "b08d57",
    "df1855": "c9a227",   # metallic
    "ff0064": "d4af37",
    "e01a1a": "b8860b",
    "ffd4e1": "f6eeda",   # pale pink fill -> pale champagne

    # --- Headings: deep bronze-gold, readable on ivory.
    "012c79": "7a5f2a",
    "051f4d": "5c4720",
    "06397d": "6b5326",
    "15246b": "5c4720",
    "061528": "3d2f15",
    "2e375a": "6b5326",
    "004aad": "9a7b3f",
    "1c00c2": "9a7b3f",
    "0c61f2": "8c6e3f",
    "0a67e9": "8c6e3f",
    "3c72f9": "8c6e3f",
    "016eff": "8c6e3f",

    # --- warm accents
    "f36e36": "c09a52",
    "ef9300": "c9a227",
    "ffbd59": "e3cf9c",
    "fde298": "f2e7c8",
}


def hex_to_rgb(h):
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def luminance(rgb):
    r, g, b = rgb
    return 0.299 * r + 0.587 * g + 0.114 * b


def apply(html):
    total = 0
    report = []
    for old, new in MAP.items():
        o, n = hex_to_rgb(old), hex_to_rgb(new)
        count = 0

        # #rrggbb (either case)
        for form in (old, old.upper()):
            c = html.count("#" + form)
            if c:
                html = html.replace("#" + form, "#" + new)
                count += c

        # rgb(r, g, b) / rgba(r, g, b, a) with flexible spacing
        pat = re.compile(r'rgba?\(\s*%d\s*,\s*%d\s*,\s*%d\s*(,[^)]*)?\)' % o)

        def sub(m):
            tail = m.group(1) or ""
            return ("rgba(%d, %d, %d%s)" % (n + (tail,))) if tail else ("rgb(%d, %d, %d)" % n)

        html, k = pat.subn(sub, html)
        count += k

        if count:
            total += count
            report.append((old, new, count, luminance(o), luminance(n)))
    return html, total, report


def main():
    with open(PAGE, encoding="utf-8") as f:
        html = f.read()

    html, total, report = apply(html)

    if not total:
        print("Không còn màu cũ nào — đã đổi trước đó.")
        return

    with open(PAGE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"{'cũ':>9s} -> {'mới':<9s} {'lần':>5s}   độ sáng cũ→mới")
    for old, new, c, lo, ln in sorted(report, key=lambda r: -r[2]):
        print(f"  #{old} -> #{new} {c:5d}   {lo:5.0f} → {ln:5.0f}")
    print(f"\nTổng: {total} vị trí màu đã đổi sang tông vàng gold.")


if __name__ == "__main__":
    main()
