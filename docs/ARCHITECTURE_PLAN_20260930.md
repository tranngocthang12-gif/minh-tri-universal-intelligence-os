# Kế hoạch kiến trúc MINH TRÍ — 2026-09-30

- **Phase:** `FOUNDATION_PROTOTYPE` (theo `docs/PROJECT_STATE.json`, `version` `0.1.0`)
- **Mốc tham chiếu:** `main` tại commit `d4237384ad8a89b968edd6b9194f867dc70364e7`
- **Tính chất:** tài liệu kế hoạch. Không đổi code, không đổi trạng thái dự án, không mở v0.2.
- **Tách biệt:** repo này (`minh-tri-universal-intelligence-os`) **tách riêng khỏi `sieu-du-an`**. Kế hoạch này không sửa, không nhập luật, không nhận thẩm quyền từ `sieu-du-an`. `docs/PHILOSOPHY.md` chỉ dẫn link tới một văn bản ranh giới của Owner bên đó để tham khảo; không có phụ thuộc code hay dữ liệu.

## (a) Hệ là gì

MINH TRÍ v0.1 là **walking skeleton của Tầng 1**: một hệ ghi nhận và kiểm soát việc học, chạy offline bằng Python 3.10+, không cần API key (README). Tầng 1 giữ hợp đồng sự kiện, trạng thái, khung vấn đề, cổng và phép tính; Tầng 2 là các miền chuyên ngành gắn vào sau (docs/ARCHITECTURE.md).

Luồng chính đã có trong code: `SOURCE → EVIDENCE → CLAIM → PREDICTION → RESOLUTION → LESSON`, kèm `PROCEDURE`, sổ provider, ba ghế đề xuất/phản biện/trọng tài, `WAIT` khi không có mục tiêu hợp lệ, và sổ sự kiện JSONL có chuỗi SHA-256.

Hệ **chưa** là: AI tự suy nghĩ, hệ tự cải thiện đã được chứng minh, hay hệ có dữ liệu thật. Theo `PROJECT_STATE.json`: `providers_connected: false`, `real_data_validated: false`, `real_business_loop_validated: false`, `external_actions_enabled: false`, `owner_identity_verified: false`.

## (b) 8 chi là lăng kính đời, không phải API

Repo không có mục nào tên đúng là "8 chi". Nguồn gần nhất là `docs/PHILOSOPHY.md`, mục "Ranh giới Phật học": Bát Chánh Đạo được dùng như **lăng kính ứng dụng hiện đại**, và tài liệu nói rõ đây "không phải định nghĩa kinh điển … hay tám dịch vụ phần mềm". Bảng câu hỏi ở đó là "câu hỏi hiện đại của dự án, không phải lời kinh hay cách định nghĩa tám chi phần".

Kế hoạch này giữ đúng ranh giới đó:

- Tám phạm vi soi xét là **câu hỏi Owner/người phản biện tự đặt trước khi quyết định**, không phải module, endpoint hay lệnh.
- Không tạo lệnh, schema hay trường dữ liệu mang tên chi phần. Không chấm điểm "đạt chánh …" bằng code.
- Mọi khẳng định về ý nghĩa giáo lý cần nguồn Nikāya và được xét ở luồng riêng (theo PHILOSOPHY.md). Tài liệu này không diễn giải giáo lý.

Tên tám phạm vi dưới đây lấy nguyên văn từ bảng trong `docs/PHILOSOPHY.md`.

## (c) Bảng map 8 chi vào các lệnh Tầng 1 đã có

Các lệnh dùng ở đây chỉ gồm những gì đang có trong repo:

- Lệnh CLI (`src/minhtri/cli.py`): `init`, `apply`, `status`, `verify`, `repair-snapshot`.
- Kiểu lệnh JSON (`ALLOWED_FIELDS` trong `src/minhtri/core.py`): `register_domain`, `register_provider`, `open_goal`, `set_goal_status`, `frame_problem`, `record_source`, `record_evidence`, `register_procedure`, `propose_claim`, `register_prediction`, `freeze_prediction`, `record_resolution`, `review_claim`, `adjudicate_claim`, `propose_lesson`, `activate_trial_lesson`.

