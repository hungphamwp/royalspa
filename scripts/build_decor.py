#!/usr/bin/env python3
"""Render the remaining decorative / section graphics.

These slots are the last ones still empty after build_photos and build_cards.
They fall into three kinds:

* Blocks whose entire copy lives in the image — the CAM KẾT grid, the quy-trình
  banner and the section titles carry no DOM text at all, so their wording is
  rendered here (taken from the customer's content doc, sections 8 and 9).
* Chrome for the interactive widgets — the lucky-wheel face and its hub, the
  tri-ân voucher art. The labels around them are real DOM text, so the art
  underneath stays deliberately typography-free.
* Flat section backdrops and small footer marks, which just need to sit in the
  brand's cream/plum palette instead of 404-ing.

The DMCA badge is re-drawn as a neutral "bản quyền" mark: the original was a
third-party certification badge belonging to the previous brand, and reusing a
trust seal the customer has not actually registered for would be a false claim.
"""
import math
import os
from PIL import Image, ImageChops, ImageDraw, ImageFilter

from build_cards import (CREAM, GOLD, GOLD_LT, GOLD_PALE, INK, PLUM, PLUM_DK, WHITE, F_BOLD, F_REG, F_XBOLD,
                         gilt, gilt_rounded,
                         centre, fit, fit_all, font, photo, rounded, shade, text_w, wrap)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "images")

CAM_KET = [
    ("Tư vấn trung thực", "Đúng tình trạng, đúng nhu cầu"),
    ("Không phát sinh chi phí", "Báo giá minh bạch từ đầu"),
    ("Mỹ phẩm chính hãng", "Nguồn gốc rõ ràng"),
    ("Vệ sinh vô khuẩn", "Dụng cụ tiệt trùng từng buổi"),
    ("Không chèo kéo", "Khách tự do lựa chọn"),
    ("Đồng hành đến khi hài lòng", "Theo dõi sau liệu trình"),
]

QUY_TRINH = [
    ("01", "Tiếp nhận thông tin"),
    ("02", "Thăm khám - Soi da"),
    ("03", "Tư vấn liệu trình"),
    ("04", "Thực hiện liệu trình"),
    ("05", "Hướng dẫn tại nhà"),
    ("06", "Theo dõi sau dịch vụ"),
]


def save(im, name):
    p = os.path.join(IMG, name)
    if name.lower().endswith((".jpg", ".jpeg")):
        im.convert("RGB").save(p, "JPEG", quality=90, optimize=True)
    else:
        im.save(p)


def soft_bg(size, base=(253, 251, 247), accent=(248, 243, 231)):
    """A near-white ivory wash behind whole sections.

    Kept almost neutral on purpose: the gilt only reads as gilt against a calm,
    bright ground. A heavier beige turned the whole page tan."""
    W, H = size
    small = Image.new("RGB", (16, 16), base)
    d = ImageDraw.Draw(small)
    d.ellipse([-6, -6, 11, 11], fill=accent)
    d.ellipse([9, 8, 22, 22], fill=accent)
    return small.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(2))


