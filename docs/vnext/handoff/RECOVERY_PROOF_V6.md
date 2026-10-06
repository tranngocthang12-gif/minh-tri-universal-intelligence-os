# RECOVERY PROOF v6 — ACTIVE HANDOFF

**TASK_ID:** ARCH-RECOVERY-PROOF-V6
**ROLE:** ARCHITECT_AND_BUILDER_NON_INDEPENDENT
**ACCEPTANCE AUTHORITY:** OWNER

## DONE
- Master Blueprint v1 was independently rereviewed by Claude and Grok with no material defect.
- Owner explicitly accepted Master Blueprint v1.
- PR #300 merged to protected main at `174d8817730063d51f6682c31e5f067094bcef95`.
- Fresh-read detected stale post-merge control state; PR #301 was opened to repair that transition before running v6.
- Recovery Proof v6 challenge, packet, scorer, schema, and tests are being built as bounded proof infrastructure.

## NOT DONE
- PR #301 is not accepted or merged yet.
- No independent fresh-seat v6 response exists yet.
- No v6 deterministic PASS receipt exists yet.
- Foundation Freeze remains blocked.

## NEXT ACTION
Complete CI and independent review of the bounded Recovery Proof v6 transition/harness, obtain explicit Owner acceptance, then protected-merge it; after fresh-read protected main, run an independent fresh-seat v6 response and deterministic scorer. Foundation Freeze remains blocked until v6 PASS with durable receipt.

## REQUIRED GATES
- CI PASS on exact PR #301 head.
- Different-seat or independent review for this canonical-state/core-recovery transition.
- Acceptance by the recorded non-Builder authority before protected merge.
- Fresh-read protected main after merge.
- Independent fresh-seat response under the merged v6 challenge.
- Deterministic v6 scorer PASS.
- Durable challenge/response/score/receipt provenance.
- Foundation Freeze may resume only after all v6 proof gates pass.

## REQUIRED PROOF
A fresh seat must recover, from protected main only:
1. `state/bootstrap.json`
2. accepted Master Blueprint pointer and acceptance status
3. normative Foundation Law router
4. `state/current.yaml`
5. `state/tasks.yaml`
6. current architecture
7. active handoff
8. exact blocker
9. exact next action

The response must be deterministically scored and preserved with a durable receipt.

## TRUTH BOUNDARY
This seat may build the harness and repair transition state but may not manufacture independent review, independent fresh-seat evidence, acceptance, or Foundation Freeze.

## STOP CONDITION
Do not declare Foundation Freeze complete unless v6 deterministic score is PASS, independence provenance is present, and the durable receipt is merged.
