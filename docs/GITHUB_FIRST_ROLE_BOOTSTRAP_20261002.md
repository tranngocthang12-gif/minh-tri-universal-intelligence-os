# GITHUB FIRST + ROLE BOOTSTRAP — Owner Decision — 2026-10-02

## VNEXT SINGLE BOOT ROOT — CURRENT MIGRATED ROUTE

For migrated Architecture vNext scope, the canonical boot entrypoint is `state/bootstrap.json`.

Current recovery route:
`state/bootstrap.json -> current Master Blueprint -> authoritative law precedence -> state/current.yaml -> state/tasks.yaml -> current architecture -> active task handoff -> task/domain sources`.

Older sections in this file that begin from PROJECT_STATE remain historical/unmigrated compatibility guidance only and cannot override migrated keys in `state/current.yaml` or `state/tasks.yaml`.


**Status:** STABLE OWNER BOOTSTRAP LAW / HISTORICAL IMPLEMENTATION SNAPSHOT BELOW / CURRENT MIGRATED AUTHORITY MUST BE READ FROM state/bootstrap.json -> Master Blueprint -> law -> state/current.yaml -> state/tasks.yaml  
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

The original 2026-10-02 implementation snapshot below is historical. For migrated vNext scope, current capability must be resolved from the single boot route and bounded capability/evidence records routed by current state; legacy `PROJECT_STATE.json` and `ARCHITECTURE_NOW_20261003.md` cannot override migrated authority.

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
   Every material task must satisfy the project-wide continuity/handoff law in section 8. A chat summary alone is never sufficient. The seat must leave a durable checkpoint that another zero-chat seat can recover without asking the Owner to restate recoverable context.

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

For migrated vNext scope, current status must be resolved only through `state/bootstrap.json`, the routed Master Blueprint and law, then `state/current.yaml` and `state/tasks.yaml`. `docs/PROJECT_STATE.json` is legacy compatibility/history for unmigrated keys and cannot override migrated authority.

## 8. PROJECT-WIDE CONTINUITY & MANDATORY HANDOFF LAW

**Status:** STABLE OWNER LAW / FOUNDATION INVARIANT  
**Scope:** ALL material MINH TRÍ work: law, architecture, learning, critique, security, runtime, implementation, research, content systems, and future domains.

### 8.1 LAW-FIRST gate

Before material architecture or implementation work, every seat must first resolve the current law authority.

Mandatory order:

```text
OWNER CURRENT INSTRUCTION
→ state/bootstrap.json
→ CURRENT MASTER BLUEPRINT
→ AUTHORITATIVE LAW PRECEDENCE
→ CURRENT STATE + TASK REGISTRY
→ CURRENT ARCHITECTURE
→ ACTIVE TASK HANDOFF
→ TASK/DOMAIN SOURCES
→ WORK
```

For migrated vNext scope, `state/bootstrap.json` is the single boot root. Legacy `docs/PROJECT_STATE.json` remains compatibility/history for unmigrated keys only and cannot override migrated Blueprint/Law/State/Task authority.

Architecture may implement law but may not silently outrank, bypass, or redefine stable law.

If law routing is missing, contradictory, stale, or unreadable, the affected architecture mutation is **BLOCKED** until the law conflict is resolved.

### 8.2 NO UNIQUE STATE IN CHAT

No material project state may exist only in a chat.

Material state includes at least:
- Owner decisions that affect future work;
- law/architecture decisions;
- active task state;
- important completed work;
- branch/PR/head/base identity;
- blockers and unresolved risks;
- evidence/claim status changes;
- corrections/supersessions;
- exact next action needed for continuation.

A chat may be the working interface, but it is not the durable continuity authority.

### 8.3 HANDOFF IS CONTINUOUS, NOT AN END-OF-CHAT CEREMONY

A chat can end, truncate, crash, or be replaced without warning.

Therefore a seat must not wait for the last message of a chat to create continuity.

