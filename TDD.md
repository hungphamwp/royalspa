# TDD — Rebrand Landing Page: Royal Spa By Trang Huỳnh

Tài liệu kỹ thuật đi kèm `PRD.md`. Đọc PRD trước để hiểu bối cảnh/quyết định nội dung; tài liệu này mô tả **cách triển khai** trong file `index13c1.html`.

---

## 1. Đặc điểm kỹ thuật của file nguồn

- File xuất từ **LadiPage**, toàn bộ HTML/CSS/JS nén thành **1 dòng duy nhất** (~160KB, 21 dòng thực tế chủ yếu là `<script>` blocks). Không thể sửa tay theo số dòng.
- Kiến trúc: mỗi phần tử nội dung có `id` riêng theo quy ước LadiPage:
  - `HEADLINE####` — tiêu đề (`<h1>-<h6>`)
  - `PARAGRAPH####` — đoạn văn
  - `BUTTON####` / `BUTTON_TEXT####` — nút bấm
  - `IMAGE####` — ảnh nền (`background-image` trong CSS, không phải thẻ `<img>`)
  - `VIDEO####` — thẻ video (thumbnail nền + cấu hình JS riêng)
  - `FORM####` / `FORM_ITEM####` — form và field
  - `GROUP####`, `BOX####`, `SHAPE####`, `SECTION####` — container/trang trí
- CSS nằm trong `<style id="style_element">`, mỗi id có rule riêng theo breakpoint (desktop full, rồi override cho `@media` mobile — thực tế xuất hiện dưới dạng 2-3 khối rule lặp lại cho cùng 1 id ứng với các kích thước khác nhau).
- **Toàn bộ text hiển thị nằm ngay trong DOM** dưới dạng `<h_ class='ladi-headline'>TEXT</h_>` — sửa text = string-replace trực tiếp trên chuỗi HTML, không qua biến/template.
- **Ảnh không dùng thẻ `<img>`** — dùng `background-image: url("...")` gắn theo `id` trong CSS. Phải sửa trong khối `<style>`, không phải trong khối HTML markup.
- Cuối file có 1 khối JSON cấu hình lớn (trong `script_ladipage_run`) mô tả hành vi tương tác (click action, link, popup trigger) cho từng id — vd: `"VIDEO3309":{"a":"video","ci":"https://www.youtube.com/watch?v=...","ch":"youtube","cg":true}`. Cần sửa JSON này nếu đổi hành vi (gỡ video, đổi link).

---

## 2. Phương pháp chỉnh sửa (bắt buộc dùng script, không sửa tay)

1. **Không dùng Edit tool sửa tay từng chuỗi nhỏ lẻ** trên file 160KB một dòng — dễ sai sót, khó review diff.
2. Quy trình chuẩn:
   - Backup file gốc: `cp index13c1.html index13c1.original.html` (giữ vĩnh viễn để đối chiếu/rollback).
   - Viết 1 script Python (`scripts/apply_content.py`, không commit vào deliverable cuối — chỉ dùng nội bộ) chứa **danh sách cặp (chuỗi cũ chính xác → chuỗi mới)** lấy từ bảng mapping mục 4 bên dưới, áp dụng bằng `str.replace()` **đếm số lần thay thế thực tế** và so với số lần kỳ vọng (assert) — tránh replace nhầm 0 lần hoặc thừa lần do trùng chuỗi.
   - Với các cụm chỉ xuất hiện đúng 1 lần (hầu hết headline) → replace trực tiếp theo `id="...">TEXT<`.
   - Với các cụm lặp nhiều lần (số điện thoại `84914269346` xuất hiện 3 lần, logo url xuất hiện nhiều lần) → dùng `replace_all` có kiểm đếm.
   - Sau khi áp dụng, chạy `python3 -c "import re,sys; ..."` kiểm tra **không còn chuỗi "Seoul", "seoulcenter", "84914269346"** nào sót lại trong file kết quả (grep kiểm tra tự động, xem mục 7).
