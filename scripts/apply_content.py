#!/usr/bin/env python3
"""Apply Royal Spa rebrand content changes to index13c1.html per TDD.md.
Each replacement asserts the expected occurrence count so silent
mismatches (0 or unexpected multiples) fail loudly instead of
corrupting the file.
"""
import os
import re
import sys

SRC = "index13c1.inlined.html"   # output of scripts/inline_sections.py (phase 1)
DST = "index13c1.html"

with open(SRC, encoding="utf-8") as f:
    html = f.read()

errors = []


def replace(old, new, expected, label):
    global html
    count = html.count(old)
    if count != expected:
        errors.append(f"[{label}] expected {expected} occurrence(s), found {count}: {old[:80]!r}")
        return
    html = html.replace(old, new)


# ---------------------------------------------------------------------------
# 0. HTTrack mirror comments (cosmetic code comments, invisible to users,
#    top and bottom of file) — 2 identical occurrences.
# ---------------------------------------------------------------------------
replace(
    "<!-- Mirrored from khuyenmai.thammyseoulcenter.com/?zarsrc=30 by HTTrack Website Copier/3.x [XR&CO'2014], Sun, 02 Aug 2026 06:41:02 GMT -->",
    "<!-- Royal Spa By Trang Huynh -->",
    2, "HTTrack mirror comments")

# ---------------------------------------------------------------------------
# 1. Meta / head
# ---------------------------------------------------------------------------
replace(
    "<title>Seoul Center | Thẩm Mỹ Viện Làm Đẹp Hàng Đầu Việt Nam</title>",
    "<title>Royal Spa By Trang Huỳnh | Chăm Sóc Da - Điều Trị Mụn - Triệt Lông - Gội Đầu Dưỡng Sinh TP.HCM</title>",
    1, "title")

replace(
    'meta name="keywords" content="Seoul Center, TMV Seoul Center, thẩm mỹ viện làm đẹp, nâng mũi, cắt mí, phun môi, điêu khắc chân mày"',
    'meta name="keywords" content="Royal Spa, Royal Spa By Trang Huỳnh, chăm sóc da, điều trị mụn, triệt lông công nghệ cao, gội đầu dưỡng sinh, massage thư giãn, spa TP.HCM"',
    1, "meta keywords")

replace(
    'meta name="description" content="Seoul Center Top Thẩm Mỹ Viện Làm Đẹp Hàng Đầu Việt Nam"',
    'meta name="description" content="Royal Spa By Trang Huỳnh chuyên chăm sóc da, điều trị mụn không sưng không đau, triệt lông công nghệ cao, gội đầu dưỡng sinh, massage thư giãn cổ vai gáy tại TP.HCM. Đặt lịch ngay để nhận nhiều ưu đãi hấp dẫn."',
    1, "meta description")

replace(
    'meta name="robots" content="noindex, nofollow"',
    'meta name="robots" content="index, follow"',
    1, "meta robots")

replace(
    'href="https://khuyenmai.thammyseoulcenter.com/" /><meta property="og:url" content="https://khuyenmai.thammyseoulcenter.com" />',
    'href="" /><!-- TODO: điền domain thật khi go-live --><meta property="og:url" content="" />',
    1, "canonical/og:url")

replace(
    '<meta property="og:title" content="Seoul Center | Thẩm Mỹ Viện Làm Đẹp Hàng Đầu Việt Nam" />',
    '<meta property="og:title" content="Royal Spa By Trang Huỳnh | Chăm Sóc Da - Điều Trị Mụn - Triệt Lông - Gội Đầu Dưỡng Sinh TP.HCM" />',
    1, "og:title")

replace(
    '<meta property="og:image" content="https://static.ladipage.net/5977f59d1abc544991d43c5b/1200x600-20260702082742-cfzj5.png">',
    '<meta property="og:image" content="images/og-image.jpg">',
    1, "og:image")

replace(
    '<meta property="og:description" content="Seoul Center Top Thẩm Mỹ Viện Làm Đẹp Hàng Đầu Việt Nam" />',
    '<meta property="og:description" content="Royal Spa By Trang Huỳnh chuyên chăm sóc da, điều trị mụn không sưng không đau, triệt lông công nghệ cao, gội đầu dưỡng sinh, massage thư giãn cổ vai gáy tại TP.HCM. Đặt lịch ngay để nhận nhiều ưu đãi hấp dẫn." />',
    1, "og:description")

# favicon / touch-icon / msapplication (5 occurrences, same URL)
replace(
    "https://static.ladipage.net/5977f59d1abc544991d43c5b/seoul_spa_logo_8_3-1-05-20230407085345-udhhv.png",
    "images/favicon.png",
    5, "favicon urls")

