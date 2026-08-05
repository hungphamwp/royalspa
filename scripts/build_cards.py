#!/usr/bin/env python3
"""Render the page's text-bearing graphics in Royal Spa's own wording.

Whole sections of this LadiPage export carry no HTML text at all — the price
grid, the "trải nghiệm giá tốt" strip, the promo popups and the section titles
are single images with the copy baked into the pixels. Rewriting the DOM text
therefore cannot touch them; they have to be re-rendered.

Every string here comes from the customer's content doc (services, durations,
prices, the giờ-vàng window and the triệt-lông warranty), so the rendered
prices match the page copy rather than the Seoul Center originals they replace.

Photographs are pulled from images/ (already built by build_photos.py) so the
cards show the real treatment they name.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "images")

# Royal Spa palette — champagne gold on ivory.
# PLUM/PLUM_DK keep their names because every call site means "primary fill" /
# "darkest fill"; the values mirror what recolor_gold.py writes into the CSS.
PLUM = (208, 180, 131)     # #d0b483 — primary champagne fill
PLUM_DK = (196, 164, 106)  # #c4a46a — deeper champagne (bars)
GOLD = (122, 95, 42)       # #7a5f2a — deep bronze-gold, readable on ivory
GOLD_LT = (176, 141, 87)   # #b08d57 — antique gold hairline
GOLD_PALE = (227, 207, 156)  # #e3cf9c — soft gilt on dark
CREAM = (253, 251, 247)    # #fdfbf7 — ivory
WHITE = (255, 255, 255)
INK = (58, 45, 18)         # #3a2d12 — espresso body text

# The page's own typeface. Rendering these graphics in Arial made every baked-in
# caption visibly different from the live text next to it; SVN-Gilroy is what the
# stylesheet actually loads, and all four weights carry full Vietnamese coverage.
_FONTS = os.path.join(ROOT, "fonts")
F_REG = os.path.join(_FONTS, "svn-gilroy-regular-20230920033046-9er9g.otf")
F_BOLD = os.path.join(_FONTS, "svn-gilroy-bold-20230920033037-pirse.otf")
F_XBOLD = os.path.join(_FONTS, "svn-gilroy-xbold-20230920033046-faeub.otf")
F_BLACK = os.path.join(_FONTS, "svn-gilroy-heavy-20230920033037-eygn7.otf")

# --- metallic gilding -------------------------------------------------------
# Stops mirror the CSS ramp in gild_overrides.py so rendered plates and the
# live gradients read as the same metal.
GILT_STOPS = [(0.00, (191, 159, 101)), (0.22, (230, 213, 172)), (0.42, (246, 239, 221)),
              (0.60, (220, 199, 154)), (0.80, (196, 164, 106)), (1.00, (226, 208, 168))]


def gilt(size, stops=GILT_STOPS, angle=135):
    """A diagonal metallic-gold gradient the size of `size`."""
    W, H = size
    n = max(W, H) * 2
    row = Image.new("RGB", (n, 1))
    px = row.load()
    for x in range(n):
        t = x / (n - 1)
        for i in range(len(stops) - 1):
            a, b = stops[i], stops[i + 1]
            if a[0] <= t <= b[0]:
                k = 0 if b[0] == a[0] else (t - a[0]) / (b[0] - a[0])
                px[x, 0] = tuple(round(a[1][j] + (b[1][j] - a[1][j]) * k) for j in range(3))
                break
        else:
            px[x, 0] = stops[-1][1]
    band = row.resize((n, n), Image.BILINEAR).rotate(angle, resample=Image.BILINEAR)
    left, top = (n - W) // 2, (n - H) // 2
    return band.crop((left, top, left + W, top + H))


def gilt_rounded(size, radius, outline=None, width=0):
    """Gilt gradient clipped to a rounded rectangle, as an RGBA layer."""
    W, H = size
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, W - 1, H - 1], radius, fill=255)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.paste(gilt((W, H)), (0, 0), mask)
    if outline and width:
        ImageDraw.Draw(layer).rounded_rectangle([0, 0, W - 1, H - 1], radius,
                                                outline=outline + (255,), width=width)
    return layer


def font(path, size):
    return ImageFont.truetype(path, max(1, int(size)))


def text_w(d, s, f):
    b = d.textbbox((0, 0), s, font=f)
    return b[2] - b[0]


def centre(d, cx, y, s, f, fill):
    d.text((cx - text_w(d, s, f) / 2, y), s, font=f, fill=fill)


def fit(d, s, path, size, max_w, floor=10):
    """Largest size at or below `size` whose rendering of `s` fits `max_w`."""
    f = font(path, size)
    while f.size > floor and text_w(d, s, f) > max_w:
        f = font(path, f.size - 1)
    return f


def fit_all(d, strings, path, size, max_w, floor=10):
    """One size that fits every string — for grids of sibling cards.

    `fit` sizes each label independently, which is right for a lone caption but
    wrong for a set: in the CAM KẾT grid it left five cards at 16px and the one
    with the longest title at 12px, so the block read as uneven.
    """
    return min((fit(d, s, path, size, max_w, floor) for s in strings),
               key=lambda f: f.size)


def wrap(d, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if text_w(d, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def photo(name, size):
    """Cover-crop a already-built photo to `size`."""
    im = Image.open(os.path.join(IMG, name)).convert("RGB")
    tw, th = size
    t = tw / th
    w, h = im.size
    if w / h > t:
        nw = round(h * t)
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = round(w / t)
        im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    return im.resize(size, Image.LANCZOS)


def shade(im, strength=0.55, frm=0.35):
    """Darken the lower part of a photo so text stays readable over it."""
    w, h = im.size
    ov = Image.new("L", (1, h), 0)
    for y in range(h):
        p = (y / h - frm) / max(1e-6, 1 - frm)
        ov.putpixel((0, y), int(max(0, min(1, p)) * 255 * strength))
    mask = ov.resize((w, h))
    dark = Image.new("RGB", (w, h), (28, 22, 10))
    return Image.composite(dark, im, mask)


def scrim(im, top_frac, strength=0.94):
    """Opaque-ish gradient behind the caption block.

    These rooms are white curtains and pale walls, so a soft full-card fade left
    the captions sitting on near-white pixels. Anchoring a dedicated scrim to
    where the text actually starts keeps the photo bright above it and the
    caption readable below.
    """
    w, h = im.size
    y0 = max(0, min(h - 1, int(h * top_frac)))
    col = Image.new("L", (1, h), 0)
    for y in range(y0, h):
        p = (y - y0) / max(1, h - y0)
        col.putpixel((0, y), int(255 * strength * (p ** 0.62)))
    dark = Image.new("RGB", (w, h), (26, 20, 9))
    return Image.composite(dark, im, col.resize((w, h)))


def rounded(im, radius):
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius, fill=255)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste(im.convert("RGB"), (0, 0), mask)
    return out


# ---------------------------------------------------------------- service card
def service_card(size, photo_name, title, price, note=None, badge=None):
    W, H = size
    base = photo(photo_name, (W, H))
    d0 = ImageDraw.Draw(base)
    f_title = font(F_BOLD, max(13, int(W * 0.098)))
    f_price = fit(d0, price, F_BLACK, max(15, int(W * 0.125)), W * 0.86)
    f_note = font(F_REG, max(10, int(W * 0.070)))
    if note:
        f_note = fit(d0, note, F_REG, f_note.size, W * 0.90)

    lines = wrap(d0, title.upper(), f_title, W * 0.86)
    lh = f_title.size + int(W * 0.018)
    block = len(lines) * lh + f_price.size + int(W * 0.05)
    if note:
        block += f_note.size + int(W * 0.02)
    y = H - block - int(H * 0.055)

    card = scrim(base, max(0.0, (y - H * 0.10) / H))
    card = rounded(card, int(W * 0.06))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle([0, 0, W - 1, H - 1], int(W * 0.06), outline=GOLD_LT, width=max(2, W // 110))
    for ln in lines:
        centre(d, W / 2, y, ln, f_title, WHITE)
        y += lh
    y += int(W * 0.022)
    centre(d, W / 2, y, price, f_price, GOLD_PALE)
    y += f_price.size + int(W * 0.02)
    if note:
        centre(d, W / 2, y, note, f_note, (226, 218, 200))

    if badge:
        f_b = font(F_BOLD, max(10, int(W * 0.062)))
        bw = text_w(d, badge, f_b) + int(W * 0.10)
        bh = f_b.size + int(W * 0.055)
        bx, by = int(W * 0.05), int(W * 0.05)
        d.rounded_rectangle([bx, by, bx + bw, by + bh], bh // 2, fill=PLUM)
        centre(d, bx + bw / 2, by + (bh - f_b.size) / 2 - 1, badge, f_b, WHITE)
    return card


def title_strip(size, main, sub=None, bg="cream", plate=False, band=None):
    """`plate` draws a plum pill behind the words, for titles that sit on a photo.
    `band` confines the drawing to a vertical slice, leaving the rest clear so a
    strip that geometrically overlaps neighbouring cards doesn't cover them."""
    W, H = size
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    if band:
        top, bot = int(H * band[0]), int(H * band[1])
        inner = title_strip((W, bot - top), main, sub, bg, plate)
        canvas.paste(inner, (0, top), inner)
        return canvas
    if plate:
        canvas.paste(gilt_rounded((W, H), int(H * 0.24)), (0, 0),
                     gilt_rounded((W, H), int(H * 0.24)))
        d = ImageDraw.Draw(canvas)
    f_main = fit(d, main.upper(), F_BLACK, max(16, int(H * (0.42 if sub else 0.52))), W * 0.94)
    f_sub = fit(d, sub, F_REG, max(12, int(H * 0.22)), W * 0.94) if sub else None
    colour = INK if (plate or bg != "cream") else GOLD
    y = int(H * 0.12) if sub else (H - f_main.size) / 2 - int(H * 0.06)
    centre(d, W / 2, y, main.upper(), f_main, colour)
    if sub:
        centre(d, W / 2, y + f_main.size + int(H * 0.10), sub, f_sub,
               (74, 54, 10) if (plate or bg != "cream") else GOLD)
    return canvas