3. Ảnh: khách hàng đặt file vào thư mục `images/` theo đúng tên quy ước ở mục 5 → script thay `url("https://w.ladicdn.com/...")` cũ bằng `url("images/<tên-file-quy-ước>")` tương ứng, giữ nguyên toàn bộ phần còn lại của rule CSS (kích thước, background-size: cover, position...).

---

## 3. Bảng mapping toàn bộ text (id → cũ → mới)

> Đây là bảng thực thi — khớp 1:1 với nội dung đã chốt ở `PRD.md` mục 4. Text lấy nguyên văn để đưa vào script thay thế.

### 3.1 Meta / Head

| Vị trí | Chuỗi cũ | Chuỗi mới |
|---|---|---|
| `<title>` | `Seoul Center \| Thẩm Mỹ Viện Làm Đẹp Hàng Đầu Việt Nam` | `Royal Spa By Trang Huỳnh \| Chăm Sóc Da - Điều Trị Mụn - Triệt Lông - Gội Đầu Dưỡng Sinh TP.HCM` |
| `meta[name=description]` | `Seoul Center Top Thẩm Mỹ Viện Làm Đẹp Hàng Đầu Việt Nam` | `Royal Spa By Trang Huỳnh chuyên chăm sóc da, điều trị mụn không sưng không đau, triệt lông công nghệ cao, gội đầu dưỡng sinh, massage thư giãn cổ vai gáy tại TP.HCM. Đặt lịch ngay để nhận nhiều ưu đãi hấp dẫn.` |
| `meta[name=keywords]` | `Seoul Center, TMV Seoul Center, thẩm mỹ viện làm đẹp, nâng mũi, cắt mí, phun môi, điêu khắc chân mày` | `Royal Spa, Royal Spa By Trang Huỳnh, chăm sóc da, điều trị mụn, triệt lông công nghệ cao, gội đầu dưỡng sinh, massage thư giãn, spa TP.HCM` |
| `meta[name=robots]` | `noindex, nofollow` | `index, follow` |
| `og:title` | (như title cũ) | (như title mới) |
| `og:description` | (như description cũ) | (như description mới) |
| `og:image` | `https://static.ladipage.net/.../1200x600-...png` | `images/og-image.jpg` |
| `canonical` href, `og:url` | `https://khuyenmai.thammyseoulcenter.com[/]` | **để trống `""` + comment `<!-- TODO: điền domain thật khi go-live -->`** |
| favicon/apple-touch-icon/msapplication-TileImage (5 thẻ, cùng 1 URL lặp lại) | `https://static.ladipage.net/.../seoul_spa_logo_...udhhv.png` | `images/favicon.png` |

### 3.2 Menu (desktop anchor + mobile popup)

| id | Cũ | Mới |
|---|---|---|
| HEADLINE3901 | `Dịch Vụ` | *(giữ nguyên)* |
| HEADLINE3902 | `Về Chúng Tôi` | *(giữ nguyên)* |
| HEADLINE3903 | `Trải Nghiệm Khách Hàng` | *(giữ nguyên)* |
| HEADLINE3904 | `Cam Kết` | *(giữ nguyên)* |
| HEADLINE3905 | `Liên Hệ` | *(giữ nguyên)* |
| HEADLINE3906 | `Chương Trình` | *(giữ nguyên)* |
| BUTTON_TEXT3436 | `Nhận Ưu Đãi` | *(giữ nguyên)* |
| HEADLINE3908 | `VỀ CHÚNG TÔI` | *(giữ nguyên)* |
| HEADLINE3909 | `CAM KẾT` | *(giữ nguyên)* |
| HEADLINE3910 | `DỊCH VỤ SEOUL` | `DỊCH VỤ ROYAL SPA` |
| HEADLINE3911 | `CHƯƠNG TRÌNH` | *(giữ nguyên)* |
| HEADLINE3912 | `TRẢI NGHIỆM KHÁCH HÀNG` | *(giữ nguyên)* |
| HEADLINE3913 | `NHẬN ƯU ĐÃI` | *(giữ nguyên)* |

### 3.3 Hero

