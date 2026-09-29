# Lộ trình có cổng

| Mốc | Đầu ra cụ thể | Điều kiện qua cổng |
| --- | --- | --- |
| v0.1 — khung chạy được | Lõi độc lập miền, sổ sự kiện, problem frame, dự đoán, ba ghế, `WAIT`, gate thử | Ca kiểm tra offline đạt; không tự phong dữ liệu giả thành hiểu biết thật |
| v0.1a — AI Commons `SHADOW` | Hợp đồng nhiệm vụ cho N participant, ba ghế độc lập theo provider family, lưu phản biện/kết luận trong sổ riêng | Ca giả lập chứng minh thiếu bằng chứng hoặc có phản chứng thì `HOLD`; không tự ghi vào bài học chuẩn |
| v0.2 — một vòng dữ liệu thật chỉ đọc | Một adapter được Owner cho phép, nguồn có provenance, dự báo ghi trước, kết quả đo được | Mốc dự đoán độc lập trước kết quả; dữ liệu được đối soát; không hành động bên ngoài |
| Sau v0.2 — AI Commons `CONTROLLED` | Xác thực Owner/provider, phân quyền ngữ cảnh, ngân sách/timeout, một adapter model thực và log chi phí | Một pilot read-only so baseline và được Owner duyệt; không tự mở quyền nhạy cảm |
| v0.3 — học từ sai số | Baseline, bảng điểm theo procedure/provider và review lỗi; đề xuất sửa quy trình | Nhiều vòng thật đủ mẫu; người phản biện chỉ ra được sai lầm và cách sửa được thử lại |
| v0.4 — thử chuyển miền | Một miền khác dùng cùng hợp đồng lõi, dữ liệu và chuyên gia riêng | Không rò dữ liệu/luật miền; kết quả không suy rộng quá phạm vi |
| Sau đó — hành động có giới hạn | Quyền cụ thể cho từng adapter, Owner gate được xác thực, rollback và giám sát | Có ích hơn baseline trong thí nghiệm thật, vượt kiểm rủi ro và quyền |

Không dùng số lượng tài liệu, số agent hay tần suất tự học làm thước đo năng lực. Mỗi mốc được mở khi có bằng chứng giải quyết nút thắt trước đó. Chi phí thật, dữ liệu cá nhân, quyền nội dung và các hành động khó đảo ngược luôn thuộc quyết định Owner.
