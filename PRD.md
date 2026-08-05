# PRD — Rebrand Landing Page: Royal Spa By Trang Huỳnh

**Nguồn nội dung:** `ĐỀ XUẤT NỘI DUNG WEBSITE TRỌN VẸN CHO ROYAL SPA BY TRANG HUỲNH BY TRANG HUỲNH.docx`
**File HTML gốc:** `index13c1.html` (landing page clone, xuất từ LadiPage, thương hiệu gốc "Seoul Center" — thẩm mỹ viện)
**Ngày lập:** 2026-08-04

---

## 1. Mục tiêu dự án

Thay toàn bộ **nội dung chữ** và **hình ảnh** trong file `index13c1.html` từ thương hiệu gốc "Seoul Center" (thẩm mỹ viện) sang thương hiệu **Royal Spa By Trang Huỳnh** (spa chăm sóc da, điều trị mụn, triệt lông, gội đầu dưỡng sinh, massage), dựa trên nội dung trong file Word đề xuất.

### Ràng buộc cứng (không được vi phạm)
- **Không đổi giao diện / layout / cấu trúc HTML** — giữ nguyên toàn bộ section, id, class, CSS, thứ tự phần tử, breakpoint desktop/mobile.
- Chỉ thay: (a) nội dung text hiển thị, (b) hình ảnh (do khách hàng tự cung cấp và chèn), (c) các giá trị liên hệ (số điện thoại, địa chỉ), (d) thẻ meta/SEO.
- Không thêm/xoá phần tử DOM, không đổi kỹ thuật hiển thị (trừ 1 ngoại lệ kỹ thuật bắt buộc — xem mục 6.3).

### Lưu ý phạm vi ảnh
Khách hàng sẽ **tự chèn hình ảnh** vào dự án (không yêu cầu Claude tải ảnh từ Google Drive). PRD này mô tả **vị trí, mô tả nội dung, kích thước yêu cầu** cho từng ảnh để khách hàng chuẩn bị đúng — chi tiết kỹ thuật (tên file, đường dẫn) nằm trong `TDD.md`.

---

## 2. Bối cảnh hiện trạng file HTML

File là bản xuất tĩnh từ **LadiPage** (landing page builder), 1 trang dài (one-page), **không phải website nhiều trang**. Menu chỉ là các anchor cuộn tới section trong cùng 1 trang, không phải 11 trang riêng như mục "MENU WEBSITE" trong file Word liệt kê. Đây là điều **quan trọng cần hiểu trước khi triển khai**:

- Nội dung trong file Word (đủ 14 mục, từ SEO tổng thể đến blog chuẩn SEO) được **ánh xạ vào các block có sẵn** của trang landing hiện tại — không tạo trang mới.
- Trang gốc có nhiều cơ chế marketing đặc thù ngành thẩm mỹ viện (form tư vấn "bác sĩ", vòng quay may mắn, popup nhận quà, đếm ngược flash-sale, thư viện video dịch vụ) — các cơ chế này **được giữ nguyên cấu trúc**, chỉ đổi nội dung/chủ đề cho phù hợp Royal Spa.
- Một phần các "section" trong file là **Global Section rỗng** của LadiPage (nội dung thật lưu trên cloud LadiPage, không có trong file tĩnh này) — xem mục 8 "Giới hạn kỹ thuật đã biết".

---

## 3. Nhận diện thương hiệu Royal Spa (rút ra từ ảnh bìa Fanpage trong Drive)

Ảnh bìa `Ảnh bìa Royal Spa by Trang Huynh.png` (thư mục Avatar - Cover) cho thấy:
- **Logo:** biểu tượng vương miện (crown) màu vàng đồng + chữ "ROYAL SPA" (serif, chữ hoa) + dòng chữ script nhỏ "by Trang Huỳnh" bên dưới.
- **Tagline hiện có trên bộ nhận diện:** "Spa 5 sao — Tiêu chuẩn Hàn Quốc" (kèm cờ Việt Nam + Hàn Quốc).
- **Tông màu:** be/kem, vàng đồng (rose gold), trắng — sang trọng, nhẹ nhàng, khác hẳn tông đỏ hồng của Seoul Center gốc.
- **Đối tác công nghệ:** CHA Meditech, Cellromax, Cellterm, Calluma, Dreamsys (logo đối tác xuất hiện trên ảnh bìa — có thể dùng lại nếu khách hàng muốn nhấn mạnh "hợp tác thương hiệu Hàn Quốc", không bắt buộc).

