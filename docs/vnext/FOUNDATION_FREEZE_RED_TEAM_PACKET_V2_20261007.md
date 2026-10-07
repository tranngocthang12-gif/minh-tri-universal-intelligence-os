# MINH TRÍ — FOUNDATION FREEZE RED-TEAM PACKET v2 — 2026-10-07

**STATUS: FROZEN REVIEW PACKET CANDIDATE — DO NOT CLAIM FOUNDATION FROZEN FROM THIS PACKET ALONE**

**Target protected main SHA:** `3514178286bcf17d2956f1fa36eeb3699425a96f`

## Review objective

Determine whether any material defect remains that blocks final Foundation Freeze after Recovery Proof v9/C9 PASS.

## Canonical inputs

Review the same current target and these inputs:
- `state/bootstrap.json`
- `docs/vnext/FOUNDATION_LAW_CONSOLIDATED_V1_20261006.md`
- `docs/vnext/MASTER_BLUEPRINT_V1_20261006.md`
- `docs/vnext/OWNER_DECISION_MASTER_BLUEPRINT_V1_POST_MERGE_RATIFICATION_20261007.md`
- `state/current.yaml`
- `state/tasks.yaml`
- `docs/vnext/handoff/MASTER_BLUEPRINT_V1.md`
- `docs/vnext/handoff/FOUNDATION_ACCEPTANCE_FREEZE_V1.md`
- `eval/recovery/v9/challenge.json`
- `eval/recovery/v9/packet.json`
- `eval/recovery/v9/attempts/C9_response.json`
- `eval/recovery/v9/attempts/C9_score.json`
- `eval/recovery/v9/attempts/C9_receipt.json`
- `eval/recovery/v8/attempts/C8_score.json`
- `eval/recovery/v8/C8_SNAPSHOT_DEFECT_20261007.md`
- `eval/recovery/v7/attempts/C7_score.json`
- `eval/recovery/v7/C7_EVIDENCE_CONTRACT_DEFECT_20261007.md`
- `eval/recovery/v6/attempts/C6_score.json`
- `eval/recovery/v6/C6_HARNESS_DEFECT_20261007.md`

## Critic mandate

Act as an independent read-only Foundation critic. Inspect only material freeze blockers:
- constitutional or law-precedence conflict;
- canonical-state/task/handoff inconsistency;
- Owner-sovereignty or role-separation violation;
- recovery-proof overclaim;
- unhandled C6/C7/C8 historical defects;
- C9 evidence or provenance defect;
- split-brain or stale-current-state risk;
- unsafe freeze/reopen semantics;
- any CRITICAL/HIGH/MEDIUM defect that makes Foundation Freeze unsafe.

For each finding return:
- finding_id;
- severity: CRITICAL / HIGH / MEDIUM / LOW;
- evidence_ref;
- defect;
- consequence;
- smallest_repair.

Final verdict must be exactly one of:
- `NO_MATERIAL_DEFECT_FOUND`
- `MATERIAL_DEFECTS_FOUND`

Critic has no merge authority and cannot declare Foundation frozen.

## Binding requirement

Every final critic receipt used for Foundation Freeze must bind:
- this exact packet path/version;
- the exact review target main SHA;
- the packet content SHA;
- critic/provider identity;
- findings;
- verdict.

All material findings require durable project disposition before final Owner acceptance.