def offer_bar(size, left_text, right_text, top=0.0, hole=(0.42, 0.58)):
    """A plum bar with its copy placed left and right of a reserved centre gap."""
    W, H = size
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    y0 = int(H * top)
    bar = gilt_rounded((W, H - y0), int((H - y0) * 0.22), outline=GOLD, width=3)
    canvas.paste(bar, (0, y0), bar)
    d = ImageDraw.Draw(canvas)
    # No strapline here: the button covers the bar down to 90% of its height, so a
    # second line would sit underneath it.
    bh = H - y0
    slot = W * hole[0] - W * 0.05
    f = fit(d, max(left_text, right_text, key=len), F_BLACK, int(bh * 0.32), slot)
    cy = y0 + (bh - f.size) / 2 - bh * 0.12
    centre(d, W * hole[0] / 2, cy, left_text, f, INK)
    centre(d, W * (1 + hole[1]) / 2, cy, right_text, f, INK)
    return canvas


def promo_card(size, photo_name, headline, price, lines=(), radius_frac=0.05, band=None):
    """`band` = (top, bottom) as fractions, limiting where copy may sit.

    Some of these images are the popup's full background with a lead form
    overlaid on the lower half, so vertically centred copy would sit underneath
    the name/phone inputs. Passing the form's start keeps the text clear of it.
    """
    W, H = size
    card = photo(photo_name, (W, H))
    card = shade(card, 0.80, 0.02)
    card = rounded(card, int(W * radius_frac))
    d = ImageDraw.Draw(card)
    top_f, bot_f = band if band else (0.0, 1.0)
    zone_top, zone_h = H * top_f, H * (bot_f - top_f)

    f_h = font(F_BLACK, max(16, int(W * 0.082)))
    f_p = fit(d, price, F_BLACK, max(20, int(W * 0.135)), W * 0.88)
    f_l = font(F_REG, max(11, int(W * 0.052)))
    if lines:
        f_l = fit(d, max(lines, key=len), F_REG, f_l.size, W * 0.90)

    def layout(fh, fp, fl):
        hl = wrap(d, headline.upper(), fh, W * 0.88)
        return hl, len(hl) * (fh.size + 6) + fp.size + int(W * 0.06) + len(lines) * (fl.size + 6)

    # The promo slots differ wildly in shape (2.4:1 down to 0.85:1). Shrink until
    # the whole block clears the card, otherwise the last line falls off the edge.
    hl, total = layout(f_h, f_p, f_l)
    while total > zone_h * 0.92 and f_h.size > 12:
        f_h = font(F_BLACK, f_h.size - 1)
        f_p = font(F_BLACK, max(14, f_p.size - 2))
        f_l = font(F_REG, max(10, f_l.size - 1))
        hl, total = layout(f_h, f_p, f_l)
    y = zone_top + (zone_h - total) / 2
    for ln in hl:
        centre(d, W / 2, y, ln, f_h, WHITE)
        y += f_h.size + 6
    y += int(W * 0.03)
    centre(d, W / 2, y, price, f_p, GOLD_PALE)
    y += f_p.size + int(W * 0.03)
    for ln in lines:
        centre(d, W / 2, y, ln, f_l, (226, 218, 200))
        y += f_l.size + 6
    return card


