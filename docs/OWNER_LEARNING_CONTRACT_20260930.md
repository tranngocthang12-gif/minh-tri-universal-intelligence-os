# Hợp đồng học của Owner — 2026-09-30

- **Phase:** `FOUNDATION_PROTOTYPE`, v0.1. v0.2 chưa bắt đầu.
- **Mốc code đối chiếu:** `main` tại `d4237384ad8a89b968edd6b9194f867dc70364e7` (`src/minhtri/core.py`, `src/minhtri/cli.py`)
- **Tính chất:** tài liệu quyết định sản phẩm của Owner. Không đổi code. Tách biệt với `sieu-du-an`.
- **Phạm vi:** đây là **sản phẩm cho đời sống/công việc**, không phải thực hành tôn giáo và không phải hệ đa AI.

## Sáu quyết định sản phẩm của Owner

1. Xây như người: hôm nay thấy thứ có giá trị thì HỌC. Việc học cái gì do Owner quyết, không tự quét mạng.
2. Mai đổi nghề: Owner bảo học miền mới. Cùng một não Tầng 1, không xây não thứ hai.
3. AI CÓ THỂ THAY THẾ. Không cần đa AI. Provider/model là ghế. Cùng claim không một provider ngồi hai ghế (đề + phản).
4. Có phản biện (critic) nhưng critic cũng là ghế thay được, không phải "bầy agent".
5. Học xã hội = Owner/dán case, không crawler.
6. Không chi tiền, không tự VERIFIED, không đụng sieu-du-an.

## Luồng học

```text
Owner mang nguồn
  → record_source / record_evidence
  → (tùy chọn) propose_claim / review_claim (adjudicate_claim)
  → chỉ Owner mới activate_trial_lesson
```

Mỗi bước là **một file JSON** chạy bằng CLI `apply` (`minhtri.bat apply <file>.json`, hoặc `PYTHONPATH=src python3 -m minhtri apply <file>.json`). Kiểm sổ bằng `status` và `verify`.

Để trung thực, luồng trên là bản rút gọn. Theo code hiện tại, muốn đi tới `activate_trial_lesson` thì bắt buộc có thêm các bước sau:

- `register_domain`, `open_goal`, `frame_problem` trước `propose_claim`, vì claim phải gắn với một problem thuộc goal đang `OPEN`.
- `register_provider` cho mọi ghế, và `register_procedure` để đăng ký dự đoán.
- Ít nhất hai dự đoán qua `register_prediction` → `freeze_prediction` → `record_resolution`, với `due_at` ở tương lai.
- `review_claim` và `adjudicate_claim` với verdict `ACCEPT_FOR_TRIAL`, rồi `propose_lesson` (lesson ở trạng thái `CANDIDATE`).
- Nguồn kết quả của các dự đoán phải là `FIRST_PARTY` + `CLEAR`, từ ít nhất hai nguồn khác nhau. Miền `HIGH_STAKES` luôn bị chặn.

Nếu chỉ muốn **ghi nhận** điều đã học mà chưa cần thành quy tắc thử, dừng ở `record_source`/`record_evidence`, hoặc thêm `propose_claim` (claim luôn là `HYPOTHESIS`).

## Đối chiếu với code: đang được thực thi hay còn khoảng trống

| Quyết định | Code hiện có thực thi gì | Khoảng trống (chưa sửa code) |
| --- | --- | --- |
| 1. Owner chọn điều học, không tự quét mạng | `core.py`/`cli.py` không import thư viện mạng. Dữ liệu chỉ vào qua `apply` từng file JSON. Mọi evidence được gắn `verification: "DECLARED_UNVERIFIED"` | Code không kiểm *ai* đã chạy `apply`; "do Owner quyết" là quy ước vận hành |
| 2. Miền mới, cùng một não | `register_domain` chỉ thêm một bản ghi (`id`, `name`, `risk_class`, `measurement_contract`) vào cùng sổ và cùng lõi, không cần sửa code. Test `test_two_domains_do_not_change_core_and_wait_is_explicit` kiểm hai miền trên cùng lõi. Evidence, claim, procedure và prediction bị chặn khi vượt ranh giới miền | Không có lệnh lưu trữ hay đóng một miền; chỉ đóng goal bằng `set_goal_status` (`CLOSED`/`BLOCKED`). Tri thức miền không tự nạp |
| 3. Provider/model là ghế; không ngồi hai ghế | Ghế là các trường tham chiếu provider: `propose_claim.provider_id` (đề), `register_procedure.provider_id` (dự đoán), `review_claim.critic_provider_id` (phản), `adjudicate_claim.adjudicator_provider_id` (trọng tài). `review_claim` chặn critic trùng người đề hoặc provider của các procedure đã dự đoán cho claim đó. `adjudicate_claim` chặn trọng tài trùng người đề, critic hoặc người dự đoán. Có test cho trường hợp tự phản biện (`critic_provider_id="maker"`) | **Không có trường "seat" riêng**; ghế suy ra từ tên trường. `register_provider` chỉ có `id`, `name`, `kind` (`MODEL`/`HUMAN`/`TOOL`). Tách ghế theo **ID khai báo**: một model thật đăng ký hai ID vẫn qua cổng. `register_prediction` **không** kiểm lại ghế, nên critic có thể trở thành người dự đoán qua một procedure đăng ký *sau* khi review đã ghi |
| 4. Critic là ghế thay được, không phải bầy agent | Critic chỉ là một `critic_provider_id` bất kỳ đã đăng ký. Code không có điều phối agent, không gọi model | Không có |
| 5. Học xã hội = Owner dán case | `record_source` có `kind: "THIRD_PARTY"`, `uri`, `captured_at`, `rights_status`. Không có crawler hay API | `PUBLIC` chưa có trong enum (chỉ là nhãn dự kiến); "ai đo" chưa có trường. Xem mục HỌC TỪ XÃ HỘI trong `ARCHITECTURE_PLAN_20260930.md` |
| 6. Không chi tiền, không tự VERIFIED, không đụng sieu-du-an | Không có lệnh chi tiền, giao dịch hay phát hành. Không có đường nào dẫn tới `VERIFIED`: mức cao nhất là `TRIAL_RULE`, gắn `validation: "DECLARED_DATA_ONLY_NOT_CAUSAL_PROOF"`. Code không tham chiếu `sieu-du-an` | Là quy ước quản trị cho repo và agent, không phải cổng máy |
| Chỉ Owner activate | `activate_trial_lesson` yêu cầu `owner_ack == "HUMAN_OWNER_APPROVED"` cùng các cổng dự đoán, nguồn và phân xử ở trên | `owner_ack` là **chuỗi khai báo**; ai chạy được CLI đều gõ được. `owner_identity_verified: false` |

## Quản trị

Owner merge. Kiến trúc sư hay agent không tự merge, không push thẳng `main`. Mọi thay đổi code để lấp khoảng trống ở trên phải có quyết định riêng của Owner và PR riêng.
