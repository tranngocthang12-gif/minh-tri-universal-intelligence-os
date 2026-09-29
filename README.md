# MINH TRÍ — Universal Intelligence OS

> **BẮT BUỘC TRƯỚC KHI LÀM VIỆC:** mọi chat/AI/agent/người đóng góp phải đọc [PROJECT_LAW.md](PROJECT_LAW.md) rồi [BOOTSTRAP.md](BOOTSTRAP.md), sau đó đọc trạng thái/code/test/task hiện hành. Model/chat memory không thay thế project memory. Khi làm qua AI Commons, participant phải ghi Brain Acknowledgement Receipt khớp exact Law/Bootstrap/Brain/Task trước khi nộp kết quả.

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

## Sân chơi cho nhiều AI — bản thử có kiểm soát

Sau khi khởi tạo lõi, chạy `demo_arena.bat` trên Windows hoặc `PYTHONPATH=src python3 demo_arena.py` trên macOS/Linux. Demo tạo một sổ tạm, bốn **participant giả lập**, một nhiệm vụ, hai phản biện và kết luận `HOLD` vì một phản biện còn mở. Không gọi ChatGPT, Claude, Gemini, Grok hay API nào; kiểm tra bảy participant trong bộ test chứng minh số ghế không bị viết cứng thành bốn.

Để nhập đầu ra AI bằng tay trong sổ của anh: chạy `minhtri.bat init` nếu chưa có `brain/`, rồi `minhtri.bat arena init`. Mỗi lệnh `minhtri.bat arena apply duong-dan\lenh.json` nhận một JSON `{"type":"...","data":{...}}`; trước tiên đăng ký `register_participant`, mở `open_task`, mỗi participant chạy `acknowledge_brain`, rồi mới nộp `submit_proposal`, `submit_critique`, `submit_adjudication`. Lệnh mở nhiệm vụ trả `task_fingerprint` cùng `brain_revision` và `brain_fingerprint`; task còn ghim `runtime_state_head`. `minhtri.bat arena task ID` xuất gói nhiệm vụ, Brain Manifest, toàn văn PROJECT_LAW/BOOTSTRAP, bản tư tưởng và duy nhất các evidence được phép để chuyển cho AI theo cách thủ công. Nếu Git revision, một artifact lõi trong manifest hoặc runtime state thay đổi, task cũ bị chặn và phải mở lại. Xem [hợp đồng sân chơi](docs/AI_COMMONS_ARCHITECTURE_V0.1.md) để biết ý nghĩa các trường và cổng quyền. `arena status` và `arena verify` kiểm tra sổ riêng; `arena repair-snapshot` tái dựng cache sau khi kiểm sổ. Không lệnh nào tự ghi bài học vào lõi.

Trạng thái hiện tại là `SHADOW`: [Core Protection Contract](docs/CORE_PROTECTION_CONTRACT_V0.1.md) và [Universal Brain Architecture](docs/UNIVERSAL_BRAIN_ARCHITECTURE_V0.1.md) vẫn là ứng viên; danh tính nhà cung cấp tự khai; evidence được phép chỉ từ nguồn giả lập cùng miền và quyền `CLEAR` do người nhập khai báo. Chưa có kết nối model, xác thực Owner, chi phí API hay hành động bên ngoài. Sân chơi này là hợp đồng và cổng thử nghiệm để chuẩn bị mở cho N AI sau khi lõi và vòng dữ liệu thật được kiểm chứng.

## Bản đầu tiên làm được gì

- Mở một miền mới mà không sửa lõi; mở mục tiêu và khung vấn đề (thực trạng, điều kiện giả định, đích, can thiệp, trách nhiệm, rủi ro), đặt ưu tiên, tạm chặn hoặc đóng. Không có mục tiêu hợp lệ thì trả `WAIT`.
- Ghi `SOURCE → EVIDENCE → CLAIM → PREDICTION → RESOLUTION → LESSON`, kèm `PROCEDURE` và danh tính provider khai báo. Dự đoán phải được đóng băng trước khi có kết quả; code tự tính điểm trúng khoảng và sai số điểm giữa.
- Tách vai đề xuất, phản biện và trọng tài bằng ID provider; chặn cùng một provider chiếm hai ghế của cùng nhận định.
- Chỉ cho kích hoạt một bài học ở trạng thái `TRIAL_RULE` khi goal còn mở, có ít nhất hai dự đoán đã giải quyết, hai nguồn kết quả first-party khác nhau, mọi phản biện/trọng tài chấp nhận và Owner ghi xác nhận. Goal bị chặn/đóng hoặc có phản biện mới bất lợi thì quy tắc thử thành `SUSPENDED`; không có đường tự động nâng thành `VERIFIED`.
- Từ chối kích hoạt quy tắc trong miền rủi ro cao ở bản này. Không có chức năng chi tiền, giao dịch, phát hành hoặc tự sửa luật.
- Kiểm sổ JSONL bằng chuỗi SHA-256, tái dựng trạng thái và so với cache. File Git cần được commit để tạo mốc độc lập chống việc viết lại cả chuỗi.

## Lệnh JSON mẫu

```json
{
  "type": "register_provider",
  "data": {"id": "researcher_a", "name": "Researcher A", "kind": "MODEL", "family_id": "provider_family_a"}
}
```

Gọi `minhtri.bat apply duong-dan\lenh.json`. Xem [hợp đồng và luồng dữ liệu](docs/ARCHITECTURE.md) để biết các lệnh tiếp theo. Các ví dụ YouTube và tài chính chỉ chứng minh rằng cùng một lõi nhận được hai miền; chúng **không** chứa dữ liệu thị trường hay khuyến nghị đầu tư.

## Ranh giới trung thực

Đây là hệ **ghi nhận và kiểm soát việc học**, chưa phải AI tự suy nghĩ như người hay hệ tự cải thiện đã được chứng minh. ID nhà cung cấp và xác nhận Owner là khai báo; CLI offline không xác thực danh tính. Nguồn và số liệu người dùng nhập chưa được máy kiểm chứng. Chuỗi hash phát hiện sửa cục bộ một phần, không chống người có quyền viết lại toàn bộ sổ; Git commit hoặc mốc độc lập mới tăng sức chứng thực. Kết quả dự đoán không tự chứng minh quan hệ nhân quả. Cổng rủi ro và xác thực dữ liệu trước hành động thực cần được làm ở giai đoạn kế tiếp.

## Trạng thái

`FOUNDATION_PROTOTYPE`: cài đặt kiểm soát cục bộ và ca thử bằng dữ liệu giả định. Chưa kết nối Claude/ChatGPT/Gemini/Grok, YouTube, TikTok, ngân hàng hoặc dữ liệu tài chính. Chưa xác nhận vòng tạo giá trị thực.