def backdrop(size, photo_name):
    """A quiet, heavily-dimmed photo panel for popups that stack content on top."""
    W, H = size
    card = photo(photo_name, (W, H))
    veil = Image.new("RGB", (W, H), (250, 245, 234))
    card = Image.blend(card, veil, 0.72)
    return rounded(card, int(min(W, H) * 0.04))


def badge_slogan(size):
    W, H = size
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    pad = int(W * 0.04)
    d.rounded_rectangle([pad, pad, W - pad, H - pad], int(H * 0.18), fill=PLUM + (235,))
    d.rounded_rectangle([pad + 6, pad + 6, W - pad - 6, H - pad - 6], int(H * 0.16),
                        outline=GOLD_LT + (255,), width=3)
    f1 = font(F_BLACK, int(H * 0.135))
    f2 = font(F_BOLD, int(H * 0.105))
    centre(d, W / 2, H * 0.26, "ROYAL SPA", f1, CREAM)
    centre(d, W / 2, H * 0.26 + f1.size + 4, "BY TRANG HUỲNH", font(F_BOLD, int(H * 0.085)), GOLD_LT)
    for i, ln in enumerate(["NÂNG NIU", "VẺ ĐẸP TỰ NHIÊN"]):
        centre(d, W / 2, H * 0.58 + i * (f2.size + 6), ln, f2, CREAM)
    return canvas


