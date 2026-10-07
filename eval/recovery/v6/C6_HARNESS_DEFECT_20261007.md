# Recovery Proof C6 harness defect — 2026-10-07

**Status:** MATERIAL HARNESS DEFECT / C6 IMMUTABLE FAIL / FOUNDATION FREEZE BLOCKED

## Deterministic result
C6 score is **FAIL** with exactly one scorer error: `recovered_facts mismatch`.

## Contract defect
The v6 challenge declares `exact_nested_contract=true`, but the public v6 response schema exposes `recovered_facts` only as an unconstrained object. The scorer nevertheless requires exact equality with the excluded `historical_snapshot.json.expected_facts`.

Because the fresh seat is forbidden from reading that snapshot, the nested output shape required for PASS is not publicly specified.

This is a harness-contract regression relative to v5, whose public response schema enumerated the exact nested `recovered_facts` shape while keeping expected values hidden.

## Disposition
1. Preserve C6 as deterministic FAIL; never rewrite or reinterpret it as PASS.
2. Do not treat C6 FAIL alone as proof that protected-main continuity recovery failed, because the evaluation contract is confounded.
3. Replace C6 with a new proof generation using a new challenge id and nonce.
4. Publicly expose the exact nested key/type contract while keeping expected values hidden.
5. Add a regression test that public schema shape equals hidden expected-facts shape.
6. Merge the repaired harness only after required CI and Owner acceptance for the Class F package.
7. Run a genuinely new fresh zero-chat seat only after protected-main merge and fresh-read.
8. Foundation Freeze remains blocked until the replacement proof passes with durable independence provenance and receipt.
