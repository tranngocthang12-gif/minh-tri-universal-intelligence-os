# Kiến trúc MINH TRÍ hiện hành — 2026-10-02

**Status:** CURRENT ARCHITECTURE RECORD / OWNER-DIRECTED / IMPLEMENTATION PARTLY UNTESTED  
**Canonical branch:** `main`  
**Fresh-head rule:** mọi ghế phải đọc live `main` trước công việc quan trọng; không đóng đinh SHA cũ thành luật.  
**Previous current-state document:** `ARCHITECTURE_NOW_20261001.md` — HISTORICAL SNAPSHOT, giữ nguyên lịch sử.

## 1. Authority

```text
OWNER
→ STABLE LAW / GOVERNANCE
→ PROJECT_STATE.json
→ CURRENT ARCHITECTURE RECORD
→ APPROVED GITHUB RECORDS
→ DOMAIN SOURCES / LESSONS / HISTORY
→ CHAT MEMORY
```

- Owner quyết mục tiêu, quyền, gate và thay đổi luật.
- GitHub là bộ nhớ bền trước chat cho mọi quyết định/trạng thái quan trọng.
- Chat không phải canonical memory.
- File mới hơn không tự thắng; trạng thái CURRENT/CANDIDATE/HISTORICAL và authority chain quyết định.
- Không biết thì nói KHÔNG BIẾT; không tự VERIFIED.

## 2. One brain, replaceable seats

- Não tổ chức = luật + current state + repo + sổ Owner.
- GPT/Claude/Gemini/Grok/tool chỉ là ghế/dụng cụ thay được.
- Mỗi ghế phải bootstrap lại vai từ GitHub/current state trước việc quan trọng.
- Không cần chat cũ để tiếp tục nếu handoff/current state đầy đủ.

## 3. Work-arrival bootstrap

Trước công việc quan trọng, ghế phải xác định:
1. project;
2. Owner muốn gì;
3. vai hiện tại;
4. active task;
5. mode: READ-ONLY / WRITE-AUTHORIZED / SECURITY-HOLD;
6. source of truth;
7. required gates;
8. known / unknown.

Sau đó fresh-read tài liệu authority liên quan.

## 4. Synchronization contract

```text
PULL
→ CHECK
→ WORK
→ SELF-CRITIQUE / VALIDATE
→ HANDOFF
→ OWNER/GOVERNANCE GATE
→ PROMOTE
→ NEXT SEAT FRESH-READS
```

Không dùng auto-write hai chiều không kiểm soát giữa chat, GitHub, Library và local brain.

### Current transport capability
- GitHub → ChatGPT seat: AVAILABLE.
- ChatGPT seat → GitHub: AVAILABLE khi được Owner/permission cho phép.
- Project/Library sources → seat: AVAILABLE.
- Project Instructions → chats in Project: AVAILABLE.
- Local brain read stack is IMPLEMENTED: `BrainReader → BrainTransport → BrainHTTP → dedicated MCP`.
- Dedicated MCP runtime on the Owner PC is PROVEN and exposes exactly `brain.verify` + `brain.recovery_packet`; mutation is not exposed.
- ChatGPT → dedicated local MCP is CONNECTED through OpenAI Secure MCP Tunnel for the current seat. Live connector discovery exposes exactly `brain.verify` + `brain.recovery_packet`, and both tools successfully read the fixed Owner-PC brain.
- Secure MCP Tunnel transport is READY and connector discovery is PROVEN for the current seat. Fresh-seat recovery remains a separate promotion gate before `end_to_end_seat_brain_transport` may become true.
- Desktop Commander is a maintenance/break-glass plane with broader machine authority; it must not be treated as the canonical read-only brain transport.
- seat → local `brain/` durable mutation: NOT CONNECTED / BLOCKED.

## 5. Runtime planes and trust boundaries

### 5.1 Authority plane
```text
OWNER
→ STABLE LAW / GOVERNANCE
→ PROJECT_STATE
→ CURRENT ARCHITECTURE
→ APPROVED GITHUB RECORDS
```
This plane decides what is authoritative; it is not a runtime data transport.

### 5.2 Brain read plane
```text
ChatGPT seat
→ Secure MCP Tunnel / supported remote MCP path
→ dedicated MCP
→ BrainReader
→ fixed local brain/
```
Allowed surface: exactly `brain.verify` and `brain.recovery_packet`.
No shell, arbitrary filesystem, caller-selected brain path, ledger mutation, publication, spending, or deletion.

### 5.3 Brain write plane
```text
explicit write-authorized workflow
→ Owner gate
→ Ledger.apply / repair boundary
→ local brain/
```
The write plane is separate from the read plane. It must never be reachable through the dedicated read-only MCP connector.

### 5.4 Maintenance / break-glass plane
Desktop Commander belongs only to maintenance/break-glass operations. It can have broader machine authority for installation, diagnosis, runtime repair, or explicit Owner-authorized maintenance. It is NOT evidence that the canonical read-only connector is connected.

Invariant: Desktop Commander success alone must never set `local_brain_connected=true`, `chatgpt_to_owner_pc_brain_connector=CONNECTED_READONLY`, or `end_to_end_seat_brain_transport=true`.

### 5.5 Witness plane
```text
verified local ledger head
→ anchor
→ external witness publication
→ canonical read-back
→ historical-prefix comparison
```
Current proof level is process-separated only. It does not prove full-device-compromise independence.