After every **material state transition**, the seat must durably update the task/checkpoint/handoff before relying on that transition in later work.

Material transitions include:
- a decision is made;
- a PR is opened, merged, closed, superseded, or materially changed;
- a task changes status;
- a blocker is discovered or cleared;
- a claim/lesson is promoted, narrowed, disputed, corrected, or superseded;
- the exact next action changes;
- work moves to another seat/chat/model;
- a long-running task pauses.

If the chat disappears immediately after a material transition, the latest durable checkpoint must still be sufficient for recovery.

### 8.4 MANDATORY HANDOFF CONTRACT

Every material task must leave a durable handoff containing, directly or by canonical references:

- `TASK_ID` / workstream identity;
- Owner objective and bounded scope;
- authority/law references needed to continue;
- last verified canonical main SHA;
- working branch, base SHA, head SHA, and PR number when applicable;
- current task status;
- what is DONE;
- what is NOT DONE;
- important evidence/claim status and truth boundary;
- blockers / risks / unresolved conflicts;
- mutations already performed;
- exact **NEXT ACTION**;
- dependencies and required gates;
- PC/Local Brain requirement when applicable;
- durable result/evidence locations.

The handoff must distinguish:
- **canonical main state**;
- **unmerged branch/candidate state**;
- **historical/chat-only notes**.

An unmerged branch handoff may guide resumption of that branch, but it never outranks current canonical main.

### 8.5 NEW-SEAT RECOVERY RULE

A new chat/seat/model must not start material work from model memory or an old chat summary when canonical recovery is available.

It must fresh-read:
1. `state/bootstrap.json`;
2. the current Master Blueprint routed by the boot root;
3. the authoritative law-precedence router and relevant Stable Laws;
4. `state/current.yaml` and `state/tasks.yaml`;
5. the current architecture routed by current state;
6. the active task result/handoff/branch state;
7. task/domain sources and required evidence.

Legacy `docs/PROJECT_STATE.json` may be read only for unmigrated keys/history and cannot override migrated Blueprint/Law/State/Task authority.

Then it must continue from the durable `NEXT ACTION` unless:
- the Owner explicitly redirects;
- the task is already completed/superseded;
- fresh canonical evidence proves the handoff stale.

A new seat should not ask the Owner to repeat information that can be recovered from canonical project records.

### 8.6 STALE / MISSING / CONFLICTING HANDOFF — FAIL CLOSED

If a handoff is missing, stale, or conflicts with current authority:
- do not invent the missing state;
- do not mutate canonical state based on chat recollection;
- reconstruct from GitHub main, task registry, branch/PR history, and durable evidence;
- record the reconciliation/correction;
- only then resume mutation.

Current canonical state and law always outrank an older handoff.

### 8.7 INTERRUPTION AND WRITE-PATH FAILURE

If GitHub write is unavailable:
- explicitly mark the new material state **NOT YET DURABLY RECORDED**;
- do not claim handoff completion;
- continue only work that is safe without the blocked mutation;
- once write access returns, persist the missing checkpoint before depending on it for further architecture progression.

### 8.8 ARCHITECTURE FOUNDATION GATE

The vNext architecture may not be declared complete until project-wide continuity can demonstrate that a genuine zero-chat seat can:
- recover current law;
- recover current state/task;
- identify the exact active work and next action;
- distinguish canonical from unmerged/historical state;
- continue without Owner recap;
- reject a stale/conflicting handoff.

Static CI routing tests are required immediately.
A genuine fresh-seat recovery proof is required before final architecture completion.

### 8.9 PROTECTED CHANGE

This continuity/handoff law is foundational.

Weakening or superseding it requires:
- explicit Owner decision;
- protected branch;
- review appropriate to foundational law;
- required CI;
- merge;
- fresh-read canonical main.

No architecture PR, runtime automation, model, seat, or PC-side process may silently weaken this invariant.


## 9. THIS RECORD

This file is a governance/architecture record created from the Owner instruction:

> "TẤT CẢ GHI TRONG GITHUB TRƯỚC"

