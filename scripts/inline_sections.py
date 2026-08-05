#!/usr/bin/env python3
"""Phase 1 — make the page self-contained.

The LadiPage export ships 12 "global sections" as empty <div>s that the
LadiPage runtime fills at page load by fetching HTML from the original
Seoul Center account's CDN. That means (a) the design isn't actually in
our file, and (b) whatever Seoul Center publishes later shows up on our
page. This inlines the real markup + CSS + interaction config for all 12
so the file owns its own code and never calls out to LadiPage again.

Input : index13c1.original.html + _sections/*.html (downloaded from
        https://g.ladicdn.com/section/<store>-<global_id>.html)
Output: index13c1.inlined.html  (input for phase 2, apply_content.py)
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "index13c1.original.html")
DST = os.path.join(ROOT, "index13c1.inlined.html")
SECTION_DIR = os.path.join(ROOT, "_sections")

with open(SRC, encoding="utf-8") as f:
    html = f.read()

errors = []
merged_config = {}
inlined = 0

section_files = sorted(os.listdir(SECTION_DIR))
for fname in section_files:
    if not fname.endswith(".html"):
        continue
    sid = fname[:-5]
    with open(os.path.join(SECTION_DIR, fname), encoding="utf-8") as f:
        blob = f.read()

    # Strip the CDN wrapper: <div data-id="SID" class="ladi-section-global">…</div>
    wrapper = re.match(
        r'^<div data-id="' + re.escape(sid) + r'"[^>]*class="ladi-section-global">(.*)</div>\s*$',
        blob, re.S)
    if not wrapper:
        errors.append(f"[{sid}] unexpected wrapper format")
        continue
    inner = wrapper.group(1)

    # Pull the interaction config out; it gets merged into the page-level
    # script_event_data so the runtime wires up carousels/popups/forms.
    cfg_match = re.search(r'<script type="application/json">(.*?)</script>', inner, re.S)
    if cfg_match:
        try:
            cfg = json.loads(cfg_match.group(1))
            merged_config.update(cfg)
        except json.JSONDecodeError as e:
            errors.append(f"[{sid}] bad interaction JSON: {e}")
        inner = inner.replace(cfg_match.group(0), "")

    # Drop the publish-time comment (noise).
    inner = re.sub(r'<!--Publish time:[^>]*-->', '', inner)

    # Kill the live-fetch hooks on the inlined section itself.
    inner = re.sub(r'\s*data-global-id="[a-f0-9]+"', '', inner)
    inner = re.sub(r'\s*data-store-id="[a-f0-9]+"', '', inner)

    # Swap the empty placeholder for the real thing.
    placeholder = f'<div id="{sid}" data-global-id="'
    idx = html.find(placeholder)
    if idx == -1:
        errors.append(f"[{sid}] placeholder div not found in page")
        continue
    end = html.find("</div>", idx) + len("</div>")
    html = html[:idx] + inner + html[end:]
    inlined += 1

if errors:
    print("ERRORS — aborting:")
    for e in errors:
        print(" -", e)
    sys.exit(1)

# Merge the collected section configs into the page-level event data.
marker = 'id="script_event_data" type="application/json">'
start = html.find(marker) + len(marker)
end = html.find("</script>", start)
page_cfg = json.loads(html[start:end])
before = len(page_cfg)
page_cfg.update(merged_config)
html = html[:start] + json.dumps(page_cfg, ensure_ascii=False, separators=(",", ":")) + html[end:]

with open(DST, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Inlined {inlined} global sections.")
print(f"script_event_data keys: {before} -> {len(page_cfg)}")
print(f"Remaining data-global-id refs: {html.count('data-global-id')}")
print("Wrote", DST)