# ---------------------------------------------------------------------------
# 2. Menu
# ---------------------------------------------------------------------------
replace('id="HEADLINE3910" class=\'ladi-element\'><h2 class=\'ladi-headline\'    >DỊCH VỤ SEOUL</h2>',
        'id="HEADLINE3910" class=\'ladi-element\'><h2 class=\'ladi-headline\'    >DỊCH VỤ ROYAL SPA</h2>',
        1, "HEADLINE3910 mobile menu")

# ---------------------------------------------------------------------------
# 3. Hero
# ---------------------------------------------------------------------------
replace('>THẨM MỸ VIỆN<br></h3>', '>ROYAL SPA BY TRANG HUỲNH<br></h3>', 1, "HEADLINE3871 hero title")
replace('>SEOUL CENTER<br></h3>', '>Chạm Đến Vẻ Đẹp Tự Nhiên - Đánh Thức Sự Tự Tin<br></h3>', 1, "HEADLINE3872 hero subtitle")

OLD_PARA = ("Hệ thống Thẩm Mỹ Seoul Center là thương hiệu uy tín, chất lượng với nhiều chi nhánh trong và ngoài nước. "
            "Seoul Center đi đầu trong ngành Làm đẹp- Thẩm mỹ, không ngừng cập nhật những xu hướng mới nhất từ các nước phát triển, "
            "ứng dụng thành công tại Việt Nam.<br>\n<br>Thương hiệu xây dựng hệ thống cơ sở vật chất sang trọng, đẳng cấp với phòng dịch vụ tiêu chuẩn 5 sao, "
            "phòng chờ khách vip thoải mái, tiện nghi. Cùng với hội đồng bác sĩ chuyên khoa giàu kinh nghiệm.<br><br>Là địa chỉ tin cậy, đem đến nhiều dịch vụ chất lượng. "
            "Nổi bật nhất là những dịch vụ spa, thẩm mỹ ngoại khoa, phun xăm.\n<br>\n<br>Tất cả phương pháp đều được chuyển giao từ những nước phát triển, "
            "đảm bảo tiêu chuẩn an toàn, chất lượng, áp dụng thành công cho hàng triệu khách hàng.<br>")
NEW_PARA = ("Ra đời với mong muốn mang đến những giá trị làm đẹp an toàn, khoa học và bền vững, Royal Spa By Trang Huỳnh không chỉ là nơi chăm sóc sắc đẹp "
            "mà còn là không gian thư giãn giúp khách hàng tái tạo năng lượng và tìm lại sự cân bằng trong cuộc sống.<br>\n<br>"
            "Với đội ngũ chuyên viên được đào tạo bài bản, quy trình chăm sóc chuyên nghiệp cùng hệ thống công nghệ hiện đại, "
            "Royal Spa By Trang Huỳnh luôn đặt sự hài lòng và an toàn của khách hàng lên hàng đầu.<br><br>"
            "Chúng tôi tin rằng: Mỗi người phụ nữ đều xứng đáng sở hữu vẻ đẹp tự nhiên, khỏe mạnh và tự tin nhất.<br>")
replace(OLD_PARA, NEW_PARA, 1, "PARAGRAPH3427 hero intro")

replace('>✎ TƯ VẤN NGAY</h3>', '>✎ ĐẶT LỊCH NGAY</h3>', 1, "BUTTON_TEXT3441")

# hero-gallery 4 images: external link -> internal section scroll
replace(
    'href="https://mientrung.seoulcenter.com.vn/cay-collagen-tuoi-thuy-phan" target="_blank" id="IMAGE4326"',
    'href="#G1717122335463_SECTION2682" id="IMAGE4326"', 1, "IMAGE4326 href")
replace(
    'href="https://mientrung.seoulcenter.com.vn/cay-collagen-tuoi-thuy-phan" target="_blank" id="IMAGE4329"',
    'href="#G1717122335463_SECTION2682" id="IMAGE4329"', 1, "IMAGE4329 href")
replace(
    'href="https://mientrung.seoulcenter.com.vn/cay-collagen-tuoi-thuy-phan" target="_blank" id="IMAGE4327"',
    'href="#G1717122335463_SECTION2682" id="IMAGE4327"', 1, "IMAGE4327 href")
replace(
    'href="https://mientrung.seoulcenter.com.vn/cay-collagen-tuoi-thuy-phan" target="_blank" id="IMAGE4328"',
    'href="#G1717122335463_SECTION2682" id="IMAGE4328"', 1, "IMAGE4328 href")

