# Hình ảnh & bảng màu — Royal Spa

88 vị trí ảnh đều dùng ảnh/đồ hoạ của Royal Spa. Không còn ảnh thương hiệu cũ, không còn ảnh tải từ CDN bên ngoài.

`service-11/12/13.jpg` không được trang gọi trực tiếp — chúng là nguồn để
`build_cards.py` dựng 3 thẻ "trải nghiệm giá tốt" (trước đây 6 thẻ chỉ dùng 4 ảnh,
hai cặp bị trùng nhau).

Dung lượng `images/`: **10M**.

## Bảng màu (vàng champagne)

Mảng lớn dùng champagne nhạt để không bị "mù tạt"; vàng kim loại đậm chỉ dùng
làm điểm nhấn nhỏ. Nền trang giữ ivory sáng.

| Vai trò | Mã | Dùng ở đâu |
|---|---|---|
| Gradient champagne (nền) | `#bf9f65 → #f6efdd → #e2d0a8` | thanh header, footer, nút, dải ưu đãi |
| Gradient vàng (chữ) | `#6b5326 → #c9a227 → #6b5326` | 10 tiêu đề lớn (clip vào chữ) |
| Vàng đồng đậm | `#7a5f2a` | tiêu đề phụ, viền, chữ trên nền sáng |
| Nâu espresso | `#3a2d12` | chữ trên nền champagne |
| Ivory | `#fdfbf7` | nền trang; chữ trên nền nâu đồng đậm |

## Menu (theo file Word)

File Word liệt kê 11 mục cho một website nhiều trang. Bản này là landing page 1 trang,
nên mỗi mục được trỏ tới đúng khối đang chứa nội dung đó:

| Menu | Cuộn tới |
|---|---|
| Trang Chủ | banner đầu trang |
| Giới Thiệu | khối giới thiệu thương hiệu |
| Dịch Vụ | Thư viện dịch vụ (chăm sóc da, điều trị mụn, triệt lông, gội đầu, massage) |
| Bảng Giá | Bảng giá dịch vụ đầy đủ |
| Hình Ảnh Khách Hàng | Không gian làm đẹp + Hoạt động tại Royal Spa |
| Liên Hệ | Footer (địa chỉ, hotline, giờ làm việc) |

**Chưa đưa vào menu:** 5 mục dịch vụ con (Chăm sóc da, Điều trị mụn, Triệt lông,
Gội đầu dưỡng sinh, Massage) vì cả 5 đều nằm trong "Dịch Vụ" của trang 1 trang;
và "Tin tức làm đẹp" vì file Word mới có tên đề tài, chưa có bài viết.

## Thư mục

- `images/` — đưa lên hosting.
- `fonts/` — 4 file SVN-Gilroy (font gốc của trang), dùng để render chữ lên ảnh.
- `_nguon-anh/` — ảnh & video gốc từ Drive (~2GB). **Không cần upload.**
- `index13c1.pre-gold.html` — bản trước khi đổi màu, để chạy lại quy trình đổi màu từ đầu.

## Dựng lại (chạy đúng thứ tự)

```bash
python3 scripts/build_brand.py      # logo, favicon, og-image
python3 scripts/build_photos.py     # ảnh thật (tự xoay đúng EXIF, tự cân sáng)
python3 scripts/build_cards.py      # card bảng giá, popup khuyến mãi
python3 scripts/build_decor.py      # tiêu đề, cam kết, quy trình, footer

# đổi màu (chỉ chạy lại khi bắt đầu từ index13c1.pre-gold.html)
python3 scripts/recolor_gold.py     # plum/navy -> vàng
python3 scripts/gild_overrides.py   # gradient + sửa tương phản chữ

# dọn phần thừa của thương hiệu cũ (chạy được nhiều lần, không đổi gì thêm)
python3 scripts/strip_thirdparty.py # gỡ GA/GTM/Zalo Ads/CRM của Seoul Center
python3 scripts/fix_spin_prizes.py  # nhãn vòng quay theo ưu đãi của Royal Spa
```

**Đổi ảnh một dịch vụ:** sửa dòng tương ứng trong bảng `PLAN` của `scripts/build_photos.py`.

**Đổi giá / chữ trên card:** sửa bảng `grid` và `cheap` trong `scripts/build_cards.py`.

## Nhận diện — 5 file

| File | KB |
|---|---|
| `favicon.png` | 41 |
| `logo-am-ban-ngang.png` | 32 |
| `logo-gold.png` | 46 |
| `logo.png` | 38 |
| `og-image.jpg` | 67 |


