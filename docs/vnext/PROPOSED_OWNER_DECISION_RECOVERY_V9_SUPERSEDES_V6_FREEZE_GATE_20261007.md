# PROPOSED OWNER DECISION — RECOVERY PROOF v9/C9 SUPERSEDES LEGACY v6 FREEZE CONDITION — 2026-10-07

**Status:** PROPOSED ONLY — NOT EFFECTIVE  
**Authority if accepted:** Owner  
**Decision class:** Foundation / recovery-gate supersession  
**Prior decision affected:** `docs/vnext/OWNER_DECISION_MASTER_BLUEPRINT_V1_POST_MERGE_RATIFICATION_20261007.md`, required remediation items 5-6 only

## Proposed decision

For the Foundation Freeze recovery gate only, Recovery Proof v9/C9 shall supersede the earlier literal requirement that Recovery Proof v6 itself must PASS.

Replacement proof:
- challenge: `ARCH-MASTER-BLUEPRINT-RECOVERY-V9-20261007-C9`;
- response: `eval/recovery/v9/attempts/C9_response.json`;
- score: `eval/recovery/v9/attempts/C9_score.json` = PASS;
- receipt: `eval/recovery/v9/attempts/C9_receipt.json`;
- proof-time protected-main SHA recorded by the receipt: `5c38243166339cd4e745c4e2b4b3ecfc2ae9bd0f`;
- independence provenance: PRESENT;
- completion_eligible: true.

## Historical preservation

This proposal does not regrade prior failures:
- C6 remains immutable FAIL;
- C7 remains immutable FAIL;
- C8 remains immutable FAIL;
- v9/C9 is a replacement proof, not a retroactive PASS for v6/v7/v8.

## Scope

If accepted, this supersession changes only the recovery-proof condition blocking Foundation Freeze. It does not:
- declare Foundation FROZEN;
- waive final independent Foundation review;
- waive disposition of material findings;
- weaken Owner acceptance;
- alter Foundation Law precedence.

## Effectiveness condition

This proposal becomes a durable Owner decision only if:
1. Owner explicitly accepts the exact PR/head containing this file before merge;
2. that exact accepted head is merged to protected main;
3. protected main is fresh-read after merge.

Until then, the earlier v6 wording remains unsuperseded.
