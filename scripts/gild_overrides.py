#!/usr/bin/env python3
"""Turn the flat gold into real gilding, and repair the contrast it breaks.

Two jobs, both appended as one stylesheet at the end of <head> so they win on
cascade order without editing a single original rule:

1. *Gradient.* Metallic gold is never one colour — it is a ramp from shadow
   through highlight and back. Every fill that recolor_gold.py painted a flat
   gilt gets a linear-gradient in its place, and the display headings get the
   same ramp clipped to the glyphs, so titles read as polished metal rather
   than mustard text.

2. *Ink.* Gold is a light colour, so labels that used to be white-on-plum land
   as white-on-gold at roughly 2:1. The ID list below is the output of a
   contrast audit run against the live DOM — it walked every text node,
   resolved the fill actually painted behind it (LadiPage paints fills on
   sibling `.ladi-box` / `.ladi-button-background` elements, not on ancestors),
   and kept everything under 4.5:1. Each is re-inked to espresso, or to deep
   gold where that still clears 4.5:1 so headings stay gold.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "index13c1.html")
MARKER = "royalspa-gild-overrides"

ESPRESSO = "#3a2d12"
DEEP_GOLD = "#7a5f2a"
IVORY = "#fdfbf6"

# The gilt values recolor_gold.py writes, as they appear in the stylesheet.
GILT_FILLS = {
    "rgb(196, 164, 106)", "rgb(208, 180, 131)", "rgb(214, 187, 141)",
    "rgb(222, 198, 156)", "rgb(176, 141, 87)", "rgb(201, 162, 39)",
    "rgb(212, 175, 55)", "rgb(184, 134, 11)",
}

# Shadow -> highlight -> shadow. Deep enough at the ends that espresso text on
# top still clears contrast at every point along the ramp.
GRAD_FILL = ("linear-gradient(100deg,#d3bb8d 0%,#f2e8d2 22%,#e4d2a9 42%,"
             "#f6efdd 58%,#e0cca2 78%,#d3bb8d 100%)")
# For glyphs: same metal, shifted darker so it reads on ivory.
GRAD_TEXT = ("linear-gradient(135deg,#6b5326 0%,#a8863f 22%,#c9a227 42%,"
             "#8c6e3f 62%,#b08d57 82%,#6b5326 100%)")

# Display headings that should read as polished metal.
GILD_TEXT_IDS = [
    "HEADLINE3871", "HEADLINE3872",          # hero lockup
    "HEADLINE3971", "HEADLINE3972",          # thư viện dịch vụ
    "G1703818171569_HEADLINE3985",           # không gian làm đẹp
    "G1719394824941_HEADLINE2013",           # hoạt động
    "G1761556313318_HEADLINE3985",           # thay lời tri ân
    "G1761724761034_HEADLINE3993",           # vòng quay
]

# id -> ink, from the contrast audit
INK = {k: ESPRESSO for k in [
    "G1759745653409_GROUP3828", "G1759745653409_HEADLINE3956",
    "G1759745653409_GROUP3829", "G1759745653409_HEADLINE3957",
        "HEADLINE3901", "HEADLINE3902", "HEADLINE3903", "HEADLINE3904", "HEADLINE3905",
    "HEADLINE3906", "BUTTON3436", "BUTTON_TEXT3436",
    "G1755161786222_HEADLINE2906", "G1755161786222_HEADLINE4097",
    "G1761556313318_HEADLINE3986",
    "G1743067768131_BUTTON18", "G1743067768131_BUTTON_TEXT18", "G1743067768131_GROUP11",
    "G1743067768131_FORM4", "G1743067768131_BUTTON16", "G1743067768131_BUTTON_TEXT16",
    "G1743067768131_HEADLINE18", "G1743067768131_BUTTON17", "G1743067768131_BUTTON_TEXT17",
    "G1743067768131_BUTTON19", "G1743067768131_BUTTON_TEXT19",
    "G1743067768131_HEADLINE2891", "G1743067768131_HEADLINE3949",
    "G1743067768131_PARAGRAPH3518", "G1743067768131_GROUP3979", "G1743067768131_HEADLINE4112",
    "G1743067768131_GROUP3980", "G1743067768131_HEADLINE4113", "G1743067768131_GROUP3981",
    "G1743067768131_HEADLINE4114", "G1743067768131_GROUP3982", "G1743067768131_HEADLINE4115",
    # hero CTA, footer strapline, and the running marquee
    "BUTTON3441", "BUTTON_TEXT3441",
    "G1743067768131_HEADLINE2896",
    ]}
INK.update({"G1761724761034_HEADLINE3219": DEEP_GOLD})
# Countdown caption + the four unit labels. #9a7b3f on white measures 3.9:1 and
# these are 13-15px, so they need 4.5:1; deep bronze on white clears 6:1 and
# keeps them gold.
INK.update({k: DEEP_GOLD for k in [
    "G1761556313318_PARAGRAPH3442", "G1761556313318_PARAGRAPH3443",
    "G1761556313318_PARAGRAPH3444", "G1761556313318_PARAGRAPH3445",
    "G1761556313318_PARAGRAPH3446",
]})
# The two tab titles sit on gilt bars. Gilt text on a gilt bar reads as grey mud,
# so they take solid espresso and are kept out of GILD_TEXT_IDS.
INK.update({k: ESPRESSO for k in [
    "GROUP3847", "GROUP3848", "HEADLINE3973",
    "GROUP3861", "GROUP3862", "HEADLINE3980",
]})
# The service chips all sit on fills that receive GRAD_FILL, so the pixels
# behind them are the light end of the champagne ramp — espresso. Only the
# marquee keeps a solid deep-bronze fill, where ivory wins.
INK.update({k: IVORY for k in [
    "G1756351929798_HTML_CODE3247",      # running marquee strip
]})
INK.update({k: ESPRESSO for k in [
    "G1759745653409_GROUP3830", "G1759745653409_HEADLINE3958",
]})
# Caught by the same audit run at 375px. These three only fail on mobile — the
# desktop layout sizes the first as large text and hides the other two — but
# re-inking them is right at both widths.
INK.update({"G1717122335463_HEADLINE3245": DEEP_GOLD})     # 15px on ivory, 3.98:1
INK.update({k: ESPRESSO for k in [
    "G1761556313318_BUTTON1406", "G1761556313318_BUTTON_TEXT1406",   # white on gilt, 1.66:1
    "BUTTON3454", "BUTTON_TEXT3454",                                 # white on gilt, 2.37:1
]})
INK.update({k: ESPRESSO for k in [
    "G1759745653409_GROUP3840", "G1759745653409_GROUP3841", "G1759745653409_GROUP3842",
    "G1759745653409_GROUP3843",
    "G1759745653409_HEADLINE3962", "G1759745653409_HEADLINE3966",
    "G1759745653409_HEADLINE3967",
]})

TEXT_PARTS = ("", " .ladi-headline", " .ladi-paragraph", " .ladi-button-text",
              " h1", " h2", " h3", " h4", " h5", " h6", " p", " span")

# Layout repairs — not caused by the gilding, but by Vietnamese copy being longer
# than the template's original. id -> extra declarations.
LAYOUT = {
    "G1755161786222_BUTTON_TEXT3336":
        ("background-image:none !important;-webkit-background-clip:border-box !important;"
         "background-clip:border-box !important;color:#3a2d12 !important;"
         "-webkit-text-fill-color:#3a2d12 !important"),
    # 28px renders this line at ~673px inside a 660px box, so it wraps to two
    # lines and the second one is clipped by the 74px bar — the trailing "3" of
    # "MUA 10 TẶNG 3" disappears. 26px measures 625px and stays on one line.
    "G1759745653409_HEADLINE3955": "font-size:26px !important;line-height:1.25 !important",
}

# Price grid, evened up. The template shipped these at heights 391-421px with
# x offsets that drifted by 6px, so the block read as ragged. `left` is relative
# to the 1200px .ladi-container: 4 x 266 cards, 20px outer margin, 32px gutter.
GRID = {
    "G1717122335463_IMAGE4534": (20, 266, 420),
    "G1717122335463_IMAGE4535": (318, 266, 420),
    "G1717122335463_IMAGE4536": (616, 266, 420),
    "G1717122335463_IMAGE4537": (914, 266, 420),
    "G1717122335463_IMAGE4538": (20, 266, 420),
    "G1717122335463_IMAGE4539": (318, 266, 420),
    "G1717122335463_IMAGE4540": (616, 266, 420),
    "G1717122335463_IMAGE4541": (914, 266, 420),
}

# Desktop-only geometry fixes for blocks the template left ragged.
#
# The three service chips in the promo bar were sized to their own labels —
# 142 / 98 / 142px — and the short one carried a solid bronze fill while the
# other two got the champagne gradient, so the row read as a mistake rather than
# a set. All three become one 142px chip on a 5px gutter; the group grows from
# 392 to 436px leftward, which still clears the headline (it ends at 748).
CHIPS = {
    # "trải nghiệm giá tốt": the third column sat 16px right of where an even
    # 3-up grid puts it, so the block was both lopsided and off-centre in its
    # 1200px container. 143.58 + 200 + 156.42 x2 lands the last column at 856.
    "G1770091972748_IMAGE4610": "left:856.42px !important",
    "G1770091972748_IMAGE4612": "left:856.42px !important",
    # The fixed HOTLINE button (left:30px, bottom:80px, 251px wide) sits over the
    # copyright mark by ~30px whenever the footer is in view — and because both
    # are anchored to the viewport bottom the overlap is the same at every
    # window height. Moving the mark right of the button clears it for good.
    "G1743067768131_IMAGE15": "left:200px !important",

    "G1759745653409_GROUP3831": "left:812px !important;width:436px !important",
    "G1759745653409_GROUP3828": "left:0 !important;width:142px !important",
    "G1759745653409_GROUP3830": "left:147px !important;width:142px !important",
    "G1759745653409_GROUP3829": "left:294px !important;width:142px !important",
    "G1759745653409_BOX3347":   "width:142px !important",
    "G1759745653409_BOX3349":   "width:142px !important",
    "G1759745653409_BOX3348":   "width:142px !important",
    # match the two 16px labels; 3958 shipped at 14px and top-aligned differently
    "G1759745653409_HEADLINE3958":
        "left:3.5px !important;top:9.5px !important;width:135px !important",
}
# The odd chip's box paints a flat #8c6e3f that GILT_FILLS does not cover, so it
# never picked up the ramp its two neighbours have.
# BOX3349 is the desktop bar's odd chip; BOX3352 is the mobile bar's, which is a
# separate element tree (GROUP3840-3842) rather than a reflow of the desktop one.
CHIP_FILL = ["G1759745653409_BOX3349", "G1759745653409_BOX3352"]
CHIP_LABEL_FS = ["G1759745653409_HEADLINE3958"]

# Same headline on mobile: the box is only 292px wide there. At 14px the string
# measures 337px, wraps to two lines and the second one runs under the service
# chips sharing the bar. 11px measures 265px and stays on one line.
LAYOUT_MOBILE = {
    "G1759745653409_HEADLINE3955":
        "font-size:11px !important;line-height:1.3 !important;white-space:nowrap !important",
    # The lucky-wheel title block ships at left:-16.4px, which clips the "V" of
    # "VÒNG QUAY MAY MẮN" off the left edge. On mobile the wheel sits below it
    # rather than beside it, so the 216px block can simply be centred in 420.
    "G1761724761034_GROUP3105": "left:102px !important",
    # "XEM CHI TIẾT" ships at 147x79 over a 420px bar whose reserved gap is
    # 134px, so it overhung both baked-in lines. 118x63 fits with 8px either side.
    "G1770091972748_IMAGE4613": "width:118px !important;height:63px !important;left:151px !important",
}
# The button's painted layer is sized independently of its box.
LAYOUT_MOBILE_IMG = {"G1770091972748_IMAGE4613": (118, 63)}


def gilt_fill_selectors(html):
    """Selectors whose rule paints one of the flat gilt values."""
    found = []
    for m in re.finditer(r'([^{}]{1,600}?)\{([^{}]*)\}', html):
        sel, body = m.group(1), m.group(2)
        cm = re.search(r'background-color:\s*(rgb\(\s*\d+,\s*\d+,\s*\d+\s*\))', body)
        if not cm:
            continue
        if re.sub(r'\s+', ' ', cm.group(1)) in GILT_FILLS:
            s = sel.strip().lstrip(',').strip()
            if s and "@" not in s:
                found.append(s)
    return found


def build_css(html):
    out = [f'<style id="{MARKER}" type="text/css">',
           "/* 1. flat gilt -> metallic ramp */"]
    for sel in gilt_fill_selectors(html):
        out.append(f"{sel}{{background-image:{GRAD_FILL} !important}}")

    # The odd chip's box paints a flat #8c6e3f that GILT_FILLS does not cover,
    # so it never picked up the ramp its two neighbours have. Not media-scoped:
    # the mismatch shows at both widths, only the geometry differs.
    for eid in CHIP_FILL:
        out.append(f"#{eid} > .ladi-box{{background-image:{GRAD_FILL} !important;"
                   "background-color:rgb(222, 198, 156) !important}")

    out.append("/* 2. display headings clipped to the same metal */")
    for eid in GILD_TEXT_IDS:
        sel = ", ".join(f"#{eid}{p}" for p in
                        ("  .ladi-headline", " h1", " h2", " h3", " h4", " h5", " h6"))
        out.append(
            f"{sel}{{background-image:{GRAD_TEXT} !important;"
            "-webkit-background-clip:text !important;background-clip:text !important;"
            "-webkit-text-fill-color:transparent !important;color:transparent !important}")

    out.append("/* 3. contrast repair for labels sitting on the gilt */")
    for eid, ink in INK.items():
        sel = ", ".join(f"#{eid}{p}" for p in TEXT_PARTS)
        # The stroke colour has to follow the fill. Several of these headlines
        # carry `-webkit-text-stroke: 1px #fff`, which was a halo against the old
        # plum. Left white over a light gilt it eats the Vietnamese diacritics —
        # "buổi" renders as "buoi" — so the stroke is re-tinted to match the ink.
        out.append(f"{sel}{{color:{ink} !important;-webkit-text-fill-color:{ink} !important;"
                   f"-webkit-text-stroke-color:{ink} !important}}")

    # The wheel's prize labels are white with a black shadow, from when the
    # segments were deep plum. On the champagne wheel white measures 1.9:1, so
    # they take espresso and drop the shadow that would muddy it.
    out.append("#G1761724761034_SPINLUCKY2558 > .ladi-spin-lucky,"
               "#G1761724761034_SPINLUCKY2558 .ladi-spin-lucky-label"
               f"{{color:{ESPRESSO} !important;-webkit-text-fill-color:{ESPRESSO} !important;"
               "text-shadow:none !important}")

    out.append("/* 4. layout repairs for over-long Vietnamese copy */")
    for eid, decls in LAYOUT.items():
        sel = ", ".join(f"#{eid}{p}" for p in
                        ("", " .ladi-headline", " h1", " h2", " h3", " h4", " h5", " h6"))
        out.append(f"{sel}{{{decls}}}")

    out.append("/* 5. even up the price grid (template heights ran 391-421px) */")
    out.append("@media (min-width: 768px){")
    for eid, (left, w, h) in GRID.items():
        out.append(f"#{eid}{{left:{left}px !important;width:{w}px !important;height:{h}px !important}}")
        out.append(f"#{eid} > .ladi-image > .ladi-image-background{{width:{w}px !important;"
                   f"height:{h}px !important;top:0 !important;left:0 !important}}")
    for eid, decls in CHIPS.items():
        out.append(f"#{eid}{{{decls}}}")
    for eid in CHIP_LABEL_FS:
        out.append(f"#{eid} .ladi-headline{{font-size:16px !important}}")
    out.append("}")

    out.append("/* 6. mobile-only layout repairs */")
    out.append("@media (max-width: 767px){")
    for eid, decls in LAYOUT_MOBILE.items():
        sel = ", ".join(f"#{eid}{p}" for p in
                        ("", " .ladi-headline", " h1", " h2", " h3", " h4", " h5", " h6"))
        out.append(f"{sel}{{{decls}}}")
    for eid, (w, h) in LAYOUT_MOBILE_IMG.items():
        out.append(f"#{eid} > .ladi-image > .ladi-image-background"
                   f"{{width:{w}px !important;height:{h}px !important;top:0 !important;left:0 !important}}")
    out.append("}")

    out.append("</style>")
    return "\n".join(out)


def main():
    with open(PAGE, encoding="utf-8") as f:
        html = f.read()

    html = re.sub(r'<style id="%s".*?</style>\s*' % MARKER, "", html, flags=re.S)
    assert html.count("</head>") == 1
    css = build_css(html)
    html = html.replace("</head>", css + "\n</head>")

    with open(PAGE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Gradient vàng: {len(gilt_fill_selectors(html))} vùng nền, "
          f"{len(GILD_TEXT_IDS)} tiêu đề; sửa màu chữ: {len(INK)} phần tử.")


if __name__ == "__main__":
    main()