| id | Cũ | Mới |
|---|---|---|
| HEADLINE3871 (font lớn, 50.8px) | `THẨM MỸ VIỆN` | `ROYAL SPA BY TRANG HUỲNH` |
| HEADLINE3872 (font nhỏ hơn, 37px) | `SEOUL CENTER` | `Chạm Đến Vẻ Đẹp Tự Nhiên - Đánh Thức Sự Tự Tin` |
| PARAGRAPH3427 | *(đoạn giới thiệu Seoul Center — xem file gốc)* | `Ra đời với mong muốn mang đến những giá trị làm đẹp an toàn, khoa học và bền vững, Royal Spa By Trang Huỳnh không chỉ là nơi chăm sóc sắc đẹp mà còn là không gian thư giãn giúp khách hàng tái tạo năng lượng và tìm lại sự cân bằng trong cuộc sống. Với đội ngũ chuyên viên được đào tạo bài bản, quy trình chăm sóc chuyên nghiệp cùng hệ thống công nghệ hiện đại, Royal Spa By Trang Huỳnh luôn đặt sự hài lòng và an toàn của khách hàng lên hàng đầu. Chúng tôi tin rằng: Mỗi người phụ nữ đều xứng đáng sở hữu vẻ đẹp tự nhiên, khỏe mạnh và tự tin nhất.` |
| BUTTON_TEXT3441 | `✎ TƯ VẤN NGAY` | `✎ ĐẶT LỊCH NGAY` |

**Hành vi liên kết (JSON config, không phải text):** 4 ảnh `IMAGE4326/4327/4328/4329` hiện có `"a":"link","dw":"https://mientrung.seoulcenter.com.vn/cay-collagen-tuoi-thuy-phan","dv":"_blank"` → đổi thành hành vi cuộn nội bộ giống HEADLINE3901: `"a":"section","dw":"G1717122335463_SECTION2682"` (bỏ `dv`/`_blank`, bỏ `dr`, giữ `dr:"action"`). Áp dụng cho cả 4 id, xoá luôn 4 thuộc tính `href="https://mientrung..."` và `target="_blank"` tương ứng trong markup HTML (đổi `<a href="...">` bao ngoài các ảnh này thành `<div>` hoặc bỏ hẳn href — **khuyến nghị**: đổi `href` thành `href="#G1717122335463_SECTION2682"` để không phải đổi thẻ, ít rủi ro hơn đổi tag).

### 3.4 Thư viện dịch vụ

| id | Cũ | Mới |
|---|---|---|
| HEADLINE3971 | `THƯ VIỆN DỊCH VỤ - SEOUL CENTER` | `THƯ VIỆN DỊCH VỤ - ROYAL SPA` |
| HEADLINE3972 | `HÀNG TRIỆU KHÁCH HÀNG ĐÃ TRẢI NGHIỆM` | `5.000+ KHÁCH HÀNG ĐÃ TRẢI NGHIỆM` |
| HEADLINE3973 (tab 1) | `DỊCH VỤ THẨM MỸ LÀN DA` | `CHĂM SÓC DA & ĐIỀU TRỊ MỤN` |
| HEADLINE3974 | `COLLAGEN ORGANIC` | `CHĂM SÓC DA CƠ BẢN` |
| HEADLINE3975 | `ĐIỀU TRỊ MỤN` | `CHĂM SÓC DA CHUYÊN SÂU` |
| HEADLINE3976 | `MESO KHÔNG KIM` | `COMBO CHĂM SÓC MẶT & CỔ` |
| HEADLINE3977 | `ĐIỀU TRỊ THÂM NÁM` | `AQUA PEELING` |
| HEADLINE3978 | `ĐIỀU TRỊ SẸO, MỤN` | `LASER TONING` |
| HEADLINE3979 | `TRIỆT LÔNG TOÀN THÂN` | `ĐIỀU TRỊ MỤN CHUYÊN SÂU` |
| HEADLINE3980 (tab 2) | `DỊCH VỤ PHUN, XÓA XĂM THẨM MỸ` | `TRIỆT LÔNG - GỘI ĐẦU - MASSAGE` |
| HEADLINE3981 | `PHUN XĂM CHÂN MÀY` | `TRIỆT LÔNG CÔNG NGHỆ CAO` |
| HEADLINE3982 | `ĐIÊU KHẮC CHÂN MÀY` | `GỘI ĐẦU DƯỠNG SINH` |
| HEADLINE3983 | `PHUN MÔI COLLAGEN` | `MASSAGE THƯ GIÃN TOÀN THÂN` |
| HEADLINE3984 | `XÓA XĂM` | `DETOX THẢI ĐỘC DA ĐỘC QUYỀN` |
| BUTTON_TEXT3454 | `✎ TƯ VẤN DỊCH VỤ` | *(giữ nguyên)* |

