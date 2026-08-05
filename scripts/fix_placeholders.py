#!/usr/bin/env python3
"""Regenerate images/*.jpg|.png placeholders as real raster bytes.

localize_images.py wrote one SVG payload to every expected image path so
empty slots would look intentional. That works when a browser sniffs file
content (some file:// loads), but any real HTTP server sets
Content-Type from the extension (image/jpeg for .jpg, image/png for .png).
Browsers then refuse to decode SVG XML served as image/jpeg — the whole
hero/gallery/service grid renders blank the moment this page is opened
through an actual web server instead of double-clicked from Finder.

This rewrites every placeholder whose bytes don't match its extension into
a genuine raster image with the same look (pink background, dashed
border, "ROYAL SPA / Anh cho thay" caption), so the placeholder renders
correctly everywhere until the customer drops in real photos under the
same filename. Files already replaced with real photos (content matches
extension) are left untouched.
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "images")

BG = (247, 228, 234)
BORDER = (217, 169, 187)
TITLE = (153, 24, 61)
SUBTITLE = (184, 116, 140)

RASTER_EXTS = {".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG"}

# PRD muc 5 rows 1 and 22: these two slots are layered decoratively over
# other content (logo over header bar, badge over a promo popup image) and
# are specced "nen trong suot" (transparent background). An opaque
# placeholder here doesn't just look wrong, it blots out whatever sits
# underneath it — e.g. badge-slogan.png fully hides the "tri tham nach
# 499k" popup artwork it's supposed to decorate. Keep these transparent.
TRANSPARENT_NAMES = {"logo.png", "badge-slogan.png"}


def is_svg_text(path):
    with open(path, "rb") as f:
        head = f.read(200)
    return head.lstrip().startswith(b"<svg")


def make_placeholder(path, fmt, transparent=False):
    w, h = 800, 500
    if transparent:
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    else:
        img = Image.new("RGB" if fmt == "JPEG" else "RGBA", (w, h), BG if fmt == "JPEG" else BG + (255,))
    draw = ImageDraw.Draw(img)
    draw.rectangle([12, 12, w - 12, h - 12], outline=BORDER, width=3)
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 34)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 22)
    except OSError:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    def center_text(y, text, font, color):
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        draw.text(((w - tw) / 2, y), text, font=font, fill=color)

    center_text(225, "ROYAL SPA", font_title, TITLE)
    center_text(275, "Anh cho thay", font_sub, SUBTITLE)
    img.save(path, format=fmt)


def main():
    fixed, skipped = [], []
    for name in sorted(os.listdir(IMG_DIR)):
        path = os.path.join(IMG_DIR, name)
        ext = os.path.splitext(name)[1].lower()
        fmt = RASTER_EXTS.get(ext)
        if not fmt:
            continue
        if is_svg_text(path):
            make_placeholder(path, fmt, transparent=name in TRANSPARENT_NAMES)
            fixed.append(name)
        else:
            skipped.append(name)
    print(f"Regenerated {len(fixed)} placeholder(s) as real {'/'.join(set(RASTER_EXTS.values()))}.")
    print(f"Left {len(skipped)} file(s) untouched (already real images).")


if __name__ == "__main__":
    main()
