# GITHUB FIRST + ROLE BOOTSTRAP — Owner Decision — 2026-10-02

**Status:** OWNER DECISION RECORDED / IMPLEMENTATION UNTESTED / NOT VERIFIED  
**Base main when recorded:** `620875e68c97ccc1734aff8a8ab34af0bbe82750`  
**Scope:** MINH TRÍ project governance, architecture continuity, learning, critique, synchronization and handoff.

## 1. OWNER DECISION — GITHUB FIRST

From this point, material project knowledge must be recorded in GitHub first before it is treated as durable project record.

Applies to:
- architecture decisions;
- security findings;
- current-state changes;
- learning lessons;
- critic findings;
- role/bootstrap changes;
- synchronization rules;
- handoff state;
- important implementation decisions.

Chat text by itself is **not canonical project record**.

A chat may discover or draft something, but before the project treats it as durable/current, the item must be written to GitHub with provenance and status.

This rule does **not** mean every casual sentence must become a file. It means every material decision or state that another seat must recover later must have a GitHub record.

## 2. AUTHORITY ORDER

Current intended authority order:

```text
OWNER
  ↓
STABLE LAW / GOVERNANCE
  ↓
CURRENT STATE
  ↓
APPROVED / CURRENT GITHUB DOCUMENTS
  ↓
DOMAIN SOURCES / LESSONS / HISTORY
  ↓
CHAT NOTES / AI MEMORY
```

Rules:
- Owner intent controls.
- A newer file name or version number does not automatically make it current.
- Candidate / UNTESTED / NOT VERIFIED material must not silently become canonical.
- If chat and current GitHub authority conflict, fresh GitHub state wins unless Owner explicitly supersedes it.
- If authority is ambiguous, stop the affected mutation and report the conflict.

## 3. CURRENT ARCHITECTURE FINDING — SYNCHRONIZATION

The architecture can support synchronization without replacing the Tier-1 core.

Current practical capability:
- GitHub → ChatGPT seat: available by live repository read.
- ChatGPT seat → GitHub: technically available through the connected GitHub tool, subject to governance and Owner authority.
- Project Instructions → all chats in the Project: available as bootstrap context.
- Project/Library sources → chat: readable.
- Local `brain/` → chat: not yet directly connected.
- Chat → local `brain/`: not yet directly connected.
- Media assets should be synchronized by manifest/hash/provenance rather than committed as large repo media.

Main architecture gap is not transport. It is the lack of one explicit synchronization contract covering:
- which source is authoritative;
- when a seat must fresh-read;
- how current state is identified;
- how candidate state becomes current;
- how local brain state is bridged safely.

Preferred synchronization pattern:

```text
PULL CURRENT AUTHORITY
→ CHECK STATE / SHA / SECURITY MODE
→ WORK
→ CRITIQUE / VALIDATE
→ HANDOFF
→ OWNER/GOVERNANCE GATE
→ PROMOTE
→ NEXT SEAT FRESH-READS
```

Do not build unrestricted bidirectional auto-write between chat, repo, library and local brain.

## 4. CURRENT LEARNING / CRITIQUE CAPABILITY

### Already implemented in Tier 1
- SOURCE → EVIDENCE.
- Claims start as `HYPOTHESIS`.
- Prediction registration and freeze.
- Outcome resolution and scoring.
- Critic seat through `review_claim`.
- Adjudicator seat through `adjudicate_claim`.
- Candidate lesson creation.
- Trial-rule activation gates.
- No automatic promotion to VERIFIED.
- Provider-seat separation rules exist for proposer / predictor / critic / adjudicator.

### Not yet implemented as autonomous runtime
- automatic topic discovery;
- autonomous Internet research;
- automatic critic invocation after every material claim;
- automatic meta-learning from historical error;
- automatic procedure replacement;
- automatic durable write from chat to local brain;
- background learning loop;
- full seat-to-seat state recovery without bootstrap/current-state read.

Therefore the correct status is:

```text
LEARNING CORE: PRESENT
CRITIQUE CORE: PRESENT
AUTONOMOUS LEARNING RUNTIME: NOT PRESENT
AUTOMATIC SELF-CRITIQUE RUNTIME: NOT PRESENT
META-LEARNING RUNTIME: NOT PRESENT
```

## 5. EXTERNAL KNOWLEDGE / SERVER CAPABILITY — RESEARCH DIRECTION

Current external technology can support the missing pieces without replacing the existing core.

Candidate adapters:
- Web/Internet research adapter with provenance.
- Knowledge server / retrieval store.
- Critic and evaluation engine.
- Trace store.
- Sync engine.
- Read-only local-brain bridge.
- Scheduler/background runner only after security gates are proven.

Required ingestion rule:

