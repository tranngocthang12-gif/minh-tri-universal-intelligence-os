# MINH TRÍ — EXPERT INTELLIGENCE ARCHITECTURE V2 (EIA-V2)
## ĐỀ ÁN KIẾN TRÚC TRÍ TUỆ CHUYÊN GIA — BẢN MỤC TIÊU ĐỂ PHẢN BIỆN

Ngày: 2026-10-09.
Tình trạng: ARCHITECT PROPOSAL / UNACCEPTED / NOT CANONICAL / NOT AN IMPLEMENTED AI CAPABILITY.
Độ lớn thay đổi nếu muốn thay Master Blueprint: Class F — Foundation. Các thí nghiệm trong vùng mở rộng có thể là Class D/O/S riêng; tài liệu này tự nó không mở lại Foundation.
Cơ sở protected main đọc trực tiếp: a5ed9d8347a60b95503fe2e5de6b95fd8375eb76 (Foundation V1 FROZEN).
Repo: tranngocthang12-gif/minh-tri-universal-intelligence-os.
Tác giả đề xuất: current ChatGPT Total Architect seat; tác giả KHÔNG được tự kiểm định hoặc tự phê duyệt.
Owner intent: xây MINH TRÍ chuyên sâu, sắc bén, có năng lực giải quyết việc mới như một chuyên gia đã học lâu dài; không phải thư viện chép bài hay chatbot trả lời chung chung. Ưu tiên học hiểu, thực chiến chỉ khi Owner giao. Học và ghi nhớ chính thức không phụ thuộc PC online. Đây là **đề xuất dựa trên trao đổi hiện tại**, không phải luật mới đã chấp nhận.

## 0. Luận đề trọng tâm / falsifiable North Star

MINH TRÍ không được tuyên bố vượt trội chỉ vì lưu nhiều tài liệu, viết dài, có nhiều phản biện AI, dùng nhiều token, hay thêm công cụ. Năng lực chuyên gia được định nghĩa bằng hiệu suất trên nhiệm vụ khó **mới, chưa có sẵn lời giải trong kho**, qua so sánh đối chứng độc lập, chứng cứ truy ngược được, và khả năng tự chỉ ra sai lầm/giới hạn. Mục tiêu không phải tự huấn luyện lại mô hình nền chỉ bằng hội thoại: GitHub/RAG/ghi chú không thay đổi trọng số mô hình. Đây là kiến trúc tạo ra **năng lực hệ thống quan sát được** (model + evidence + structured reasoning + verification), chưa phải tuyên bố đổi trí thông minh bên trong mô hình.

Ba câu hỏi kiểm định: (i) biết điều gì, chắc chắn đến đâu; (ii) giải thích/áp dụng được đến đâu; (iii) khi gặp vấn đề chưa biết, giải được đúng và tốt hơn giải pháp nền trong ràng buộc công bằng không?

## 1. Hệ ràng buộc không được phá

- Owner chọn mục tiêu và phạm vi; kết quả thực chiến/đăng tải/sửa hệ thống ngoài phạm vi nghiên cứu cần ủy quyền rõ.
- GitHub protected main là nguồn nhớ chuẩn DUY NHẤT. Một boot root, một law router, một current state, một task registry; các view/trích xuất không thành brain thứ hai.
- Foundation V1 FROZEN: không sửa law, state, Master Blueprint hoặc bật runtime tự trị bằng một đề xuất này. Class F cần đường governance, Owner chấp nhận; Class S cần review/approval riêng. Không tự merge, tự VERIFIED.
- Chat/model/provider/PC thay thế được; PC offline vẫn nghiên cứu và lưu candidate lên GitHub nếu GitHub còn nối. Local Brain chỉ mirror, khi online lại đọc từ canonical main; không bao giờ sửa ngược main bằng trạng thái local cũ.
- Mọi kiến thức mới tách bốn chiều: nguồn, kết luận, năng lực chứng minh, trạng thái chấp nhận. Kiến thức chưa review=PENDING_REVIEW; ACTIVE không có nghĩa mô hình đã thành chuyên gia.
- Ưu tiên học sâu. Không coi xếp hạng cao hoặc kết quả benchmark là chứng chỉ đại học/thạc sĩ/tiến sĩ.
- Nhiệm vụ Phật học giữ kinh sớm làm trục, Pāli/đối dịch theo nguy cơ, Mi Tiên Vấn Đáp bắt buộc như lớp giải thích hậu kỳ; không gộp thành lời Phật.
- Không ép Owner mở máy hoặc thao tác GitHub mới tiếp tục học khi connector có thể làm được.

