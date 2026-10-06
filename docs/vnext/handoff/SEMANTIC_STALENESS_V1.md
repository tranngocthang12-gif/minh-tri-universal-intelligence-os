# Semantic Staleness Guard v1 handoff

**TASK_ID:** ARCH-SEMANTIC-STALENESS-V1

## DONE
- Continuity Core v1 is DONE.
- Transition-Safe Proof v1 passed CI through PR #286.
- Single Boot Root v1 passed CI and merged through PR #287.

## NOT DONE
- Semantic dependency freshness checks are not yet implemented.
- PR #266 stale-writer primitive has not yet been salvaged into current main.

## NEXT ACTION
- Salvage the bounded stale-writer primitive from PR #266, then add semantic dependency checks for superseded/refuted/disputed knowledge without adding a workflow engine.

## REQUIRED GATES
- Fail closed on ambiguous semantic freshness when policy requires freshness.
- Do not reject unrelated main advances.
- Do not create distributed locks, workflow engines, or autonomous merge.
- CI must pass before merge.