→ Khuyến nghị dùng tông màu này khi khách hàng tự thiết kế/chọn các ảnh đồ hoạ thay thế (banner, badge khuyến mãi) để đồng bộ nhận diện.

---

## 4. Ánh xạ nội dung chi tiết theo từng khối

> Cột "Vị trí (id)" tham chiếu đúng id phần tử trong HTML gốc — dùng để đối chiếu với `TDD.md`.

### 4.1 Thẻ SEO tổng thể (`<head>`)

| Thẻ | Nội dung cũ | Nội dung mới |
|---|---|---|
| `<title>` | Seoul Center \| Thẩm Mỹ Viện Làm Đẹp Hàng Đầu Việt Nam | **Royal Spa By Trang Huỳnh \| Chăm Sóc Da - Điều Trị Mụn - Triệt Lông - Gội Đầu Dưỡng Sinh TP.HCM** |
| `meta description` | Seoul Center Top Thẩm Mỹ Viện Làm Đẹp Hàng Đầu Việt Nam | **Royal Spa By Trang Huỳnh chuyên chăm sóc da, điều trị mụn không sưng không đau, triệt lông công nghệ cao, gội đầu dưỡng sinh, massage thư giãn cổ vai gáy tại TP.HCM. Đặt lịch ngay để nhận nhiều ưu đãi hấp dẫn.** |
| `meta keywords` | Seoul Center, TMV Seoul Center, thẩm mỹ viện làm đẹp, nâng mũi, cắt mí, phun môi, điêu khắc chân mày | Royal Spa, Royal Spa By Trang Huỳnh, chăm sóc da, điều trị mụn, triệt lông công nghệ cao, gội đầu dưỡng sinh, massage thư giãn, spa TP.HCM |
| `meta robots` | noindex, nofollow | **index, follow** (đề xuất — vì đây sẽ là site chính thức, không phải trang landing chạy ads ẩn) |
| `og:title`, `og:description` | (giống title/description cũ) | giống title/description mới ở trên |
| `og:image` | ảnh Seoul Center | ảnh đại diện Royal Spa (khách hàng cung cấp) |
| `canonical`, `og:url` | `https://khuyenmai.thammyseoulcenter.com` | **Cần domain thật của Royal Spa** — chưa có nên để trống/placeholder, KHÔNG tự đặt domain (xem mục 8) |
| favicon / apple-touch-icon | logo Seoul Center | logo Royal Spa (khách hàng cung cấp) |

### 4.2 Menu điều hướng (thanh menu trên cùng)

Menu hiện tại gồm 6 mục anchor trong-trang. Toàn bộ nhãn menu này **đã trung tính về thương hiệu** (không chứa chữ "Seoul") nên **giữ nguyên**, chỉ map lại đích tới nội dung Royal Spa tương ứng:

| Nhãn menu | Trỏ tới section | Giữ/Đổi |
|---|---|---|
| Dịch Vụ | Thư viện dịch vụ | Giữ nguyên |
| Về Chúng Tôi | Giới thiệu thương hiệu | Giữ nguyên |
| Trải Nghiệm Khách Hàng | Feedback khách hàng | Giữ nguyên |
| Cam Kết | Cam kết (xem giới hạn mục 8.1) | Giữ nguyên |
| Liên Hệ | Thông tin liên hệ | Giữ nguyên |
| Chương Trình | Ưu đãi/khuyến mãi | Giữ nguyên |

Menu popup mobile (hamburger) lặp lại các nhãn trên, riêng 1 nhãn **"DỊCH VỤ SEOUL"** phải đổi thành **"DỊCH VỤ ROYAL SPA"** (có chứa tên thương hiệu cũ).

### 4.3 Banner Hero (đầu trang)