## 2. Chẩn đoán kiến trúc V1 và khoảng thiếu

Cái đã có: điều hành/luật, protected GitHub, state/tasks, evidence/provenance, knowledge atoms/hubs, Knowledge Fast Lane, semantic staleness, protected recovery và independent critic architecture. Các đề xuất Learning Loop (PR #333) và meaning fidelity (PR #335) là candidate, KHÔNG phải runtime tự học đã được xác nhận. PR #343 về bảy bước/ba cổng học chung là candidate Class F, chưa xem là canonical.

Khoảng thiếu quan trọng nhất: **cầu nối từ KNOWLEDGE (biết bài nào, dẫn nguồn nào) sang CAPABILITY (làm được gì khi gặp bài mới)**. Không có bằng chứng hiện hành cho thấy đọc/ghi chép nhiều đã cải thiện đáng kể khả năng giải bài ngoài ngữ cảnh; kịch bản tự phản biện dễ thành hợp thức hóa lời mình; split giữa checkpoint chat và protected main vẫn tồn tại (A172/A173 vs chat A205/A206). Không mở Foundation chỉ để sửa triệu chứng; cần chứng minh thiếu hụt bằng phép đo.

## 3. Kiến trúc mục tiêu — 6 chức năng logic nằm trên Foundation cũ

### F0 — Governance/continuity floor (GIỮ NGUYÊN)
Owner, law precedence, Master Blueprint, current/task registry, protected main, evidence, Class F/S/D/O gates, no-self-certification. Tất cả chức năng dưới đây là CONTRACT/VIEWS của hệ đang có, chưa mặc nhiên là microservice hoặc hệ lưu mới.

### F1 — Evidence Fabric: học đúng thế giới
Lưu Source -> Passage -> Claim -> Reason/Counterclaim -> Provenance; nguồn có ID, bản dịch/bản gốc, hiệu lực, phạm vi, người kiểm, trạng thái. Mỗi claim chỉ nói điều nguồn thật sự hỗ trợ; phân biệt claim trích văn bản, tổng hợp, giải thích thứ cấp và chưa chắc chắn. Hồ sơ có supersession, phụ thuộc, conflict và chất lượng chứng cứ. Không nhồi prompt bằng tài liệu không chọn lọc; retrieval có bound theo quyền, thời gian và đúng nguồn.

### F2 — Understanding Models: hiểu và giữ được cơ chế
Thêm **góc nhìn khái niệm** không phải brain mới: mô hình nguyên lý, điều kiện cần/đủ khi có chứng cứ, ngoại lệ, giả định ẩn, phản ví dụ, mối quan hệ nhân quả *chỉ khi có căn cứ*, ranh giới áp dụng. Trong Phật học: diễn giải phải gắn văn bản và phân tầng kinh sớm/Milinda; trong kinh tế: phải nêu giả định, dữ liệu và điều kiện môi trường. Một biểu đồ đẹp không được thay thế chứng cứ.

### F3 — Skill & Method Atlas: biết cách làm
Lưu **quy trình có thể kiểm** cho từng loại vấn đề: chẩn đoán, phân rã, chọn công cụ, tính toán/diễn giải, đối chứng, kiểm lỗi, điểm dừng, khi nào không đủ dữ liệu. Gắn mỗi phương pháp vào kiến thức chứng minh và các bài thử qua/không qua. Atlas là view/record hợp lệ dưới schema knowledge hiện có hoặc thay đổi Class S riêng nếu cần; tuyệt đối không thêm kho quyền lực thứ hai. Không gọi “kỹ năng đã có” cho đến khi thử được trên tình huống mới.

### F4 — Expert Reasoning Session: áp dụng nhiều lĩnh vực khi Owner hỏi
Với nhiệm vụ được giao: đọc mục tiêu -> nêu câu hỏi/giả định -> trích chọn nguồn -> dựng mô hình vấn đề -> tìm nhiều phương án -> phản ví dụ/tấn công -> chọn đáp án có điều kiện -> kiểm tra -> trình bày quyết định và điều chưa biết. Triệu hồi toán, kinh tế, kinh nghiệm kỹ thuật tùy vấn đề, KHÔNG bắt buộc 3 AI cho mọi câu. Một mô hình có thể kiêm nghiên cứu ban đầu và phản biện sơ bộ nhưng không tự là người kiểm chứng/duyệt độc lập. Rationale cần là lập luận có chứng cứ công khai được, không yêu cầu chuỗi suy nghĩ bí mật từ model.

### F5 — Capability Assurance & Expert Evaluation: chứng minh năng lực
Mọi mục tiêu chuyên sâu gắn bản đồ cấp năng lực quan sát được, câu hỏi chuyển giao mới, phản biện độc lập, công cụ kiểm tra khách quan nếu có, người chấm mù thông tin sản phẩm, hồ sơ lỗi và retest chậm sau học. G1 source, G2 understanding/transfer, G3 continuity; bổ sung **G4 outcome evidence** chỉ là tên logic cho hiệu suất ngoài mẫu, chưa phải luật mới hoặc status mới.

### F6 — Curriculum/Reflection: phát triển năng lực có hướng dẫn
Phân tích gap giữa mục tiêu của Owner và performance đã đo: lựa chọn chủ đề kế tiếp có **giá trị học dự kiến cao** (chỗ thiếu nguyên lý/khả năng vận dụng) chứ không chạy theo A-number. Thực hành phản chứng, học từ sai lầm và kiểm tra lặp lại sau thời gian; kiến thức mâu thuẫn được mở tranh luận và sửa có lineage. Việc chọn mục tiêu mới quan trọng vẫn cần Owner; không tự bật autonomous/self-modifying learning. Ngân sách theo domain, độ khó và thời gian Owner cho phép.

## 4. “Tấm bằng” và năng lực: không đánh tráo

MINH TRÍ có thể *học theo mức độ sâu tương tự* lộ trình đại học -> thạc sĩ -> tiến sĩ, nhưng chỉ được gắn **mức năng lực được thử**, không tuyên bố có bằng cấp. Mô hình bậc:

- L0 — Source recall: tìm và trích đúng nguồn.
- L1 — Conceptual comprehension: giải thích nguyên lý, giới hạn, khác biệt, phản ví dụ.
- L2 — Method execution: giải bài cùng dạng với các ràng buộc biến đổi.
- L3 — Novel transfer: giải việc khác ngữ cảnh, tránh học thuộc mẫu.
- L4 — Professional judgment: đề xuất và bác bỏ phương án, định lượng sai số, chấm độc lập có so sánh baseline và tiêu chí thực dụng.
- L5 — Controlled real-world delivery: chỉ sau Owner giao việc; đo kết quả thực, quyền riêng tư, an toàn, hậu kiểm.

Mỗi domain có vector năng lực riêng; không có một điểm IQ/điểm tốt nghiệp chung. Điểm L4 trong kinh tế không chứng minh L4 Phật học. “Thành thạo” luôn ghi nhiệm vụ, thời gian, phiên bản mô hình, quyền công cụ và sai số.

## 5. Vòng học phát triển năng lực thực sự (không chỉ viết tiếp checkpoint)

OWNER GOAL -> CANONICAL RECOVERY -> SOURCE/CORPUS AUDIT -> MODEL OF UNDERSTANDING -> CONTRADICTION/COUNTEREXAMPLE -> METHOD PRACTICE -> FROZEN HELD-OUT TRANSFER -> DIFFERENT-SEAT CRITIC / EXPERT CHECK -> PROPOSED KNOWLEDGE+SKILL RESULT (PENDING_REVIEW) -> GOVERNED ACCEPTANCE+PROTECTED MERGE -> ZERO-CHAT RECOVERY -> DELAYED RETEST -> CURRICULUM GAP.

Mỗi lần học phải tách:
- Learned content: điều biết, nguồn và giới hạn.
- Learned procedure: phương pháp có thể thực thi; tiền điều kiện và lỗi thường gặp.
- Demonstrated capability: mã bài thử chưa thấy, phiên bản model, dữ liệu/công cụ, câu trả lời, chấm độc lập, thất bại.
- Durable continuity: commit main đã chấp nhận, fresh read, minh chứng chat mới phục hồi.

Không có G2/G4 thì hồ sơ được phép là kiến thức nguồn hay giả thuyết, nhưng không có claim “đã giỏi”. Không có protected merge thì việc học vẫn có thể tiếp tục, nhưng báo “candidate only”.

## 6. Evaluation khoa học — so sánh công bằng với GPT thường

Chỉ số “vượt trội AI phổ thông” PHẢI đặt theo domain và hoàn cảnh sử dụng:

- A0: base GPT cùng phiên bản, không biết kho MINH TRÍ, cùng mục tiêu và khả năng công cụ.
- A1: cùng GPT với retrieval tài liệu tương đương nhưng không có curriculum/structured reasoning.
- A2: MINH TRÍ (cùng nền model) với records/skill atlas/decision protocol và allowed tools.
- A3: chuyên gia độc lập hoặc giải chuẩn, nếu có, để đánh giá độ chuyên nghiệp; không coi một AI critic đơn độc là ground truth.

Giữ hoặc ghi rõ chênh lệch về model/provider, token, tổng chi phí, thời gian, web access, nguồn, phiên bản; A1 rất quan trọng để không nhầm lợi ích RAG và lợi ích năng lực được luyện. Trộn thứ tự, ẩn danh outputs cho ít nhất hai người chấm với bài quan trọng, đối chiếu bất đồng theo quy trình, không để producer xem đáp án/câu hỏi held-out trước. Pre-register benchmark trước khi học và trước review; kiểm tra contamination từ lịch sử chat/PR; giữ private answer keys ngoài retrieval của seat giải.

Dùng cả chỉ tiêu đúng/sai và năng lực: factual source fidelity; completeness; assumption discovery; quality of alternatives; transfer; calibration/abstention; robustness trước dữ liệu thay đổi; execution correctness; cost/latency; safety; reproducibility. Báo thất bại nghiêm trọng và vùng bất định, không chỉ điểm trung bình. Với khoa học xã hội/Phật học có nhiều cách hiểu: rubric cho phép đa quan điểm có nguồn, không ép một đáp án giáo điều.

**Go/no-go:** bắt đầu pilot nhỏ có đối chứng. Chỉ khẳng định “vượt trội trong tác vụ X ở cấu hình Y” nếu hiệu quả vượt A1 trong phép đo được chấp nhận, cỡ mẫu, sai số và độ bền phù hợp. Không đặt lời hứa tỷ lệ cải thiện ảo, không lấy CI code làm proof chuyên gia, không dùng đề đã lộ. Ghi rõ tình huống A2 thua A1 và sửa hoặc rollback.

Các nguồn tham khảo **chỉ là gợi ý phương pháp đo, không thẩm quyền của MINH TRÍ**:
- Stanford HELM — evaluation đa kịch bản/đa chiều, reproducible: https://crfm.stanford.edu/helm/index.html
- NIST AI RMF Playbook — MEASURE, ghi rõ cả thuộc tính không đo được: https://airc.nist.gov/airmf-resources/playbook/measure/
- METR time-horizon methodology — độ tin cậy trên task và thời lượng; chỉ tham khảo khi nghiên cứu tự chủ: https://metr.org/time-horizons/

## 7. Ba ví dụ đánh giá chuyển giao

**Toán học cao cấp / tối ưu sản xuất:** sau học giải tích, đại số tuyến tính, tối ưu, Owner cho case mới có nguyên liệu, biến số, ràng buộc phi tuyến, sai số đo. MINH TRÍ phải chọn mô hình, chứng minh tính hợp lệ/giải số khi cần, chỉ ra trường hợp mô hình hỏng, so sánh phương án, đánh giá nhạy cảm. Không được coi chép một thuật toán từ sách là hoàn thành. Test toán có thể chấm bằng bài giải chuẩn, kiểm tra độc lập và giả lập số; không tự tối ưu hệ thống sản xuất thật.

**Kinh tế / doanh nghiệp:** một doanh nghiệp báo lãi nhưng rủi ro phá sản; mô hình hóa dòng tiền, vốn lưu động, nợ, unit economics, cấu trúc thị trường, hành vi cạnh tranh, kịch bản suy thoái, phân tích nhân quả vs tương quan. Kiểm tra bằng dữ kiện chưa có trong tài liệu đã học, nêu điều kiện gây đảo chiều quyết định; không tự cho là lời khuyên đầu tư chuyên nghiệp.

**Tư duy Đức Phật:** một câu hỏi mới khiến hai kinh sớm có vẻ bất đồng, và Mi Tiên nêu ẩn dụ giải thích. Trả lời phải tách TEXT_ATTESTED / CROSS_TEXT_SYNTHESIS / LATER-PARACANONICAL / UNCERTAINTY; kiểm Pāli, song song nếu có, giới hạn phiên dịch, phản ví dụ và lịch sử chú giải. Thước đo là trung thành chứng cứ, sâu về lập luận, sửa được cách hiểu cũ, không đếm số lần nói “duyên khởi/vô ngã”. Không đánh giá Phật học bằng khung khoa học hiện đại trái mục tiêu Owner.

## 8. Dữ liệu và “bộ nhớ” không tạo gánh nặng kiến trúc

Không tạo database trạng thái thứ hai. Kho nguồn/claim/method/outcome là các loại hồ sơ, hub, manifest/derived views trong knowledge đã được quản trị (nếu schema thiếu trường, trình Class S rất hẹp thay vì schema toàn cục mới). Nhu cầu retrieval lớn lên có thể dùng index có thể tái tạo, nhưng index là disposable cache, không canonical. Thuật toán chọn bài học/công cụ chỉ là dịch vụ có thể thay thế; tool mới không được quyết định luật. Prompt/corpus không được thay cho quyền truy cập; phòng ngừa prompt injection, source laundering, link rot, license, leakage, trộn dữ liệu nhạy cảm. Giao quyền rõ ràng READ, DRAFT, EVAL, SUBMIT; EXECUTE/DEPLOY/WRITE_EXTERNAL đòi Owner explicit theo từng nghiệp vụ.

PC offline: chat tiếp tục, lưu candidate GitHub nếu có quyền/kết nối, CI/reviewer/acceptance theo gate; Local Brain mirror status NOT_WRITTEN không phải blocker cho GitHub-first learning. Nếu GitHub down, chat-only là NOT YET DURABLY RECORDED; không hứa phục hồi.

## 9. Dòng công việc và governance; không tự bật máy học

Class F (có thể): mọi sửa đổi định nghĩa mục tiêu và thẩm quyền của accepted Master Blueprint, luật nền, source of truth, freeze/reopen.
Class S: thay task/handoff routing, core learning/eval interfaces, knowledge schema; independent review bắt buộc theo scope.
Class D/O: lesson, curriculum cho lĩnh vực cụ thể, bounded knowledge/evaluation candidate.
Các đề xuất PR #333/#335/#343 phải được review riêng, không dùng sự có mặt của chúng để khẳng định EIA-V2 đã hoạt động. Không đưa architecture mới vào law bằng “ẩn ý” hoặc đổi active task sang proposal. Owner acceptance vẫn là gate quan trọng.

**Cách triển khai rủi ro thấp:** tách kiến trúc ý tưởng V2 (có thể Class F nếu được chọn thay Master Blueprint) khỏi các thí nghiệm bổ sung dưới Foundation V1 (Class D/O, và S nếu đụng schemas/pipeline). Chỉ đề nghị mở Foundation nếu thí nghiệm đo cho thấy defect cấu trúc thật và Owner xác nhận điều kiện reopen phù hợp.

## 10. Kế hoạch tiến hóa từng vòng (không triển khai ồ ạt)

- P0 — Baseline & truth hygiene: inventory accepted vs candidate, sửa route A172/A173 theo Class S, đối soát A173–A207, xác lập benchmark mới và tập câu hỏi riêng, kiểm tra independence/contamination. Đầu ra: baseline A0/A1, báo chênh lệch, chi phí.
- P1 — One deep-learning pilot: chọn 1 trong 3 domain (ưu tiên Phật học theo Owner); dùng kiến trúc hiện có để học 1 chủ đề khó thật; G1–G3 và đánh giá G4 thí điểm. Đầu ra: source-bound case, known counterexample, held-out transfer, reviewer report, provenance.
- P2 — Replicate across domains: lặp với toán và kinh tế; kiểm kỹ năng chuyên môn riêng và chuyển giao liên lĩnh vực, đọc lại bằng chat khác; thống kê so sánh A1 vs A2. Đầu ra: scorecards không tô hồng.
- P3 — Only evidence-driven software: nếu pilot cho lợi ích rõ mà thực hiện tay tốn chi phí, implement phần nhỏ nhất theo Class S/D; reuse PR #333/#335 chỉ sau review. Đầu ra: bounded program, test negatives, security, rollback, CI, reviewer.
- P4 — Controlled expert execution: Owner chỉ đạo thực chiến cụ thể, phạm vi dữ liệu/quyền/lợi ích rõ; đánh giá chất lượng/chi phí/hậu quả. Không dùng P1–P3 làm giấy phép auto publish, auto trade, auto coding vào main, auto operate PC.

Thước đo vận hành cần có:
1) 100% tuyên bố “accepted” có protected-main provenance hợp lệ;
2) 0 self-VERIFIED/autonomous merge;
3) independent zero-chat retrieval đúng state/checkpoint/corrections/open audits;
4) số điểm và độ ổn định trên unseen transfer/baseline control;
5) tỷ lệ câu trả lời dẫn nguồn sai, bịa, che giấu bất định và critical errors;
6) cost per useful solved problem, không chạy theo tokens/PR count;
7) tỉ lệ phản biện dẫn đến sửa mô hình/chọn giải pháp tốt hơn, không đếm số critic đơn thuần.

