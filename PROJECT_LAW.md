# MINH TRÍ — PROJECT LAW / LUẬT KIẾN TRÚC

**Owner:** Trần Ngọc Thắng  
**Phiên bản ứng viên:** 0.2 · **Ngày:** 2026-09-29  
**Trạng thái Git hiện tại:** `OWNER-DIRECTED CANDIDATE / NOT MERGED / NO NEW EXTERNAL AUTHORITY`

> **READ BEFORE WORK.** Bất kỳ chat, AI, agent, người đóng góp hoặc tiến trình nào muốn đưa ra nhận định trạng thái, sửa kiến trúc, tạo code hoặc xử lý task cho MINH TRÍ phải đọc luật này, `BOOTSTRAP.md`, `docs/PROJECT_STATE.json`, Brain Manifest hiện hành và context của task trước khi làm việc.

Luật này là bề mặt kiến trúc tối cao của repo MINH TRÍ **sau khi được Owner chấp nhận vào revision chuẩn**. Khi còn ở nhánh/PR chưa merge, nó là ứng viên do Owner chỉ đạo xây, không tự vượt quyền Owner và không tự trở thành luật của `main`.

## 1. Mục đích của MINH TRÍ

MINH TRÍ là **bộ não tổ chức trên GitHub**: tích lũy cách học, cách hiểu, trí nhớ bền, bằng chứng, dự đoán, phản biện, quyết định, bài học và lịch sử sai/sửa. Hệ phải tồn tại độc lập với bất kỳ model AI cụ thể nào.

GPT, Claude, Gemini, Grok hay AI tương lai là **participant/chuyên gia thay thế được**. Không AI nào được sở hữu chân lý, quyền Owner hoặc trí nhớ duy nhất cần để tiếp tục dự án.

Chứng khoán, YouTube, kế toán, sản xuất nội dung và các miền tương lai là **Tầng 2**. Chúng dùng chung Tầng 1 về học, bằng chứng, quyền, phản biện và đo kết quả; tri thức chuyên ngành không được làm bẩn lõi phổ quát.

## 2. Thứ bậc quyền và nguồn chân lý vận hành

Khi có xung đột, ưu tiên theo thứ tự:

```text
1. OWNER CURRENT EXPLICIT DIRECTIVE
          ↓
2. ACCEPTED PROJECT_LAW + ACCEPTED BRAIN REVISION
          ↓
3. PROJECT_STATE + TIER-1 CONTRACTS + DETERMINISTIC GATES
          ↓
4. VERSIONED TASK / PERMISSION / EVIDENCE PACKET
          ↓
5. DOMAIN RULES / CURRENT DATA / TOOLS
          ↓
6. AI OUTPUT = PROPOSAL ONLY
          ↓
7. MODEL MEMORY / CHAT MEMORY = NON-CANONICAL CONTEXT
```

Một file có mặt trên GitHub, một branch, một PR, một câu AI nói hay một kết quả tốt đơn lẻ **không tự trở thành project law**.

## 3. Bất biến lõi bắt buộc