| Vị trí | Nội dung cũ | Nội dung mới |
|---|---|---|
| Dòng tiêu đề lớn | THẨM MỸ VIỆN / SEOUL CENTER | **ROYAL SPA BY TRANG HUỲNH** (dòng lớn) |
| Dòng phụ đề | (chung với trên) | **Chạm Đến Vẻ Đẹp Tự Nhiên - Đánh Thức Sự Tự Tin** (dòng nhỏ hơn) |
| Đoạn giới thiệu (paragraph) | Đoạn giới thiệu Seoul Center (16 năm, hệ thống chi nhánh...) | **"Ra đời với mong muốn mang đến những giá trị làm đẹp an toàn, khoa học và bền vững, Royal Spa By Trang Huỳnh không chỉ là nơi chăm sóc sắc đẹp mà còn là không gian thư giãn giúp khách hàng tái tạo năng lượng và tìm lại sự cân bằng trong cuộc sống. Với đội ngũ chuyên viên được đào tạo bài bản, quy trình chăm sóc chuyên nghiệp cùng hệ thống công nghệ hiện đại, Royal Spa By Trang Huỳnh luôn đặt sự hài lòng và an toàn của khách hàng lên hàng đầu. Chúng tôi tin rằng: Mỗi người phụ nữ đều xứng đáng sở hữu vẻ đẹp tự nhiên, khỏe mạnh và tự tin nhất."** |
| Nút CTA | ✎ TƯ VẤN NGAY | **✎ ĐẶT LỊCH NGAY** |
| Ảnh nền banner (desktop + mobile) | Đồ hoạ ghép "16 năm Seoul Center" (có ảnh 2 người đại diện, toà nhà, giải thưởng bịa) | Ảnh thật Royal Spa (khách hàng cung cấp) — xem mục 5 |
| 4 ảnh nhỏ dưới đoạn giới thiệu | 1 ảnh phòng dịch vụ (có logo Seoul) + 2 ảnh nhân viên "quy trình" + 1 ảnh chuyên viên | 4 ảnh thật Royal Spa (khách hàng cung cấp) — bỏ link ngoài trỏ về site Seoul Center, chuyển thành cuộn tới section Dịch Vụ |

### 4.4 Khối ưu đãi nổi bật (3 popup quảng cáo góc trang)

Trang gốc có sẵn đúng **3 popup khuyến mãi độc lập** (mỗi popup = 1 ảnh đồ hoạ có chữ + 1 form thu thập số điện thoại). File Word cũng có đúng **3 ưu đãi hot đầu trang** → khớp 1:1, không cần bịa thêm nội dung:

| Popup (vị trí) | Nội dung đồ hoạ mới (khách hàng tự thiết kế ảnh theo nội dung này) |
|---|---|
| Popup "UUDAI79K" | 🔥 **Điều trị mụn chuẩn Spa — Không sưng - Không đau — Chỉ từ 299.000 VNĐ** |
| Popup "PHUNMOI" | 💆‍♀️ **Gội thư giãn cổ vai gáy — Giờ vàng 09:00-14:00 (Thứ Hai - Thứ Sáu) — Chỉ 99.000 VNĐ** |
| Popup "MIENTRUNG" | ✨ **Trị thâm nách chuyên sâu — Chỉ từ 499.000 VNĐ** |

Nút bấm trong các popup này ("NHẬN VOUCHER", "NHẬN ƯU ĐÃI") và các nhãn đếm ngược ("Khuyến Mãi Sẽ Hết Sau", "Ngày/Giờ/Phút/Giây") **giữ nguyên** — đã trung tính thương hiệu.

Khối marquee chạy chữ trên cùng (2 dải chữ chạy) → dùng để đăng 2 ưu đãi thành viên trong file Word mục 11: **"MUA 5 BUỔI TẶNG 1 BUỔI"** và **"MUA 10 BUỔI TẶNG 3 BUỔI"** — *(lưu ý: xem giới hạn kỹ thuật mục 8.1, khối này hiện đang rỗng trong file tĩnh).*

### 4.5 Giới thiệu thương hiệu ("Về Chúng Tôi")

Dùng chung nội dung đoạn giới thiệu ở mục 4.3 (đã đưa vào hero). Nếu cần tách riêng thành section "Về Chúng Tôi" độc lập sau này, đây chính là nội dung dùng lại.

### 4.6 "Tại sao khách hàng chọn Royal Spa" / "Cam Kết"

File Word có 2 danh sách gần giống nhau:
- Mục 6: 8 lý do chọn Royal Spa (✔ Liệu trình cá nhân hoá, ✔ Kỹ thuật viên tận tâm, ✔ Công nghệ hiện đại, ✔ Sản phẩm chính hãng, ✔ Không gian sang trọng, ✔ Chi phí minh bạch, ✔ Không chèo kéo, ✔ Đồng hành xuyên suốt)
- Mục 9: 6 cam kết (✓ Tư vấn trung thực, ✓ Không phát sinh chi phí, ✓ Mỹ phẩm chính hãng, ✓ Vệ sinh vô khuẩn, ✓ Không chèo kéo, ✓ Đồng hành đến khi hài lòng)