**Xử lý kỹ thuật bắt buộc — chuyển từ Video sang Ảnh tĩnh** (10 id: `VIDEO3309`…`VIDEO3318`):
1. Trong CSS: rule `#VIDEO330X > .ladi-video > .ladi-video-background{background-image:url("https://img.youtube.com/vi/XXXX/hqdefault.jpg");...}` → đổi URL thành ảnh dịch vụ tương ứng do khách hàng cung cấp (`images/service-01.jpg` … `service-10.jpg`), **giữ nguyên toàn bộ phần còn lại của rule** (`background-size: cover;` v.v.).
2. Trong JSON cấu hình cuối file (`script_ladipage_run`): xoá hẳn 10 cặp key `"VIDEO330X":{"a":"video","ci":"https://www.youtube.com/watch?v=...","ch":"youtube","cg":true}` — không thay số/link khác, xoá để vô hiệu hoá hành vi mở popup video (vì không có video thật thay thế).
3. Giữ nguyên phần tử `<div id="SHAPE330X">` (icon nút play chồng lên ảnh) — **không xoá** vì thuộc cấu trúc DOM/layout gốc; icon play sẽ không có tác dụng (không mở gì khi click) nhưng về mặt hình ảnh vẫn đồng nhất với thiết kế — đây là đánh đổi chấp nhận được để tránh đổi cấu trúc DOM.

### 3.5 3 popup khuyến mãi (ảnh có chữ — khách hàng tự thiết kế theo nội dung dưới, ảnh xong thì chỉ cần đổi `url()`)

| id ảnh | Popup gắn với | Nội dung chữ cần có trong ảnh mới |
|---|---|---|
| `IMAGE4615` (trong `UUDAI79K` / `FORM3298`) | Ưu đãi mụn | `ĐIỀU TRỊ MỤN CHUẨN SPA — KHÔNG SƯNG - KHÔNG ĐAU — CHỈ TỪ 299.000Đ` |
| `IMAGE4519` (trong `PHUNMOI` / `FORM3284`) | Ưu đãi gội giờ vàng | `GỘI THƯ GIÃN CỔ VAI GÁY — GIỜ VÀNG 09:00-14:00 (T2-T6) — CHỈ 99.000Đ` |
| ảnh nền `MIENTRUNG` (trong `FORM3301`) | Ưu đãi trị thâm nách | `TRỊ THÂM NÁCH CHUYÊN SÂU — CHỈ TỪ 499.000Đ` |

Các trường/nút trong 3 form này (Họ tên, SĐT, "NHẬN VOUCHER"/"NHẬN ƯU ĐÃI", đếm ngược "Khuyến Mãi Sẽ Hết Sau/Ngày/Giờ/Phút/Giây") **không đổi text** — đã trung tính.

### 3.6 Form tư vấn "Bác sĩ" (`BACSI`, `FORM3277`)

| id | Cũ | Mới |
|---|---|---|
| `IMAGE4455` (ảnh trong popup) | ảnh bác sĩ nam | ảnh chuyên viên/chủ spa Trang Huỳnh (khách hàng cung cấp) |
| `BUTTON_TEXT3449` | `CHUYỂN HƯỚNG ĐẾN FACEBOOK` | *(giữ nguyên nhãn)* |
| Config JSON `FORM3277.option.dynamic_form_config` | `redirect_url: "https://www.facebook.com/thammyvienseoulcenter"` | **xoá `redirect_url`** (đặt thành form không redirect, hoặc `""`) — không tự đoán link Fanpage thật. *Khi khách hàng cung cấp URL Fanpage, chỉ cần điền lại giá trị này.* |

