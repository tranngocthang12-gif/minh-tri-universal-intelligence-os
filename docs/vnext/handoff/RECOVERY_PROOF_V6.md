# RECOVERY PROOF v6 — ACTIVE HANDOFF

**TASK_ID:** ARCH-RECOVERY-PROOF-V6
**ROLE:** ARCHITECT_AND_BUILDER_NON_INDEPENDENT
**ACCEPTANCE AUTHORITY:** OWNER

## CURRENT TRUTH
- Master Blueprint v1 was Owner-accepted and merged in PR #300.
- Protected main merge commit: `174d8817730063d51f6682c31e5f067094bcef95`.
- Foundation Freeze remains blocked.
- This seat may build the v6 harness but may not manufacture the independent fresh-seat response.

## NEXT ACTION
Build and merge the bounded Recovery Proof v6 transition and harness against the accepted Master Blueprint route, then run an independent fresh-seat response and deterministic scorer; Foundation Freeze remains blocked until v6 PASS with durable receipt.

## REQUIRED PROOF
A fresh seat must recover, from protected main only:
1. `state/bootstrap.json`
2. accepted Master Blueprint pointer
3. normative Foundation Law router
4. `state/current.yaml`
5. `state/tasks.yaml`
6. active handoff
7. exact next action and blocker

The response must be deterministically scored and preserved with a durable receipt.

## STOP CONDITION
Do not declare Foundation Freeze complete unless v6 deterministic score is PASS and independence provenance is present.