→ Nội dung **đã soạn sẵn, sử dụng khi có vị trí trong HTML** (xem giới hạn mục 8.1 — hiện khối "CAM KẾT" đang là block rỗng trong file tĩnh).

### 4.7 Thư viện dịch vụ (khối 10 thẻ dịch vụ, 2 tab)

Đây là khối nội dung lớn nhất cần đổi. Bản gốc dùng **video YouTube** cho từng thẻ dịch vụ; vì Royal Spa hiện chưa có video dịch vụ public, khối này **chuyển thành lưới ảnh tĩnh** (giữ nguyên layout thẻ/tab, chỉ đổi ảnh + tên dịch vụ — xem mục 6.3 để biết lý do kỹ thuật).

| Vị trí | Cũ | Mới |
|---|---|---|
| Tiêu đề khối | THƯ VIỆN DỊCH VỤ - SEOUL CENTER | **THƯ VIỆN DỊCH VỤ - ROYAL SPA** |
| Phụ đề | HÀNG TRIỆU KHÁCH HÀNG ĐÃ TRẢI NGHIỆM | **5.000+ KHÁCH HÀNG ĐÃ TRẢI NGHIỆM** *(khớp số liệu thật trong mục "Con số biết nói")* |
| **Tab 1** | DỊCH VỤ THẨM MỸ LÀN DA | **CHĂM SÓC DA & ĐIỀU TRỊ MỤN** |
| Thẻ 1.1 | Collagen Organic | **Chăm sóc da cơ bản** *(60 phút \| 300.000đ)* |
| Thẻ 1.2 | Điều trị mụn | **Chăm sóc da chuyên sâu** *(60 phút \| 500.000đ)* |
| Thẻ 1.3 | Meso không kim | **Combo chăm sóc mặt & cổ** *(60 phút \| 650.000đ)* |
| Thẻ 1.4 | Điều trị thâm nám | **Aqua Peeling** *(30 phút \| 200.000đ)* |
| Thẻ 1.5 | Điều trị sẹo, mụn | **Laser Toning** *(30 phút \| 300.000đ)* |
| Thẻ 1.6 | Triệt lông toàn thân | **Điều trị mụn chuyên sâu** *(60 phút \| 400.000đ)* |
| **Tab 2** | DỊCH VỤ PHUN, XÓA XĂM THẨM MỸ | **TRIỆT LÔNG - GỘI ĐẦU - MASSAGE** |
| Thẻ 2.1 | Phun xăm chân mày | **Triệt lông công nghệ cao** *(An toàn - Nhẹ nhàng - Hiệu quả lâu dài)* |
| Thẻ 2.2 | Điêu khắc chân mày | **Gội đầu dưỡng sinh** *(Thảo dược - Phục hồi tóc - Thư giãn cổ vai gáy)* |
| Thẻ 2.3 | Phun môi Collagen | **Massage thư giãn toàn thân** *(Tinh dầu - Đá nóng)* |
| Thẻ 2.4 | Xóa xăm | **Detox thải độc da độc quyền** *(60 phút \| 600.000đ)* |
| Nút CTA cuối khối | ✎ TƯ VẤN DỊCH VỤ | Giữ nguyên |

*Ghi chú:* Combo chăm sóc da mụn lưng, Peel vi kim tảo biển, Phi kim/Lăn kim/Điện di tinh chất, Trị thâm nách... trong file Word nhưng không có slot 10 thẻ → đưa vào **Bảng Giá** dạng đầy đủ nếu sau này bổ sung trang riêng (ngoài phạm vi PRD này, xem mục 9).

### 4.8 Quy trình chăm sóc chuẩn

File Word mục 8 có 6 bước (Tiếp nhận → Thăm khám/soi da → Tư vấn liệu trình → Thực hiện → Hướng dẫn tại nhà → Theo dõi sau dịch vụ). HTML gốc có sẵn 2 ảnh minh hoạ quy trình (không có text riêng, chỉ là ảnh nhân viên đang thao tác) nằm trong nhóm 4 ảnh ở hero (mục 4.3) — dùng làm ảnh minh hoạ chung cho quy trình chăm sóc, không có vị trí hiển thị 6 bước dạng text riêng trong file tĩnh hiện tại (xem mục 9 — ngoài phạm vi, có thể bổ sung sau).