### 3.7 Chân trang / liên hệ

| Vị trí | Cũ | Mới |
|---|---|---|
| `tel:84914269346` (3 lần, gắn ở `SHAPE3463`, `HEADLINE3914`) | `84914269346` | `84899994509` |
| `HEADLINE3914` | `GỌI NGAY` | *(giữ nguyên, chỉ đổi href tel ở trên)* |
| `HEADLINE3915` | `ĐỊA CHỈ` | `59 Vườn Lài, Phường An Phú Đông, TP. Hồ Chí Minh` *(thay nhãn bằng giá trị thật vì file không có vị trí riêng cho giá trị địa chỉ)* |
| `HEADLINE3968` | `BẠN CẦN TƯ VẤN LÀM ĐẸP XIN ĐỂ LẠI THÔNG TIN ĐỂ TIẾP TỤC ĐẾN CHAT ONLINE` | `BẠN CẦN TƯ VẤN LÀM ĐẸP? ĐỂ LẠI THÔNG TIN ĐỂ ĐƯỢC HỖ TRỢ NGAY` |
| `HEADLINE3993` | `ĐỂ LẠI SỐ ĐIỆN THOẠI – NHẬN CƠ HỘI NÂNG TẦM NHAN SẮC!` | `ĐỂ LẠI SỐ ĐIỆN THOẠI – NHẬN ƯU ĐÃI TỪ ROYAL SPA NGAY!` |
| `HEADLINE3992` | `" !::coupon_text::! "` | **giữ nguyên tuyệt đối** — biến hệ thống LadiPage render mã coupon động, không phải text tĩnh |

### 3.9 [PHÁT HIỆN KHI TEST — ĐÃ VÁ] Vô hiệu hoá live-fetch của Global Section

Kiểm thử thực tế bằng trình duyệt (không chỉ đọc mã tĩnh) phát hiện: 12 div "Global Section" (liệt kê trong mục 8.1 PRD) tuy rỗng trong markup nhưng **engine runtime `ladipagev3.min.js` tự fetch nội dung sống từ tài khoản LadiPage gốc của Seoul Center** dựa vào `data-global-id`/`data-store-id`, chèn thẳng marquee/SĐT/ảnh của Seoul Center vào trang khi chạy thật.

**Fix áp dụng:** dùng regex xoá đúng 2 attribute `data-global-id="..."` và `data-store-id="5977f59d1abc544991d43c5b"` trên cả 12 div, giữ nguyên `id`, `class="ladi-section"` và vị trí DOM:

```python
global_section_pattern = re.compile(
    r'(<div id="G\d+_[A-Z0-9_]+") data-global-id="[a-f0-9]+" data-store-id="5977f59d1abc544991d43c5b"( class="ladi-section"></div>)'
)
html, n = global_section_pattern.subn(r'\1\2', html)  # kỳ vọng n == 12
```

Đã xác nhận bằng browser test: sau khi vá, `document.getElementById('G1759745653409_MENU_MUA1TANG1').children.length === 0` (không còn nội dung ngoài được chèn), marquee/SĐT Seoul Center không còn xuất hiện.

*Ghi chú quan trọng:* danh sách 12 id (không phải 9 như khảo sát tĩnh ban đầu) — có thêm `G1755161786222_FORM_CHINHANH`, `G1703818171569_SECTION3853`, `G1719394824941_SECTION1933` phát hiện khi rà soát lại toàn văn bản tìm `data-store-id`.

### 3.10 Dựng lại nội dung tĩnh cho 7/12 khối global-section