It preserves the current findings without modifying Tier-1 runtime code.

No claim in this document is automatically VERIFIED merely because it is in GitHub.


## 10. SYNCHRONIZATION UPDATE — 2026-10-02 / SUPERSEDED ROUTE NOTE

The historical PROJECT_STATE-first route below has been superseded for migrated vNext scope by the Single Boot Root and Master Blueprint route.

Current migrated route:

```text
state/bootstrap.json
→ MASTER BLUEPRINT
→ AUTHORITATIVE LAW PRECEDENCE
→ state/current.yaml
→ state/tasks.yaml
→ CURRENT ARCHITECTURE
→ ACTIVE HANDOFF
→ task/domain source
```

Rules:
- `state/bootstrap.json` is the machine-readable root for migrated current authority.
- `docs/PROJECT_STATE.json` remains compatibility/history for unmigrated keys only.
- historical Law Index / architecture files remain provenance only once superseded.
- Old files remain for provenance and are not deleted.
- A seat must fresh-read live authority rather than trust a SHA copied into an old chat.
- Synchronization means Blueprint/Law/State/Task/Architecture authority records agree. Current local-brain reachability still requires fresh connector observation; historical bridge/deployment evidence is not current-liveness proof.


## 11. CURRENT-STATE ROUTING CLARIFICATION — UPDATED FOR MIGRATED VNEXT

This bootstrap contains historical implementation snapshots by design. For migrated vNext changing facts, read `state/bootstrap.json` first, then the routed Master Blueprint, law precedence, `state/current.yaml`, and `state/tasks.yaml`.

Use `docs/PROJECT_STATE.json` only for unmigrated keys/history and never to override migrated Blueprint/Law/State/Task authority.

A capability historically proven reachable does not mean it is currently reachable. An unexpired authorization timestamp does not prove its in-memory runtime process still exists.

## 11. MANDATORY UNIVERSAL LEARNING BOOTSTRAP — Owner law 2026-10-04

For every current or future learning track, material work requires this live canonical bootstrap order:

1. `state/bootstrap.json`;
2. the current Master Blueprint routed by the boot root;
3. the authoritative law-precedence router;
4. `docs/LAW_UNIVERSAL_LEARNING_CONTINUITY_20261004.md`;
5. `state/current.yaml` and `state/tasks.yaml`;
6. the current Architecture routed by current state;
7. this role bootstrap;
8. the active learning checkpoint/plan for the relevant track;
9. task/domain sources.

Every material checkpoint must be durably recorded in GitHub with learned/corrected content, evidence/status, CURRENT, NEXT, OPEN AUDITS/UNKNOWNS and provenance. Chat memory is not a durable substitute. Recorded does not mean VERIFIED. If the durable write path is blocked, state NOT YET DURABLY RECORDED and continue only the independent work that remains safe.

For Buddhist-thought work, resolve the live learning checkpoint from the current task/domain handoff reached through `state/bootstrap.json -> Master Blueprint -> law -> state/current.yaml -> state/tasks.yaml`. Legacy `PROJECT_STATE.json`, `RECOVERY_MANIFEST.json`, and older checkpoint files are provenance/compatibility only for migrated authority and must not define CURRENT/NEXT.

## 12. MILINDAPAÑHA / MI TIÊN VẤN ĐÁP — BUDDHIST STUDY REQUIREMENT

For any material work in the Buddhist-thought learning track, the seat must include Mi Tiên Vấn Đáp / Milindapañha in the study process throughout the track.

It is mandatory as a supporting/paracanonical reasoning source, especially for argument structure, objections, distinctions and analogies. It must not replace early-discourse attestation. Claims about early Buddhist thought still return to early discourses for confirmation and must preserve `TEXT_ATTESTED`, `CROSS_TEXT_SYNTHESIS`, and `LATER/PARACANONICAL` boundaries.

Every durable Buddhist checkpoint must record whether Milindapañha was consulted and what role it played.