# JSON click-action config for the same 4 images (separate from href, drives ladipage JS router)
for iid in ["IMAGE4326", "IMAGE4327", "IMAGE4328", "IMAGE4329"]:
    old = (f'"{iid}":{{"a":"image","cs":[{{"dr":"action","dv":"_blank",'
            f'"dw":"https://mientrung.seoulcenter.com.vn/cay-collagen-tuoi-thuy-phan","a":"link"}}]}}')
    new = f'"{iid}":{{"a":"image","cs":[{{"dr":"action","dw":"G1717122335463_SECTION2682","a":"section"}}]}}'
    replace(old, new, 1, f"{iid} JSON action")

# ---------------------------------------------------------------------------
# 4. Service library (10 cards + 2 tab labels + titles)
# ---------------------------------------------------------------------------
replace('>THƯ VIỆN DỊCH VỤ - SEOUL CENTER</h3>', '>THƯ VIỆN DỊCH VỤ - ROYAL SPA</h3>', 1, "HEADLINE3971")
replace('>HÀNG TRIỆU KHÁCH HÀNG ĐÃ TRẢI NGHIỆM&nbsp;<br></h3>', '>5.000+ KHÁCH HÀNG ĐÃ TRẢI NGHIỆM<br></h3>', 1, "HEADLINE3972")
replace('>DỊCH VỤ THẨM MỸ LÀN DA</h3>', '>CHĂM SÓC DA & ĐIỀU TRỊ MỤN</h3>', 1, "HEADLINE3973 tab1")
replace('>COLLAGEN ORGANIC</h3>', '>CHĂM SÓC DA CƠ BẢN</h3>', 1, "HEADLINE3974")
replace('>ĐIỀU TRỊ MỤN</h3>', '>CHĂM SÓC DA CHUYÊN SÂU</h3>', 1, "HEADLINE3975")
replace('>MESO KHÔNG KIM</h3>', '>COMBO CHĂM SÓC MẶT & CỔ</h3>', 1, "HEADLINE3976")
replace('>ĐIỀU TRỊ THÂM NÁM</h3>', '>AQUA PEELING</h3>', 1, "HEADLINE3977")
replace('>ĐIỀU TRỊ SẸO, MỤN&nbsp;</h3>', '>LASER TONING</h3>', 1, "HEADLINE3978")
replace('>TRIỆT LÔNG TOÀN THÂN</h3>', '>ĐIỀU TRỊ MỤN CHUYÊN SÂU</h3>', 1, "HEADLINE3979")
replace('>DỊCH VỤ PHUN, XÓA XĂM THẨM MỸ</h3>', '>TRIỆT LÔNG - GỘI ĐẦU - MASSAGE</h3>', 1, "HEADLINE3980 tab2")
replace('>PHUN XĂM CHÂN MÀY</h3>', '>TRIỆT LÔNG CÔNG NGHỆ CAO</h3>', 1, "HEADLINE3981")
replace('>ĐIÊU KHẮC CHÂN MÀY</h3>', '>GỘI ĐẦU DƯỠNG SINH</h3>', 1, "HEADLINE3982")
replace('>PHUN MÔI COLLAGEN</h3>', '>MASSAGE THƯ GIÃN TOÀN THÂN</h3>', 1, "HEADLINE3983")
replace('>XÓA XĂM&nbsp;</h3>', '>DETOX THẢI ĐỘC DA ĐỘC QUYỀN</h3>', 1, "HEADLINE3984")
# BUTTON_TEXT3454 '✎ TƯ VẤN DỊCH VỤ' kept as-is (no change)

# Disable the 10 youtube video click-configs (keep DOM/CSS untouched here; handled in JSON step below)
VIDEO_IDS_URLS = {
    "VIDEO3309": "dPk5IGyUyn0", "VIDEO3310": "j4M9XCRf_WY", "VIDEO3311": "SFK7oQTrc3A",
    "VIDEO3312": "ZYRTYWaXUG4", "VIDEO3313": "XcptC9FijH4", "VIDEO3314": "7U79HnjBhf8",
    "VIDEO3315": "43CdjJHf7Ds", "VIDEO3316": "6bnqVM-0nOI", "VIDEO3317": "e5KnxgrEGNo",
    "VIDEO3318": "aWxcmtfqdFw",
}
video_json_removed = 0
for vid in VIDEO_IDS_URLS:
    pattern = re.compile(rf'"{vid}":\{{"a":"video","ci":"[^"]+","ch":"youtube","cg":true\}},')
    new_html, n = pattern.subn("", html)
    if n != 1:
        errors.append(f"[{vid} JSON video config removal] expected 1 occurrence(s), found {n}")
        continue
    html = new_html
    video_json_removed += 1

