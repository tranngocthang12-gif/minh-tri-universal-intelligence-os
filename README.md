# MINH TRÍ — Universal Intelligence OS

**v0.1: walking skeleton của Tầng 1.** Tầng 1 giữ cách học, phản biện, dự đoán và giới hạn quyền. Tầng 2 là các miền chuyên ngành có thể gắn vào sau. Bản này chạy offline bằng Python 3.10+, không cần API key hay gói Python bên ngoài.

## Chạy nhanh trên Windows

Giải nén dự án, mở Command Prompt trong thư mục này và chạy thử **một lệnh**:

```bat
demo.bat
```

Để khởi tạo sổ học thật do anh kiểm soát và nhập từng đơn vị:

```bat
minhtri.bat init
minhtri.bat apply examples\01-domain-youtube.json
minhtri.bat apply examples\02-goal-youtube.json
minhtri.bat apply examples\03-domain-finance.json
minhtri.bat apply examples\04-problem-youtube.json
minhtri.bat status
minhtri.bat verify
```

Trên macOS/Linux: `PYTHONPATH=src python3 -m minhtri init` và thay `minhtri.bat` bằng `PYTHONPATH=src python3 -m minhtri` ở các lệnh còn lại. Dữ liệu cục bộ nằm trong `brain/` và được loại khỏi gói Git công khai. Mỗi file JSON trong `examples/` là **một lệnh**, được thực thi riêng và lưu thành một sự kiện.

## Cốt lõi là sổ của Owner

- Giá trị nằm ở **sổ sự kiện của Owner** (`brain/events.jsonl`), không nằm ở AI nào. Đổi Claude, ChatGPT, Gemini hay Grok thì sổ vẫn còn; AI chỉ là ghế thay được.
- Hôm nay Owner chọn học gì thì ghi lại nguồn, bài học mong đợi và độ chắc: `minhtri.bat --owner-id <id> learn --domain-id youtube --uri <link> --text "<case>" --note "<vì sao học>" --expected-lesson "<điều mong học>" --uncertainty "<độ chắc>"`. Link chỉ được lưu, không được tải về.
- Mai đổi nghề thì `learn --domain-id <miền-mới> --domain-name "<Tên>"`. Focus cũ chuyển sang `SUPERSEDED`; cùng một lõi Tầng 1, không xây não mới.
- `minhtri.bat focus` xem đang học gì. `minhtri.bat --owner-id <id> unfocus` dừng focus. Cổng Owner cần ID + secret: chạy `minhtri.bat hash-secret` một lần, dán hash vào `config/owner.json`, rồi `set MINHTRI_OWNER_SECRET=<secret>` trước khi dùng `learn`/`unfocus`; xem [docs/OWNER_GATE.md](docs/OWNER_GATE.md). Không xóa dòng nào trong sổ; `verify` vẫn kiểm được toàn bộ lịch sử.
- Nguồn mặc định là `THIRD_PARTY`, quyền `UNKNOWN`, và evidence là `DECLARED_UNVERIFIED`. Bài học mong đợi chỉ là `UNTESTED_EXPECTATION`, không phải lesson hay `VERIFIED`.
- **Không tự học ban đêm:** không có tiến trình nền, lịch chạy, crawler hay gọi mạng. Sổ chỉ đổi khi Owner chạy một lệnh.
- `examples/05-owner-learn-social-case.json` là nguồn **GIẢ ĐỊNH/hư cấu** (`example.invalid`), không nói về công ty thật.

## Bản đầu tiên làm được gì

- Mở một miền mới mà không sửa lõi; mở mục tiêu và khung vấn đề (thực trạng, điều kiện giả định, đích, can thiệp, trách nhiệm, rủi ro), đặt ưu tiên, tạm chặn hoặc đóng. Không có mục tiêu hợp lệ thì trả `WAIT`.
- Ghi `SOURCE → EVIDENCE → CLAIM → PREDICTION → RESOLUTION → LESSON`, kèm `PROCEDURE` và danh tính provider khai báo. Dự đoán phải được đóng băng trước khi có kết quả; code tự tính điểm trúng khoảng và sai số điểm giữa.
- Tách vai đề xuất, phản biện và trọng tài bằng ID provider; chặn cùng một provider chiếm hai ghế của cùng nhận định.
- Chỉ cho kích hoạt một bài học ở trạng thái `TRIAL_RULE` khi có ít nhất hai dự đoán đã giải quyết, hai nguồn kết quả first-party khác nhau, phản biện/trọng tài chấp nhận và Owner ghi xác nhận. Không có đường tự động nâng thành `VERIFIED`.
- Từ chối kích hoạt quy tắc trong miền rủi ro cao ở bản này. Không có chức năng chi tiền, giao dịch, phát hành hoặc tự sửa luật.
- Kiểm sổ JSONL bằng chuỗi SHA-256, tái dựng trạng thái và so với cache. File Git cần được commit để tạo mốc độc lập chống việc viết lại cả chuỗi.

## Lệnh JSON mẫu

```json
{
  "type": "register_provider",
  "data": {"id": "researcher_a", "name": "Researcher A", "kind": "MODEL"}
}
```

Gọi `minhtri.bat apply duong-dan\lenh.json`. Xem [hợp đồng và luồng dữ liệu](docs/ARCHITECTURE.md) để biết các lệnh tiếp theo. Các ví dụ YouTube và tài chính chỉ chứng minh rằng cùng một lõi nhận được hai miền; chúng **không** chứa dữ liệu thị trường hay khuyến nghị đầu tư.

## Ranh giới trung thực

Đây là hệ **ghi nhận và kiểm soát việc học**, chưa phải AI tự suy nghĩ như người hay hệ tự cải thiện đã được chứng minh. ID nhà cung cấp và xác nhận Owner là khai báo; CLI offline không xác thực danh tính. Nguồn và số liệu người dùng nhập chưa được máy kiểm chứng. Chuỗi hash phát hiện sửa cục bộ một phần, không chống người có quyền viết lại toàn bộ sổ; Git commit hoặc mốc độc lập mới tăng sức chứng thực. Kết quả dự đoán không tự chứng minh quan hệ nhân quả. Cổng rủi ro và xác thực dữ liệu trước hành động thực cần được làm ở giai đoạn kế tiếp.

## Trạng thái

`FOUNDATION_PROTOTYPE`: cài đặt kiểm soát cục bộ và ca thử bằng dữ liệu giả định. Chưa kết nối Claude/ChatGPT/Gemini/Grok, YouTube, TikTok, ngân hàng hoặc dữ liệu tài chính. Chưa xác nhận vòng tạo giá trị thực.
