# OWNER DECISION — RECOVERY PROOF v9/C9 SUPERSEDES LEGACY v6 FREEZE CONDITION — 2026-10-07

**Status:** EFFECTIVE — OWNER ACCEPTED ON PR #315 EXACT HEAD AND MERGED TO PROTECTED MAIN  
**Authority:** Owner  
**Decision class:** Foundation / recovery-gate supersession  
**Accepted PR:** #315  
**Accepted exact head:** `a94c9d26b0736f752c4fd26972e888cf40bd017c`  
**Protected merge:** `850b98c4be6ec054049794559082c0d38c9b1b11`  
**Prior decision affected:** `docs/vnext/OWNER_DECISION_MASTER_BLUEPRINT_V1_POST_MERGE_RATIFICATION_20261007.md`, required remediation items 5-6 only

## Decision

For the Foundation Freeze recovery gate only, Recovery Proof v9/C9 supersedes the earlier literal requirement that Recovery Proof v6 itself must PASS.

Replacement proof:
- challenge: `ARCH-MASTER-BLUEPRINT-RECOVERY-V9-20261007-C9`;
- response: `eval/recovery/v9/attempts/C9_response.json`;
- score: `eval/recovery/v9/attempts/C9_score.json` = PASS;
- receipt: `eval/recovery/v9/attempts/C9_receipt.json`;
- proof-time protected-main SHA recorded by the receipt: `5c38243166339cd4e745c4e2b4b3ecfc2ae9bd0f`;
- independence provenance: PRESENT;
- completion_eligible: true.

## Historical preservation

- C6 remains immutable FAIL.
- C7 remains immutable FAIL.
- C8 remains immutable FAIL.
- v9/C9 is a replacement proof, not a retroactive PASS for v6/v7/v8.

## Scope

This supersession changes only the recovery-proof condition blocking Foundation Freeze. It does not:
- declare Foundation FROZEN;
- waive final independent Foundation review;
- waive disposition of material findings;
- weaken Owner acceptance;
- alter Foundation Law precedence.

## Provenance

Owner acceptance on PR #315 explicitly accepted both:
1. the material-finding repair package; and
2. this v9-for-v6 supersession decision,
bound to exact head `a94c9d26b0736f752c4fd26972e888cf40bd017c`.

That accepted head was merged to protected main as `850b98c4be6ec054049794559082c0d38c9b1b11` and then fresh-read.