# ---------------------------------------------------------------------------
# 5. Consultation form ("bác sĩ" popup) — Facebook redirect
# ---------------------------------------------------------------------------
replace(
    '&#34;redirect_url&#34;:&#34;https://www.facebook.com/thammyvienseoulcenter&#34;,&#34;type&#34;:&#34;form_redirect_url&#34;,&#34;no_delete&#34;:true',
    '&#34;redirect_url&#34;:&#34;&#34;,&#34;type&#34;:&#34;form_redirect_url&#34;,&#34;no_delete&#34;:true',
    1, "FORM3277 facebook redirect_url")

# ---------------------------------------------------------------------------
# 5b. Other Seoul-Center-specific leftovers found via QA grep pass
# ---------------------------------------------------------------------------
# click-to-call JSON actions (separate from the tel: hrefs) — 4 occurrences
replace('"dw":"84914269346","a":"phone"', '"dw":"84899994509","a":"phone"', 5, "JSON click-to-call phone actions")

# thank-you-page redirect URLs on the 3 promo popup forms — no Royal Spa domain
# yet, so clear rather than guess (same policy as the Facebook redirect above)
replace(
    'redirect_url&#34;:&#34;https://uudai.seoulcenter.com.vn/cam-on-quy-khach&#34;',
    'redirect_url&#34;:&#34;&#34;',
    1, "UUDAI79K form thank-you redirect")
replace(
    'redirect_url&#34;:&#34;https://khuyenmai.seoulcenter.com.vn/cam-on-quy-khach&#34;',
    'redirect_url&#34;:&#34;&#34;',
    5, "PHUNMOI/MIENTRUNG form thank-you redirects")

# internal LadiPage cookie-domain scoping list — old domain is inert once
# hosted elsewhere; clear it rather than guess the new domain
replace('DOMAIN_SET_COOKIE = ["thammyseoulcenter.com"]', 'DOMAIN_SET_COOKIE = []', 1, "DOMAIN_SET_COOKIE")

# ---------------------------------------------------------------------------
# 6. Footer / contact
# ---------------------------------------------------------------------------
replace("tel:84914269346", "tel:84899994509", 4, "tel: phone number")
replace('>ĐỊA CHỈ</h2>', '>59 Vườn Lài, Phường An Phú Đông, TP. Hồ Chí Minh</h2>', 1, "HEADLINE3915 address")
replace(
    '>BẠN CẦN TƯ VẤN LÀM ĐẸP<br>XIN ĐỂ LẠI THÔNG TIN ĐỂ TIẾP TỤC ĐẾN CHAT ONLINE<br></h3>',
    '>BẠN CẦN TƯ VẤN LÀM ĐẸP?<br>ĐỂ LẠI THÔNG TIN ĐỂ ĐƯỢC HỖ TRỢ NGAY<br></h3>',
    1, "HEADLINE3968")
replace(
    '>ĐỂ LẠI SỐ ĐIỆN THOẠI – NHẬN CƠ HỘI NÂNG TẦM NHAN SẮC!<br></h3>',
    '>ĐỂ LẠI SỐ ĐIỆN THOẠI – NHẬN ƯU ĐÃI TỪ ROYAL SPA NGAY!<br></h3>',
    1, "HEADLINE3993")