## 11. Mười rủi ro cần Grok/Claude phá

R1. Vẽ lại Foundation bằng thuật ngữ hào nhoáng, tăng chi phí mà không tăng năng lực.
R2. Source snapshots đúng hash nhưng nội dung bịa/lệch bản dịch hoặc đã bị cấy prompt injection.
R3. Dùng retrieval làm gian lận benchmark; câu hỏi held-out bị lộ qua chat/PR/corpus.
R4. Cùng một model mang hai “ghế” giả vờ độc lập; reviewer gật đầu vì cùng giả định.
R5. Reward hacking: hệ học cách vượt rubric thay vì cải thiện giải quyết vấn đề.
R6. Tri thức đúng bị “skill graph” tóm sai, causal overclaim và lỗi supersession lan truyền.
R7. Chat mới tái dựng current/next khác nhau vì task pointer stale hoặc draft lấn main.
R8. Owner phải quản lý quá nhiều gate, chi phí phản biện và pháp lý hơn lợi ích.
R9. System claims vượt trội GPT chỉ do nhiều context/token/công cụ hơn, không công bằng.
R10. Đổi model/provider khiến kết quả benchmark và phương pháp cũ suy thoái; không phát hiện.

## 12. Câu hỏi chính sách cần phản biện trước khi viết mã

