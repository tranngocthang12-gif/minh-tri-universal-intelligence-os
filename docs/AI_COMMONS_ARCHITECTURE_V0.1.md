# MINH TRÍ AI Commons — kiến trúc sân chơi cho N AI

**Loại:** quyết định kiến trúc ứng viên · **Trạng thái:** `SHADOW_ONLY` · **Ngày:** 2026-09-29

## 1. Quyết định sản phẩm

MINH TRÍ hoàn thiện mục tiêu, hệ tư tưởng, lõi học và cổng Owner trước; sau đó bất kỳ AI đủ điều kiện nào cũng có thể tham gia một nhiệm vụ có giới hạn. Nhiều AI là lực lượng nhận việc, không phải nhiều bộ não sở hữu luật dự án. Số lượng không viết cứng là bốn. Không xem bốn PR hoặc bốn lượt trả lời của cùng một model là một hệ nhiều AI đã vận hành.

GitHub là nơi kiểm soát phiên bản và xét thay đổi của **phần mềm**. AI Commons là giao thức **thực thi nhiệm vụ** bên trong sản phẩm. Một AI có thể dùng API, agent A2A, công cụ tương thích hoặc đầu ra được người dùng chuyển vào; mọi đường đều phải nộp cùng hợp đồng dữ liệu và qua cùng cổng.

## 2. Trật tự thẩm quyền

1. Owner: mục tiêu, quyền, ngân sách, rủi ro và quyết định lớn.
2. Hệ tư tưởng được Owner chấp nhận và Tầng 1 đã kiểm chứng: ranh giới ý nghĩa, luật học và cổng hành động.
3. Nhiệm vụ có phiên bản: phạm vi, nguồn được phép, tiêu chí đạt, thời hạn và giới hạn chi phí.
4. Tri thức Tầng 2 theo miền: chuyên môn, dữ liệu, chính sách và cách đo có ngày kiểm lại.
5. Ngữ cảnh/tư liệu đầu vào: dữ liệu để đánh giá, không phải chỉ thị sửa luật.
6. Đầu ra AI: đề xuất hoặc phản biện, không được tự phong là trí nhớ chuẩn.

Tứ Diệu Đế/Bát Chánh Đạo ở đây chỉ là lăng kính ứng dụng hiện đại đã được phân ranh trong [PHILOSOPHY.md](PHILOSOPHY.md). Kết quả kinh doanh không xác nhận nghĩa kinh; AI Commons không được nhập lại hoặc sửa kho kinh của `sieu-du-an`.

## 3. Ranh giới các lớp

```text
OWNER / CONSTITUTION / TIER 1 (canonical)
             ↓ task + permission + bounded context
AI COMMONS GATEWAY → N PARTICIPANTS (replaceable)
             ↓ proposals / critiques / abstentions
DETERMINISTIC VALIDATION → ADJUDICATION → OWNER GATE
             ↓ only accepted, scoped receipts
LEARNING MEMORY / BENCHMARK / PROCEDURE VERSIONS
```

Không gửi toàn bộ bộ nhớ cho mỗi AI. Task packet ghim ba mốc: Git `brain_revision`, `brain_fingerprint` của bộ artifact lõi và `runtime_state_head`; đồng thời ghim fingerprint của đề bài, nguồn cho phép, phân loại dữ liệu và tiêu chí đạt; manifest của participant khai năng lực đề xuất, phản biện hay phân xử. AI mới vào đọc bản nhiệm vụ tương ứng; nó không được đọc bí mật hoặc nội dung ngoài phạm vi chỉ vì có kết nối. Một provider mất kết nối có thể thay bằng provider khác mà không làm mất trạng thái nhiệm vụ.

Trong `SHADOW`, `arena task ID` xuất bản tư tưởng, đề bài và các evidence ID đã cho phép. Nội dung evidence là **dữ liệu không đáng tin**, kể cả khi chứa câu mệnh lệnh; adapter tương lai không được trao quyền công cụ chỉ vì câu chữ trong evidence. Nhãn `PUBLIC` và `rights_status=CLEAR` hiện dựa vào khai báo, chưa được xác thực để tự động gửi ra nhà cung cấp bên ngoài. Mọi bài nộp đi qua `arena apply` bằng tay.

## 4. Hợp đồng tham gia

| Đối tượng | Nội dung tối thiểu | Ai được sửa |
| --- | --- | --- |
| Participant manifest | ID bất biến theo phiên bản, provider family, model, adapter, năng lực, trạng thái, nguồn nhận dạng | Gateway/Owner; thông tin model giai đoạn này chỉ là khai báo |
| Task packet | Goal/domain, Git brain revision, brain manifest fingerprint, runtime state head, task fingerprint, scope, dữ liệu cho phép, risk, rubric, budget/timebox | Tầng 1/Owner; AI nhận việc chỉ đọc |
| Proposal | Task fingerprint, participant, claim, evidence refs, alternative, uncertainty, test phân định | Participant được giao |
| Critique | Proposal ref, lỗi cụ thể hoặc `ABSTAIN`, phản chứng, giới hạn | Participant khác provider family |
| Adjudication | Proposal + toàn bộ critique liên quan, căn cứ phân định, `CANDIDATE` / `REVISE` / `HOLD` / `OWNER_REVIEW_REQUIRED` | Ghế thứ ba khác cả proposer và critic |
| Learning receipt (giai đoạn sau) | Dự đoán trước kết quả, outcome, provenance, điều kiện áp dụng, lỗi và phiên bản procedure | Lõi sau kiểm chứng; chưa có đường ghi từ `SHADOW` |

