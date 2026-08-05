#!/usr/bin/env python3
"""Derive the Royal Spa brand assets from the customer's Facebook cover art.

The only vector-quality rendition of the logo we were given is baked into
`_nguon-anh/Avatar - Cover/Ảnh bìa Royal Spa by Trang Huynh.png` — a 5000px
cover whose logo sits on a near-white cream field. We key that field out to
recover a transparent lotus-crown + wordmark, then recompose it.

Recomposition (not just a crop) is required because the source lockup is
stacked/portrait while every slot in the page is landscape: the header box is
200x61 (3.3:1) and the footer 261x97 (2.7:1). Dropping the portrait art into
those with `background-size: cover` would crop the wordmark off entirely.

Outputs: logo.png (gold, light backgrounds), logo-am-ban-ngang.png (cream,
the dark footer bar), favicon.png (square crown), og-image.jpg (social card).
"""
import os
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COVER = os.path.join(ROOT, "_nguon-anh", "Avatar - Cover", "Ảnh bìa Royal Spa by Trang Huynh.png")
IMG = os.path.join(ROOT, "images")

GOLD = (166, 124, 26)
ESPRESSO = (58, 42, 8)
CREAM = (253, 251, 246)
PLUM = (166, 124, 26)

# Luminance of the cover's cream field vs. the gold strokes; the ratio between
# them is what turns into alpha.
BG_LUM, INK_LUM = 246.0, 150.0
# Below this alpha a pixel is the cover's decorative swirl bleeding through,
# not logo ink, so it is forced fully transparent.
NOISE_FLOOR = 0.18


def extract_logo():
    src = Image.open(COVER).convert("RGB")
    W, H = src.size
    crop = src.crop((int(W * 0.50), int(H * 0.02), int(W * 0.75), int(H * 0.30)))
    a = np.asarray(crop).astype(np.float32)
    lum = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    alpha = np.clip((BG_LUM - lum) / (BG_LUM - INK_LUM), 0, 1)
    alpha[alpha < NOISE_FLOOR] = 0.0
    alpha = np.clip((alpha - NOISE_FLOOR) / (1 - NOISE_FLOOR), 0, 1)
    rgb = np.broadcast_to(np.array(GOLD, dtype=np.float32), a.shape).copy()
    logo = Image.fromarray(np.dstack([rgb, alpha * 255]).astype(np.uint8), "RGBA")
    return logo.crop(logo.getbbox())


def split(logo):
    """Separate the stacked lockup into crown and wordmark at the ink gap.

    The cut is found rather than hard-coded: keying moves the trimmed bbox by
    a few pixels, and a fixed offset silently slices the top off "ROYAL SPA".
    """
    ink = (np.asarray(logo)[..., 3] > 20).sum(axis=1)
    lo, hi = int(len(ink) * 0.35), int(len(ink) * 0.70)
    cut = lo + int(np.argmin(ink[lo:hi]))
    crown = logo.crop((0, 0, logo.width, cut))
    word = logo.crop((0, cut, logo.width, logo.height))
    return crown.crop(crown.getbbox()), word.crop(word.getbbox())


def tint(im, colour):
    a = np.asarray(im).astype(np.uint8).copy()
    a[..., 0], a[..., 1], a[..., 2] = colour
    return Image.fromarray(a, "RGBA")


