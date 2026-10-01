# Cổng Owner (owner_id khai báo)

Các lệnh `learn`, `unfocus`, và `apply` với kiểu `set_learning_focus` hoặc `activate_trial_lesson` (lệnh có `owner_ack`) chỉ chạy khi `--owner-id` trùng `owner_id` trong `config/owner.json`. File này bị gitignore; mẫu nằm ở `config/owner.example.json`. Có thể chỉ đường dẫn khác bằng `--owner-config` hoặc biến `MINHTRI_OWNER_CONFIG`.
Nếu thiếu config, lệnh bị chặn với lý do `MISSING_OWNER_CONFIG` (fail closed). Nếu ID lệch, lý do là `OWNER_MISMATCH`; nếu không truyền ID, lý do là `OWNER_ID_REQUIRED`. Khi bị chặn, sổ không bị ghi thêm dòng nào.
Đây **không phải xác thực danh tính**: cổng chỉ so chuỗi ID khai báo. Ai sửa được file config hoặc gõ đúng ID đều qua, và người có quyền ghi thư mục sổ vẫn có thể viết lại sổ.
Code không đổi cổng `activate_trial_lesson`: vẫn cần hai kết quả từ nguồn `FIRST_PARTY` + `CLEAR`. Nguồn `PUBLIC` được nhận nhưng không bao giờ dẫn tới `TRIAL_RULE` hay `VERIFIED`.
Ví dụ trên Windows: `minhtri.bat --owner-id <id-của-anh> learn --domain-id youtube --uri <link> --note "<vì sao học>"`.

## Cập nhật 2026-10-01: thêm secret và ghi người duyệt

- Ngoài ID, các lệnh trên còn cần **secret**: SHA-256 của secret phải trùng `owner_secret_sha256` trong `config/owner.json` (so bằng `hmac.compare_digest`). Thiếu trường này thì bị chặn với `OWNER_SECRET_REQUIRED`; không truyền secret thì `MISSING_OWNER_SECRET`; lệch thì `OWNER_SECRET_MISMATCH`. Giá trị mẫu (`doi-ten-owner`, 64 số 0) bị từ chối với `INVALID_OWNER_CONFIG`.
- Tạo hash: `minhtri.bat hash-secret` (hoặc `python -m minhtri hash-secret`). Lệnh hỏi secret không hiện chữ và chỉ in `{"owner_secret_sha256": ...}`. Dán hash vào `config/owner.json`. **Không bao giờ** đưa secret vào git.
- Nên truyền secret qua biến môi trường `MINHTRI_OWNER_SECRET` thay vì cờ `--owner-secret`, vì cờ có thể bị lưu trong lịch sử shell.
- Sự kiện ghi qua các lệnh có cổng giờ có trường `approved_by` (owner_id đã qua cổng), trường này nằm trong hash chuỗi. Secret và hash của secret không bao giờ được ghi vào sổ. Sự kiện cũ không có trường này vẫn `verify` được.
- Vẫn **không phải xác thực danh tính**: ai có file config và biết secret đều qua; hệ thống không nhận ra người thật. SHA-256 không salt và nhanh, nên nếu config bị lộ và secret yếu thì có thể dò ra secret.
- **Vẫn còn lỗ**: gọi thẳng `Ledger.apply` trong Python (có thể tự điền `approved_by` bất kỳ) hoặc sửa file sổ bằng tay thì đi vòng qua cổng. Người có quyền ghi có thể băm lại toàn bộ chuỗi và snapshot; muốn phát hiện thì cần một mốc bên ngoài (ví dụ commit Git).
