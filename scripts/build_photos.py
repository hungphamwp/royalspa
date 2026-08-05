#!/usr/bin/env python3
"""Fill the page's photographic slots from the customer's own media.

Sources live in `_nguon-anh/` (the Drive download, kept out of `images/` so the
deliverable doesn't ship 2GB of raw footage). Most stills are HEIC, which no
browser renders, and several services — triệt lông, gội đầu, massage, detox —
were only ever filmed, never photographed, so their stills are pulled out of
the videos via QuickLook.

Every slot is cropped to the aspect ratio the stylesheet actually paints it at.
The CSS uses `background-size: cover`, so handing it a mismatched ratio would
silently crop heads or signage out of frame; cropping here, with an explicit
focus point per slot, keeps the subject centred.
"""
import os
import subprocess
import tempfile

import numpy as np
from PIL import Image, ImageOps, ImageStat

# Slots dimmer than this get auto-levelled. The gội-đầu and massage rooms were
# filmed under very low light — those frames land near 40/255, where the white
# caption printed over them is unreadable.
DARK_LIMIT = 90

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_nguon-anh")
IMG = os.path.join(ROOT, "images")

A = "Ảnh gốc"
V_GOI = "Gội"
V_TRIET = "Triệt lông"
V_DETOX = "DETOX"
V_COVAIGAY = "_ Video/Cổ vai gáy"