def horizontal_lockup(crown, word, height=200, colour=GOLD, ratio=None, pad=0.0):
    """Crown at left, wordmark at right.

    `ratio` pins the canvas to the aspect the slot is painted at, and `pad`
    keeps the artwork inside a safe margin. Both matter because the slots use
    `background-size: cover`: art wider than its box loses its edges, which is
    exactly how the wordmark ends up reading "ROYAL S".
    """
    crown, word = tint(crown, colour), tint(word, colour)
    ch = int(height * 0.86)
    cw = max(1, round(crown.width * ch / crown.height))
    crown = crown.resize((cw, ch), Image.LANCZOS)
    wh = int(height * 0.62)
    ww = max(1, round(word.width * wh / word.height))
    word = word.resize((ww, wh), Image.LANCZOS)

    gap = int(height * 0.10)
    art = Image.new("RGBA", (cw + gap + ww, height), (0, 0, 0, 0))
    art.paste(crown, (0, (height - ch) // 2), crown)
    art.paste(word, (cw + gap, (height - wh) // 2), word)
    if ratio is None and pad == 0.0:
        return art

    inner = 1.0 - 2 * pad
    ch_ = round(height / inner)
    cw_ = round(ch_ * ratio) if ratio else round(art.width / inner)
    scale = min((cw_ * inner) / art.width, (ch_ * inner) / art.height)
    art = art.resize((max(1, round(art.width * scale)), max(1, round(art.height * scale))), Image.LANCZOS)
    canvas = Image.new("RGBA", (cw_, ch_), (0, 0, 0, 0))
    canvas.paste(art, ((cw_ - art.width) // 2, (ch_ - art.height) // 2), art)
    return canvas


def square_icon(crown, size=512, colour=GOLD):
    crown = tint(crown, colour)
    inner = int(size * 0.78)
    w = max(1, round(crown.width * inner / crown.height))
    if w > inner:
        w, h = inner, max(1, round(crown.height * inner / crown.width))
    else:
        h = inner
    crown = crown.resize((w, h), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.paste(crown, ((size - w) // 2, (size - h) // 2), crown)
    return canvas


def og_card(crown, word, size=(1200, 630)):
    from PIL import ImageDraw, ImageFont
    W, H = size
    card = Image.new("RGB", size, CREAM)
    d = ImageDraw.Draw(card)
    d.rectangle([0, 0, W, 10], fill=GOLD)
    d.rectangle([0, H - 10, W, H], fill=GOLD)

    lock = horizontal_lockup(crown, word, height=210)
    lw = min(int(W * 0.62), lock.width)
    lock = lock.resize((lw, max(1, round(lock.height * lw / lock.width))), Image.LANCZOS)
    card.paste(lock, ((W - lock.width) // 2, int(H * 0.22)), lock)

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 38)
    except OSError:
        font = ImageFont.load_default()
    for i, line in enumerate(["CHĂM SÓC DA · ĐIỀU TRỊ MỤN · TRIỆT LÔNG",
                              "GỘI ĐẦU DƯỠNG SINH · MASSAGE THƯ GIÃN"]):
        bb = d.textbbox((0, 0), line, font=font)
        d.text(((W - (bb[2] - bb[0])) / 2, int(H * 0.68) + i * 54), line, font=font, fill=PLUM)
    return card


def main():
    logo = extract_logo()
    crown, word = split(logo)

    # Header paints logo.png at 3.22:1 and the mobile menu at 2.95:1; the footer
    # negative sits in a 2.69:1 box. Match each and keep a margin for the rest.
    # Those bars are now mirror gold (#B8901F), so the on-page lockup is the dark
    # espresso cut — cream-on-gold measures 2.5:1 and disappears at 60px tall,
    # while espresso-on-gold clears 4.9:1. The gold cut stays as the master for
    # light backgrounds and print.
    horizontal_lockup(crown, word, colour=ESPRESSO, ratio=3.05, pad=0.07).save(
        os.path.join(IMG, "logo.png"))
    horizontal_lockup(crown, word, colour=GOLD, ratio=3.05, pad=0.07).save(
        os.path.join(IMG, "logo-gold.png"))
    horizontal_lockup(crown, word, colour=ESPRESSO, ratio=2.69, pad=0.09).save(
        os.path.join(IMG, "logo-am-ban-ngang.png"))
    square_icon(crown).save(os.path.join(IMG, "favicon.png"))
    og_card(crown, word).save(os.path.join(IMG, "og-image.jpg"), quality=90)
    print("logo.png, logo-am-ban-ngang.png, favicon.png, og-image.jpg")


if __name__ == "__main__":
    main()
