#!/usr/bin/env python3
"""Phase 3 — stop serving Seoul Center's photos from Seoul Center's CDN.

After phase 1 inlined the real section markup, ~66 distinct images still
point at w.ladicdn.com under Seoul Center's store id. Those are their
photos on their CDN: not ours to publish, and liable to change or vanish
without notice. This rewrites every image reference to a local
images/<slug>.<ext> path, drops a visible placeholder at each path so the
layout still reads, and writes IMAGES.md mapping every slot back to the
original URL so the right replacement can be picked by eye.

Web fonts (svn-gilroy-*.otf) are deliberately left on the CDN — swapping
them would change the typography, which is the one thing we're preserving.

Run after apply_content.py; edits index13c1.html in place.
"""
import os
import re
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "index13c1.html")
IMG_DIR = os.path.join(ROOT, "images")
MANIFEST = os.path.join(ROOT, "IMAGES.md")

os.makedirs(IMG_DIR, exist_ok=True)

with open(PAGE, encoding="utf-8") as f:
    html = f.read()

# Every CDN reference that is an image (fonts stay put).
refs = re.findall(r'url\("(https://w\.ladicdn\.com/[^"]+)"\)', html)
image_refs = [u for u in refs if not u.endswith(".otf")]

# Group by asset basename: the same photo appears at several size prefixes
# (/s550x550/, /s1500x800/ …) and must collapse to one local file.
by_asset = defaultdict(set)
for url in image_refs:
    by_asset[url.rsplit("/", 1)[-1]].add(url)


def slugify(basename):
    """readable-name-from-ladipage-basename.ext"""
    name, ext = os.path.splitext(basename)
    # strip trailing -YYYYMMDDHHMMSS-hash chunks LadiPage appends
    name = re.sub(r'-\d{14}-[a-z0-9_\-]+$', '', name, flags=re.I)
    name = re.sub(r'-\d{14}$', '', name)
    name = re.sub(r'-min$', '', name)
    name = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    name = re.sub(r'-{2,}', '-', name)
    if not name or name.isdigit():
        name = "asset-" + name if name else "asset"
    return name[:60] + (ext.lower() if ext else ".png")


# Resolve slug collisions deterministically.
slugs, used = {}, {}
for basename in sorted(by_asset):
    slug = slugify(basename)
    if slug in used:
        stem, ext = os.path.splitext(slug)
        used[slug] += 1
        slug = f"{stem}-{used[slug]}{ext}"
    used.setdefault(slug, 1)
    slugs[basename] = slug

# Rewrite every reference.
replaced = 0
for basename, urls in by_asset.items():
    target = "images/" + slugs[basename]
    for url in urls:
        n = html.count(f'url("{url}")')
        html = html.replace(f'url("{url}")', f'url("{target}")')
        replaced += n

with open(PAGE, "w", encoding="utf-8") as f:
    f.write(html)

# A single visible placeholder, copied to every expected filename, so empty
# slots look intentional instead of broken while real photos are gathered.
PLACEHOLDER = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500">'
    '<rect width="800" height="500" fill="#f7e4ea"/>'
    '<rect x="12" y="12" width="776" height="476" fill="none" stroke="#d9a9bb" '
    'stroke-width="3" stroke-dasharray="14 10"/>'
    '<text x="400" y="240" font-family="Arial,sans-serif" font-size="34" font-weight="bold" '
    'fill="#99183d" text-anchor="middle">ROYAL SPA</text>'
    '<text x="400" y="290" font-family="Arial,sans-serif" font-size="22" '
    'fill="#b8748c" text-anchor="middle">Ảnh chờ thay</text></svg>'
)
created = 0
# Slots renamed by apply_content.py (hero, logo, service cards, promos…) need
# placeholders too — they're referenced but were never CDN-backed here.
named_slots = sorted(set(re.findall(r'(?:url\("|content="|href=")(images/[^"]+)"', html)))
for rel in named_slots:
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(PLACEHOLDER)   # SVG payload; browsers render it regardless of extension
        created += 1