### 5.6 Recovery-proof plane
- zero-chat process harness: PASS;
- dedicated MCP local runtime: PASS;
- first external anchor read-back: PASS;
- current ChatGPT seat over the canonical read-only connector: PASS;
- fresh ChatGPT seat over the same connector: PENDING;
- therefore end-to-end seat transport remains false.

### 5.7 Promotion invariants
A state promotion is valid only when its prerequisites are proven:
1. `local_brain_connected=true` records a proven connector capability; current reachability is tracked separately under `current_runtime_liveness`.
2. `end_to_end_seat_brain_transport=true` requires the discovered toolset to remain exactly the two read-only brain tools and a fresh-seat recovery PASS.
3. Desktop Commander evidence cannot satisfy either promotion gate.

### 5.8 Runtime evidence versus liveness
Canonical runtime state uses two non-interchangeable layers:
- `last_proven_runtime_evidence`: durable observations that were actually witnessed and must not be erased merely because a PC, tunnel, or connector later goes offline;
- `current_runtime_liveness`: the latest reachability observation only, with values such as `UP`, `DOWN`, `UNKNOWN`, or `TRANSIENT`.

A one-time live check is not persistence proof. CI success is not deployment proof. An implemented design is not runtime proof. No `LIVE_CURRENT`-style canonical claim is allowed without continuous heartbeat evidence.

For liveness, `current_runtime_liveness` is the sole authoritative field. Older fields whose names contain `current`, `live`, or `active` are retained only for backward-compatible historical evidence and must not override the liveness layer.

At the 2026-10-02 21:35 +07 observation, Desktop Commander was offline and the Local Brain connector reported that tunnel-client had not been seen for more than 300 seconds. Therefore tunnel/connector liveness is DOWN, Owner-PC liveness itself is UNKNOWN, and the earlier PASS evidence remains historical proof rather than current liveness.

### 5.9 Canonical research gate
The autonomy runtime may not accept a caller-provided string or CLI flag to open research. It derives the gate from canonical `docs/PROJECT_STATE.json` and opens only when all three are true simultaneously:
- `fresh_chat_seat_validation == PASS`;
- `end_to_end_seat_brain_transport == true`;
- `research_adapter_gate == OPEN_AFTER_FRESH_SEAT_PASS`.

Unreadable or malformed canonical state fails closed. Autonomy remains proposal-only with `write_capability=false`, no automatic VERIFIED promotion, and no automatic trial activation.

### 5.10 Independent witness gate
The witness adapter contract already defines the interface boundary, but full-device-independent witness promotion remains blocked until authority, provider, and credentials are genuinely independent from both GitHub authority and the Owner PC. Same-authority GitHub evidence remains useful process-separated evidence only.

## 6. Learning and critique

Tier-1 đã có:
- SOURCE → EVIDENCE → CLAIM/HYPOTHESIS;
- PREDICTION → FREEZE → RESOLUTION;
- CRITIC;
- ADJUDICATOR;
- LESSON CANDIDATE;
- TRIAL_RULE gate;
- không có automatic VERIFIED.

Chưa có runtime tự trị:
- autonomous topic discovery;
- automatic Internet ingestion;
- mandatory automatic critic after every chat claim;
- background learning;
- meta-learning;
- automatic procedure promotion;
- direct durable write to local brain.

## 7. Security state

Security remains first-order.

Current security status:
- CLOSED P0: caller-controlled Owner config authority selector is blocked.
- CLOSED P0: direct Python `Ledger.apply` and snapshot repair authenticate inside the mutation boundary.
- CLOSED P0 governance: `main` requires PRs and the GitHub Actions `test` check is now required with strict/up-to-date enforcement; no bypass actors are configured.
- PARTIAL: first real external anchor is published and read-back against the Owner-PC ledger passes, but the present witness proves process separation only, not full-device-compromise independence.
- OPEN: a compromise of the Owner PC can still reach the current GitHub witness authority; therefore no state may claim fully independent witness protection yet.
- OPEN: Owner Gate is not real-person identity verification; shared-secret trust remains local.
- OPEN: provider IDs are declared identities, not proof of independent actors.
- OPEN: autonomous mutation remains blocked until the remaining trust chain is proven.

Until those are hardened, autonomous write/publish/spend/delete remains blocked unless Owner explicitly authorizes the specific action.

## 8. Current operational rules

- GitHub first for material project memory.
- Fresh-read live authority before important work.
- Preserve history; mark superseded material instead of rewriting history as if it never existed.
- Tool/version snapshots are not stable law.
- Owner can skip a process step; seat states one risk sentence and continues.
- Publication, spending, destructive changes, rights uncertainty and security-sensitive changes remain gated.
- Every material task leaves a handoff.

## 9. Current focus

Current workstream: Secure MCP Tunnel + ChatGPT connector discovery are now PASS for the current seat; next is fresh-seat recovery over the canonical read-only connector. Research Adapter remains blocked until the fresh-seat gate passes.

Production/domain work may proceed only under current Owner instruction and relevant gates.

## 10. Required bootstrap files

A seat recovering from zero chat memory should read, in order:
1. `docs/PROJECT_STATE.json`
2. `docs/LAW_INDEX_20261002.md`
3. this file
4. `docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md`
5. task/domain-specific source

That is the minimum GitHub recovery route. The merged zero-chat test proves a local Python recovery contract only; it does not prove end-to-end ChatGPT-to-local-brain transport.