# ---------------------------------------------------------------------------
# 7. Images -> local paths (per TDD table). Only rewrite url(); keep rest of
#    each CSS rule (sizes/background-size/position) untouched.
# ---------------------------------------------------------------------------
IMAGE_URL_MAP = {
    # logo (2 sizes, header)
    "https://w.ladicdn.com/s500x400/5977f59d1abc544991d43c5b/seoul_spa_logo_8_3-1-04-min-20250219021940-lqcdy.png": "images/logo.png",
    "https://w.ladicdn.com/s550x400/5977f59d1abc544991d43c5b/seoul_spa_logo_8_3-1-04-min-20250219021940-lqcdy.png": "images/logo.png",
    # hero banner
    "https://w.ladicdn.com/s1440x712/5977f59d1abc544991d43c5b/1903x704-20260702075015-zt7tu.png": "images/hero-banner-desktop.jpg",
    "https://w.ladicdn.com/s768x632/5977f59d1abc544991d43c5b/800x1200-20260702075015-mlhbd.png": "images/hero-banner-mobile.jpg",
    # hero gallery 4 photos (desktop + mobile sizes share same file)
    "https://w.ladicdn.com/s600x600/5977f59d1abc544991d43c5b/mt_ag-20240531025950-fwrou.jpg": "images/hero-gallery-1.jpg",
    "https://w.ladicdn.com/s550x550/5977f59d1abc544991d43c5b/mt_ag-20240531025950-fwrou.jpg": "images/hero-gallery-1.jpg",
    "https://w.ladicdn.com/s500x500/5977f59d1abc544991d43c5b/quy-trinh-1-20251011032141-aqxx7.png": "images/hero-gallery-2.jpg",
    "https://w.ladicdn.com/s550x550/5977f59d1abc544991d43c5b/quy-trinh-1-20251011032141-aqxx7.png": "images/hero-gallery-2.jpg",
    "https://w.ladicdn.com/s550x550/5977f59d1abc544991d43c5b/quy-trinh-2-20251011032141-t6gml.png": "images/hero-gallery-3.jpg",
    "https://w.ladicdn.com/s500x500/5977f59d1abc544991d43c5b/quy-trinh-2-20251011032141-t6gml.png": "images/hero-gallery-3.jpg",
    "https://w.ladicdn.com/s500x500/5977f59d1abc544991d43c5b/szhfahpm-ud9-20240531025538-4wkdo.jpg": "images/hero-gallery-4.jpg",
    # service cards (video thumbnails -> static photos)
    "https://img.youtube.com/vi/dPk5IGyUyn0/hqdefault.jpg": "images/service-01.jpg",
    "https://img.youtube.com/vi/j4M9XCRf_WY/hqdefault.jpg": "images/service-02.jpg",
    "https://img.youtube.com/vi/SFK7oQTrc3A/hqdefault.jpg": "images/service-03.jpg",
    "https://img.youtube.com/vi/ZYRTYWaXUG4/hqdefault.jpg": "images/service-04.jpg",
    "https://img.youtube.com/vi/XcptC9FijH4/hqdefault.jpg": "images/service-05.jpg",
    "https://img.youtube.com/vi/7U79HnjBhf8/hqdefault.jpg": "images/service-06.jpg",
    "https://img.youtube.com/vi/43CdjJHf7Ds/hqdefault.jpg": "images/service-07.jpg",
    "https://img.youtube.com/vi/6bnqVM-0nOI/hqdefault.jpg": "images/service-08.jpg",
    "https://img.youtube.com/vi/e5KnxgrEGNo/hqdefault.jpg": "images/service-09.jpg",
    "https://img.youtube.com/vi/aWxcmtfqdFw/hqdefault.jpg": "images/service-10.jpg",
    # consultant photo (BACSI form)
    "https://w.ladicdn.com/s550x550/5977f59d1abc544991d43c5b/zjrupx8g-bs-khoa-20240625074034-tj5of.png": "images/consultant-photo.jpg",
    # 3 promo popup graphics
    "https://w.ladicdn.com/s700x550/5977f59d1abc544991d43c5b/79k-20260407081157-6ib87.png": "images/promo-mun-299k.jpg",
    "https://w.ladicdn.com/s700x500/5977f59d1abc544991d43c5b/79k-20260407081157-6ib87.png": "images/promo-mun-299k.jpg",
    "https://w.ladicdn.com/s700x500/5977f59d1abc544991d43c5b/may-moi-799k-pc-20260128075354-11hcq.png": "images/promo-goi-99k.jpg",
    "https://w.ladicdn.com/s423x496/5977f59d1abc544991d43c5b/kv-4-20260702080429-oaa2m.png": "images/promo-nach-499k.jpg",
    "https://w.ladicdn.com/s408x494/5977f59d1abc544991d43c5b/kv-4-20260702080429-oaa2m.png": "images/promo-nach-499k.jpg",
    # slogan badge
    "https://w.ladicdn.com/s750x650/5977f59d1abc544991d43c5b/group-51-20260702080628-7echh.png": "images/badge-slogan.png",
}

# ---------------------------------------------------------------------------
# 7c. Content of the 12 inlined global sections (phase 1 pulled the real
#     Seoul Center markup down from their CDN so we own the design; this
#     swaps their copy for Royal Spa's).
# ---------------------------------------------------------------------------

