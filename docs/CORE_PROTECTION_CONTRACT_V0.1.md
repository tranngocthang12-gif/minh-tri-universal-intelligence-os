# MINH TRÍ Core Protection Contract v0.1

**Loại:** hợp đồng kiến trúc ứng viên · **Trạng thái:** `SHADOW / NOT PROJECT LAW` · **Ngày:** 2026-09-29

Mục tiêu của hợp đồng này là bảo vệ lõi MINH TRÍ khỏi trôi kiến trúc khi nhiều AI, nhiều miền và nhiều phiên làm việc cùng tham gia. GitHub giữ phiên bản bền; AI chỉ đề xuất thay đổi. Một file có mặt trên GitHub hoặc một PR được tạo ra không tự trở thành luật hay trí nhớ chuẩn.

## 1. Bất biến lõi

1. **Owner sovereignty.** Owner giữ mục tiêu, quyền, vốn/ngân sách, mức rủi ro và quyết định mở hành động bên ngoài. AI không tự nâng quyền.
2. **AI replaceability.** Không model/provider nào được sở hữu luật, trí nhớ chuẩn hoặc trạng thái duy nhất cần để tiếp tục công việc.
3. **Project memory is durable.** Chat/model memory là ngữ cảnh tạm. Trạng thái cần kế tục phải có biểu diễn bền, phiên bản hóa và có provenance.
4. **Evidence before belief.** Đầu ra AI là proposal/critique. Nó không tự trở thành fact, lesson hay quyền hành động.
5. **Prediction before outcome.** Dự đoán muốn dùng để chứng minh năng lực phải được đăng ký/đóng băng trước kết quả.
6. **Dissent cannot be hidden.** Phản biện vật chất chưa giải quyết giữ `HOLD`; số đông không tạo ra sự thật.
7. **Domain isolation.** Lõi sở hữu cách học/quyền/gate; luật và tri thức chuyên ngành ở Tầng 2.
8. **Fail closed.** Thiếu quyền, sai phiên bản brain/runtime, thiếu evidence hoặc rủi ro chưa xử lý thì dừng thay vì tự nới điều kiện.
9. **No automatic truth promotion.** `CANDIDATE` hay `TRIAL_RULE` không tự thành `VERIFIED`.
10. **Replayable decisions.** Cần truy lại được task, nguồn, phiên bản brain, runtime state, người/AI tham gia và kết quả kiểm.
11. **Measured learning.** Khẳng định “học tốt hơn” cần outcome thật và baseline; số agent, số tài liệu hay số lần tự học không đủ.

## 2. Thứ bậc thay đổi

```text
OWNER PURPOSE / BOUNDARY
        ↓
CANONICAL BRAIN ON ACCEPTED GIT REVISION
        ↓
TIER-1 CONTRACTS + DETERMINISTIC GATES
        ↓
VERSIONED TASK + PERMISSION + CONTEXT
        ↓
DOMAIN KNOWLEDGE / DATA
        ↓
AI OUTPUT = UNTRUSTED PROPOSAL
```

`main` là nhánh tích hợp mục tiêu hiện tại của repo. Nhánh/PR là bề mặt ứng viên để kiểm; tồn tại trên GitHub không đồng nghĩa đã được Owner chấp nhận hay đã được kiểm đúng ý nghĩa.

## 3. Brain manifest

Một task AI phải ghim tối thiểu ba mốc độc lập về ý nghĩa:

- `brain_revision`: Git revision của checkout dùng để tạo task;
- `brain_fingerprint`: SHA-256 của manifest các artifact lõi được chỉ định;
- `runtime_state_head`: đầu chuỗi event của trạng thái runtime lúc task mở.

Manifest v0.1 bao phủ `PROJECT_LAW.md`, `BOOTSTRAP.md`, `AGENTS.md`, `PHILOSOPHY`, `ARCHITECTURE`, hợp đồng bảo vệ lõi, kiến trúc Universal Brain, AI Commons, `PROJECT_STATE` và `ROADMAP`. Thay đổi bất kỳ artifact này hoặc runtime head làm task cũ stale trong SHADOW.

Hash/schema chỉ kiểm **đúng cấu trúc và đúng phiên bản**. Nó không chứng minh nội dung đúng, không xác thực danh tính Owner/provider và không chứng minh Git revision do người nhập khai là revision thật nếu chạy ngoài một Git checkout.

## 4. Cổng sửa lõi

Mọi thay đổi reducer, authority, memory contract hoặc invariant phải có bề mặt review trả lời:

1. invariant nào bị tác động;
2. lỗi/thắt nút nào được tái hiện;
3. test hồi quy và test phản chứng nào chặn tái phát;
4. ảnh hưởng replay/ledger cũ và kế hoạch migration;
5. quyền nào thay đổi hoặc không thay đổi;
6. cách rollback;
7. bằng chứng nào là cấu trúc, bằng chứng nào là semantic, và phần hiệu quả thật còn chưa biết.

Nếu migration hoặc quyền chưa rõ: `HOLD`. Không âm thầm viết lại lịch sử để làm test xanh.

## 5. Thu hoạch trí tuệ từ repo khác

Repo khác trong tài khoản là **nguồn kinh nghiệm**, không phải luật tự động của MINH TRÍ. Chỉ chưng cất cơ chế phổ quát; tri thức ngành ở lại Tầng 2. Mỗi phần nhập vào phải ghi repo, exact head/artifact, cơ chế lấy, giới hạn và test mới của MINH TRÍ. Không lấy tên gọi hoặc kết luận cũ làm bằng chứng rằng cơ chế đã đúng trong hệ mới.

## 6. Ranh giới Phật học

Tứ Diệu Đế/Bát Chánh Đạo có thể làm lăng kính ứng dụng hiện đại cho cách nhìn vấn đề và hành động kiếm tiền có trách nhiệm, theo `PHILOSOPHY.md`. Không đồng nhất KPI, lợi nhuận, sự cố kỹ thuật hay chiến lược kinh doanh với nghĩa kinh. Khẳng định giáo lý phải đi theo luồng nguồn kinh riêng; kết quả kinh doanh không xác nhận nghĩa kinh.

## 7. Điều kiện kiểm hợp đồng v0.1

- thay một brain artifact → task cũ bị chặn;
- đổi Git revision → task cũ bị chặn;
- đổi runtime core head → task cũ bị chặn;
- task packet xuất được Project Law + Bootstrap + manifest/fingerprint nhưng chỉ gửi evidence được phép;
- participant chưa có acknowledgement receipt đúng Law/Bootstrap/Brain/Task bị chặn trước proposal/critique/adjudication;
- thay model/participant không làm thay brain contract;
- không có đường từ SHADOW output sang canonical lesson hoặc external action.

**Chưa chứng minh:** hiệu quả đa AI, chất lượng semantic, độc lập provider, nguồn thật, tiết kiệm chi phí hay lợi thế kinh doanh.