# slot -> (source, WxH, focus)
# focus: vertical bias of the crop window, 0.0 = top .. 1.0 = bottom.
#
# Sources are matched to each slot's orientation. Only 22 of the ~140 stills are
# genuinely landscape once EXIF rotation is applied, so the wide slots draw from
# that short list; forcing a portrait phone photo into a 2:1 banner throws away
# ~60% of its height and was what made these blocks look mis-framed.
PLAN = {
    # hero — calm, bright treatment room; headline text is overlaid on top of it
    # The customer's Facebook cover is the brand's own key visual — logo, chân
    # dung chủ spa, tagline and partner marks in one frame — so it is the banner.
    # TRANGCHU carries no overlaid text, so nothing competes with it.
    "hero-banner-desktop.jpg": ("Avatar - Cover/Ảnh bìa Royal Spa by Trang Huynh.png",
                                (1440, 712), 0.5, 0.55),
    # Mobile paints TRANGCHU at 420x632 — a 0.66:1 *portrait* box, not the 1.21:1
    # the stylesheet's nominal size suggests. A 2.63:1 cover cannot be cropped
    # into that without losing most of it, and letterboxing leaves dead ivory
    # bands, so the mobile banner is recomposed vertically from the same artwork.
    "hero-banner-mobile.jpg":  ("mobilebanner:", (768, 1156), 0.5),

    # 4 square tiles under the hero intro: không gian, chuyên viên, khách, cơ sở
    "hero-gallery-1.jpg": (f"{A}/IMG_6883.HEIC", (600, 600), 0.5),
    "hero-gallery-2.jpg": (f"{A}/IMG_9091.HEIC", (600, 600), 0.5),
    "hero-gallery-3.jpg": (f"{A}/IMG_9108.HEIC", (600, 600), 0.5),
    "hero-gallery-4.jpg": (f"{A}/Spa/_._/IMG_0358.JPG", (600, 600), 0.5),

    # 10 service cards (16:9) — order fixed by TDD 3.4, all landscape sources
    "service-01.jpg": (f"{A}/IMG_9279.HEIC", (720, 405), 0.5),          # chăm sóc da cơ bản
    "service-02.jpg": (f"{A}/IMG_3387.HEIC", (720, 405), 0.5),          # chăm sóc da chuyên sâu
    "service-03.jpg": (f"{A}/IMG_3388.HEIC", (720, 405), 0.5),          # combo mặt & cổ
    "service-04.jpg": (f"{A}/IMG_6878.HEIC", (720, 405), 0.5),          # aqua peeling
    "service-05.jpg": (f"{A}/IMG_9120.HEIC", (720, 405), 0.5),          # laser toning
    "service-06.jpg": (f"{A}/IMG_8505.JPG", (720, 405), 0.5),           # điều trị mụn chuyên sâu
    "service-07.jpg": (f"vid:{V_TRIET}/1JMQ8N5R3_61O9Q4.mp4", (1080, 604), 0.5),   # triệt lông
    "service-08.jpg": (f"vid:{V_GOI}/1JM86D3JQ_61O9Q4.mp4", (1080, 604), 0.42),    # gội đầu
    "service-09.jpg": (f"vid:{V_COVAIGAY}/1JODFBP6Q_61O9Q4.mp4", (1080, 604), 0.5),  # massage đầu
    "service-10.jpg": (f"vid:{V_DETOX}/1J5GCR1DS_61O9Q4.mp4", (1080, 604), 0.5),   # detox
    # Three more so the six "trải nghiệm giá tốt" cards stop repeating each
    # other: the block had gội-đầu twice and the same massage frame twice.
    "service-11.jpg": (f"vid:{V_GOI}/1JM883U5K_61O9Q4.mp4", (600, 814), 0.45),     # gội phục hồi
    "service-12.jpg": (f"vid:{V_COVAIGAY}/1JODEOQMB_61O9Q4.mp4", (600, 814), 0.5), # massage lưng
    "service-13.jpg": (f"vid:{V_GOI}/1JM8689LQ_61O9Q4.mp4", (600, 814), 0.42),     # gội thảo dược

    # người tư vấn (chủ spa) + avatar nhỏ trên thanh promo
    "consultant-photo.jpg": ("Avatar - Cover/IMG_7306.JPG", (460, 460), 0.0),
    "bod.jpeg":             ("Avatar - Cover/IMG_7306.JPG", (200, 200), 0.0),

    # HOẠT ĐỘNG TẠI ROYAL SPA — carousel, 2:1 landscape
    "trai-nghiem-khach-hang-1.jpg":                         (f"{A}/IMG_0602.HEIC", (1280, 648), 0.5),
    "412972196-753102780196210-670028661699914443-n-1.jpg": (f"{A}/IMG_0645.HEIC", (1280, 648), 0.5),
    "415226550-756874179819070-3244573965065649515-n.jpg":  (f"{A}/IMG_3507.HEIC", (1280, 648), 0.5),
    "415254840-756874153152406-438359351930390222-n.jpg":   (f"{A}/IMG_4617.JPG", (1280, 648), 0.5),
    "416138640-761033932736428-9071160629185595640-n.jpg":  (f"{A}/IMG_6879.HEIC", (1280, 648), 0.5),
    "416558486-759908876182267-5920374145598890621-n.jpg":  (f"{A}/IMG_9309.HEIC", (1280, 648), 0.5),
    "416683153-759908829515605-6469412522089706723-n.jpg":  (f"{A}/IMG_9452.JPG", (1280, 648), 0.5),
    "416710410-759908982848923-2770817965731378380-n.jpg":  (f"{A}/Spa/_._/IMG_9514.HEIC", (1280, 648), 0.5),
    "416710824-759908839515604-5511287744794537422-n.jpg":  ("_ Ảnh/IMG_0280.JPG", (1280, 648), 0.35),
    "artboard-1.jpg":                                       ("_ Ảnh/IMG_0317.JPG", (1280, 648), 0.35),

    # KHÔNG GIAN LÀM ĐẸP — portrait tiles, all portrait sources
    "2c.jpg":                (f"{A}/IMG_6207.JPG", (700, 900), 0.5),
    "3b.jpg":                (f"{A}/IMG_8503.JPG", (700, 900), 0.5),
    "3d.jpg":                (f"{A}/IMG_9254.HEIC", (700, 900), 0.5),
    "3f.jpg":                (f"{A}/IMG_9453.JPG", (700, 900), 0.5),
    "4c.jpg":                (f"{A}/Ngày 29-3/IMG_1690.HEIC", (700, 900), 0.5),
    "artboard-2-copy.jpg":   (f"{A}/Ngày 29-3/IMG_1691.HEIC", (700, 900), 0.5),
    "artboard-2-copy-6.jpg": (f"{A}/Ngày 29-3/IMG_1695.HEIC", (700, 900), 0.5),
    "artboard-2-copy-7.jpg": (f"{A}/Ngày 29-3/IMG_1699.HEIC", (700, 900), 0.5),
    "artboard-2-copy-9.jpg": (f"{A}/IMG_8502.JPG", (700, 900), 0.5),
}