"Hỗ trợ" nghĩa là lệnh có trường hoặc cổng giúp **ghi lại** câu trả lời cho câu hỏi đó. Nó không có nghĩa là máy trả lời hộ hay đã kiểm chứng câu trả lời. Chỗ nào không có lệnh phù hợp thì ghi **chưa có lệnh**.

| Phạm vi soi xét (PHILOSOPHY.md) | Câu hỏi trước quyết định | Lệnh Tầng 1 đã có hỗ trợ ghi nhận | Khoảng trống |
| --- | --- | --- | --- |
| Cái thấy | Ta biết gì từ nguồn nào; đâu là giả thuyết hoặc điều chưa biết? | `record_source` (`kind`, `rights_status`), `record_evidence`, `frame_problem` (`reality`, `unknowns`, `conditions` luôn `HYPOTHESIS`), `propose_claim` (claim khởi đầu là `HYPOTHESIS`) | Không xác minh nguồn gốc độc lập; `FIRST_PARTY` chỉ là khai báo |
| Định hướng | Mục tiêu và động cơ có tạo hại hay ép kết luận vì lợi nhuận? | `open_goal` (`objective`, `owner_boundary`), `frame_problem` (`harm_checks`, `target`), `set_goal_status` (`BLOCKED`/`CLOSED`) | Chỉ ghi văn bản; **chưa có lệnh** đánh giá động cơ/xung đột lợi ích |
| Lời nói | Nội dung xuất bản có nói chắc hơn bằng chứng hoặc che phản chứng? | `propose_claim` (`alternative`, `falsifier`, `evidence_ids`), `review_claim`, `adjudicate_claim` | Hệ không có chức năng xuất bản; **chưa có lệnh** kiểm nội dung trước khi xuất bản |
| Hành động | Việc định làm có hợp quyền, đảo ngược được và phù hợp mức rủi ro? | `register_domain` (`risk_class` `NORMAL`/`HIGH_STAKES`), `frame_problem` (`intervention`, `control`, `responsibility`), `activate_trial_lesson` (`owner_ack`, `scope`; `HIGH_STAKES` luôn bị chặn) | **Chưa có lệnh** kiểm tính đảo ngược/rollback; `external_actions_enabled: false` |
| Cách kiếm sống | Cơ chế có tạo giá trị thật cho người nhận hay dựa vào lừa dối? | Chỉ gián tiếp qua trường văn bản `harm_checks`, `responsibility` của `frame_problem` | **Chưa có lệnh** chuyên cho câu hỏi này; `real_business_loop_validated: false` |
| Nỗ lực | Nút thắt nào đáng giải quyết và lúc nào nên dừng nghiên cứu? | `open_goal` (`priority` 1–5), `set_goal_status`, `status` (chọn goal `OPEN` ưu tiên cao nhất hoặc trả `WAIT`) | **Chưa có lệnh** đặt tiêu chí dừng nghiên cứu hay đo nút thắt |
| Theo dõi trạng thái | Còn thiếu dữ liệu, lỗi mở, kết quả quá hạn hay kỹ năng suy giảm nào? | `status` (đếm theo loại), `verify` (kiểm chuỗi hash và cache), `repair-snapshot` | `status` không liệt kê dự đoán quá hạn, lỗi mở hay suy giảm: **chưa có lệnh** |
| Tập trung | Một vòng nhỏ nào đáng làm trọn vẹn trước khi mở thêm việc? | `status` → `next_goal` (một goal `READY` hoặc `WAIT`); vòng `register_prediction` → `freeze_prediction` → `record_resolution` | **Chưa có lệnh** giới hạn số việc mở cùng lúc (WIP limit) |