### 4.9 Feedback khách hàng

Không có vị trí hiển thị danh sách feedback dạng text trong file tĩnh (phần "TRẢI NGHIỆM KHÁCH HÀNG" là mục menu trỏ tới global-section rỗng — xem mục 8.1). 4 câu feedback trong file Word được giữ lại làm nội dung dự phòng khi bổ sung khối này sau.

### 4.10 Con số biết nói

Không có khối thống kê số liệu (5.000+, 95%, 10+, 100%) trong file tĩnh hiện tại. Số liệu **5.000+ khách hàng** đã được tận dụng ở mục 4.7 (phụ đề thư viện dịch vụ) để không lãng phí.

### 4.11 Form tư vấn / popup thu thập lead

Có 4 form thu thập lead trong trang (form tư vấn "bác sĩ", 3 form trong popup khuyến mãi). Toàn bộ nhãn field ("Họ và tên", "Số điện thoại", placeholder tên/SĐT khách) **đã trung tính, giữ nguyên**.

Riêng **form tư vấn** (gắn với popup ảnh "bác sĩ" — không phù hợp vì Royal Spa không phải phòng khám):
- Ảnh minh hoạ (hiện là ảnh bác sĩ nam áo blouse trắng) → đổi thành ảnh **chuyên viên/chủ spa Trang Huỳnh** (khách hàng cung cấp).
- Nút "CHUYỂN HƯỚNG ĐẾN FACEBOOK" giữ nguyên nhãn, nhưng đích chuyển hướng (link Fanpage Facebook) **cần khách hàng cung cấp URL Fanpage thật** — hiện tại sẽ vô hiệu hoá link này thay vì đoán URL (xem mục 8.2).

### 4.12 Chân trang / Liên hệ

| Vị trí | Cũ | Mới |
|---|---|---|
| Số điện thoại (nút gọi nhanh, xuất hiện 3 lần trong file) | 0914 269 346 | **0899 994 509** |
| Nhãn "ĐỊA CHỈ" | (label, không có giá trị địa chỉ đi kèm trong file tĩnh) | **59 Vườn Lài, Phường An Phú Đông, TP. Hồ Chí Minh** |
| Giờ làm việc | (không có trong file tĩnh) | 09:00 - 20:00 *(bổ sung nếu có vị trí khi triển khai)* |
| Fanpage | (không có trong file tĩnh) | Royal Spa By Trang Huỳnh *(cần URL thật)* |

### 4.13 Slogan đề xuất

**"Royal Spa By Trang Huỳnh — Nâng Niu Vẻ Đẹp Tự Nhiên"** — dùng cho badge trang trí sẵn có trong hero (ảnh badge "16 năm" của Seoul Center → thay bằng badge slogan này, khách hàng tự thiết kế ảnh).

---

## 5. Danh sách hình ảnh cần chuẩn bị (khách hàng tự chèn)

| # | Vị trí trong trang | Mô tả nội dung ảnh cần | Kích thước khuyến nghị (desktop / mobile) | Loại |
|---|---|---|---|---|
| 1 | Logo header + footer | Logo Royal Spa (crown + wordmark), nền trong suốt | ~400×120px (PNG trong suốt) | Logo |
| 2 | Favicon / touch-icon | Biểu tượng vuông logo Royal Spa | 512×512px | Icon |
| 3 | Banner Hero nền | Ảnh đại diện Royal Spa (không gian spa / chân dung chủ spa) | 1440×712px / 768×632px | Ảnh chụp |
| 4-7 | 4 ảnh dải dưới đoạn giới thiệu hero | Ảnh thật: không gian spa, chuyên viên đang thao tác, khách hàng trải nghiệm | ~600×600px mỗi ảnh (vuông) | Ảnh chụp |
| 8-17 | 10 thẻ dịch vụ (mục 4.7) | Ảnh minh hoạ từng dịch vụ tương ứng (chăm da, aqua peeling, laser toning, mụn, triệt lông, gội đầu, massage, detox...) | ~720×450px/ảnh (crop cover) | Ảnh chụp |
| 18 | Ảnh chuyên viên tư vấn (form BÁC SĨ cũ) | Chân dung chuyên viên/chủ spa Trang Huỳnh | ~450×450px | Ảnh chụp |
| 19 | Popup "Điều trị mụn 299k" | Đồ hoạ có chữ (xem nội dung mục 4.4) | 423×473px / 408×446px | Đồ hoạ thiết kế |
| 20 | Popup "Gội giờ vàng 99k" | Đồ hoạ có chữ (xem nội dung mục 4.4) | 423×473px / 408×446px | Đồ hoạ thiết kế |
| 21 | Popup "Trị thâm nách 499k" | Đồ hoạ có chữ (xem nội dung mục 4.4) | 423×496px / 408×494px | Đồ hoạ thiết kế |
| 22 | Badge slogan trang trí | "Royal Spa By Trang Huỳnh — Nâng Niu Vẻ Đẹp Tự Nhiên" dạng badge/cutout | ~412×305px, nền trong suốt | Đồ hoạ thiết kế |
| 23 | OG image (chia sẻ mạng xã hội) | Ảnh đại diện thương hiệu | 1200×630px | Ảnh/Đồ hoạ |