# --- Marquee ticker --------------------------------------------------------
replace(
    "SEOUL CENTER | ƯU ĐÃI VIP 💎 CHẠM TỚI VẺ ĐẸP HOÀN HẢO – 50 SUẤT ĐẶC QUYỀN DÀNH CHO KHÁCH HÀNG TRONG KHU VỰC",
    "ROYAL SPA BY TRANG HUỲNH 💎 ĐIỀU TRỊ MỤN CHỈ TỪ 299.000Đ – GỘI THƯ GIÃN GIỜ VÀNG CHỈ 99.000Đ – TRỊ THÂM NÁCH CHỈ TỪ 499.000Đ",
    1, "marquee text")

# --- Top promo bar + branch-gift popup (same campaign copy) ----------------
replace(
    '<span style="color: rgb(182, 30, 76);">MUA 1 ĐƯỢC 3 – </span><span style="color: rgb(6, 57, 125);">SINH NHẬT VÀNG 16 NĂM</span>',
    '<span style="color: rgb(182, 30, 76);">ƯU ĐÃI THÀNH VIÊN – </span><span style="color: rgb(6, 57, 125);">MUA 5 TẶNG 1, MUA 10 TẶNG 3</span>',
    1, "promo bar headline")
replace(">MUA 1 ĐƯỢC 3 – SINH NHẬT VÀNG 16 NĂM</h3>",
        ">ƯU ĐÃI THÀNH VIÊN – MUA 5 TẶNG 1, MUA 10 TẶNG 3</h3>",
        1, "branch-gift popup headline")

for old, new, n, label in [
    (">Combo Đẹp Toàn Diện<br></h3>", ">Chăm Sóc Da Chuyên Sâu<br></h3>", 1, "combo1"),
    (">Combo&nbsp; Đẹp Toàn Diện<br></h3>", ">Chăm Sóc Da Chuyên Sâu<br></h3>", 1, "combo1b"),
    (">Combo Trẻ Hoá Chuyên Sâu<br></h3>", ">Gội Đầu Dưỡng Sinh<br></h3>", 1, "combo2"),
    (">Combo Trẻ Hoá<br>&nbsp;Chuyên Sâu<br></h3>", ">Gội Đầu<br>&nbsp;Dưỡng Sinh<br></h3>", 1, "combo2b"),
    (">01 Thẻ Tiền 500.000 Đ<br></h3>", ">Massage Thư Giãn<br></h3>", 2, "combo3"),
]:
    replace(old, new, n, label)

replace(
    "∙ Combo 1 - Đẹp Toàn Diện<br>∙ Combo 2 - Trẻ Hoá Chuyên Sâu<br>∙ Tặng 01 Thẻ Tiền 500.000 Đ<br>",
    "∙ Mua 5 buổi tặng 1 buổi<br>∙ Mua 10 buổi tặng 3 buổi<br>∙ Tư vấn liệu trình cá nhân hoá miễn phí<br>",
    1, "branch-gift popup bullets")

# --- Referral / thank-you section -----------------------------------------
replace(
    ">Hệ thống Thẩm Mỹ Viện Quốc Tế Seoul Center<br>Dành Tặng Người Thân/ Bạn Bè Của Anh/Chị Món Quà Đặc Biệt<br></h3>",
    ">Royal Spa By Trang Huỳnh<br>Dành Tặng Người Thân/ Bạn Bè Của Anh/Chị Món Quà Đặc Biệt<br></h3>",
    1, "referral headline")

# --- Gallery section titles ------------------------------------------------
replace(
    '<span style="color: rgb(21, 36, 107);">HOẠT ĐỘNG CHI NHÁNH</span> SEOUL CENTER<br>',
    '<span style="color: rgb(21, 36, 107);">HOẠT ĐỘNG TẠI</span> ROYAL SPA<br>',
    1, "activity gallery title")
# "Trusted by Vietnamese celebrities" is a claim Royal Spa can't make — retitled
# to something true about the same photo carousel.
replace(">ĐỊA ĐIỂM LÀM ĐẸP UY TÍN, TIN CẬY CỦA CÁC SAO VIỆT</h3>",
        ">KHÔNG GIAN LÀM ĐẸP TẠI ROYAL SPA BY TRANG HUỲNH</h3>",
        1, "celebrity gallery title")

# --- Footer: brand buttons -------------------------------------------------
replace(">HỆ THỐNG PHÒNG KHÁM CHUYÊN KHOA DA LIỄU SEOUL CENTER</h3>",
        ">ROYAL SPA BY TRANG HUỲNH</h3>", 1, "footer button 18")
replace(">PHÒNG KHÁM CHUYÊN KHOA THẨM MỸ SEOUL CENTER</h3>",
        ">DỊCH VỤ TẠI ROYAL SPA</h3>", 1, "footer button 17")
