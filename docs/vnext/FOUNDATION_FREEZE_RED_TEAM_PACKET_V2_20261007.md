# MINH TRÍ — FOUNDATION FREEZE RED-TEAM PACKET v2 — 2026-10-07

**STATUS: FROZEN REVIEW PACKET CANDIDATE — FOUNDATION NOT YET FROZEN**

**Review target protected-main SHA:** `923f177af4f065ba5c3dbcbc18d538b2f79cf712`

## Purpose

Run the final independent Foundation review after:
- Master Blueprint v1 prospective Owner ratification;
- preserved C6/C7/C8 historical FAIL records;
- Recovery Proof v9/C9 deterministic PASS;
- post-C9 control-state reconciliation merged and fresh-read.

This packet does not itself accept or freeze Foundation.

## Canonical review inputs

Read from protected main at exactly `923f177af4f065ba5c3dbcbc18d538b2f79cf712`:

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

## Independent critic mandate

Act as an independent read-only Foundation critic. Do not use prior-chat conclusions as authority.

Audit only for material Foundation-freeze blockers:

1. constitution / Owner-sovereignty defect;
2. law-precedence conflict or second law router;
3. canonical state/task/handoff split-brain or stale operational truth;
4. role-separation / self-certification violation;
5. recovery-proof overclaim or invalid C9 evidence/provenance;
6. unhandled implications of preserved C6/C7/C8 failures;
7. unsafe freeze/reopen semantics;
8. a CRITICAL/HIGH/MEDIUM defect that makes final Foundation Freeze unsafe.

For each finding return:
- `finding_id`
- `severity`: CRITICAL / HIGH / MEDIUM / LOW
- `evidence_ref`
- `defect`
- `consequence`
- `smallest_repair`

Final verdict must be exactly:
- `NO_MATERIAL_DEFECT_FOUND`
or
- `MATERIAL_DEFECTS_FOUND`

## Binding contract

The critic response used for final freeze must state:
- critic/provider;
- packet path: `docs/vnext/FOUNDATION_FREEZE_RED_TEAM_PACKET_V2_20261007.md`;
- packet git blob SHA supplied by the project after this candidate is frozen;
- review target main SHA: `923f177af4f065ba5c3dbcbc18d538b2f79cf712`;
- findings;
- verdict.

The critic has no merge authority and cannot declare Foundation frozen.

Every CRITICAL/HIGH/MEDIUM finding must be durably repaired or explicitly Owner-dispositioned before final Foundation acceptance.