1. **Owner sovereignty** — Owner giữ mục tiêu, vốn/ngân sách, rủi ro, quyền thương hiệu, quyền dữ liệu, chiến lược lớn và quyền mở hành động bên ngoài.
2. **AI replaceability** — thay model/provider không được làm mất mục tiêu, task, bằng chứng, checkpoint, bài học chuẩn hay quyền.
3. **Project memory != model memory** — thông tin cần kế tục phải nằm trong bộ não bền, không phụ thuộc một chat.
4. **Read before reconstruct** — phiên/chat mới phải bootstrap từ repo trước khi nhận định trạng thái hoặc xây.
5. **Evidence before belief** — AI output là proposal/critique; không tự thành fact.
6. **Prediction before outcome** — dự đoán muốn dùng làm bằng chứng năng lực phải được đăng ký trước kết quả.
7. **Dissent cannot be hidden** — phản biện vật chất chưa giải quyết giữ `HOLD`; đa số không tạo ra sự thật.
8. **Role separation** — proposer, critic và adjudicator phải tách theo contract; cùng provider family không được giả thành độc lập.
9. **Domain isolation** — luật/metric/causal model chuyên ngành ở Tầng 2; lõi chỉ giữ cơ chế phổ quát.
10. **Fail closed** — thiếu quyền, sai brain version, sai runtime state, thiếu provenance hoặc bất định trọng yếu thì dừng.
11. **No automatic truth promotion** — `CANDIDATE`/`TRIAL_RULE` không tự thành `VERIFIED`.
12. **Replayable decisions** — quyết định phải truy được revision, task, evidence, participant, critique, gate và outcome.
13. **Measured learning** — “tự học/tốt hơn” phải đo so baseline bằng outcome thật, kể cả chi phí và sai lầm.
14. **No silent architecture mutation** — AI không được tự đổi luật lõi trong lúc xử lý task; chỉ được mở change proposal/PR để review.
15. **Structural != semantic != effectiveness** — test xanh chỉ chứng minh điều test đo; không tự chứng minh hiểu đúng hay tạo giá trị thật.
16. **Elastic N-AI workcell** — AI Commons dùng số participant phù hợp với từng nhiệm vụ; không hard-code số ghế, tên model hay provider. Participant/model/provider đều thay thế được.
17. **Independence is measured, not assumed** — số participant và số provider family độc lập phải được ghi riêng. Nhiều participant cùng family có thể cùng làm việc nhưng không được tính giả thành nhiều nguồn độc lập.
18. **Three logical roles, not three permanent AIs** — proposer/critic/adjudicator là chức năng áp trên từng proposal; không khóa vĩnh viễn một model vào một vai.
19. **Handoff before continuation** — task/checkpoint/handoff thuộc MINH TRÍ. Chat/AI mới phải đọc và xác nhận handoff bền hiện hành trước khi tiếp tục.
20. **Checkpoint last** — durable delta và validation phải được ghi trước; checkpoint/handoff/completion receipt là bước chốt cuối của một đơn vị công việc.
21. **Architecture memory is durable** — ý tưởng/lô-gic lõi đã được Owner chấp thuận phải nằm trong luật/contract/versioned state, không dựa vào trí nhớ một chat.
22. **External cases are priors, not local proof** — case thành công/thất bại bên ngoài có thể tạo hypothesis/prior và cảnh báo lỗi, nhưng không tự chứng minh transfer vào bối cảnh hiện tại.

## 4. Bản kiến trúc công việc bắt buộc

### 4.1 Luồng từ Owner đến hành động và học lại

```text
                          HUMAN OWNER
                              │
                 purpose · boundary · authority
                              ▼
                    GITHUB UNIVERSAL BRAIN
 PROJECT_LAW · BOOTSTRAP · philosophy · architecture · state · code
                              │
                              ▼
                        BRAIN MANIFEST
 revision + artifact hashes + brain fingerprint + runtime state head
                              │
                              ▼
                       CANONICAL TASK
 goal · scope · permissions · evidence · acceptance · risk · expiry
                              │
                              ▼
                    TASK / ROLE ORCHESTRATOR
                              │
               ┌──────────────┼──────────────┐
               ▼              ▼              ▼
           PROPOSER        CRITIC(S)      ADJUDICATOR
          AI / human       AI / human       AI / human
               │              │              │
               └──────────────┼──────────────┘
                              ▼
                   DETERMINISTIC GATES
      version · evidence · role separation · risk · authority
                              │
                      ┌───────┼────────┐
                      ▼       ▼        ▼
                    HOLD    REVISE   CANDIDATE
                                       │
                                       ▼
                                  OWNER GATE
                                       │
                          external action CLOSED
                          until separately authorized
                                       │
                                       ▼
                                  REAL OUTCOME
                                       │
                                       ▼
 source → evidence → claim → prediction → resolution → lesson → procedure
                                       │
                                       ▼
                       ERROR / BASELINE / SCORECARD
                                       │
                                       ▼
                             LEARN AND UPDATE
                                       │
                           new reviewed revision
                                       └──────────→ GITHUB BRAIN
```

