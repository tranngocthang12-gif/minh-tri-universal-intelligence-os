# Kiến trúc Tầng 1 v0.1

```text
OWNER PURPOSE / BOUNDARY
          ↓
DOMAIN REGISTRY → GOAL ROUTER (OPEN / BLOCKED / CLOSED / WAIT)
          ↓
PROBLEM FRAME (reality / conditions / target / intervention)
          ↓
SOURCE → EVIDENCE → CLAIM → PREDICTION → RESOLUTION → LESSON
                       ↘  REVIEW → ADJUDICATION  ↗
          PROCEDURE / PROVIDER REGISTRY
          ↓
EVENT LEDGER → DERIVED STATE → GIT REVIEWED PROMOTION (future)
```

Các mũi tên biểu thị tham chiếu dữ liệu, không phải khẳng định rằng một chứng cứ tự chứng minh một kết luận. Nguồn, Evidence, Claim, Prediction, Resolution, Lesson và Procedure là bảy đối tượng dùng chung tham khảo từ [kiến trúc v1.0 của Trung Tâm Tài Chính](https://github.com/tranngocthang12-gif/TRUNG-T-M-T-I-CH-NH-Financial-Intelligence-Media-Factory/blob/main/architecture/ARCHITECTURE_v1.0.md). Vòng học một đơn vị, ba ghế, `WAIT` và checkpoint cuối tham khảo [LOI_TU_HOC_v2](https://github.com/tranngocthang12-gif/nao-nha-may/blob/main/LOI/LOI_TU_HOC_v2.md).

## Biên Tầng 1 / Tầng 2

Tầng 1 sở hữu hợp đồng sự kiện, trạng thái, khung nhìn vấn đề, cổng và phép tính. Tầng 2 sở hữu từ điển ngành, nguồn dữ liệu, metric, phép gán nguyên nhân, luật/chính sách hiện hành và giới hạn riêng. `register_domain` khai `measurement_contract` và `risk_class`; nó không tự nạp tri thức miền. YouTube và finance trong `examples/` chỉ là ca thiết lập. `HIGH_STAKES` luôn chặn kích hoạt quy tắc thử trong v0.1.

## Sổ sự kiện

Một lệnh JSON được kiểm rồi mới thêm đúng một dòng `events.jsonl`; mỗi dòng ghi `seq`, `prev`, `at`, `command`, `hash`. Cache `state.json` cập nhật sau cùng. Khi mất điện giữa hai bước, `verify` báo lỗi và `repair-snapshot` tái tạo cache từ sổ sau khi đã kiểm. Mọi lệnh ghi được khóa một writer cục bộ. Không chạy song song nhiều máy vào cùng thư mục.

## Luồng học có cổng

1. Mở domain và goal, lập khung vấn đề, ghi nguồn/evidence; claim khởi đầu luôn là `HYPOTHESIS`. Vai trò điều kiện trong khung chỉ là giả thuyết, chưa phải nhân quả đã chứng minh.
2. Khai procedure và dự đoán có metric, đơn vị, khoảng, hạn và cách đo khi goal còn `OPEN`. `freeze_prediction` bị chặn khi đã đến hạn hoặc goal không còn mở. Chụp mốc Git trước khi số liệu kết quả xuất hiện nếu muốn chứng minh đăng ký trước với bên thứ ba.
3. Ghi kết quả vào evidence mới với thời điểm quan sát sau khi đóng băng và đến hạn, rồi `record_resolution` để code chấm khoảng. Phép chấm chưa chứng minh nguyên nhân hay chất lượng nguồn.
4. Provider khác phản biện, provider thứ ba phân xử. Mọi phiếu phản biện của cùng claim đều phải thuận mới được phân xử `ACCEPT_FOR_TRIAL`; phiếu bất đồng đến sau vẫn chặn kích hoạt.
5. Tạo lesson `CANDIDATE`; chỉ có thể thành `TRIAL_RULE` khi goal còn mở, không còn phiếu bất đồng, có hai kết quả từ hai nguồn first-party khai báo khác nhau và xác nhận Owner. Nếu goal bị chặn/đóng hoặc phát sinh phản biện bất lợi, quy tắc thử đang có chuyển sang `SUSPENDED` và không tự mở lại. Không tự đổi thành `VERIFIED`.

## Hợp đồng lệnh

Mỗi JSON có đúng `{"type": "...", "data": {...}}`. Các kiểu và trường bắt buộc nằm trong `src/minhtri/core.py`; trường thừa bị từ chối. ID dùng chữ thường, số, gạch nối/gạch dưới, bắt đầu bằng chữ và dài 2–64 ký tự. Thời gian dùng ISO 8601 có múi giờ (ví dụ `2026-09-29T07:00:00Z`).

| Lệnh | Trường bắt buộc trong `data` |
| --- | --- |
| `register_domain` | `id`, `name`, `risk_class`, `measurement_contract` |
| `register_provider` | `id`, `name`, `kind` |
| `open_goal` | `id`, `domain_id`, `objective`, `priority`, `owner_boundary` |
| `set_goal_status` | `goal_id`, `status`, `reason` |
| `frame_problem` | `id`, `goal_id`, `reality`, `conditions`, `target`, `intervention`, `unknowns`, `control`, `influence`, `responsibility`, `harm_checks` |
| `record_source` | `id`, `domain_id`, `uri`, `captured_at`, `kind`, `rights_status` |
| `record_evidence` | `id`, `domain_id`, `source_id`, `statement`, `observed_at`; thêm `value`, `metric` khi có số |
| `register_procedure` | `id`, `domain_id`, `provider_id`, `version`, `method` |
| `propose_claim` | `id`, `problem_id`, `provider_id`, `statement`, `evidence_ids`, `alternative`, `falsifier` |
| `register_prediction` | `id`, `claim_id`, `procedure_id`, `metric`, `unit`, `lower`, `upper`, `due_at`, `resolution_method` |
| `freeze_prediction` | `prediction_id` |
| `record_resolution` | `id`, `prediction_id`, `evidence_id` |
| `review_claim` | `id`, `claim_id`, `critic_provider_id`, `verdict`, `reason` |
| `adjudicate_claim` | `id`, `claim_id`, `review_id`, `adjudicator_provider_id`, `verdict`, `reason` |
| `propose_lesson` | `id`, `claim_id`, `statement`, `limits`, `prediction_ids`, `adjudication_id` |
| `activate_trial_lesson` | `lesson_id`, `owner_ack`, `scope` |

Verdict là `ACCEPT_FOR_TRIAL`, `HOLD` hoặc `REVISE`. Xác nhận Owner mẫu là `HUMAN_OWNER_APPROVED` và chỉ là chữ ký khai báo, chưa có xác thực danh tính. Dùng riêng với môi trường được kiểm soát.

## Bước tiếp theo có điều kiện

1. Chọn một vấn đề thật và kho dữ liệu Owner cho phép; xây adapter chỉ đọc có provenance và timestamp kiểm được.
2. Xác thực danh tính Owner/provider, quyền tư liệu, nguồn gốc file và chứng thực mốc dự đoán trước khi cho tác vụ tác động bên ngoài.
3. Dùng một pilot đo dự đoán so với baseline; phê duyệt thay đổi procedure bằng dữ liệu thật. Chỉ thêm meta-learning/champion khi đủ số mẫu và thấy nút thắt.
