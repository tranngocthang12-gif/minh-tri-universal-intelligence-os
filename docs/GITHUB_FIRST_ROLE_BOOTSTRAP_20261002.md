# GITHUB FIRST + ROLE BOOTSTRAP — Owner Decision — 2026-10-02

**Status:** STABLE OWNER BOOTSTRAP LAW / HISTORICAL IMPLEMENTATION SNAPSHOT BELOW / CURRENT CAPABILITY MUST BE READ FROM PROJECT_STATE + CURRENT ARCHITECTURE  
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
- Local `brain/` → chat: read-only connector capability has been implemented and historically runtime-proven; current reachability must come only from `PROJECT_STATE.current_runtime_liveness`.
- Chat → local `brain/`: write access remains a separate Owner-gated write plane; the read connector never implies write capability.
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

### Current runtime boundary

The original 2026-10-02 implementation snapshot below is historical. Current capability must be read from `PROJECT_STATE.json` and `ARCHITECTURE_NOW_20261003.md`.

Current high-level rule:
- learning, critique, meta-learning and Learning Assurance engines are implemented as bounded/proposal-only mechanisms;
- background autonomous runtime remains OFF;
- Research Adapter remains fail-closed until genuine fresh-seat validation;
- no automatic durable mutation, automatic VERIFIED or automatic trial activation.

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
   - OWNER GOAL → SOURCE / EXTERNAL CASE CAPITAL → PROVENANCE / RESEARCH TRACE → EVIDENCE.
   - CLAIM/HYPOTHESIS must retain alternative + falsifier + counterevidence when material.
   - Use adaptive deliberation metadata for risk/conflict/tool-dependent work; do not store private chain-of-thought.
   - For important critique: freeze target/evidence packet, record critic provenance, and use negative controls when useful.
   - If measurable: PREDICTION → OUTCOME / RESOLUTION.
   - Produce LESSON CANDIDATE → OWNER/GOVERNANCE GATE → bounded TRIAL RULE.
   - Revalidation and meta-learning remain proposal-only; context capsules are context only, never canonical truth.
   - Never automatic VERIFIED.

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

Historical security findings and their current classification:
- OPEN/PARTIAL: Owner Gate is shared-secret authorization, not proof of a real human identity.
- CLOSED P0: direct Python `Ledger.apply` now authenticates inside the mutation boundary; the old CLI-bypass finding is historical.
- PARTIAL: whole-ledger rewrite risk is mitigated by external anchors/history checks, but the current witness is not full-device independent.
- OPEN/PARTIAL: declared provider IDs and same-provider critic runs are not proof of independent actors.
- CLOSED governance baseline: main PR + strict required `test` check + no ruleset bypass actors are enforced; additional reviewer/CODEOWNER hardening remains optional/open.

Current status must be read from `PROJECT_STATE.json` and the current architecture, not inferred from this historical bootstrap section.

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

The durable bootstrap route is resolved dynamically from `PROJECT_STATE.json`. As of 2026-10-03:

```text
PROJECT_STATE.json
→ LAW_INDEX_20261003.md
→ ARCHITECTURE_NOW_20261003.md
→ GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md
→ task/domain source
```

Rules:
- `PROJECT_STATE.json` points to the current Law Index and architecture; never infer "current" from the date embedded in this bootstrap file.
- historical Law Index / architecture files remain provenance only once superseded.
- `PROJECT_STATE.json` is the machine-readable pointer to current authority.
- Old files remain for provenance and are not deleted.
- A seat must fresh-read live authority rather than trust a SHA copied into an old chat.
- Synchronization means authority records agree. Current local-brain reachability must be proved by fresh connector observation; historical bridge/deployment evidence is not current-liveness proof.


## 11. CURRENT-STATE ROUTING CLARIFICATION — 2026-10-04

This bootstrap contains historical implementation snapshots by design. For all changing facts — runtime liveness, lease activity, active learning tracks, Candidate status, open gates — read `docs/PROJECT_STATE.json` first and treat this file only as stable governance/bootstrap guidance.

A capability historically proven reachable does not mean it is currently reachable. An unexpired authorization timestamp does not prove its in-memory runtime process still exists.

## 11. MANDATORY UNIVERSAL LEARNING BOOTSTRAP — Owner law 2026-10-04

For every current or future learning track, material work requires this live canonical bootstrap order:

1. `docs/PROJECT_STATE.json`;
2. the current Law Index routed by PROJECT_STATE;
3. `docs/LAW_UNIVERSAL_LEARNING_CONTINUITY_20261004.md`;
4. the current Architecture routed by PROJECT_STATE;
5. this role bootstrap;
6. the active learning checkpoint/plan for the relevant track;
7. task/domain sources.

Every material checkpoint must be durably recorded in GitHub with learned/corrected content, evidence/status, CURRENT, NEXT, OPEN AUDITS/UNKNOWNS and provenance. Chat memory is not a durable substitute. Recorded does not mean VERIFIED. If the durable write path is blocked, state NOT YET DURABLY RECORDED and continue only the independent work that remains safe.

The Buddhist-thought continuity route is `docs/learning/BUDDHIST_THOUGHT_CHECKPOINT_20261004.md`; the preserved handoff is A30–A33 completed → NEXT A34.