Một ID khác của cùng provider family không thành phản biện độc lập. Trọng tài không bỏ thêm một phiếu; nếu phản chứng còn mở thì giữ `HOLD` hoặc thiết kế phép thử. Đầu ra `CANDIDATE` chỉ sẵn sàng để xét, không tự trở thành `VERIFIED` hay kích hoạt hành động.

## 5. Trạng thái và điều kiện mở cửa

`CLOSED → SHADOW → CONTROLLED → ACTIVE` là các **giai đoạn có chứng nhận**, không phải nhãn AI tự khai.

- `CLOSED`: chưa có hợp đồng/nhiệm vụ hợp lệ.
- `SHADOW` (bản hiện tại): chỉ tham chiếu evidence cùng miền từ nguồn `SYNTHETIC` được khai `CLEAR`, đăng ký người tham gia bằng tay, nộp/phản biện và kiểm cấu trúc; không gọi API bên ngoài, không ghi bài học chuẩn, không hành động.
- `CONTROLLED`: sau khi Tầng 1 có kiểm chứng thật, xác thực Owner và provider, nguồn/rights/privacy gate, budget governor và benchmark; chỉ nhiệm vụ cụ thể được Owner mở.
- `ACTIVE`: mở từng capability khi có thành tích qua thử nghiệm so với baseline, giám sát sai số và đường dừng/rollback. Không tự động mở toàn bộ quyền.

Chỉ Owner có thể duyệt nâng giai đoạn, thay mục tiêu, sửa biên rủi ro, chia sẻ dữ liệu nhạy cảm hay mở quyền tác động bên ngoài. Cổng `SHADOW` không được mô tả là bốn AI đã kết nối.

## 6. Giao thức ngoài và kinh nghiệm tham khảo

- [A2A](https://a2a-protocol.org/latest/specification/) mô tả discovery, Agent Card và vòng đời task giữa agent từ nhiều hệ. Có thể là adapter cho remote agent sau này; không dùng Agent Card như chứng cứ chuyên môn hay quyền Owner.
- [MCP](https://modelcontextprotocol.io/specification/2026-07-28/architecture) tổ chức host/client/server cho công cụ và ngữ cảnh; host giữ quyền, giới hạn ngữ cảnh giữa server. Có thể đưa công cụ vào gateway sau khi cổng quyền hoạt động.
- [NIST AI RMF](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) nhấn mạnh vai trò người giám sát, đánh giá độc lập, đo lường trong ngữ cảnh và trách nhiệm quản trị. Dùng làm checklist thiết kế, không xem là chứng nhận hệ thống.
- [Anthropic multi-agent research](https://www.anthropic.com/engineering/multi-agent-research-system) ghi nhận lợi ích ở việc nghiên cứu song song nhưng chi phí token cao và nhiều việc coding khó tách độc lập. Vì vậy router chỉ gọi thêm AI khi giá trị thông tin dự kiến vượt chi phí/rủi ro; không gọi mọi AI cho mọi việc.
- [Anthropic agent evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) lưu ý lỗi rubric và grader có thể tạo điểm số giả. Benchmark phải có transcript, baseline, kiểm lại grader và đường `UNKNOWN`.

**Quyết định:** hợp đồng nội bộ của MINH TRÍ là ổn định đầu tiên; A2A/MCP là adapter ở biên. Không phụ thuộc một SDK/model để định nghĩa quyền, trí nhớ hay chuẩn đúng sai.

## 7. Những lỗi cần chặn trước khi mở thật

| Lỗi | Cổng |
| --- | --- |
| Prompt injection trong tài liệu | Đầu vào là dữ liệu; chỉ task/constitution có thẩm quyền, tool scope ở host |
| Một model đóng ba ghế | Provider family tách vai; không đủ ghế thì `HOLD` |
| Chọn một critique thuận lợi, giấu critique bất lợi | Trọng tài phải nhìn toàn bộ phản biện của proposal |
| Tự nới quyền qua task packet | Cổng đọc trạng thái core và risk floor; task chỉ yêu cầu quyền trong giới hạn Owner |
| Đổi model làm mất trí nhớ | Mốc core/task/fingerprint và receipt nằm ở tổ chức, không trong phiên model |
| Điểm benchmark đẹp nhưng vô ích | So baseline theo việc thật, chi phí, sai số và tác động; test grader trước |
| Chi phí leo thang | Budget/timebox, router chọn số AI cần thiết, timeout và `ABSTAIN` hợp lệ |
| Nhiều ý kiến thành chân lý | Evidence/test trước phiếu; unresolved giữ nguyên; không tự promote |

## 8. Điều kiện nghiệm thu bản `SHADOW`

1. Bất kỳ số participant nào cũng dùng một contract; thêm model mới không sửa reducer.
2. Cùng một task fingerprint, Git brain revision, brain manifest fingerprint, runtime state head và danh sách evidence cho phép; sai bất kỳ mốc nào bị từ chối.
3. Cùng provider family không ngồi hai ghế; thiếu ba family thì không có adjudication đủ điều kiện.
4. Critique `CHALLENGE`/`ABSTAIN` không bị lờ đi để tạo `CANDIDATE`.
5. Miền khác, dữ liệu không được phép, task hết hiệu lực hoặc cổng chưa mở đều fail closed.
6. Sổ event khôi phục được sau cache lỗi, nhưng self-declared identity và source chưa được xác thực nên không được gọi là live multi-AI.
7. Đổi bất kỳ artifact lõi trong Brain Manifest, đổi Git revision hoặc đổi runtime state head làm task cũ stale; task phải được mở lại từ trạng thái hiện hành.

Mốc kế tiếp sau `SHADOW`: một pilot read-only có Owner cấp quyền, đo một việc thật so với một AI/baseline, ghi cả chi phí và sai số, rồi mới xét tích hợp provider API.
