# Cổng Owner (owner_id khai báo)

Các lệnh `learn`, `unfocus`, và `apply` với kiểu `set_learning_focus` hoặc `activate_trial_lesson` (lệnh có `owner_ack`) chỉ chạy khi `--owner-id` trùng `owner_id` trong `config/owner.json`. File này bị gitignore; mẫu nằm ở `config/owner.example.json`. Có thể chỉ đường dẫn khác bằng `--owner-config` hoặc biến `MINHTRI_OWNER_CONFIG`.
Nếu thiếu config, lệnh bị chặn với lý do `MISSING_OWNER_CONFIG` (fail closed). Nếu ID lệch, lý do là `OWNER_MISMATCH`; nếu không truyền ID, lý do là `OWNER_ID_REQUIRED`. Khi bị chặn, sổ không bị ghi thêm dòng nào.
Đây **không phải xác thực danh tính**: cổng chỉ so chuỗi ID khai báo. Ai sửa được file config hoặc gõ đúng ID đều qua, và người có quyền ghi thư mục sổ vẫn có thể viết lại sổ.
Code không đổi cổng `activate_trial_lesson`: vẫn cần hai kết quả từ nguồn `FIRST_PARTY` + `CLEAR`. Nguồn `PUBLIC` được nhận nhưng không bao giờ dẫn tới `TRIAL_RULE` hay `VERIFIED`.
Ví dụ trên Windows: `minhtri.bat --owner-id <id-của-anh> learn --domain-id youtube --uri <link> --note "<vì sao học>"`.