Sau khi vô hiệu hoá live-fetch (mục 3.9), 12 khối trở nên rỗng. **7 khối được dựng lại thành section tĩnh thuần Royal Spa** (HTML + CSS inline, không phụ thuộc LadiPage cloud), dùng đúng bảng màu gốc (`#99183D`, `#AC1D45`, nền hồng `#fdf3f6`) và font `UZOLUdJTFJPWSBCTxELkURg` của trang:

| id khối | Nội dung dựng mới | Nguồn nội dung |
|---|---|---|
| `G1759745653409_MENU_MUA1TANG1` | Thanh promo đầu trang: ưu đãi thành viên (Mua 5 tặng 1 / Mua 10 tặng 3) | PRD mục 4.4 |
| `G1756351929798_MARQUEE_UUDAIVIP` | Marquee chạy chữ: 3 ưu đãi hot | PRD mục 4.4 |
| `G1717122335463_SECTION2682` | **BẢNG GIÁ DỊCH VỤ đầy đủ** — 6 nhóm: Chăm sóc da, Điều trị mụn, Gội đầu dưỡng sinh, Massage thư giãn, Hỗ trợ chăm sóc da, Triệt lông công nghệ cao (kèm 13 vùng + chính sách bảo hành 1/5 năm) + dải ưu đãi thành viên | File Word mục 7, 11 |
| `G1770091972748_UUDAI_79K` | **Bảng giá "Trải nghiệm giá tốt"** — 6 thẻ dịch vụ giá hấp dẫn nhất (từ 60.000đ), có badge Giờ Vàng và "Không sưng – Không đau" | File Word mục 4, 7 |
| `G1763087890781_CAMKET` | Lưới 6 cam kết của Royal Spa | File Word mục 9 |
| `G1719394824941_SECTION1933` | Khối "HOẠT ĐỘNG TẠI ROYAL SPA" — lưới 4 ảnh (ô chờ thay, xem bảng ảnh mục 5) | Theo yêu cầu khách hàng |
| `G1743067768131_FOOTER_SC` | Footer đầy đủ: tên thương hiệu, slogan, mô tả ngắn, địa chỉ, hotline (click-to-call), giờ làm việc, fanpage, dòng bản quyền | File Word mục 14 |

**5 khối còn lại giữ rỗng** (`G1755161786222_FORM_CHINHANH`, `G1776841708745_PHUNXAM_Q2`, `G1761556313318_UUDAI_NGUOITHAN`, `G1761724761034_VONGQUAY`, `G1703818171569_SECTION3853`) — lý do: popup quà tặng theo chi nhánh và gallery "sao Việt" không áp dụng cho spa 1 cơ sở; banner phun xăm không thuộc dịch vụ Royal Spa; vòng quay may mắn và đếm ngược tri ân cần engine widget tương tác riêng của LadiPage, không dựng lại được bằng HTML tĩnh.

### 3.8 Badge trang trí (đồ hoạ "16 năm")

| id | Vai trò | Nội dung mới |
|---|---|---|
| `IMAGE4626` (group-51, badge cutout gần form) | Badge trang trí | Đồ hoạ mới: `Royal Spa By Trang Huỳnh — Nâng Niu Vẻ Đẹp Tự Nhiên` (khách hàng tự thiết kế, giữ style cutout trong suốt) |

---

## 4. Danh sách các chuỗi KHÔNG được đổi (giữ nguyên tuyệt đối)

- `!::coupon_text::!` — biến hệ thống.
- Toàn bộ class `ladi-*`, id `style_ladi`/`style_animation`/`style_page`/`style_element`/`style_lazyload`, các `<script>` block (`script_lazyload`, `script_event_data`, `script_ladipage_run`) — **trừ 2 điểm sửa JSON đã nêu ở mục 3.4.2 và 3.6** (xoá key video, xoá redirect_url).
- Toàn bộ font `.otf` (`svn-gilroy-*`) — không đổi.
- Icon SVG `data:image/svg+xml...` (mũi tên, dấu X, check...) — trung tính, không đổi.
- 9 khối Global Section rỗng (`data-global-id="..."`) — không chèn nội dung, không xoá div (xem PRD mục 8.1).

