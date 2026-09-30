# Kiến trúc MINH TRÍ lúc này — 2026-10-01

- **Ngày:** 2026-10-01 (giờ Việt Nam, UTC+7)
- **Mốc:** `main` tại `1693ba934e408e44d38e45d7958697c88efd4b00` (sau PR #25)
- **Phase:** `FOUNDATION_PROTOTYPE`, v0.1. v0.2 chưa bắt đầu. `next_checkpoint` trong `docs/PROJECT_STATE.json` không đổi: `ONE_READ_ONLY_REAL_DOMAIN_PILOT_WITH_PROVENANCE_AND_OWNER_GATE`.
- **Tính chất:** tài liệu, không đổi code, không thêm example. Tách biệt với `sieu-du-an`.

## ĐÓNG HỌC HIỂU (tạm)

- `examples/06`–`17` là **hàng đợi học**, không phải sản xuất. Tất cả đều là `set_learning_focus`, nguồn giữ chỗ hư cấu `gia-dinh-kenh-a-case` (THIRD_PARTY, rights UNKNOWN), `UNTESTED_EXPECTATION`, KHÔNG VERIFIED.
- Thực hành xuất bản làm **sau thạc sĩ** (ví dụ 10).
- Lệnh tối cao trên chat (ví dụ 17): Owner bỏ bước thì vẫn làm, nêu một câu rủi ro, không cãi.

## CỐT LÕI ĐÃ CÓ

- Ledger `SOURCE → EVIDENCE → CLAIM → PREDICTION → RESOLUTION → LESSON`, kèm lệnh CLI `learn` / `focus` / `unfocus` (kiểu lệnh `set_learning_focus`). Sổ chỉ nối thêm, `verify` kiểm chuỗi hash.
- Một não Tầng 1; AI là ghế thay được, không phải đa AI.
- Owner chọn học gì: [OWNER_LEARNING_CONTRACT_20260930.md](OWNER_LEARNING_CONTRACT_20260930.md).
- Kiểm thử cục bộ gồm `tests/test_core.py`, `test_learning_focus.py`, `test_cli_learn.py` và `test_examples.py`: 15 test, chạy bằng `PYTHONPATH=src python3 -m unittest discover -s tests`. Repo không có CI.

## LÁT CẮT KIẾN TRÚC TIẾP (code/docs, không bài học mới)

### 1. Một trang ghế × tool

Bảng này chỉ lấy từ ghi chú của `examples/06`–`17`; số trong ngoặc là số ví dụ. Ô không có trong ví dụ để `—`, không suy thêm. Các ví dụ không dùng từ "chủ tịch", nên cột **Chủ tịch** ở đây ghi những việc ví dụ giao cho **Owner**. Nếu "chủ tịch" không phải Owner, Owner sửa lại. Cột **Ghế chat viết prompt** không nằm trong bốn ghế đã nêu, nhưng có trong ví dụ 08 và 09 nên được giữ lại.

| Tool | Owner định nghĩa | Không dùng cho | Chủ tịch (Owner) | Thị trường | Đạo diễn | Phản biện | Ghế chat viết prompt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Suno / Suno Studio | 1 bài đúng brief → tách stem → sửa 1 lớp → xuất (07); làm đoạn ngắn (09) | chat xuất/gộp file >1GB (09) | tự làm, tự ghi kết quả (07); chấm (08) | — | — | — | Claude viết prompt + checklist Suno Studio, không xuất nhạc (08); GPT viết prompt + nhớ số đoạn, mỗi chat dán luật (09) |
| FL Studio 2026 | bàn sửa nhạc sau Suno: kéo wav, extract stems, sửa 1 lớp, export (15); khả năng tách stem là lời Owner, chưa kiểm | ghép file 9h; thay CapCut/Canva/Flow (15) | — | — | — | — | — |
| Google Flow | bàn ảnh + clip ngắn (12) | 40 phút; nhạc; dựng tập (12) | — | — | — | — | — |
| CapCut | dựng ghép clip + nhạc + chữ (13) | ra nhạc; 40 phút một prompt; file 9h thì dùng bat (13) | — | — | — | — | — |
| Canva | ảnh + chữ; thumbnail 1280x720 (14) | nhạc; dựng tập (14) | — | — | — | — | — |
| Chung (không gắn tool) | — | — | chọn đề (16); bỏ bước được, ghế chat nêu 1 câu rủi ro rồi vẫn làm (17) | ai xem, clip cùng loại, khác gì, luật YT/Content ID; ≥2 nguồn; không biến 1 clip triệu view thành luật (16); học thị trường và chính sách MV/nhạc AI (06) | kinh 1 trang; tên file PHIM_Txx_Cxx; 8–12 cảnh/tập; không take 40 phút liền (11); học cấu trúc, chưa quay tập 0 (10) | nguồn? nóng/tham? chắc hơn chứng? phá cấm tuần?; không vừa đề vừa chấm (16) | không dùng chat làm sổ (09) |

### 2. Quy ước kho thư mục trên máy Owner (ĐỀ XUẤT, Owner quyết)

Repo **không chứa media**; `brain/` đã nằm trong `.gitignore`. Các tên `NGU_YYMMDD_NN`, `PHIM_Txx_Cxx`, thumbnail 1280x720 và "bat ghép trên máy Owner" là tên Owner đã đặt (ví dụ 09, 11, 13, 14, 15). Tên các thư mục cha dưới đây chỉ là **đề xuất** của kiến trúc sư:

```text
<thư mục gốc do Owner chọn>/
  brain/                 sổ MINH TRÍ (minhtri --home ...), không đưa media vào đây
  NHAC_NGU/              NGU_YYMMDD_NN.<đuôi Owner chọn>   (09)
  PHIM/Txx/              PHIM_Txx_Cxx.<đuôi>                (11)
  KINH/                  kinh 1 trang cho mỗi phim/tập      (10, 11)
  THUMBNAIL/             ảnh 1280x720                        (14)
  BAT/                   bat ghép sẵn có của Owner (không nằm trong repo) (09, 13, 15)
```

Không đặt file >1GB qua chat (09). Nếu lỗi tải thì chia nhỏ (09). Thư mục và sổ là bản ghi; chat chỉ là ghế (09).

### 3. Điểm dừng học

Không thêm example (18 trở đi) trừ khi Owner nêu tên bài học.

### 4. Lỗ code đã biết (ghi lỗ, chưa sửa trừ khi Owner bảo sửa)

- `owner_ack` chỉ là chữ: `activate_trial_lesson` so với chuỗi `HUMAN_OWNER_APPROVED`, không xác thực danh tính (`owner_identity_verified: false`).
- Provider ID tự khai: tách ghế trong `review_claim` / `adjudicate_claim` dựa trên ID khai báo; một model đăng ký hai ID vẫn qua cổng.
- `PUBLIC` chưa có trong enum: `record_source.kind` chỉ nhận `FIRST_PARTY`, `THIRD_PARTY`, `SYNTHETIC`.
- `register_prediction` không kiểm lại ghế: critic có thể thành người dự đoán qua một procedure đăng ký sau review (đã đối chiếu `src/minhtri/core.py` tại mốc trên).
- `learn` / `unfocus` không kiểm ai đang chạy CLI.

## Quản trị

Owner merge. Kiến trúc sư không tự merge PR này.

## Luật kinh nghiệm (2026-10-01)

- Xem [LAW_EVIDENCE_AND_HUMILITY_20261001.md](LAW_EVIDENCE_AND_HUMILITY_20261001.md): 5 luật nguyên văn của Owner, trạng thái UNTESTED.
- Không lấy lời AI làm VERIFIED; không biết thì nói KHÔNG BIẾT; áp dụng ghế phản biện cho mọi claim trên chat và sổ.
- Luật động: tool là ghế/dụng cụ, không phải luật — xem [LAW_DYNAMIC_TOOLS_20261001.md](LAW_DYNAMIC_TOOLS_20261001.md).