def plain_panel(size, main, sub=None, fill=PLUM, radius=0.04, ink=INK):
    W, H = size
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    if fill is CREAM:
        d.rounded_rectangle([0, 0, W - 1, H - 1], int(min(W, H) * radius), fill=CREAM + (255,),
                            outline=GOLD + (255,), width=max(2, H // 60))
    else:
        r = int(min(W, H) * radius)
        lay = gilt_rounded((W, H), r, outline=GOLD, width=max(2, H // 60))
        canvas.paste(lay, (0, 0), lay)
        d = ImageDraw.Draw(canvas)
    f1 = fit(d, main.upper(), F_BLACK, max(14, int(H * 0.20)), W * 0.82)
    centre(d, W / 2, H * (0.32 if sub else 0.5) - (0 if sub else f1.size * 0.62), main.upper(), f1, ink)
    if sub:
        f2 = font(F_REG, max(11, int(H * 0.10)))
        centre(d, W / 2, H * 0.58, sub, f2, GOLD_LT)
    return canvas


def save(im, name):
    p = os.path.join(IMG, name)
    if name.lower().endswith((".jpg", ".jpeg")):
        im.convert("RGB").save(p, "JPEG", quality=90, optimize=True)
    else:
        im.save(p)


def main():
    # ---- BẢNG GIÁ (SECTION2682): 8 cards @ 266x420 + heading strip
    grid = [
        ("triet-long-10-buoi.png", "service-07.jpg", "Triệt lông công nghệ cao", "10 buổi", "Bảo hành 1 năm", "HOT"),
        ("tri-mun.png", "service-06.jpg", "Điều trị mụn chuyên sâu", "400.000đ", "60 phút", None),
        ("meso-ko-kim.png", "service-04.jpg", "Aqua Peeling", "200.000đ", "30 phút", None),
        ("collagen-organic-fix-ten.png", "service-01.jpg", "Chăm sóc da cơ bản", "300.000đ", "60 phút", None),
        ("cham-soc-da-cao-cap.png", "service-02.jpg", "Chăm sóc da chuyên sâu", "500.000đ", "60 phút", None),
        ("tri-nam.png", "service-05.jpg", "Laser Toning", "300.000đ", "30 phút", None),
        ("phun-may-799k.png", "service-03.jpg", "Combo mặt & cổ", "650.000đ", "60 phút", None),
        ("phun-moi-collagen-799k.png", "service-10.jpg", "Detox thải độc da", "600.000đ", "60 phút", "ĐỘC QUYỀN"),
    ]
    for name, ph, title, price, note, badge in grid:
        save(service_card((400, 630), ph, title, price, note, badge), name)
    save(title_strip((764, 112), "Bảng giá dịch vụ", "Royal Spa By Trang Huỳnh"),
         "text-dic-vu-duoc-uey-thich.png")

    # ---- TRẢI NGHIỆM GIÁ TỐT (UUDAI_79K): 6 cards @ 200x271 + title + CTA + strip
    cheap = [
        ("xu-ly-nhan-mun.png", "service-13.jpg", "Gội đầu thảo dược", "60.000đ", "30 phút", None),
        ("triet-long-nach-mep-3-buoi.png", "service-11.jpg", "Gội phục hồi tóc", "100.000đ", "45 phút", None),
        ("tam-body.png", "service-09.jpg", "Gội thư giãn cổ vai gáy", "99.000đ", "09:00 - 14:00 · T2 - T6", "GIỜ VÀNG"),
        ("giam-mo-dtox-dong-y.png", "service-04.jpg", "Aqua Peeling", "200.000đ", "30 phút", None),
        ("ha-luxury-tre-hoa-toan-dien.png", "service-12.jpg", "Massage cổ vai gáy", "250.000đ", "45 phút", None),
        ("ro-tai-tao-mo-ecm.png", "service-01.jpg", "Chăm sóc da cơ bản", "300.000đ", "60 phút", None),
    ]
    for name, ph, title, price, note, badge in cheap:
        save(service_card((300, 407), ph, title, price, note, badge), name)
    save(title_strip((598, 128), "Trải nghiệm giá tốt", "Ưu đãi dành cho khách hàng mới"), "title-phu.png")
    # Sits on the plum strip below, so it is cream-on-plum rather than plum-on-plum.
    save(plain_panel((400, 214), "Xem chi tiết", None, CREAM, 0.28, ink=GOLD), "cta.png")
    # 1200x314 box with two neighbours inside it: the bottom price cards hang
    # 112px into its top, and the "Xem chi tiết" button covers 500..700 x 176..283.
    # So the plum bar starts below the cards and the copy is split either side of
    # the button rather than centred under it.
    # The gap is a fraction of the bar, so it shrinks with the bar on mobile —
    # but the "XEM CHI TIẾT" button on top does not shrink as fast, and at 420px
    # a 20% gap left it covering the ends of both lines. 32% clears the button at
    # both widths (see the mobile width override in gild_overrides.py).
    save(offer_bar((1200, 314), "Mua 5 buổi tặng 1", "Mua 10 buổi tặng 3",
                   top=0.36, hole=(0.34, 0.66)), "hoa-truoc.png")

    # ---- 3 popup khuyến mãi — wording verbatim from section 4 of the content doc
    save(promo_card((792, 462), "service-06.jpg", "Điều trị mụn chuẩn Spa", "Chỉ từ 299.000 VNĐ",
                    ("Không sưng - Không đau",)), "promo-mun-299k.jpg")
    save(promo_card((790, 328), "service-08.jpg", "Gội thư giãn cổ vai gáy", "Chỉ 99.000 VNĐ",
                    ("Áp dụng khung giờ vàng 09:00 - 14:00", "Từ Thứ Hai đến Thứ Sáu")),
         "promo-goi-99k.jpg")
    # In the MIENTRUNG popup the background is almost fully covered: IMAGE4626 sits
    # over its top 285px and the lead form over the rest. So the offer copy goes on
    # IMAGE4626 (badge-slogan.png, below) and this stays a quiet backdrop.
    save(backdrop((634, 744), "service-07.jpg"), "promo-nach-499k.jpg")

    # Popup backdrops. These carry no copy on purpose: each already has its own
    # artwork element plus a lead form stacked on top, so any text baked in here
    # would read through the inputs.
    save(backdrop((634, 710), "consultant-photo.jpg"), "km.png")
    save(backdrop((634, 710), "service-01.jpg"), "1080x6288.png")
    save(backdrop((612, 669), "service-08.jpg"), "avtaytb.png")
    save(backdrop((897, 489), "service-02.jpg"), "bg.png")

    # IMAGE4626 — the one element actually visible in the trị-thâm-nách popup,
    # so it carries that offer (PRD 4.4) rather than a generic slogan badge.
    save(promo_card((618, 458), "service-07.jpg", "Trị thâm nách chuyên sâu", "Chỉ 499.000 VNĐ",
                    ("Royal Spa By Trang Huỳnh",), radius_frac=0.06, band=(0.06, 0.94)),
         "badge-slogan.png")
    print("Đã dựng card dịch vụ, popup và badge.")


if __name__ == "__main__":
    main()