### 4.2 Luồng bắt buộc cho mọi chat/AI

```text
NEW CHAT / NEW AI / NEW AGENT
          │
          ▼
READ PROJECT_LAW.md
          │
READ BOOTSTRAP.md
          │
READ current PROJECT_STATE
          │
VERIFY Brain Manifest / revision
          │
READ exact Task Packet + allowed evidence
          │
READ latest durable handoff / checkpoint
          │
ACKNOWLEDGE exact Brain/Law/Bootstrap + handoff hashes
          │
          ▼
ONLY THEN: propose / critique / adjudicate / code
          │
          ▼
REPORT: sources + unknowns + scope + verification
          │
          ▼
PERSIST material durable delta / checkpoint
```

Nếu không có đủ các phần trên: `HOLD / READ_BEFORE_WORK`.

## 5. Brain contract

Mọi task cho AI phải ghim ít nhất:

- `brain_revision` — exact Git SHA dùng để tạo task;
- `brain_fingerprint` — fingerprint manifest artifact lõi;
- `architecture_law_sha256` — hash `PROJECT_LAW.md`;
- `bootstrap_sha256` — hash `BOOTSTRAP.md`;
- `runtime_state_head` — đầu chuỗi trạng thái core lúc task mở;
- `task_fingerprint` — fingerprint task sau khi đóng băng context.

Thay một trong các mốc trên làm task cũ **STALE**. Không được âm thầm tiếp tục theo luật cũ.

Participant muốn nộp proposal/critique/adjudication phải có **Brain Acknowledgement Receipt** khớp task hiện hành. Receipt chỉ chứng minh participant đã xác nhận nhận đúng gói; **không chứng minh đã hiểu đúng**, vì vậy semantic review vẫn bắt buộc.

## 6. Luật học và tự phản biện

Một vòng học đủ phải có, theo mức phù hợp:

```text
REALITY / SOURCE
      ↓
UNKNOWN / UNCERTAINTY
      ↓
CLAIM + ALTERNATIVE + FALSIFIER
      ↓
PREREGISTERED PREDICTION / ACCEPTANCE THRESHOLD
      ↓
INDEPENDENT CRITIQUE
      ↓
DISCRIMINATING TEST
      ↓
OUTCOME
      ↓
RESOLUTION VS BASELINE
      ↓
ERROR ANALYSIS
      ↓
PROCEDURE CHANGE
      ↓
RETEST
      ↓
SCOPED LESSON
```

Không có outcome thật thì không được gọi kết quả là “đã chứng minh hiệu quả”. Một lần đúng không đủ thành luật.

## 7. AI Commons — N participant co giãn, AI thay thế được

- AI Commons official workcell dùng **N participant** được giao cho từng task; `N` không phải hằng số toàn dự án.
- Không hard-code GPT/Claude/Gemini/Grok hay bất kỳ provider/model nào.
- Số participant và số provider family độc lập là hai đại lượng khác nhau và phải được báo cáo riêng.
- Nhiều participant cùng provider family được phép cùng làm việc, nhưng không được tính giả thành nhiều nguồn độc lập.
- Blind round, khi task cần, chỉ được freeze sau khi **mọi participant đã được giao trong session hiện tại** nộp contribution; không có luật `4/4`.
- Mức độc lập tối thiểu, nếu task cần, thuộc contract/risk của chính task; không dùng một con số cố định làm chân lý kiến trúc.
- Ba vai proposer/critic/adjudicator là chức năng logic xoay theo proposal; family separation vẫn áp dụng ở nơi contract yêu cầu phản biện/phân xử độc lập.
- Sau reveal, participant được phép cross-critique, tìm counter-evidence/alternative và đề xuất discriminating test.
- `ABSTAIN` là kết quả hợp lệ.
- Không bỏ phiếu để tạo truth. Bất đồng vật chất chưa giải quyết giữ `HOLD`.
- Replacement trước blind freeze chỉ nhận frozen packet và không được xem contribution khác; replacement sau reveal nhận canonical revealed state và phải được ghi là non-blind.
- Đường official cho proposal/critique/adjudication là **ElasticWorkcell → Arena gateway sau REVEALED**. Direct Arena API/ledger là low-level compatibility/replay surface và không chứng minh một phiên multi-AI chính thức đã hoàn thành.
- Chi tiết bền nằm ở `docs/ARCHITECTURE_MEMORY_AND_CONTINUITY_V0.1.md`.

