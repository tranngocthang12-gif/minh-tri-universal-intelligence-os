# CRITICAL REVIEW OF IMPLEMENTED WORK — 2026-10-02

**Status:** CURRENT AUDIT RECORD / FRESH-READ OF MAIN
**Audited main:** `3824d6bdbf7ca63d0caed7a1bb27ad265751f7fd`
**Method:** adversarial review of canonical state, merged PR history, current docs, core security boundary, BrainReader, anchor verifier and exact-main CI.

## What is actually established

- PRs #39, #40, #42, #43 and #44 are merged; #41 was correctly superseded and closed unmerged.
- Current main exact SHA has GitHub Actions `test` = SUCCESS.
- Ledger mutations authenticate inside `Ledger.apply` / `repair_snapshot` against the fixed Owner config path.
- BrainReader is a read-only Python facade and verifies ledger+snapshot before returning head/focus/lesson matches.
- A zero-chat unit/integration test proves recovery through BrainReader from a temporary local ledger without a prior chat transcript.
- The anchor module deterministically distinguishes exact match, missing anchor, rollback, same-count head mismatch and malformed/tampered anchor records.

## Critical findings

### C1 — CURRENT STATE IS STALE
`docs/PROJECT_STATE.json` still says next checkpoint is `SECURE_CURRENT_STATE_SYNC_AND_READ_ONLY_BRAIN_BRIDGE`, even though that bridge and subsequent zero-chat/anchor-verifier work are already merged. This weakens GitHub-first recovery because the machine-readable pointer is behind reality.

**Required:** update current state after every promoted checkpoint, not only add historical docs.

### C2 — CURRENT ARCHITECTURE CONTAINS FIXED SECURITY FINDINGS AS IF OPEN
`ARCHITECTURE_NOW_20261002.md` still lists caller-controlled owner config and direct `Ledger.apply` bypass as known open risks. Those specific P0 paths were changed by #40. Historical risk records are useful, but CURRENT architecture must distinguish CLOSED, PARTIAL and OPEN.

### C3 — SECURITY P0 DOC STATUS IS STALE
`SECURITY_P0_HARDENING_20261002.md` still describes a candidate/current-head-requires-CI state even though the patch was merged and later main CI passed. Status text now under-reports evidence and can confuse a fresh seat.

### C4 — ZERO-CHAT TEST IS NOT A REAL CHAT/RUNTIME BRIDGE
The test proves Python-level recovery from a supplied local filesystem path. It does **not** prove that a new ChatGPT/Claude/Gemini seat can access the Owner's real local `brain/`, discover its path, authenticate transport, or bootstrap itself automatically. Therefore “chat quên, sổ không” is proven only at the local module contract, not end-to-end product/runtime level.

### C5 — BRAINREADER HAS NO CROSS-READ SNAPSHOT TOKEN
Each BrainReader call verifies independently. A caller that obtains head, then focus, then lessons can receive records from different ledger heads if a legitimate write occurs between calls. The returned head lets a careful caller detect this, but there is no atomic recovery packet or required-head parameter.

**Required:** add a single recovery packet or compare-and-read contract for bootstrap consistency.

### C6 — EXTERNAL ANCHOR SECURITY CONTROL IS NOT COMPLETE
The verifier is local code only. No anchor is currently published to storage outside the ledger writer's authority. An attacker with full local write can still rewrite ledger history; the verifier cannot help without a previously preserved external record.

### C7 — ANCHOR CHAIN CONTINUITY IS NOT VERIFIED
`previous_anchor` is included in the anchor digest, but current `verify_anchor` does not accept/verify a prior anchor record or prove that the pointer references the actual prior anchor. The unit test proves tampering changes the digest, not chain continuity.

### C8 — ANCHOR INPUT VALIDATION IS ASYMMETRIC
`make_anchor` validates head format, but `verify_anchor` does not fully validate local head or anchored head/previous-anchor formats before comparison. A correctly self-digested but malformed record can pass some structural checks. Harden verifier schema validation before treating it as a security primitive.

### C9 — OWNER AUTHENTICATION IS STILL A LOCAL SHARED-SECRET GATE
The gate is not real-person identity verification. Secret verification remains a local trust boundary; arbitrary code with access to the secret/config can authenticate. Password verifier design also remains weaker than a modern password KDF. This is acceptable only as a prototype boundary, not strong identity assurance.

### C10 — CI PASS IS NARROW EVIDENCE
The workflow runs Python 3.11 unit tests after `pip install .`. It does not currently prove supported-version matrix behavior, lint/type/static security checks, packaging reproducibility, or external integration behavior. “CI PASS” must not be generalized to “system verified.”

### C11 — BRANCH-PROTECTION DETAILS ARE NOT VERIFIED IN THIS AUDIT
The main branch reports protected, but the integration was denied access to the detailed branch-protection endpoint during this audit. Required-review/status-check/bypass specifics are therefore UNKNOWN here and must not be asserted from stale observations.

### C12 — AUTONOMOUS LEARNING REMAINS ABSENT
Research Adapter, automatic critic orchestration, lesson-proposal orchestration, meta-learning and background autonomy are not implemented. The earlier plan correctly puts them after security/recovery work. Do not infer autonomy from the presence of learning primitives.

## Adversarial conclusion

The work improved the project materially, especially by moving mutation authentication inside the ledger boundary and by separating read-only recovery from mutation. The main weakness is now **state/governance drift**: implementation advanced faster than CURRENT documents. The second weakness is **overclaim risk**: zero-chat and external-anchor work are useful primitives, but neither is end-to-end operational protection yet.

## Correct next order

1. synchronize `PROJECT_STATE.json`, CURRENT architecture and security status with canonical main;
2. add atomic/read-consistent recovery packet and test;
3. harden anchor schema + actual chain-continuity verification;
4. select and permission-review an independent external anchor target before implementing publication;
5. only then resume Research Adapter;
6. keep automatic critic / lesson proposal / background autonomy after those gates.

No publication/spending/external autonomous mutation is authorized by this audit.