*Chi tiết tên file, đường dẫn thư mục, id phần tử HTML tương ứng từng ảnh trên → xem `TDD.md` mục "Bảng ánh xạ hình ảnh".*

---

## 6. Quyết định & giả định quan trọng (đã chốt, không cần hỏi lại)

1. **Giữ nguyên toàn bộ layout/CSS/breakpoint** — chỉ sửa nội dung text (trong các thẻ headline/paragraph/button có sẵn) và thuộc tính `url()` của ảnh nền.
2. **10 thẻ "video dịch vụ" chuyển thành 10 thẻ ảnh tĩnh** (bỏ cơ chế phát video YouTube vì không có video thật của Royal Spa) — giữ nguyên lưới/tab/kích thước thẻ, chỉ đổi ảnh nền + tên dịch vụ, gỡ hành vi click-mở-video.
3. **3 popup khuyến mãi hiện có** ánh xạ đúng 3 ưu đãi hot trong file Word (mục 4.4) — không cần thêm/bớt popup.
4. Các khối rỗng do phụ thuộc LadiPage cloud (marquee, cam kết, vòng quay...) **giữ nguyên trạng thái rỗng** — không chèn nội dung mới vào vì không có cấu trúc DOM sẵn có để sửa (xem mục 8.1).
5. 4 ảnh dưới đoạn giới thiệu hero: bỏ liên kết ngoài trỏ về site cũ của Seoul Center, chuyển thành cuộn nội bộ tới khối Dịch Vụ.
6. Link Facebook redirect trong form tư vấn: **vô hiệu hoá** (không tự đoán URL Fanpage).
7. Domain thật (canonical/OG url): để trống/placeholder, chưa có domain chính thức.

---

## 7. Tiêu chí nghiệm thu

- [ ] Không còn bất kỳ chuỗi nào chứa "Seoul", "Seoul Center", "thammyseoulcenter" trong file HTML.
- [ ] Toàn bộ số điện thoại hiển thị/liên kết `tel:` là 0899 994 509.
- [ ] Địa chỉ, giờ làm việc đúng theo file Word.
- [ ] 10 thẻ dịch vụ hiển thị đúng tên + đúng ảnh do khách hàng cung cấp, không còn phát video YouTube cũ.
- [ ] 3 popup khuyến mãi hiển thị đúng nội dung ưu đãi Royal Spa.
- [ ] Toàn bộ layout desktop và mobile giữ nguyên như bản gốc khi so sánh trực quan (không lệch vị trí, không vỡ layout).
- [ ] Thẻ `<title>`, meta description, favicon, OG tags đã cập nhật theo Royal Spa.
- [ ] File chạy được độc lập (mở trực tiếp bằng trình duyệt) không lỗi console nghiêm trọng liên quan tới phần đã sửa.

---

## 8. Giới hạn kỹ thuật đã biết (quan trọng — đọc trước khi triển khai)

### 8.1 Global Section — ĐÃ PHÁT HIỆN RỦI RO NGHIÊM TRỌNG VÀ ĐÃ VÁ

File chứa 12 khối LadiPage gọi là "Global Section" (marquee ưu đãi đầu trang, khối Cam Kết, "79K", "Phun xăm Q2", "Ưu đãi người thân", "Vòng quay may mắn", Footer chính, Section2682, Section3853, Section1933, Form chi nhánh...). Trong **mã nguồn tĩnh**, các khối này trông rỗng (`<div ... class="ladi-section"></div>` không có nội dung con), nên đánh giá ban đầu là "vô hại, chỉ cần bỏ qua".

