# Recovery Proof C7 evidence-contract defect — 2026-10-07

**Status:** MATERIAL HARNESS DEFECT / C7 IMMUTABLE FAIL / FOUNDATION FREEZE BLOCKED

## Deterministic result

C7 was executed by the canonical v7 scorer in GitHub Actions Security P0 #1096.

Result: **FAIL**

Exact scorer error:

`missing required evidence refs: tools/score_master_blueprint_recovery_v7.py`

The C7 grading test was actually discovered and executed under `unittest`; this is not a false-green CI result.

## Contract defect

The v7 public response schema defines `evidence_refs` only as a unique non-empty string array with a minimum item count.

The scorer compares that array against `historical_snapshot.json.required_evidence_refs`, which is excluded from the fresh seat.

Although the public packet exposes a `scorer_ref`, neither the public response schema nor the challenge states that every hidden `required_evidence_refs` entry must appear in the response evidence list.

Therefore a PASS-critical evidence-membership contract remains partly hidden.

## Disposition

1. Preserve C7 as immutable deterministic **FAIL**.
2. Never append the missing scorer ref to C7 after the fact and never regrade C7 as PASS.
3. Do not treat this FAIL alone as evidence that protected-main continuity recovery failed; the failure is confounded by a hidden evidence-membership requirement.
4. Build a new proof generation with a new challenge id and nonce.
5. Publish the full required evidence-ref membership contract in allowed public inputs while keeping expected fact values hidden.
6. Add a regression test proving every scorer-required evidence ref is public before a fresh seat runs.
7. Foundation Freeze remains blocked until the replacement proof achieves deterministic PASS + independence provenance + durable receipt.