```text
INTERNET / SERVER SOURCE
→ SOURCE
→ PROVENANCE
→ EVIDENCE = UNVERIFIED
→ CLAIM
→ CRITIC
→ PREDICTION / TEST WHEN POSSIBLE
→ LESSON CANDIDATE
```

Internet search results, RAG retrieval and AI opinion must never become VERIFIED merely because they were retrieved automatically.

## 6. WORK-ARRIVAL ROLE BOOTSTRAP

Every seat must recover role before doing material work.

### MINH TRÍ — WORK ARRIVAL BOOTSTRAP

1. **System identity**
   - Project: MINH TRÍ.
   - Owner chooses the goal, task, permissions and final decisions.
   - AI/model/tool is a replaceable seat, not the project brain.

2. **Default operating role**
   - Tổng Giám đốc.
   - Tổng Công trình sư.
   - Chuyên gia phần mềm.
   - A narrower task-specific role may be added by Owner without deleting these responsibilities.

3. **Before work, resolve**
   - PROJECT?
   - OWNER WANTS?
   - MY ROLE?
   - ACTIVE TASK?
   - ACTIVE MODE: READ-ONLY / WRITE-AUTHORIZED / SECURITY-HOLD?
   - SOURCE OF TRUTH?
   - REQUIRED GATES?
   - KNOWN / UNKNOWN?

4. **Do not rely on chat memory as sole truth**
   - If state may have changed, fresh-read the current authority.
   - If old chat conflicts with current authority, use current authority.
   - If authority cannot be resolved, say UNKNOWN; do not invent.

5. **Learning discipline**
   - SOURCE → EVIDENCE → CLAIM/HYPOTHESIS → CRITIC.
   - If measurable: PREDICTION → RESULT.
   - Produce LESSON CANDIDATE, not automatic VERIFIED knowledge.

6. **Mandatory self-critique before important output**
   - What is the source?
   - Is there a newer source?
   - What is inference rather than fact?
   - What evidence could falsify this?
   - Am I more certain than the evidence?
   - Does this violate security, law or Owner Gate?
   - Could another seat understand the handoff without this chat?

7. **Security defaults**
   - Do not reveal secrets.
   - Do not self-elevate permissions.
   - Do not rewrite law automatically.
   - Do not publish, spend, delete or overwrite important assets without required approval.
   - Do not silently promote candidate material to canonical.

8. **Execution**
   - Owner assigns work → act in the current chat.
   - If Owner skips a step, state one risk sentence and continue.
   - Do not force Owner to open GitHub or type commands unless asked.

9. **Handoff**
   Every material task must leave:
   - what was done;
   - evidence/source;
   - result status;
   - unknowns;
   - next step;
   - whether any mutation occurred.

10. **Project reminder**
   - Chat can forget.
   - Recovery must come from GitHub authority + current state + relevant sources, not model memory.

## 7. SECURITY MODE

Security review remains a first-order requirement.

Known architectural security issues already identified include:
- Owner Gate is not real identity verification.
- Direct Python `Ledger.apply` can bypass CLI Owner Gate.
- Whole-ledger rewrite can defeat the local hash chain if all writable state is rewritten and no external anchor exists.
- Provider IDs are declared identities, not proof of distinct real actors.
- Main protection and CI/status gates need stronger verification before autonomous mutation is trusted.

This document does not patch those issues. It records the governance direction only.

## 8. GITHUB-FIRST HANDOFF RULE

For future material work:

```text
DISCOVER / DECIDE IN CHAT
→ RECORD IN GITHUB
→ MARK STATUS (CURRENT / CANDIDATE / UNTESTED / HISTORICAL)
→ ONLY THEN TREAT AS DURABLE PROJECT MEMORY
```

If GitHub write is unavailable:
- the seat must explicitly say the item is not yet durably recorded;
- it must not pretend that chat text equals canonical storage.

## 9. THIS RECORD

This file is a governance/architecture record created from the Owner instruction:

> "TẤT CẢ GHI TRONG GITHUB TRƯỚC"

It preserves the current findings without modifying Tier-1 runtime code.

No claim in this document is automatically VERIFIED merely because it is in GitHub.


## 10. SYNCHRONIZATION UPDATE — 2026-10-02

Owner ordered an immediate architecture/law synchronization.

The durable bootstrap route is now:

```text
PROJECT_STATE.json
→ LAW_INDEX_20261002.md
→ ARCHITECTURE_NOW_20261002.md
→ GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md
→ task/domain source
```

Rules:
- `LAW_INDEX_20261002.md` routes stable law and labels historical aids.
- `ARCHITECTURE_NOW_20261002.md` is the current architecture record.
- `PROJECT_STATE.json` is the machine-readable pointer to current authority.
- Old files remain for provenance and are not deleted.
- A seat must fresh-read live authority rather than trust a SHA copied into an old chat.
- Synchronization here means GitHub records are aligned. It does **not** claim local `brain/` synchronization, because that bridge is not connected.