---

## 5. Bảng ánh xạ hình ảnh (quy ước tên file, khách hàng đặt vào `images/`)

Tạo thư mục `images/` cùng cấp với `index13c1.html`. Đặt đúng tên file sau (không cần báo lại — script áp dụng đọc đúng tên này):

| Tên file trong `images/` | id phần tử HTML | Kích thước khuyến nghị (desktop / mobile) | Ghi chú |
|---|---|---|---|
| `logo.png` | `IMAGE4354` (header), `IMAGE4359` (footer) | ~400×120 (nền trong suốt) | Cùng 1 file dùng 2 chỗ |
| `favicon.png` | `<link rel="icon">` và 4 thẻ liên quan | 512×512 | Vuông |
| `hero-banner-desktop.jpg` | `TRANGCHU` | 1440×712 | `background-size: cover` |
| `hero-banner-mobile.jpg` | `TRANGCHU` (breakpoint mobile) | 768×632 | |
| `hero-gallery-1.jpg` | `IMAGE4326` | ~600×600 | |
| `hero-gallery-2.jpg` | `IMAGE4327` | ~550×550 | |
| `hero-gallery-3.jpg` | `IMAGE4328` | ~550×550 | |
| `hero-gallery-4.jpg` | `IMAGE4329` | ~500×500 | |
| `service-01.jpg` … `service-06.jpg` | `VIDEO3309`…`VIDEO3314` | ~720×450 (crop cover) | Tab "Chăm sóc da & Điều trị mụn" |
| `service-07.jpg` … `service-10.jpg` | `VIDEO3315`…`VIDEO3318` | ~1080×600 (crop cover, thẻ tab 2 to hơn) | Tab "Triệt lông - Gội đầu - Massage" |
| `consultant-photo.jpg` | `IMAGE4455` | ~450×450 | Ảnh chuyên viên/chủ spa |
| `promo-mun-299k.jpg` | `IMAGE4615` | 700×550 (desktop) | Đồ hoạ có chữ, xem nội dung mục 3.5 |
| `promo-goi-99k.jpg` | `IMAGE4519` | 700×500 (desktop) | Đồ hoạ có chữ |
| `promo-nach-499k.jpg` | nền `MIENTRUNG` | 423×496 | Đồ hoạ có chữ |
| `badge-slogan.png` | `IMAGE4626` | ~412×305 (nền trong suốt) | |
| `og-image.jpg` | `<meta property="og:image">` | 1200×630 | |
| `hoatdong-1.jpg` … `hoatdong-4.jpg` | khối "HOẠT ĐỘNG TẠI ROYAL SPA" (`G1719394824941_SECTION1933`) | ~960×600 (tỷ lệ 16:10) | Ảnh không gian spa, phòng chăm sóc da, khách trải nghiệm, đội ngũ chuyên viên. Hiện đang là ô màu hồng nhạt chờ thay. |

**Lưu ý kỹ thuật khi thay ảnh:** mỗi id thường có **2-3 rule CSS ứng với các kích thước responsive khác nhau** (desktop/tablet/mobile) trỏ cùng 1 URL gốc — khi thay, phải thay **toàn bộ các rule** cùng id sang cùng 1 file mới (không chỉ thay rule đầu tiên tìm thấy). Dùng `replace_all` theo URL gốc chính xác (URL gốc đã unique theo từng size-prefix `s###x###/`) để đảm bảo không sót.

---

## 6. Quy trình thực thi từng bước

