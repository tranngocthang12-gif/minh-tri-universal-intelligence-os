# Đối chiếu lõi MINH TRÍ với bản thiết kế — 2026-09-29

**Kết luận:** `PARTIAL_CONFORMANT / FOUNDATION_PROTOTYPE`. Khung Tầng 1 đã chạy offline; chưa có căn cứ gọi đó là tổ chức đã học tốt qua dữ liệu thật hoặc sân chơi AI đã kết nối thực. Bản kiểm này xét `main` ở `d4237384` và bản sửa ứng viên trên PR #2. Nó không sửa luật hay trạng thái của `sieu-du-an`.

## Phạm vi thiết kế

- Trực tiếp: [PHILOSOPHY.md](PHILOSOPHY.md), [ARCHITECTURE.md](ARCHITECTURE.md), [ROADMAP.md](ROADMAP.md), [AI Commons](AI_COMMONS_ARCHITECTURE_V0.1.md).
- Tài liệu được dẫn làm kinh nghiệm: [Owner clarification](https://github.com/tranngocthang12-gif/sieu-du-an/blob/main/docs/OWNER_CLARIFICATION_REALITY_DHAMMA_ACTION_ARCHITECTURE_2026-09-20.md), [Financial Intelligence Architecture v1.0](https://github.com/tranngocthang12-gif/TRUNG-T-M-T-I-CH-NH-Financial-Intelligence-Media-Factory/blob/main/architecture/ARCHITECTURE_v1.0.md), [LOI_TU_HOC_v2](https://github.com/tranngocthang12-gif/nao-nha-may/blob/main/LOI/LOI_TU_HOC_v2.md). Các tài liệu này thuộc dự án khác; MINH TRÍ mới kế thừa nguyên lý đã ghi rõ, không mặc nhiên đạt mọi cổng trong đó.

## Kết quả đối chiếu

| Hợp đồng thiết kế | Quan sát trong code | Mức |
| --- | --- | --- |
| Lõi độc lập miền; Source → Evidence → Claim → Prediction → Resolution → Lesson, Procedure | Cùng reducer nhận ví dụ YouTube và tài chính; tham chiếu miền được chặn; dự đoán chấm khoảng bằng code | Có trong lát chạy offline |
| Goal định tuyến, `WAIT`, chặn khi Owner dừng | Goal `OPEN/BLOCKED/CLOSED`, `WAIT`; bản sửa chặn dự đoán mới/đóng băng/kích hoạt và đình chỉ trial khi goal dừng | Có trong bản sửa ứng viên |
| Dự đoán đăng ký trước rồi mới xem kết quả | Có trạng thái `REGISTERED → FROZEN → RESOLVED`; bản sửa buộc freeze trước hạn; thời điểm tự khai và hash cục bộ chưa là chứng thực độc lập | Một phần |
| Mọi phản biện được xét, bất đồng không bị giấu | Bản sửa chặn acceptance/activation nếu bất kỳ review/adjudication của claim còn bất lợi; bất đồng mới đình chỉ trial | Có trong bản sửa ứng viên, nội dung phản biện vẫn do người xét |
| Ba vai độc lập | Lõi chỉ tách theo provider ID tự khai; AI Commons `SHADOW` tách theo family ID tự khai | Một phần; chưa xác thực cùng model/đơn vị |
| Nguồn, quyền và tri thức có provenance | URI, thời điểm, loại nguồn, rights tự khai, hash chuỗi sự kiện; chưa hash nội dung nguồn hay đối soát quyền/nguồn thật | Một phần |
| Học cải thiện dự báo so baseline | Có hit khoảng và sai số điểm giữa; chưa có base rate, xác suất, calibration, scorecard, phép thử A/B và vòng thật | Chưa đạt |
| Phân tích vấn đề đúng ranh giới ý nghĩa | Khung `reality/conditions/unknowns/target/control/influence/responsibility`; chưa có mô hình cấu trúc kiểm tương tác nguyên nhân bên ngoài và phản ứng nội tâm, hay chứng cứ Nikāya trong luồng riêng | Một phần; không tự nhận diễn giải kinh |
| Owner nắm quyền thật và AI chỉ nhận nhiệm vụ | `owner_ack` là chuỗi tự khai; arena chỉ `MANUAL`, ngân sách 0, không gọi model/API hay hành động ngoài | Chưa đủ để mở quyền thật |
| Sổ bền, sửa được cache | JSONL hash chain + replay + cache; phát hiện sửa từng phần, không chống viết lại cả chuỗi; cần mốc độc lập | Có trong phạm vi cục bộ |

## Ba lỗi cổng đã tái hiện ở `main` và sửa trong PR #2

1. `freeze_prediction` sau `due_at` từng được chấp nhận. Bản sửa chặn thời điểm `>= due_at` và goal không mở.
2. Goal `BLOCKED` vẫn có thể kích hoạt `TRIAL_RULE`. Bản sửa chặn và chuyển trial đã kích hoạt sang `SUSPENDED` khi goal bị chặn/đóng.
3. Một review `ACCEPT_FOR_TRIAL` từng vượt qua review `HOLD` khác của cùng claim. Bản sửa xét tất cả review ở bước phân xử và tất cả review/adjudication ở bước kích hoạt; phản biện bất lợi mới đình chỉ trial.

Ca kiểm hồi quy nằm trong `tests/test_core.py`; bộ test toàn dự án có 15 ca. Kết quả kiểm cấu trúc **không chứng minh** tính đúng của dữ liệu, ý nghĩa, tác động hoặc lợi thế so với một AI đứng riêng.

## Cổng còn thiếu trước khi nói “đã hoạt động tốt”

1. Xác thực Owner/provider và ánh xạ family chung giữa lõi và AI Commons; hiện ID có thể tự khai và cùng một model có thể mang nhiều ID trong lõi.
2. Nguồn dữ liệu thật chỉ đọc có hash/provenance, quyền được kiểm, timestamp độc lập và phân loại dữ liệu trước khi gửi cho provider ngoài.
3. Một vòng thí nghiệm thực đã đăng ký trước: outcome được đo, baseline, sai số và điều kiện áp dụng; sau đó mới xem xét scorecard, lựa chọn procedure và meta-learning.
4. Chính sách phiên bản cho sổ cũ. Sửa reducer có thể khiến replay của sổ trước đây từng nhận một sự kiện nay bị cấm thất bại. Phải kiểm/migrate từng sổ trước khi nâng bản; không tự xóa hoặc âm thầm viết lại lịch sử.
5. Kết nối AI thật, quota và log chi phí, cổng quyền cho từng adapter, đường dừng/rollback và benchmark độc lập. `SHADOW` chưa thỏa các điều kiện này.
6. Đồng bộ xuyên hai sổ: arena kiểm core head trước khi ghi vào sổ riêng, nhưng chưa có giao dịch/khóa chung nếu hai tiến trình sửa core và arena đồng thời. Trước `CONTROLLED` cần khóa hoặc compare-and-swap mốc core trong một giao dịch, kèm ca kiểm cạnh tranh.

**Quyết định vận hành:** giữ PR #2 ở trạng thái nháp. Chỉ được kết luận “lõi có khung học kiểm soát offline”; việc hệ học tốt hơn, đúng nghĩa trong tình huống thật và phối hợp N AI hiệu quả vẫn chưa được chứng minh.