def load(spec):
    """Open a source still, decoding HEIC and video frames via macOS tools.

    Every still is passed through exif_transpose: most of these iPhone frames
    carry Orientation=6 (rotate 90°) and store the pixels un-rotated, so reading
    them raw lands the subject on its side — which is exactly how the spa photos
    ended up sideways on the page.
    """
    if spec.startswith("vid:"):
        path = os.path.join(SRC, spec[4:])
        tmp = tempfile.mkdtemp()
        subprocess.run(["qlmanage", "-t", "-s", "1400", "-o", tmp, path],
                       capture_output=True, check=False)
        made = [f for f in os.listdir(tmp) if f.endswith(".png")]
        if not made:
            raise RuntimeError(f"no frame extracted from {spec}")
        return ImageOps.exif_transpose(Image.open(os.path.join(tmp, made[0]))).convert("RGB")

    path = os.path.join(SRC, spec)
    if spec.lower().endswith(".heic"):
        tmp = tempfile.mktemp(suffix=".jpg")
        subprocess.run(["sips", "-s", "format", "jpeg", path, "--out", tmp],
                       capture_output=True, check=True)
        return ImageOps.exif_transpose(Image.open(tmp)).convert("RGB")
    return ImageOps.exif_transpose(Image.open(path)).convert("RGB")


def lift_if_dark(im):
    """Gamma-lift a frame that is too dark to carry white text.

    Gamma rather than per-channel autocontrast: autocontrast stretches R, G and
    B independently, which swung the blue-lit laser room hard towards yellow.
    A shared curve raises the level while leaving the colour balance intact.
    """
    mean = ImageStat.Stat(im.convert("L")).mean[0]
    if mean >= DARK_LIMIT or mean <= 1:
        return im
    gamma = min(2.2, DARK_LIMIT / mean)
    lut = [round(255 * (i / 255) ** (1 / gamma)) for i in range(256)]
    return im.point(lut * len(im.getbands()))


# --- colour harmonisation -----------------------------------------------
# The library is shot across half a dozen rooms under wildly different light:
# the laser room is lit violet, the detox clip is a turmeric mask under warm
# tungsten, the massage clip has a teal towel filling the frame. Dropped side
# by side on a champagne page they read as a mismatched set rather than one
# spa, which is what "màu chưa đạt" was pointing at.
#
# Two gentle moves, both deliberately partial — the point is to bring the set
# onto a common axis, not to repaint it. Pushed to 1.0 this is just autocontrast
# again, which is what turned the laser room yellow last time.
CHROMA_LIMIT = 0.34   # mean per-pixel saturation the page tolerates
CHROMA_FLOOR = 0.62   # never remove more than 38% of an image's chroma
CAST_PULL = 0.35      # how far a colour cast moves toward the page's warm grey
WARM_NEUTRAL = (1.015, 1.000, 0.975)   # the ivory ground's own channel balance


def harmonize(im):
    """Clamp runaway chroma and pull a colour cast partway to warm neutral."""
    a = np.asarray(im).astype(np.float32)
    lum = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2])[..., None]

    mx, mn = a.max(2), a.min(2)
    sat = ((mx - mn) / np.maximum(mx, 1.0)).mean()
    if sat > CHROMA_LIMIT:
        a = lum + (a - lum) * max(CHROMA_FLOOR, CHROMA_LIMIT / sat)

    m = a.reshape(-1, 3).mean(0)
    if m.mean() > 8:                     # a near-black frame has no cast to read
        target = np.array(WARM_NEUTRAL, np.float32)
        target *= m.mean() / target.mean()
        gain = 1.0 + (target / np.maximum(m, 1.0) - 1.0) * CAST_PULL
        a *= gain
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")