## 8. Luật kiến trúc khi sửa hệ

Mọi thay đổi kiến trúc/lõi phải ghi rõ:

1. vấn đề thực cần sửa;
2. nguồn và exact revision đã đọc;
3. invariant nào bị tác động;
4. phần nào là ý tưởng / candidate / implemented / empirically verified;
5. test cấu trúc;
6. test semantic khi có ý nghĩa;
7. ảnh hưởng replay/migration;
8. ảnh hưởng quyền/risk;
9. rollback;
10. unknowns;
11. scope áp dụng;
12. cách kiểm bằng dữ liệu thật.

Nếu một AI đề xuất sửa luật này, thay đổi chỉ là **LAW_CHANGE_PROPOSAL** cho tới khi Owner chấp nhận theo quy trình review.

## 9. Kim chỉ nam kiếm tiền và ranh giới Phật học

Owner định hướng mọi hoạt động kiếm tiền bằng lăng kính ứng dụng hiện đại của Tứ Diệu Đế và Bát Chánh Đạo: nhìn đúng thực tế, thấy điều kiện sinh/duy trì vấn đề, chọn đích đúng, chọn phương tiện có trách nhiệm, không lừa mình/lừa người, theo dõi hậu quả và sửa hành động.

Luật bắt buộc giữ biên:

- bài toán tài chính/YouTube/doanh nghiệp vẫn phải giải bằng dữ liệu và causal model chuyên ngành;
- ứng dụng Tứ Diệu Đế/Bát Chánh Đạo vào kiến trúc/đời sống là `MODERN_INTERPRETATION / MODERN_MODEL` trừ khi mệnh đề giáo lý được source-verified riêng;
- không đồng nhất lợi nhuận/KPI với nghĩa kinh;
- kết quả kinh doanh không phải bằng chứng đúng nghĩa kinh.

## 10. Cổng quyền hiện tại

Tại phiên bản ứng viên này:

- AI Commons = `SHADOW`;
- adapter model thật = chưa kết nối;
- external action = **CLOSED**;
- trading/spending/publishing = **CLOSED**;
- Owner/provider identity = chưa xác thực;
- real data loop = chưa chứng minh;
- autonomous merge/release = **CLOSED**.

Không tài liệu nào trong PR này tự mở các cổng trên.

## 11. Tiêu chuẩn báo cáo của mọi AI/chat

Mỗi kết luận vật chất về dự án phải cho biết:

- **Nguồn:** file/commit/test/data nào;
- **Điều chưa biết:** phần nào chưa có bằng chứng;
- **Phạm vi:** kết luận đúng ở đâu;
- **Cách kiểm:** test hoặc dữ liệu nào có thể xác nhận/bác bỏ.

Mọi AI phải nói rõ khi dự án **chưa đạt**.

## 12. Điều kiện để luật trở thành canonical

Luật này chỉ trở thành luật chuẩn của repo khi Owner chấp nhận qua revision chuẩn/merge được phép. Trước đó, đây là `OWNER-DIRECTED CANDIDATE`.

Sau khi canonical, mọi task/brain manifest phải pin luật này; mọi chat/AI làm việc qua AI Commons phải ack đúng hash trước khi đầu ra được nhận.