## Ảnh thật — 40 file

| File | KB |
|---|---|
| `2c.jpg` | 94 |
| `3b.jpg` | 85 |
| `3d.jpg` | 95 |
| `3f.jpg` | 71 |
| `412972196-753102780196210-670028661699914443-n-1.jpg` | 120 |
| `415226550-756874179819070-3244573965065649515-n.jpg` | 112 |
| `415254840-756874153152406-438359351930390222-n.jpg` | 143 |
| `416138640-761033932736428-9071160629185595640-n.jpg` | 123 |
| `416558486-759908876182267-5920374145598890621-n.jpg` | 94 |
| `416683153-759908829515605-6469412522089706723-n.jpg` | 84 |
| `416710410-759908982848923-2770817965731378380-n.jpg` | 108 |
| `416710824-759908839515604-5511287744794537422-n.jpg` | 130 |
| `4c.jpg` | 94 |
| `artboard-1.jpg` | 84 |
| `artboard-2-copy-6.jpg` | 101 |
| `artboard-2-copy-7.jpg` | 92 |
| `artboard-2-copy-9.jpg` | 85 |
| `artboard-2-copy.jpg` | 93 |
| `bod.jpeg` | 7 |
| `consultant-photo.jpg` | 23 |
| `hero-banner-desktop.jpg` | 129 |
| `hero-banner-mobile.jpg` | 88 |
| `hero-gallery-1.jpg` | 49 |
| `hero-gallery-2.jpg` | 56 |
| `hero-gallery-3.jpg` | 71 |
| `hero-gallery-4.jpg` | 43 |
| `service-01.jpg` | 42 |
| `service-02.jpg` | 44 |
| `service-03.jpg` | 44 |
| `service-04.jpg` | 47 |
| `service-05.jpg` | 35 |
| `service-06.jpg` | 52 |
| `service-07.jpg` | 68 |
| `service-08.jpg` | 65 |
| `service-09.jpg` | 76 |
| `service-10.jpg` | 81 |
| `service-11.jpg` | 34 |
| `service-12.jpg` | 65 |
| `service-13.jpg` | 65 |
| `trai-nghiem-khach-hang-1.jpg` | 120 |


## Đồ hoạ dựng — 49 file

| File | KB |
|---|---|
| `1080x6288.png` | 252 |
| `1920x800000000.png` | 16 |
| `1e.png` | 2 |
| `603x900.png` | 14 |
| `603x9003333.png` | 14 |
| `asset-1.png` | 14 |
| `avtaytb.png` | 274 |
| `background.png` | 17 |
| `badge-slogan.png` | 254 |
| `bg.png` | 275 |
| `cham-soc-da-cao-cap.png` | 231 |
| `collagen-organic-fix-ten.png` | 213 |
| `cta.png` | 4 |
| `dmca-logo-grn-btn100w.png` | 12 |
| `ds.png` | 3 |
| `giam-mo-dtox-dong-y.png` | 148 |
| `group-1.png` | 15 |
| `group-10-2.png` | 82 |
| `group-10.png` | 763 |
| `group-3dsfsdfs.png` | 50 |
| `group-7.png` | 75 |
| `ha-luxury-tre-hoa-toan-dien.png` | 158 |
| `hoa-truoc.png` | 33 |
| `hotline-spa.png` | 18 |
| `km.png` | 216 |
| `layer-36.png` | 586 |
| `meso-ko-kim.png` | 252 |
| `phun-may-799k.png` | 238 |
| `phun-moi-collagen-799k.png` | 258 |
| `png-removebg-preview.png` | 3 |
| `promo-goi-99k.jpg` | 55 |
| `promo-mun-299k.jpg` | 75 |
| `promo-nach-499k.jpg` | 27 |
| `ro-tai-tao-mo-ecm.png` | 126 |
| `sdt.png` | 4 |
| `social-media-1.png` | 7 |
| `spin-btn1.svg` | 1 |
| `tam-body.png` | 134 |
| `text-dic-vu-duoc-uey-thich.png` | 8 |
| `text.png` | 74 |
| `title-phu.png` | 9 |
| `titlee.png` | 38 |
| `tri-mun.png` | 226 |
| `tri-nam.png` | 153 |
| `triet-long-10-buoi.png` | 182 |
| `triet-long-nach-mep-3-buoi.png` | 93 |
| `vc1trbb.png` | 18 |
| `vong-quay.png` | 75 |
| `xu-ly-nhan-mun.png` | 150 |