**Kiểm thử thực tế trên trình duyệt phát hiện điều ngược lại:** khi trang chạy thật (có kết nối mạng), engine runtime của LadiPage (`ladipagev3.min.js`) đọc 2 thuộc tính `data-global-id` + `data-store-id` trên các div này và **tự động tải trực tiếp nội dung sống (live) từ tài khoản LadiPage gốc của Seoul Center** (store `5977f59d1abc544991d43c5b`) rồi chèn vào trang — bao gồm nguyên thanh marquee "SEOUL CENTER", số điện thoại cũ (0914 269 346), hình ảnh quảng cáo hiện tại của Seoul Center. Tức là nếu không xử lý, **website Royal Spa khi lên mạng thật sự sẽ tự động hiển thị thương hiệu và số điện thoại của đối thủ** — nghiêm trọng hơn nhiều so với việc chỉ "rỗng".

**Đã vá:** gỡ 2 thuộc tính `data-global-id` và `data-store-id` khỏi cả 12 div này (giữ nguyên div/section — không đổi cấu trúc DOM), vô hiệu hoá hoàn toàn việc tự tải nội dung ngoài. Đã kiểm tra lại bằng trình duyệt thật: marquee và số điện thoại lạ không còn xuất hiện.

**Bổ sung sau khi vá (theo yêu cầu khách hàng):** 7/12 khối đã được **dựng lại thành section tĩnh thuần Royal Spa** (không phụ thuộc LadiPage cloud), dùng đúng bảng màu và font của trang gốc:

| Khối | Nội dung Royal Spa đã dựng |
|---|---|
| Thanh promo đầu trang | Ưu đãi thành viên: Mua 5 tặng 1 / Mua 10 tặng 3 |
| Marquee chạy chữ | 3 ưu đãi hot (mụn 299k / gội giờ vàng 99k / thâm nách 499k) |
| Khối "79K" cũ | **Bảng giá "Trải nghiệm giá tốt"** — 6 dịch vụ giá hấp dẫn từ 60.000đ |
| Section2682 | **BẢNG GIÁ DỊCH VỤ đầy đủ** — toàn bộ 6 nhóm dịch vụ trong file Word, kèm 13 vùng triệt lông + chính sách bảo hành |
| Khối "Cam Kết" | Lưới 6 cam kết (mục 4.6 / file Word mục 9) |
| Khối "Hoạt động chi nhánh" | "HOẠT ĐỘNG TẠI ROYAL SPA" — lưới 4 ảnh (ô chờ khách hàng thay ảnh) |
| Footer | Footer đầy đủ: thương hiệu, slogan, mô tả, địa chỉ, hotline, giờ làm việc, fanpage, bản quyền |

**5 khối giữ rỗng:** popup quà tặng theo chi nhánh, banner phun xăm, đếm ngược tri ân người thân, vòng quay may mắn, gallery "sao Việt" — không áp dụng cho spa 1 cơ sở, không thuộc dịch vụ Royal Spa, hoặc cần engine widget tương tác riêng của LadiPage không thể dựng lại bằng HTML tĩnh.

### 8.2 Thiếu thông tin cần khách hàng bổ sung sau
- **URL Fanpage Facebook thật** của Royal Spa (để gắn vào nút "CHUYỂN HƯỚNG ĐẾN FACEBOOK").
- **Domain chính thức** của website (để điền canonical URL, og:url).
- Các mục này sẽ để trống/vô hiệu hoá tạm thời, không tự suy đoán.

---

## 9. Ngoài phạm vi (Out of scope)

- Tạo trang con riêng (Bảng giá đầy đủ, Blog/Tin tức, Hình ảnh khách hàng dạng gallery riêng) — file Word đề xuất cấu trúc nhiều trang nhưng file HTML hiện tại chỉ là 1 trang landing.
- Khôi phục nội dung các Global Section rỗng (mục 8.1) — cần truy cập tài khoản LadiPage gốc.
- Thiết kế lại giao diện, đổi bố cục, đổi bảng màu CSS tổng thể.
- Viết bài blog SEO chi tiết (chỉ có tên đề tài trong file Word, chưa có nội dung bài).
- Tích hợp hệ thống đặt lịch, CRM, thanh toán.
