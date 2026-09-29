# MINH TRÍ — BOOTSTRAP / READ BEFORE WORK

**Mục đích:** đường vào duy nhất cho một chat, AI, agent hoặc người mới trước khi nhận định trạng thái hay xây MINH TRÍ.

## A. Đọc theo đúng thứ tự

1. `PROJECT_LAW.md` — quyền, bất biến, kiến trúc công việc.
2. `docs/PROJECT_STATE.json` — trạng thái hiện hành, không suy từ lịch sử.
3. `docs/PHILOSOPHY.md` — mục tiêu và biên tư tưởng/Phật học.
4. `docs/ARCHITECTURE.md` — contract Tầng 1.
5. `docs/CORE_PROTECTION_CONTRACT_V0.1.md`.
6. `docs/UNIVERSAL_BRAIN_ARCHITECTURE_V0.2_CANDIDATE.md` — kiến trúc phục dựng hiện hành; v0.1 chỉ dùng như lịch sử khi cần đối chiếu.
7. `docs/ARCHITECTURE_MEMORY_AND_CONTINUITY_V0.1.md` — bất biến gốc, bốn ghế AI, replacement và handoff.
8. `docs/AI_COMMONS_ARCHITECTURE_V0.1.md`.
9. `docs/ARENA_SCHEMA_MIGRATION_V0.1.md`.
10. `docs/CANONICAL_TASK_HANDOFF_V0.1.md`.
11. `docs/EPISTEMIC_STATE_LEARNING_MATURITY_V0.1.md`.
12. `docs/GOAL_DECOMPOSITION_BOTTLENECK_GOVERNOR_V0.1.md`.
13. `docs/ROADMAP.md`.
14. Code/tests/PR liên quan tới task hiện tại.
15. Exact Task Packet + allowed evidence.
16. **Latest durable checkpoint/handoff receipt** của task; nếu task đã có lịch sử mà không tìm thấy handoff/checkpoint hợp lệ → `HOLD / MISSING_HANDOFF`.

**Không được đảo thành:** nhớ từ chat cũ → đoán trạng thái → xây.

## B. Phân loại mọi thứ trước khi dùng

Mọi thông tin phải được nhận dạng là một trong:

- `OWNER_DIRECTIVE`
- `PROJECT_LAW`
- `CURRENT_STATE`
- `IMPLEMENTED_CODE`
- `TESTED_STRUCTURE`
- `SEMANTIC_EVIDENCE`
- `REAL_OUTCOME_EVIDENCE`
- `CANDIDATE / HYPOTHESIS`
- `HISTORICAL`

Không nâng hạng bằng cảm giác hoặc đồng thuận AI.

## C. Khi Owner nói

- **“bàn”** → chỉ phân tích/phản biện; không mutation/PR.
- **“xây” / “sửa”** → tạo output reviewable/testable; không merge/release/chi tiền/mở action nếu chưa được giao.
- Owner directive mới hơn có thể thay hướng, nhưng thay đổi durable phải được ghi lại theo luật nếu cần kế tục.

## D. Receipt cho AI Commons

Task Packet phải cho participant thấy:

- exact `brain_revision`;
- `brain_fingerprint`;
- `architecture_law_sha256`;
- `bootstrap_sha256`;
- `runtime_state_head`;
- `task_fingerprint`;
- scope / permissions / risk / allowed evidence.

Trước proposal/critique/adjudication, participant phải nộp acknowledgement receipt khớp các mốc trên. Receipt = xác nhận nhận đúng gói, **không phải bằng chứng hiểu đúng**.

## E. Kết thúc một phiên/task

Không được báo hoàn tất rồi mới tái dựng bàn giao. Thứ tự bắt buộc:

1. ghi nguồn;
2. ghi unknowns;
3. ghi scope;
4. ghi cách kiểm;
5. phân biệt structural / semantic / real effectiveness;
6. persist durable delta nếu Owner đã giao xây/sửa;
7. chạy test/validation phù hợp;
8. cập nhật checkpoint với việc đã chấp nhận + exact next action;
9. tạo durable handoff/completion receipt có fingerprint;
10. replay/verify ledger sau khi ghi;
11. chỉ sau đó mới báo Owner;
12. không tự biến chat memory thành project law.

Chat/AI nhận việc tiếp theo phải đọc và ACK exact latest handoff trước continuation.

**Core rule:** `MODEL MEMORY != PROJECT MEMORY. READ BEFORE RECONSTRUCT. READ BEFORE WORK.`
