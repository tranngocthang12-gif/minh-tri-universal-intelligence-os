# MINH TRÍ — BOOTSTRAP / READ BEFORE WORK

**Mục đích:** đường vào duy nhất cho một chat, AI, agent hoặc người mới trước khi nhận định trạng thái hay xây MINH TRÍ.

## A. Đọc theo đúng thứ tự

1. `PROJECT_LAW.md` — quyền, bất biến, kiến trúc công việc.
2. `docs/PROJECT_STATE.json` — trạng thái hiện hành, không suy từ lịch sử.
3. `docs/PHILOSOPHY.md` — mục tiêu và biên tư tưởng/Phật học.
4. `docs/ARCHITECTURE.md` — contract Tầng 1.
5. `docs/CORE_PROTECTION_CONTRACT_V0.1.md`.
6. `docs/UNIVERSAL_BRAIN_ARCHITECTURE_V0.1.md`.
7. `docs/AI_COMMONS_ARCHITECTURE_V0.1.md`.
8. `docs/ROADMAP.md`.
9. Code/tests/PR liên quan tới task hiện tại.
10. Task Packet + evidence/domain docs được phép.

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

Trước handoff hoặc kết luận:

1. ghi nguồn;
2. ghi unknowns;
3. ghi scope;
4. ghi cách kiểm;
5. phân biệt structural / semantic / real effectiveness;
6. persist durable delta nếu Owner đã giao xây/sửa;
7. không tự biến chat memory thành project law.

**Core rule:** `MODEL MEMORY != PROJECT MEMORY. READ BEFORE RECONSTRUCT. READ BEFORE WORK.`
