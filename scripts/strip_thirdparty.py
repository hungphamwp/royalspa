#!/usr/bin/env python3
"""Remove the previous brand's third-party tags from the page.

The export still calls out to services that belong to Seoul Center, not to
Royal Spa. Every visitor to this page was loading them, and two of them fire
conversion events into the old brand's ad accounts:

* `app.seoulspa.vn` — a CRM helper script pulled from the previous brand's own
  server. Arbitrary third-party JavaScript with full access to the page and its
  lead forms.
* `s.zzcdn.me/ztr/ztracker.js?id=7056840457216708608` — Zalo Ads pixel; fires a
  `ViewContent` conversion on load.
* `G-6SG2KPP4L6` / `AW-17578293031` / `GTM-KNPPMC4C` — Google Analytics, Google
  Ads and Tag Manager containers.
* `static.cloudflareinsights.com` — the beacon that came along with the HTTrack
  mirror of the old site.
* `fbq('track', 'Lead MỤN', {value: 1500000})` inside the form configs — dead
  (no pixel is initialised) but it is the old brand's campaign copy.

LadiPage's own hosts (w.ladicdn.com, api1.ldpform.com, api.sales.ldpform.net,
a.ladipage.com) are the platform the page runs on and are deliberately kept.

Royal Spa can add its own analytics afterwards; nothing here is replaced with a
substitute, because guessing at someone's tracking IDs is worse than none.

Idempotent: each pattern is gone after the first run.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "index13c1.html")

# label -> pattern. Each must match at most once.
BLOCKS = {
    "Google Analytics + Google Ads":
        r'<script async src="https://www\.googletagmanager\.com/gtag/js\?id=[^"]+"></script>'
        r'<script>window\.dataLayer.*?</script>',
    "Zalo Ads pixel":
        r'<script>!function\(e,t,r,n,c\)\{if\(!e\.ztrq\).*?</script>',
    "Google Tag Manager":
        r"<script>function gtm\(w,d,s,l,i\).*?</script>",
    "Google Tag Manager (noscript)":
        r'<noscript><iframe src="https://www\.googletagmanager\.com/ns\.html\?id=[^"]*"'
        r'[^>]*></iframe></noscript>',
    "CRM app.seoulspa.vn":
        r"<!-- START country phone -->.*?<!-- END country phone -->\s*",
    "Cloudflare Insights":
        r'<script type="module" src="https://static\.cloudflareinsights\.com/[^>]*></script>\s*',
}

# The Facebook event payloads live HTML-escaped inside the LadiPage config, so
# they are matched on the escaped form.
FBQ = r'"bB":"\s*fbq\(&#39;track&#39;, &#39;Lead M[^"]*?","bA"'


def main():
    with open(PAGE, encoding="utf-8") as f:
        html = f.read()

    removed = []
    for label, pat in BLOCKS.items():
        html, n = re.subn(pat, "", html, flags=re.S)
        if n:
            removed.append(f"{label} ({n})")
        assert n <= 1, f"{label}: khớp {n} lần, cần kiểm tra lại"

    html, n = re.subn(FBQ, '"bB":"","bA"', html)
    if n:
        removed.append(f"sự kiện Facebook cũ ({n})")

    if not removed:
        print("Không còn mã theo dõi của thương hiệu cũ.")
        return

    with open(PAGE, "w", encoding="utf-8") as f:
        f.write(html)
    print("Đã gỡ: " + "; ".join(removed))


if __name__ == "__main__":
    main()
