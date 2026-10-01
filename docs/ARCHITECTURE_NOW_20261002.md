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
- local `brain/` → seat: NOT CONNECTED.
- seat → local `brain/`: NOT CONNECTED.

## 5. Learning and critique

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

## 6. Security state

Security remains first-order.

Known open risks:
- Owner Gate is not real-person identity verification.
- caller-controlled owner config path is a trust-boundary risk.
- direct Python `Ledger.apply` bypasses CLI gate.
- full ledger rewrite is not detected without an external anchor.
- provider IDs are declared identities.
- current GitHub protection/CI is not yet sufficient for autonomous mutation.

Until those are hardened, autonomous write/publish/spend/delete remains blocked unless Owner explicitly authorizes the specific action.

## 7. Current operational rules

- GitHub first for material project memory.
- Fresh-read live authority before important work.
- Preserve history; mark superseded material instead of rewriting history as if it never existed.
- Tool/version snapshots are not stable law.
- Owner can skip a process step; seat states one risk sentence and continues.
- Publication, spending, destructive changes, rights uncertainty and security-sensitive changes remain gated.
- Every material task leaves a handoff.

## 8. Current focus

Current workstream: architecture/security/synchronization hardening before autonomous learning runtime.

Production/domain work may proceed only under current Owner instruction and relevant gates.

## 9. Required bootstrap files

A seat recovering from zero chat memory should read, in order:
1. `docs/PROJECT_STATE.json`
2. `docs/LAW_INDEX_20261002.md`
3. this file
4. `docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md`
5. task/domain-specific source

That is the minimum recovery route.