replace(">HỆ THỐNG THẨM MỸ SEOUL CENTER</h3>",
        ">ĐỊA CHỈ ROYAL SPA</h3>", 1, "footer button 19")

# --- Footer: clinic disclaimers (Royal Spa is a spa, not a clinic) ---------
replace(
    '<span class="ladipage-animated-headline slide"><span class="ladipage-animated-words-wrapper" data-word="[&quot;∙Seoul Center Lưu Ý Quý Khách Hàng∙&quot;]">∙Quý Khách Hàng Sẽ Được Thực Hiện Dịch Vụ Tại Các Phòng Khám Thuộc Hệ Thống Thẩm Mỹ Quốc Tế Seoul Center Theo Chức Năng∙</span></span>',
    '<span class="ladipage-animated-headline slide"><span class="ladipage-animated-words-wrapper" data-word="[&quot;∙Royal Spa By Trang Huỳnh∙&quot;]">∙Mọi Dịch Vụ Đều Được Thực Hiện Tại Royal Spa By Trang Huỳnh – 59 Vườn Lài, Phường An Phú Đông, TP. Hồ Chí Minh∙</span></span>',
    1, "footer disclaimer animated")
replace(
    ">∙Quý Khách Hàng Sẽ Được Thực Hiện Dịch Vụ Tại Các Phòng Khám Thuộc Hệ Thống Thẩm Mỹ Quốc Tế Seoul Center Theo Chức Năng∙</h3>",
    ">∙Mọi Dịch Vụ Đều Được Thực Hiện Tại Royal Spa By Trang Huỳnh – 59 Vườn Lài, Phường An Phú Đông, TP. Hồ Chí Minh∙</h3>",
    1, "footer disclaimer static")

# --- Footer: about paragraph ----------------------------------------------
replace(
    "Hệ Thống Thẩm Mỹ Seoul Center là địa chỉ tin cậy, đem đến nhiều dịch vụ chất lượng. Nổi bật là những dịch vụ spa, chăm sóc da, phun xăm. Tự hào sở hữu đội ngũ bác sĩ chuyên môn cao, tiên phong công nghệ tiên tiến để đem đến giải pháp làm đẹp tối ưu.\n<br>Tất cả phương pháp đều được chuyển giao từ những nước phát triển, đảm bảo tiêu chuẩn an toàn, chất lượng, áp dụng thành công cho hàng triệu khách hàng.<br>",
    "Royal Spa By Trang Huỳnh là điểm đến chăm sóc sắc đẹp và thư giãn toàn diện, nổi bật với các dịch vụ chăm sóc da, điều trị mụn, triệt lông công nghệ cao, gội đầu dưỡng sinh và massage thư giãn.\n<br>Đội ngũ chuyên viên được đào tạo bài bản cùng quy trình chăm sóc chuyên nghiệp, mang đến trải nghiệm làm đẹp an toàn, hiệu quả và bền vững.<br>",
    1, "footer about paragraph")

# --- Footer: contact block -------------------------------------------------
replace(">(+84) 914 269 346<br></h3>", ">0899 994 509<br></h3>", 1, "footer phone text")
replace(">cskh@seoulcenter.vn<br></h3>", ">Fanpage: Royal Spa By Trang Huỳnh<br></h3>", 1, "footer email text")
replace(">Thời gian làm việc:<br>Từ 08:45 đến 18:30 hàng ngày<br></h3>",
        ">Thời gian làm việc:<br>Từ 09:00 đến 20:00 hàng ngày<br></h3>", 1, "footer hours")
replace('href="mailto:cskh@seoulcenter.vn"', 'href="#"', 1, "footer mailto href")
replace('"dw":"cskh@seoulcenter.vn","a":"email"', '"dw":"","a":"email"', 1, "footer email JSON")
replace('href="tel:0917 839 346"', 'href="tel:84899994509"', 1, "footer tel href")
replace('"dw":"0917 839 346","a":"phone"', '"dw":"84899994509","a":"phone"', 2, "footer phone JSON")

# --- Footer: Seoul Center's own social / legal badges (not transferable) ---
replace('href="https://www.youtube.com/@thammyvienseoulcenter" target="_blank" ', '', 1, "youtube link")
replace('href="https://www.tiktok.com/@seoulcenter.vn" target="_blank" ', '', 1, "tiktok link")
replace(
    'href="https://www.dmca.com/Protection/Status.aspx?ID=6e1e7c6a-9b03-4367-a47f-db3203774f7a&refurl=https://seoulcenter.vn" target="_blank" ',
    '', 1, "DMCA badge link")
replace('href="http://online.gov.vn/Home/WebDetails/61124" target="_blank" ', '', 1, "gov registration badge link")

