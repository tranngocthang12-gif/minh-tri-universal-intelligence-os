# SECURITY P0 HARDENING — 2026-10-02

Status: CANDIDATE PATCH / NOT VERIFIED BY TEST RUN

Scope is deliberately narrow. No music/MV files are touched.

## Patched in this branch

1. Owner authority config is pinned to `config/owner.json`.
   - caller-selected `--owner-config` is removed from CLI;
   - `MINHTRI_OWNER_CONFIG` is no longer an authority selector;
   - direct `config_path(explicit)` override fails closed.

2. Every CLI `apply` mutation now requires Owner ID + secret.

3. Direct Python `Ledger.apply(...)` without `approved_by` now fails closed.

4. `repair-snapshot` now requires Owner gate; direct `Ledger.repair_snapshot()` without approver fails closed.

## Still open

- `approved_by` is an identifier, not cryptographic proof inside the Ledger API. Code with arbitrary Python execution can still call the API with a forged non-empty id. Full in-process capability security needs a stronger design.
- Shared secret storage remains unsalted SHA-256; migrate to a password KDF or keyed verifier in a compatibility-safe change.
- Local ledger hash chain still lacks an immutable/external anchor, so an attacker with full filesystem write can rewrite the complete history and recompute hashes.
- Provider IDs remain declared identities.
- Real-person Owner identity remains unverified.
- GitHub branch/CI protections remain a separate control plane.

## Compatibility note

This patch intentionally changes write semantics: formerly ungated `apply` calls are now gated. Existing ledger replay remains readable because historical events are not rewritten.

No claim here is VERIFIED until tests are run on the exact branch commit.
