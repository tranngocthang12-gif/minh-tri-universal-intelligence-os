# AUTONOMOUS LEARNING ROADMAP — ANALYSIS — 2026-10-02

**Status:** HISTORICAL ARCHITECTURE ANALYSIS / SUPERSEDED AS CURRENT CAPABILITY DESCRIPTION  
**Current-status note (2026-10-03):** This file preserves the dependency rationale recorded on 2026-10-02. Its "current classification" and implementation-status statements are historical and must not be used as present state. Read `docs/PROJECT_STATE.json` and `docs/ARCHITECTURE_NOW_20261003.md` for current capability. The ordering principle—security and recoverability before broader autonomy—remains valid.

**Owner direction analyzed:**  
`merge/sync security → read-only brain bridge → research adapter → automatic critic → lesson proposal → background autonomous learning`

## Why this order is correct

The sequence is dependency-driven, not feature-driven. Each stage removes one failure mode that would otherwise be amplified by the next stage.

### 1. Merge / synchronize security first

Purpose:
- establish a trustworthy mutation boundary;
- make Owner authorization non-optional for durable writes;
- prevent a future autonomous process from inheriting known write bypasses.

Without this:
- an autonomous learner could write through an unsafe path;
- a compromised tool or process could alter state without the intended gate;
- later provenance would not be trustworthy.

Exit criteria:
- security PR passes CI on exact SHA;
- mutation paths are fail-closed;
- current architecture/state documents point to the hardened behavior;
- remaining risks are explicit.

### 2. Read-only local brain bridge

Purpose:
- solve the immediate continuity problem: chat/model seats forget;
- let any seat recover current focus, ledger head and relevant lessons;
- prove the bridge can read and verify without giving it mutation authority.

Initial operations:
- verify ledger;
- get head/event count;
- get current focus;
- search/read relevant lessons.

Why read-only first:
- reading wrong data is recoverable;
- autonomous writing to the wrong state is much harder to undo safely.

Exit criteria:
- seat can recover state from zero chat memory;
- no write methods exposed;
- source/head returned with every read;
- stale or failed verification returns UNKNOWN/FAIL, never silent success.

### 3. Research adapter

Purpose:
- give the system controlled access to new Internet/server knowledge;
- convert external information into project-native SOURCE and EVIDENCE objects.

Required flow:
```text
QUERY
→ SOURCE RETRIEVAL
→ PROVENANCE
→ EVIDENCE = UNVERIFIED
→ HYPOTHESIS
```

Not allowed:
- search result → VERIFIED;
- RAG match → lesson;
- model summary → canonical truth.

Exit criteria:
- citations/provenance preserved;
- domain allow/deny rules possible;
- duplicate/stale source handling exists;
- ingestion remains research-only until explicit lesson workflow.

### 4. Automatic critic

Purpose:
- prevent automation from scaling unchallenged mistakes;
- make every material claim pass a second reasoning path before lesson proposal.

Recommended order:
1. deterministic checks first;
2. same-model self-critique as cheap pre-check;
3. independent critic seat for material claims;
4. adjudication where needed.

Critic inspects:
- source support;
- contradiction;
- uncertainty;
- alternative explanations;
- policy/security/gate violations;
- whether the claim is stronger than evidence.

Exit criteria:
- material claims cannot skip critique;
- critic verdict and reasons are traceable;
- proposer and critic separation is enforced as far as runtime can prove it.

### 5. Lesson proposal

Purpose:
- close the learning loop without giving the system authority to promote its own conclusions.

Flow:
```text
EVIDENCE
→ CLAIM
→ CRITIC
→ PREDICTION/OUTCOME when measurable
→ LESSON CANDIDATE
→ OWNER/GOVERNANCE GATE
→ TRIAL RULE
```

The autonomous system may propose lessons; it must not silently promote them to stable law or VERIFIED knowledge.

Exit criteria:
- lesson has evidence links, limits and provenance;
- measurable claims include outcome history when possible;
- promotion remains gated;
- rollback/supersession is defined.

### 6. Background autonomous learning last

Purpose:
- run the previous safe loop without the Owner manually initiating each search.

A safe background learner may:
- notice approved learning goals;
- search allowed sources;
- generate hypotheses;
- request/trigger critique;
- create lesson candidates;
- report findings.

It must not automatically:
- change stable law;
- publish externally;
- spend money;
- add credentials;
- broaden its own permissions;
- mark claims VERIFIED;
- overwrite canonical state without the defined gate.

## Dependency graph

```text
SECURITY
   ↓
TRUSTED READ OF BRAIN
   ↓
CONTROLLED NEW KNOWLEDGE
   ↓
MANDATORY CRITIQUE
   ↓
GATED LESSON PROPOSAL
   ↓
BACKGROUND AUTONOMY
```

## Architectural principle

Do not optimize for maximum autonomy first.
Optimize for recoverability, provenance, bounded authority and falsifiability first.

The project should become:
- hard to forget;
- hard to silently corrupt;
- easy to audit;
- easy to stop;
before it becomes highly autonomous.

## Current classification

```text
LEARNING CORE                PRESENT
CRITIQUE CORE                PRESENT
DURABLE CHAT RECOVERY        PARTIAL
READ-ONLY BRAIN BRIDGE       ABSENT
RESEARCH ADAPTER             ABSENT
AUTOMATIC CRITIC RUNTIME     ABSENT
LESSON PROPOSAL ORCHESTRATOR ABSENT
BACKGROUND AUTONOMY          ABSENT
```

## Primary risk if order is violated

If autonomous research/write is enabled before security, read-state recovery and critique are trustworthy, the system can amplify stale state, poisoned sources or its own reasoning errors faster than the Owner can detect and correct them.
