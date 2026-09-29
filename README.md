# MINH TRÍ — Universal Intelligence OS

**v0.1: walking skeleton của Tầng 1.** Tầng 1 giữ cách học, phản biện, dự đoán và giới hạn quyền. Tầng 2 là các miền chuyên ngành có thể gắn vào sau. Bản này chạy offline bằng Python 3.10+, không cần API key hay gói Python bên ngoài.

## Cửa cộng tác bốn AI

ChatGPT, Claude, Gemini và Grok có thể cùng đóng góp **qua repo GitHub này**: mỗi bên làm trên nhánh/PR riêng từ cùng mốc `main`, người khác phản biện và một người thứ ba phân xử trên bằng chứng. Cửa sổ chat hiện tại không tự đưa ba AI bên ngoài vào như bốn người tham gia trực tiếp. Bản này chưa kết nối API của họ hay xác thực ID nhà cung cấp. Xem [quy trình bốn AI](docs/FOUR_AI_COLLABORATION.md) và [mẫu PR](.github/pull_request_template.md).

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