- Liệu “V2” nên là **north-star domain architecture** nằm dưới Master Blueprint V1 chứ chưa cần Master Blueprint V2? Nếu phải sửa Foundation, chỉ ra điều kiện reopen nào hiện thỏa và chứng cứ.
- Dùng knowledge atoms/hubs hiện có đã đủ biểu diễn skill/ability outcomes chưa? Nếu thiếu, chỉ ra trường tối thiểu và migration an toàn.
- Dữ liệu kiểm tra held-out lưu ở đâu cho đúng bảo mật và quyền của evaluator mà không thành second canonical brain?
- Ai thật sự đủ độc lập và đủ chuyên môn để chấm hiểu sâu Phật học, toán, kinh tế? Khi bất đồng thì xử lý sao?
- Làm sao lượng hóa tăng năng lực tại cùng model, cùng retrieval/tools/budget và kiểm tra độ bền khi model đổi?
- Bao nhiêu bài pilot/bao nhiêu cải thiện đủ để quyết định đầu tư tiếp? Thiết kế stop-loss, rollback và retirement.
- Đâu là kiến trúc **tối giản hơn** mà vẫn đạt mục tiêu Owner? Chủ động khuyến nghị REJECT/REDESIGN nếu không đáng.

## 13. Acceptance criteria cho riêng đề án (chưa phải accepted)

A. Owner vision được ghi đúng với ranh giới “học bây giờ, thực chiến sau”.
B. Bản thiết kế không tạo nguồn thẩm quyền thứ hai hoặc cho phép self-acceptance.
C. Có model thực nghiệm tách lưu giữ kiến thức khỏi cải thiện kết quả.
D. Có đánh giá độc lập, held-out, chống leakage, cost-normalized, domain-specific.
E. Có đường offline-PC và zero-chat recovery, không bị PC chặn học.
F. Có phân loại F/S/D/O và migration/rollback nếu sau này triển khai.
G. 2 independent fresh critics (Grok, Claude) trả bản nhận xét khác nhau, không đọc nhau; mọi critical/high/medium finding phải được Owner xử lý/sửa và rereview.
H. Chỉ Owner quyết định có chấp nhận North Star mới hoặc nâng nó lên thẩm quyền Master Blueprint; một PR tài liệu hay CI PASS không làm việc đó.

**CURRENT DECISION REQUEST:** critique first, not implement yet. Do not merge proposal or reopen Foundation until evidence-based Owner gate.