# --- Footer: branch/licence tabs -> Royal Spa's single location ------------
# Seoul Center's clinic addresses and GPHĐ licence numbers cannot be reused or
# adapted, so each tab is rewritten with Royal Spa's real details only.
ROYAL_ADDR = ('<span style="color: rgb(173, 30, 70); font-weight: 700;">∙ Royal Spa By Trang Huỳnh</span><br>'
              '59 Vườn Lài, Phường An Phú Đông, TP. Hồ Chí Minh<br>'
              'Hotline: 0899 994 509<br>Giờ làm việc: 09:00 - 20:00<br>')
for eid, label in [
    ("G1743067768131_PARAGRAPH23", "footer tab1 address"),
    ("G1743067768131_PARAGRAPH26", "footer tab2 address"),
    ("G1743067768131_PARAGRAPH28", "footer tab3 address"),
]:
    pat = re.compile(r'(id="' + eid + r'" class="ladi-element"><div class="ladi-paragraph ladi-transition">).*?(</div>)', re.S)
    new_html, n = pat.subn(lambda m: m.group(1) + ROYAL_ADDR + m.group(2), html, count=1)
    if n != 1:
        errors.append(f"[{label}] expected 1 match, got {n}")
    else:
        html = new_html

for old, new, label in [
    ("( Đối với các dịch vụ tiểu phẫu, công nghệ cao, chăm sóc da, phun xăm )",
     "( Chăm sóc da - Điều trị mụn - Triệt lông công nghệ cao )", "footer tab note 1"),
    ("( Đối với các dịch vụ công nghệ cao, chăm sóc da, phun xăm )",
     "( Gội đầu dưỡng sinh - Massage thư giãn )", "footer tab note 2"),
    ("( Đối với các dịch vụ chăm sóc da và phun xăm )",
     "( Hỗ trợ chăm sóc da chuyên sâu )", "footer tab note 3"),
]:
    replace(old, new, 1, label)

# --- Service-tile links in the price/promo section -------------------------
# Eight tiles each deep-linked to a Seoul Center campaign page. Royal Spa has
# no equivalent pages, so they scroll to the on-page consultation form instead.
n_href = len(re.findall(r'href="https://khuyenmai\.seoulcenter\.com\.vn/[^"]*" target="_blank" ', html))
if n_href != 8:
    errors.append(f"[service tile hrefs] expected 8, found {n_href}")
html = re.sub(r'href="https://khuyenmai\.seoulcenter\.com\.vn/[^"]*" target="_blank" ',
              'href="#FORM3277" ', html)

n_json = len(re.findall(r'"dr":"action","dv":"_blank","dw":"https://khuyenmai\.seoulcenter\.com\.vn/[^"]*","a":"link"', html))
if n_json != 8:
    errors.append(f"[service tile JSON actions] expected 8, found {n_json}")
html = re.sub(r'"dr":"action","dv":"_blank","dw":"https://khuyenmai\.seoulcenter\.com\.vn/[^"]*","a":"link"',
              '"dr":"action","dw":"BACSI","a":"popup"', html)

# Social / legal badge JSON actions matching the hrefs stripped above.
for pat, label in [
    (r'"dr":"action","dv":"_blank","dw":"https://www\.youtube\.com/@thammyvienseoulcenter","a":"link"', "youtube JSON"),
    (r'"dr":"action","dv":"_blank","dw":"https://www\.tiktok\.com/@seoulcenter\.vn","a":"link"', "tiktok JSON"),
    (r'"dr":"action","dv":"_blank","dw":"https://www\.dmca\.com/[^"]*","a":"link"', "DMCA JSON"),
    (r'"dr":"action","dv":"_blank","dw":"http://online\.gov\.vn/[^"]*","a":"link"', "gov badge JSON"),
]:
    new_html, n = re.subn(pat, '"dr":"action","dw":"","a":"link"', html)
    if n != 1:
        errors.append(f"[{label}] expected 1, found {n}")
    else:
        html = new_html

img_errors = []
for old_url, new_path in IMAGE_URL_MAP.items():
    count = html.count(old_url)
    if count == 0:
        img_errors.append(f"NOT FOUND: {old_url}")
        continue
    html = html.replace(old_url, new_path)

errors.extend(img_errors)

# ---------------------------------------------------------------------------
if errors:
    print("ERRORS — aborting write:")
    for e in errors:
        print(" -", e)
    sys.exit(1)

with open(DST, "w", encoding="utf-8") as f:
    f.write(html)

print("OK — all replacements applied and written to", DST)