1. `cp index13c1.html index13c1.original.html` (backup).
2. Viết script Python đọc `index13c1.html`, áp dụng tuần tự các bảng mục 3 (text) bằng `str.replace(old, new)` có đếm số lần thay + assert đúng số lần kỳ vọng (lấy từ số lần xuất hiện đã khảo sát, liệt kê trong comment script).
3. Áp dụng bảng ảnh mục 5 — chỉ chạy bước này **sau khi khách hàng đã đặt đủ ảnh vào `images/`** theo đúng tên; script kiểm tra `os.path.exists()` từng file trước khi thay, báo rõ file nào thiếu thay vì thay nửa chừng.
4. Sửa 2 điểm JSON hành vi (mục 3.4.2 xoá 10 key video, mục 3.6 xoá redirect_url) bằng regex có kiểm soát trên đúng đoạn JSON (không dùng thay thế toàn văn bản tự do vì dễ phá cấu trúc JSON).
5. Ghi đè `index13c1.html`.
6. Chạy bộ kiểm tra tự động (mục 7).
7. Mở file bằng trình duyệt (desktop width ~1440px và mobile width ~390px) đối chiếu trực quan với bản gốc đã backup — xác nhận **không lệch layout**, chỉ khác nội dung/ảnh.

---

## 7. Kiểm thử (QA checklist tự động + thủ công)

**Tự động (grep sau khi build):**
```
grep -ic "seoul" index13c1.html        # kỳ vọng: 0
grep -c "84914269346" index13c1.html   # kỳ vọng: 0
grep -c "84899994509" index13c1.html   # kỳ vọng: 3
grep -c "thammyseoulcenter" index13c1.html  # kỳ vọng: 0
grep -c "data-global-id" index13c1.html     # kỳ vọng: 0 (đã gỡ — xem mục 3.9)
```

**Thủ công (mở trình duyệt, đối chiếu bản backup):**
- [ ] Desktop 1440px: hero, thư viện dịch vụ (2 tab), 3 popup khuyến mãi, menu, footer/popup mobile — vị trí/kích thước từng khối khớp bản gốc.
- [ ] Mobile 390px: tương tự, kiểm tra riêng vì có breakpoint CSS khác desktop.
- [ ] Click từng nút CTA — không có lỗi JS console mới phát sinh (mở DevTools Console).
- [ ] Click 4 ảnh hero-gallery — cuộn đúng tới khối Dịch vụ (không còn mở tab site Seoul Center cũ).
- [ ] Click icon play trên 10 thẻ dịch vụ — không mở gì (đã chủ động vô hiệu hoá), không báo lỗi JS.
- [ ] Nút gọi nhanh ("GỌI NGAY", icon điện thoại) — trỏ đúng `tel:84899994509`.
- [ ] Toàn bộ ảnh load được (không có icon vỡ ảnh) — kiểm tra Network tab không có 404 tới `images/*`.

---

## 8. Rollback

Nếu phát hiện lỗi sau khi ghi đè: khôi phục từ `index13c1.original.html` (`cp index13c1.original.html index13c1.html`), sửa lại script, chạy lại từ bước 2. File backup **giữ lại xuyên suốt dự án**, không xoá.

---

## 9. Rủi ro / giới hạn đã biết

- 12 Global Section (marquee, cam kết, vòng quay, footer đầy đủ, form chi nhánh...) đã được vô hiệu hoá live-fetch (mục 3.9) nên hiển thị rỗng — đúng như kỳ vọng, không còn rủi ro rò rỉ thương hiệu Seoul Center. Việc xây nội dung Royal Spa mới cho các khối này (nếu cần) không thuộc phạm vi dự án này — xem PRD mục 9.
- Script `app.seoulspa.vn/assets/ajax/libs/country_phone.js` (thư viện mã vùng điện thoại cho ô nhập SĐT) được **giữ nguyên, không đổi** — đây là script tiện ích dùng chung, không phải endpoint chứa nội dung/thương hiệu Seoul Center, và không rõ cơ chế thay thế an toàn nên không động vào để tránh hỏng chức năng nhập SĐT.
- Icon nút play trên thẻ dịch vụ (mục 3.4.3) sẽ tồn tại về mặt hình ảnh nhưng không có chức năng — đánh đổi chấp nhận được để giữ nguyên cấu trúc DOM.
- Nếu khách hàng cung cấp ảnh sai tỷ lệ so với bảng mục 5, `background-size: cover` sẽ tự động crop — cần xem lại phần bị cắt (đặc biệt ảnh có chữ/mặt người ở rìa) trước khi bàn giao.
