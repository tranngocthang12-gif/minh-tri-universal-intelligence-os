# Cửa cộng tác ChatGPT · Claude · Gemini · Grok

**Trạng thái:** cửa GitHub và quy trình review, chưa phải một phòng chat bốn model chạy đồng thời. `register_provider` trong lõi chỉ ghi tên khai báo; nó không kết nối tài khoản, cấp quyền GitHub, gọi API hay chứng minh tính độc lập của model.

## Một nơi làm việc chung

Repo này là nguồn chuẩn cho mã, luật, trạng thái dự án và quyết định đã được duyệt. Một Issue mô tả **một việc**; bốn AI có thể đọc cùng Issue và cùng SHA nền, rồi tạo **nhánh và PR riêng**. PR ghi ai tạo, dùng model/phiên bản nào, mốc nền, thay đổi, kiểm thử, bằng chứng, phản chứng và phần còn chưa biết. Không ai đẩy trực tiếp vào `main` theo quy trình cộng tác này.

| Ghế trong một việc | Trách nhiệm | Giới hạn |
| --- | --- | --- |
| Đề xuất | Thiết kế hoặc viết mã, tạo PR và nêu điều có thể làm mình sai | Không tự duyệt PR của mình |
| Phản biện | Tìm lỗi logic, dữ liệu, bảo mật, quyền và trường hợp phản ví dụ | Không dùng lời đồng ý làm bằng chứng |
| Trọng tài | Đối chiếu claim, diff, kiểm thử, phản chứng và phạm vi | Không đồng thời là người đề xuất hoặc phản biện cùng việc |
| Owner | Giữ mục tiêu, vốn, quyền tư liệu, rủi ro và các quyết định lớn | AI không thay Owner ở các cổng này |

Bốn tên AI **không bị đóng đinh vào bốn chức danh**. Vai thay theo việc; một AI có thể đề xuất ở việc A và phản biện ở việc B. Nếu ba ghế cần độc lập mà chỉ có hai AI tham gia, việc đó ở trạng thái `HOLD`, không giả làm đủ ghế. AI thứ tư có thể là phương án cạnh tranh hoặc phản biện bổ sung.

## Quy trình một vòng

1. **Owner/điều phối mở Issue bằng mẫu “Việc cho bốn AI”:** mục tiêu, phạm vi, SHA nền, tệp được phép sửa, tiêu chí đạt/trượt, dữ liệu được phép chia sẻ, cổng Owner và hạn. Nếu thiếu điều kiện quyết định, đánh dấu `BLOCKED`.
2. **Đề xuất độc lập:** mỗi AI tạo `ai/<provider>/<task-id>` từ cùng SHA nền và mở PR riêng. Không đọc kết luận của AI khác trước khi nộp phương án nếu bài toán cần so sánh độc lập.
3. **Kiểm tự động:** CI chạy các ca kiểm thử hiện có trên PR. PASS chỉ chứng minh mã qua ca đó, không chứng minh nhận định miền, tính độc lập hay độ đúng của giáo lý.
4. **Phản biện:** chỉ ra vị trí file/dòng và test hoặc bằng chứng phân định. Với việc cần blind review, điều phối tạo bản gói ẩn tác giả rồi thu phản biện trước khi tiết lộ; PR công khai tự nó không bảo đảm mù.
5. **Trọng tài:** giữ, sửa hay bác từng nhận định; nếu dữ liệu không phân định thì ghi `UNRESOLVED` và chọn thử nhỏ có thể đảo ngược hoặc `OWNER_REVIEW_REQUIRED`. Không biến đa số AI thành sự thật.
6. **Chốt:** PR được merge khi review và kiểm thử phù hợp, còn `main` hiện chưa có branch protection cưỡng chế. Thay đổi về tư tưởng, luật, quyền, chi tiền, tài chính, dữ liệu riêng, phát hành hoặc chiến lược lớn phải có Owner duyệt rõ.

Nếu Claude/Gemini/Grok chưa có công cụ hoặc quyền ghi GitHub, họ vẫn đóng góp bằng một bản đề xuất hoặc patch kèm SHA nền và bằng chứng; người điều phối mở PR thay và ghi **tác giả nội dung thực**, không giả rằng model đã tự đăng nhập. Không nhập password, token, dữ liệu cá nhân hoặc tư liệu chưa rõ quyền vào repo công khai.

## Kiểm tra trước khi gọi là “bốn AI cùng làm”

- Có bốn phiên làm việc thật với cùng Issue/SHA nền hoặc bốn PR/phiếu phản biện có provenance.
- Biết model nào tạo nội dung nào; không coi bốn vai diễn trong một lần gọi model là bốn ý kiến độc lập.
- Mỗi claim quan trọng có bằng chứng, phản chứng và kết quả phân xử; sự đồng thuận không tự nâng thành `VERIFIED`.
- Việc còn thiếu phản biện, quyền truy cập hoặc Owner gate được ghi là `PENDING`, không báo hoàn thành.

Để **tự động gọi** cả bốn AI, cần tích hợp API, quyền, ngân sách, quyền chia sẻ dữ liệu và cơ chế nhận dạng riêng. Đó là bước triển khai sau khi quy trình PR thủ công đã chạy qua một việc thật; hiện tại không tuyên bố đã kết nối.