with open(MANIFEST, "w", encoding="utf-8") as f:
    f.write("# Danh sách hình ảnh cần thay — Royal Spa\n\n")
    f.write("Mỗi dòng là một vị trí ảnh trên trang. File trong `images/` hiện là ảnh "
            "placeholder (nền hồng, chữ \"Ảnh chờ thay\"). Thay bằng ảnh thật của Royal Spa, "
            "**giữ nguyên tên file** là xong — không cần sửa HTML.\n\n")
    f.write("Cột \"Ảnh gốc (tham khảo)\" là ảnh của mẫu Seoul Center ở đúng vị trí đó — mở link "
            "để biết vị trí này cần loại ảnh gì. **Không dùng lại ảnh này**, chỉ để tham khảo bố cục.\n\n")
    named = {"images/" + slugs[b]: sorted(by_asset[b])[0] for b in by_asset}
    f.write(f"Tổng: **{len(named_slots)} ảnh**.\n\n")

    f.write("## A. Ảnh chính (đã đặt tên theo vị trí — ưu tiên thay trước)\n\n")
    f.write("| # | File cần đặt trong `images/` | Dùng ở đâu |\n|---|---|---|\n")
    ROLES = {
        "images/logo.png": "Logo trên header và footer",
        "images/favicon.png": "Icon trên tab trình duyệt",
        "images/og-image.jpg": "Ảnh hiện khi chia sẻ link lên Facebook/Zalo",
        "images/hero-banner-desktop.jpg": "Banner đầu trang (máy tính)",
        "images/hero-banner-mobile.jpg": "Banner đầu trang (điện thoại)",
        "images/hero-gallery-1.jpg": "Ảnh 1 trong dải 4 ảnh dưới phần giới thiệu",
        "images/hero-gallery-2.jpg": "Ảnh 2 trong dải 4 ảnh dưới phần giới thiệu",
        "images/hero-gallery-3.jpg": "Ảnh 3 trong dải 4 ảnh dưới phần giới thiệu",
        "images/hero-gallery-4.jpg": "Ảnh 4 trong dải 4 ảnh dưới phần giới thiệu",
        "images/consultant-photo.jpg": "Ảnh chuyên viên trong popup tư vấn",
        "images/promo-mun-299k.jpg": "Popup ưu đãi điều trị mụn 299k",
        "images/promo-goi-99k.jpg": "Popup ưu đãi gội giờ vàng 99k",
        "images/promo-nach-499k.jpg": "Popup ưu đãi trị thâm nách 499k",
        "images/badge-slogan.png": "Badge slogan trang trí",
    }
    for i in range(1, 11):
        ROLES[f"images/service-{i:02d}.jpg"] = f"Thẻ dịch vụ số {i} trong Thư viện dịch vụ"
    i = 0
    for rel in named_slots:
        if rel in ROLES:
            i += 1
            f.write(f"| {i} | `{os.path.basename(rel)}` | {ROLES[rel]} |\n")

    f.write("\n## B. Ảnh trong các khối lấy từ thiết kế gốc\n\n")
    f.write("Các khối này (bảng giá, cam kết, hoạt động, footer, vòng quay…) giữ nguyên bố cục "
            "thiết kế gốc. Mở link \"tham khảo\" để thấy ảnh gốc ở đúng vị trí đó.\n\n")
    f.write("| # | File cần đặt trong `images/` | Ảnh gốc (tham khảo) |\n|---|---|---|\n")
    j = 0
    for rel in named_slots:
        if rel not in ROLES:
            j += 1
            src = named.get(rel, "")
            link = f"[xem]({src})" if src else "—"
            f.write(f"| {j} | `{os.path.basename(rel)}` | {link} |\n")

print(f"Rewrote {replaced} image references across {len(by_asset)} assets.")
print(f"Created {created} placeholder files in images/.")
print(f"Wrote {MANIFEST}")
remaining = len(re.findall(r'url\("https://w\.ladicdn\.com/(?![^"]*\.otf)', html))
print(f"Remaining non-font CDN image refs: {remaining}")