def commitments_grid(size):
    W, H = size
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    cols, rows = 3, 2
    cw, ch = W / cols, H / rows
    pad = cw * 0.045
    usable = cw - 4 * pad
    # One size for all six titles and one for all six subtitles: sizing each cell
    # on its own left the longest title visibly smaller than its five neighbours.
    # Titles are allowed two lines, otherwise "Đồng hành đến khi hài lòng" drags
    # the shared size down to 30px and the whole grid shrinks with it.
    f_t = font(F_BOLD, int(ch * 0.175))
    while f_t.size > 12 and any(len(wrap(d, t, f_t, usable)) > 2 for t, _ in CAM_KET):
        f_t = font(F_BOLD, f_t.size - 1)
    f_s = fit_all(d, [s for _, s in CAM_KET], F_REG, int(ch * 0.135), usable)

    lh = f_t.size * 1.16
    top, bot = ch * 0.32, ch - pad          # the band under the tick
    for i, (title, sub) in enumerate(CAM_KET):
        cx = (i % cols) * cw + cw / 2
        cy = (i // cols) * ch
        d.rounded_rectangle([cx - cw / 2 + pad, cy + pad, cx + cw / 2 - pad, cy + ch - pad],
                            int(ch * 0.12), fill=WHITE + (245,), outline=GOLD_LT + (255,), width=2)
        r = ch * 0.10
        d.ellipse([cx - r, cy + ch * 0.16 - r, cx + r, cy + ch * 0.16 + r], fill=PLUM)
        d.line([(cx - r * 0.42, cy + ch * 0.16), (cx - r * 0.10, cy + ch * 0.16 + r * 0.40),
                (cx + r * 0.45, cy + ch * 0.16 - r * 0.38)], fill=WHITE, width=max(2, int(r * 0.24)))

        # Titles hang from a shared top and subtitles sit on a shared bottom, so
        # the two cards whose title runs to a second line still line up with the
        # four that don't. Centring the block instead put every card's text at a
        # different height.
        y = cy + top
        for line in wrap(d, title, f_t, usable):
            centre(d, cx, y, line, f_t, PLUM_DK)
            y += lh
        centre(d, cx, cy + bot - f_s.size - ch * 0.03, sub, f_s, (122, 104, 72))
    return canvas


def process_banner(size):
    W, H = size
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle([0, 0, W - 1, H - 1], int(H * 0.05), fill=CREAM + (255,))
    f_h = fit(d, "QUY TRÌNH CHĂM SÓC CHUẨN TẠI ROYAL SPA", F_BOLD, int(H * 0.085), W * 0.9)
    centre(d, W / 2, H * 0.07, "QUY TRÌNH CHĂM SÓC CHUẨN TẠI ROYAL SPA", f_h, PLUM)
    f_s = font(F_REG, int(H * 0.042))
    centre(d, W / 2, H * 0.07 + f_h.size + H * 0.025, "6 bước khép kín – an toàn, khoa học, cá nhân hoá", f_s, GOLD)

    cols, rows = 3, 2
    top = H * 0.30
    gh = (H - top - H * 0.06) / rows
    gw = W / cols
    pad = gw * 0.05
    f_n = font(F_BOLD, int(gh * 0.30))
    f_t = fit_all(d, [l for _, l in QUY_TRINH], F_BOLD, int(gh * 0.155), gw - 4 * pad)
    for i, (num, label) in enumerate(QUY_TRINH):
        cx = (i % cols) * gw + gw / 2
        cy = top + (i // cols) * gh
        d.rounded_rectangle([cx - gw / 2 + pad, cy + pad * 0.5, cx + gw / 2 - pad, cy + gh - pad * 0.9],
                            int(gh * 0.12), fill=WHITE + (255,), outline=GOLD_LT + (255,), width=2)
        centre(d, cx, cy + gh * 0.14, num, f_n, GOLD)
        centre(d, cx, cy + gh * 0.56, label, f_t, PLUM_DK)
    return canvas


# Both wheel tones stay in the light half of the champagne ramp so one ink
# colour can serve every segment. The template alternated a pale fill with deep
# bronze and printed white labels over both: white on the pale segments measured
# 1.9:1, so half the prizes were unreadable. Espresso clears 5.3:1 on either.
WHEEL_LIGHT = (222, 198, 156)
WHEEL_DARK = (191, 159, 101)


def wheel_face(size):
    """Six alternating segments; the prize labels are DOM text drawn on top."""
    W, H = size
    ss = 4
    big = Image.new("RGBA", (W * ss, H * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    box = [0, 0, W * ss - 1, H * ss - 1]
    for i in range(6):
        fill = WHEEL_LIGHT if i % 2 == 0 else WHEEL_DARK
        d.pieslice(box, i * 60 - 90, (i + 1) * 60 - 90, fill=fill + (255,))
    d.ellipse(box, outline=CREAM + (255,), width=10 * ss)
    r = W * ss * 0.14
    cx = cy = W * ss / 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=CREAM + (255,), outline=GOLD + (255,), width=3 * ss)
    return big.resize((W, H), Image.LANCZOS)


def wheel_hub_svg(path):
    """The hub keeps its .svg extension, so it must be real SVG.

    A server sets Content-Type from the extension; PNG bytes behind a .svg name
    arrive as image/svg+xml and simply fail to decode.
    """
    def rgb(c):
        return "#%02x%02x%02x" % c

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <circle cx="100" cy="100" r="58" fill="{rgb(CREAM)}" stroke="{rgb(PLUM)}" stroke-width="7"/>
  <polygon points="100,16 78,70 122,70" fill="{rgb(PLUM)}"/>
  <text x="100" y="112" text-anchor="middle" font-family="Arial, Helvetica, sans-serif"
        font-size="30" font-weight="bold" fill="{rgb(PLUM)}">QUAY</text>
</svg>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)


def gift_visual(size, photo_name, fade_left=0.0):
    """`fade_left` dissolves the left edge to transparent.

    The "Thay Lời Tri Ân" headline runs 161px underneath this image's left edge;
    without the fade the artwork simply covers the words.
    """
    W, H = size
    card = shade(photo(photo_name, (W, H)), 0.62, 0.30)
    card = rounded(card, int(min(W, H) * 0.06))
    d = ImageDraw.Draw(card)
    f1 = fit(d, "MÓN QUÀ DÀNH TẶNG NGƯỜI THÂN", F_BOLD, int(H * 0.085), W * 0.60)
    centre(d, W * 0.62, H * 0.70, "MÓN QUÀ DÀNH TẶNG NGƯỜI THÂN", f1, WHITE)
    f2 = fit(d, "Royal Spa By Trang Huỳnh", F_REG, int(H * 0.058), W * 0.55)
    centre(d, W * 0.62, H * 0.70 + f1.size + H * 0.03, "Royal Spa By Trang Huỳnh", f2, (245, 222, 232))

    if fade_left > 0:
        # Fully clear across `fade_left`, then ramp up over the next half of it.
        # A ramp that starts at the very edge still tints the tail of the
        # headline; the headline runs 161px (=20% of this box) into the image.
        clear = max(1, int(W * fade_left))
        ramp_px = max(1, int(W * fade_left * 0.5))
        row = Image.new("L", (W, 1), 255)
        for x in range(clear + ramp_px):
            v = 0 if x < clear else (x - clear) / ramp_px
            row.putpixel((x, 0), int(255 * v ** 1.2))
        alpha = card.getchannel("A")
        card.putalpha(ImageChops.multiply(alpha, row.resize((W, H))))
    return card


def gift_seal(size):
    W, H = size
    ss = 3
    big = Image.new("RGBA", (W * ss, H * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    box = [4 * ss, 4 * ss, W * ss - 4 * ss, H * ss - 4 * ss]
    d.ellipse(box, fill=PLUM + (255,))
    d.ellipse([box[0] + 9 * ss, box[1] + 9 * ss, box[2] - 9 * ss, box[3] - 9 * ss],
              outline=GOLD_LT + (255,), width=3 * ss)
    im = big.resize((W, H), Image.LANCZOS)
    d2 = ImageDraw.Draw(im)
    f1 = fit(d2, "TRI ÂN", F_BOLD, int(H * 0.19), W * 0.62)
    f2 = fit(d2, "KHÁCH HÀNG", F_BOLD, int(H * 0.115), W * 0.66)
    f3 = fit(d2, "Royal Spa By Trang Huỳnh", F_REG, int(H * 0.072), W * 0.68)
    centre(d2, W / 2, H * 0.30, "TRI ÂN", f1, INK)
    centre(d2, W / 2, H * 0.30 + f1.size + H * 0.03, "KHÁCH HÀNG", f2, GOLD)
    centre(d2, W / 2, H * 0.66, "Royal Spa By Trang Huỳnh", f3, INK)
    return im


def voucher(size, main="VOUCHER ƯU ĐÃI", sub="Mua 5 tặng 1 · Mua 10 tặng 3", solid=False):
    W, H = size
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    rad = int(H * (0.5 if H < W * 0.3 else 0.16))
    if solid:
        lay = gilt_rounded((W, H), rad, outline=GOLD, width=3)
        canvas.paste(lay, (0, 0), lay)
        d = ImageDraw.Draw(canvas)
    else:
        d.rounded_rectangle([0, 0, W - 1, H - 1], rad, fill=CREAM + (255,),
                            outline=GOLD + (255,), width=3)
    if not sub:
        f1 = fit(d, main, F_BOLD, int(H * 0.46), W * 0.84)
        centre(d, W / 2, (H - f1.size) / 2 - H * 0.06, main, f1, INK if solid else GOLD)
        return canvas
    f1 = fit(d, main, F_BOLD, int(H * 0.30), W * 0.84)
    f2 = fit(d, sub, F_REG, int(H * 0.19), W * 0.86)
    centre(d, W / 2, H * 0.18, main, f1, INK if solid else GOLD)
    centre(d, W / 2, H * 0.56, sub, f2, INK if solid else GOLD)
    return canvas


def hotline_plate(size):
    W, H = size
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    lay = gilt_rounded((W, H), H // 2, outline=GOLD, width=3)
    canvas.paste(lay, (0, 0), lay)
    d = ImageDraw.Draw(canvas)
    f1 = fit(d, "HOTLINE", F_BOLD, int(H * 0.26), W * 0.5)
    f2 = fit(d, "0899 994 509", F_BOLD, int(H * 0.36), W * 0.82)
    centre(d, W / 2, H * 0.16, "HOTLINE", f1, GOLD)
    centre(d, W / 2, H * 0.44, "0899 994 509", f2, INK)
    return canvas


def service_button(size):
    """Blank pill behind each service-card title.

    sdt.png is the button *background* on the ten service cards; the service
    name (HEADLINE3974…) is live DOM text painted on top of it. Anything written
    here collides with that name — which is exactly how "CHĂM SÓC DA CƠ BẢN" and
    "GỌI NGAY" ended up stacked on each other.
    """
    W, H = size
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    lay = gilt_rounded((W, H), H // 2, outline=GOLD, width=max(2, H // 22))
    canvas.paste(lay, (0, 0), lay)
    return canvas


def glyph(size, kind):
    """Tiny footer marks: an ornament rule, a chat bubble, a share node."""
    W, H = size
    ss = 4
    big = Image.new("RGBA", (W * ss, H * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    w, h = W * ss, H * ss
    if kind == "rule":
        # Slim gold rule with a centre diamond — reads as footer trim rather than
        # the stray filled ellipse a plain dot produced at this size.
        y = h / 2
        t = max(1, int(h * 0.035))
        d.line([(w * 0.04, y), (w * 0.38, y)], fill=GOLD_LT + (255,), width=t)
        d.line([(w * 0.62, y), (w * 0.96, y)], fill=GOLD_LT + (255,), width=t)
        r = h * 0.18
        d.polygon([(w / 2, y - r), (w / 2 + r * 0.62, y), (w / 2, y + r), (w / 2 - r * 0.62, y)],
                  fill=GOLD + (255,))
    elif kind == "chat":
        d.rounded_rectangle([w * 0.08, h * 0.10, w * 0.92, h * 0.72], int(w * 0.16), fill=CREAM + (255,))
        d.polygon([(w * 0.30, h * 0.70), (w * 0.30, h * 0.95), (w * 0.52, h * 0.70)], fill=CREAM + (255,))
    else:
        for cx, cy in ((0.24, 0.28), (0.24, 0.72), (0.76, 0.50)):
            d.ellipse([w * (cx - .13), h * (cy - .13), w * (cx + .13), h * (cy + .13)], fill=CREAM + (255,))
        d.line([(w * .24, h * .28), (w * .76, h * .50), (w * .24, h * .72)], fill=CREAM + (255,), width=int(w * .05))
    return big.resize((W, H), Image.LANCZOS)


def copyright_mark(size):
    """Outlined cream mark — a solid white box shouted on the plum footer bar."""
    W, H = size
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle([2, 2, W - 3, H - 3], int(H * 0.22), fill=(255, 255, 255, 210),
                        outline=GOLD + (255,), width=max(2, H // 26))
    f = fit(d, "© ROYAL SPA", F_BOLD, int(H * 0.30), W * 0.80)
    f2 = fit(d, "BẢN QUYỀN NỘI DUNG", F_REG, int(H * 0.18), W * 0.84)
    centre(d, W / 2, H * 0.22, "© ROYAL SPA", f, CREAM)
    centre(d, W / 2, H * 0.58, "BẢN QUYỀN NỘI DUNG", f2, GOLD_LT)
    return canvas


def section_title(size, main, sub, plate=False, band=None):
    from build_cards import title_strip
    return title_strip(size, main, sub, plate=plate, band=band)


def main():
    # section washes
    for name, size in (("1920x800000000.png", (1440, 900)),
                       ("603x900.png", (768, 980)),
                       ("603x9003333.png", (768, 980)),
                       ("asset-1.png", (1440, 708)),
                       ("ds.png", (1440, 74))):
        save(soft_bg(size), name)
    save(soft_bg((1163, 634), (253, 251, 247), (246, 240, 226)), "background.png")

    # CAM KẾT
    # This title is positioned over the layer-36 photo, so it needs its own plate.
    save(section_title((1162, 338), "Cam kết của Royal Spa",
                       "Điều chúng tôi giữ đúng trong từng buổi hẹn", plate=True), "text.png")
    save(commitments_grid((1420, 459)), "group-3dsfsdfs.png")
    save(rounded(shade(photo("service-02.jpg", (872, 864)), 0.30, 0.55), 40), "layer-36.png")

    # QUY TRÌNH (repurposes the old phun-xăm banner slot)
    save(process_banner((1800, 974)), "group-7.png")

    # VÒNG QUAY — group-1.png (the small label) sits at 79%..94% of titlee's box,
    # so the title copy is confined above it.
    save(section_title((1102, 678), "Vòng quay may mắn",
                       "Nhận ưu đãi mỗi ngày cùng Royal Spa", band=(0.0, 0.76)), "titlee.png")
    save(voucher((628, 100), "MUA 5 TẶNG 1 · MUA 10 TẶNG 3", None, solid=True), "group-1.png")
    save(wheel_face((776, 776)), "vong-quay.png")
    wheel_hub_svg(os.path.join(IMG, "spin-btn1.svg"))

    # TRI ÂN NGƯỜI THÂN
    save(gift_visual((1225, 888), "service-02.jpg", fade_left=0.22), "group-10.png")
    save(gift_seal((840, 840)), "group-10-2.png")
    save(voucher((696, 328)), "vc1trbb.png")

    # footer + hotline marks
    save(hotline_plate((502, 150)), "hotline-spa.png")
    save(service_button((610, 82)), "sdt.png")
    save(glyph((238, 90), "rule"), "1e.png")
    save(glyph((136, 156), "chat"), "png-removebg-preview.png")
    save(glyph((196, 196), "share"), "social-media-1.png")
    save(copyright_mark((500, 180)), "dmca-logo-grn-btn100w.png")
    print("Đã dựng ảnh trang trí còn lại.")


if __name__ == "__main__":
    main()