# The brand artwork is already on-palette and is the one thing that must not be
# re-graded — its cream field is the reference everything else is pulled toward.
NO_GRADE = {"hero-banner-desktop.jpg", "hero-banner-mobile.jpg"}


COVER = "Avatar - Cover/Ảnh bìa Royal Spa by Trang Huynh.png"
PORTRAIT = "Avatar - Cover/IMG_7306.JPG"


def mobile_banner(size, ground=(253, 251, 247)):
    """Portrait banner rebuilt from the cover: brand block over the portrait."""
    W, H = size
    canvas = Image.new("RGB", (W, H), ground)

    cover = load(COVER)
    cw, ch = cover.size
    # the cover's right-hand block: lockup, "Spa 5 sao", flags and partner marks
    # start at 40%: "Spa 5 sao / TIÊU CHUẨN HÀN QUỐC" begins around there, and a
    # later start clips it to "5 sao / ÊU CHUẨN".
    block = cover.crop((int(cw * 0.40), int(ch * 0.02), int(cw * 0.975), int(ch * 0.99)))
    bw = W
    bh = max(1, round(block.height * bw / block.width))
    block = block.resize((bw, bh), Image.LANCZOS)
    canvas.paste(block, (0, 0))

    # the owner's portrait fills whatever height is left
    rest = H - bh
    if rest > 40:
        p = crop_to(load(PORTRAIT), (W, rest), focus=0.0)
        canvas.paste(p, (0, bh))
    return canvas


def fit_on_ivory(im, size, ground=(253, 251, 247)):
    """Letterbox `im` onto an ivory ground instead of cropping it."""
    W, H = size
    scale = min(W / im.width, H / im.height)
    w, h = max(1, round(im.width * scale)), max(1, round(im.height * scale))
    canvas = Image.new("RGB", (W, H), ground)
    canvas.paste(im.resize((w, h), Image.LANCZOS), ((W - w) // 2, (H - h) // 2))
    return canvas


def crop_to(im, size, focus=0.5, hfocus=0.5):
    """`focus` biases a vertical trim, `hfocus` a horizontal one (0 = left).

    The cover art needs the horizontal bias: it is 2.63:1 and the hero boxes are
    2.02:1 and 1.21:1, so a plain centre crop would cut the wordmark or the
    partner logos off one end.
    """
    tw, th = size
    target = tw / th
    w, h = im.size
    if w / h > target:                      # too wide: trim sides
        nw = round(h * target)
        x = round((w - nw) * hfocus)
        box = (x, 0, x + nw, h)
    else:                                   # too tall: trim top/bottom
        nh = round(w / target)
        y = round((h - nh) * focus)
        box = (0, y, w, y + nh)
    return im.crop(box).resize(size, Image.LANCZOS)


def main():
    os.makedirs(IMG, exist_ok=True)
    ok = 0
    for name, entry in PLAN.items():
        spec, size, focus = entry[0], entry[1], entry[2]
        hfocus = entry[3] if len(entry) > 3 else 0.5
        try:
            # Lift after cropping: brightness has to be judged on the region that
            # actually ships, not on parts of the frame that get cut away.
            if spec.startswith("mobilebanner:"):
                out = mobile_banner(size)
            elif spec.startswith("fit:"):
                out = fit_on_ivory(load(spec[4:]), size)
            else:
                out = lift_if_dark(crop_to(load(spec), size, focus, hfocus))
            if name not in NO_GRADE:
                out = harmonize(out)
        except Exception as e:                       # noqa: BLE001 - report and continue
            print(f"  !! {name}: {e}")
            continue
        dest = os.path.join(IMG, name)
        if name.lower().endswith(".png"):
            out.save(dest)
        else:
            out.save(dest, "JPEG", quality=86, optimize=True)
        ok += 1
    print(f"{ok}/{len(PLAN)} ảnh đã dựng vào images/")


if __name__ == "__main__":
    main()