Bảng này là đề xuất của kiến trúc sư, chưa qua phản biện, và không làm thay đổi hành vi code. Nếu Owner thấy khoảng trống nào cần lấp thì mở một luồng riêng. Không lấp bằng cách nhét tên chi phần vào lõi.

## (d) Cấm

1. **Không nhét nghề/domain vào lõi.** Tri thức ngành (YouTube, tài chính, …) là Tầng 2. `register_domain` chỉ khai `measurement_contract` và `risk_class`, không nạp tri thức miền. Ví dụ trong `examples/` chỉ là ca thiết lập.
2. **Không chi tiền.** Không có và không thêm chức năng chi tiền, giao dịch, phát hành hay tác động bên ngoài. `external_actions_enabled` giữ `false`. Chi phí thật luôn là quyết định của Owner.
3. **Không tự đánh dấu `VERIFIED`.** Code không có đường tự động nâng lesson lên `VERIFIED`. Tối đa là `TRIAL_RULE` qua cổng Owner. Tài liệu, commit, PR và agent cũng không được tự ghi PASS/VERIFIED khi chưa có bằng chứng.

Thêm vào đó: không kết nối provider hay integration bên ngoài trong v0.1, và không sửa repo `sieu-du-an`.

## (e) Lộ trình

**Hiện tại là v0.1. v0.2 CHƯA bắt đầu.**

| Mốc | Nội dung theo kế hoạch này | Trạng thái |
| --- | --- | --- |
| v0.1 — đứng vững | Lõi độc lập miền, sổ sự kiện, problem frame, dự đoán, ba ghế, `WAIT`, gate thử; ca kiểm offline | **Đang ở đây** (`FOUNDATION_PROTOTYPE`) |
| v0.2 — một miền đọc-only | Một miền, một adapter **chỉ đọc**, **chỉ khi Owner chọn** miền và nguồn dữ liệu; có provenance, dự đoán ghi trước | **Chưa bắt đầu**; chưa có miền nào được Owner chọn |
| v0.3 — sai số / error-awareness | Baseline, bảng điểm theo procedure/provider, review lỗi, đề xuất sửa quy trình từ sai số thật | Chưa bắt đầu |
| v0.4 — chuyển miền | Miền thứ hai dùng cùng hợp đồng lõi, không rò dữ liệu/luật miền | Chưa bắt đầu |

Chi tiết cổng của từng mốc nằm trong `docs/ROADMAP.md`. Tài liệu này không thay thế và không sửa bảng đó.

## (f) next_checkpoint hiện tại

Trích nguyên văn từ `docs/PROJECT_STATE.json` tại `main` commit `d4237384ad8a89b968edd6b9194f867dc70364e7`:

```json
"next_checkpoint": "ONE_READ_ONLY_REAL_DOMAIN_PILOT_WITH_PROVENANCE_AND_OWNER_GATE"
```

Ghi chú: checkpoint này là cổng để **vào** v0.2. Nó chưa đạt, và việc bắt đầu cần Owner chọn miền.

## (g) Quản trị

- **Owner merge.** Mọi thay đổi vào `main` đi qua Pull Request và chỉ Owner merge.
- **Kiến trúc sư (người hoặc agent) không tự merge**, không push thẳng `main`, không force-push.
- Owner giữ mục tiêu, vốn, rủi ro, thương hiệu, quyền dùng tư liệu và chiến lược lớn (PHILOSOPHY.md). Provider và agent chỉ đề xuất.
- Mỗi commit một ý. Kết quả kiểm thử được báo đúng như đã chạy, không phóng đại.

## Ghi chú trung thực

- Thuật ngữ "8 chi" không xuất hiện nguyên văn trong repo. Bảng ở mục (c) dựa trên bảng tám phạm vi soi xét trong `docs/PHILOSOPHY.md`.
- File lộ trình nằm ở `docs/ROADMAP.md`, không phải ở thư mục gốc.
- Tại thời điểm viết, repo không có CI (`.github/workflows` không tồn tại). Kiểm thử cục bộ chỉ có `tests/test_core.py` (unittest).
