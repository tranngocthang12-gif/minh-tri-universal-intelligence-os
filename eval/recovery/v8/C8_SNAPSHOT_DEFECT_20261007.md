# Recovery Proof C8 snapshot defect — 2026-10-07

**Status:** MATERIAL HARNESS DEFECT / C8 IMMUTABLE FAIL / FOUNDATION FREEZE BLOCKED

## Deterministic result

C8 was executed by the canonical v8 scorer in GitHub Actions CI #1105.

Result: **FAIL**

Exact scorer error:

`recovered_facts mismatch`

The C8 grading test was discovered and executed under `unittest`.

## Exact mismatch

There is exactly one recovered-facts mismatch:

- fresh-seat C8 recovered canonical `active_task.blocker` as:
  `RECOVERY_PROOF_V8_HARNESS_MERGE_FRESH_READ_THEN_C8_REQUIRED`
- hidden v8 snapshot expected:
  `RECOVERY_PROOF_V8_FRESH_SEAT_RESPONSE_AND_DURABLE_RECEIPT_REQUIRED`

Fresh-read of protected main confirms the C8 value matches the canonical active task in `state/tasks.yaml`.

Therefore the deterministic FAIL is caused by a hidden snapshot value that was not bound to canonical protected-main task state.

## Disposition

1. Preserve C8 as immutable deterministic **FAIL**.
2. Never alter C8 or regrade it as PASS.
3. Treat the single mismatch as a v8 gold/snapshot defect, not proof that fresh-seat recovery failed.
4. Build a new proof generation with a new challenge id and nonce.
5. Generate or validate hidden expected task fields directly against canonical protected-main state before allowing the new fresh-seat run.
6. Add a regression test proving hidden expected active-task fields equal canonical task-registry values at harness build time.
7. Foundation Freeze remains blocked until the replacement proof achieves deterministic PASS + independence provenance + durable receipt.
