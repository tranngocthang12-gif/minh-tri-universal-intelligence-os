# ARCHITECTURE REPAIR REVIEW — 2026-10-02

**Status:** REVIEW / REPAIR BACKLOG / NO NEW RUNTIME AUTHORITY
**Reviewed main:** `d0f6ccf984529940b1bea86a62c16f08d078e240`
**Also reviewed:** PR #50 head `4b56a6021e5f523bed35dee970db1a4934b105cb` (CI PASS, not yet canonical at review time).

## Findings requiring architecture repair

### P0 — no new blocker discovered in merged mutation boundary
No fresh direct bypass was found in this review of the already hardened Owner mutation boundary. This is not a full penetration test.

### P1 — external anchor still lacks an independent witness
Verifier and chain validation are canonical, but publication remains blocked because independent write authority is not proven. Do not substitute same-authority GitHub/local storage.

### P1 — real seat-to-local-brain transport is absent
BrainReader and atomic recovery packet are canonical Python code. A real authenticated private connector is not installed. PR #50 records the intended boundary only.

### P1 — Owner credential architecture needs migration
Owner authentication still uses a declared ID plus raw SHA-256 secret verifier. Required future repair:
- version credential schema;
- migrate to a password KDF or OS-backed secret verifier;
- support rotation/revocation;
- preserve fail-closed compatibility;
- never expose mutation secret to read-only transport.

### P1 — authority/state records need automatic consistency checks
State drift already occurred once. Add a CI governance test that checks machine-readable current-state pointers/status invariants against required canonical files/features. GitHub-first fails operationally if CURRENT metadata silently lags implementation.

### P1 — bootstrap needs one machine-readable recovery manifest
The bootstrap route is spread across PROJECT_STATE, LAW_INDEX, architecture and role-bootstrap docs. Add a small versioned manifest containing current authority document paths, protocol/schema versions and required recovery order. It should point to authority, not duplicate all law.

### P2 — anchor timestamps are syntactically weak
Anchor `created_at` is only checked as non-empty text. Require parseable UTC timestamps and monotonic anchor time in chain verification. Time is not identity proof, but malformed/non-monotonic checkpoint time should fail.

### P2 — old-anchor verification cannot validate an advanced ledger prefix
`verify_anchor(local_count, local_head, anchor)` returns UNKNOWN when local ledger is ahead. To turn a historical anchor into evidence for an advanced ledger, add a replay/checkpoint-head function that derives the ledger head at anchor.event_count and compares that historical prefix.

### P2 — workflow scope/name is stale
CI workflow is still named `Security P0` although it now protects the broader Tier-1 system. Rename to a neutral Tier-1 verification name and add supported Python version coverage (project declares >=3.10 but CI currently runs only 3.11).

### P2 — build dependency is not reproducibly bounded
`setuptools>=68` is open-ended. For stronger reproducibility/supply-chain control, define an intentional build dependency policy/lock strategy rather than treating any future setuptools as equivalent.

### P2 — provider independence remains declarative
Distinct provider IDs enforce logical seat separation but do not prove independent models/organizations. Before automatic critic/adjudication is trusted, attach verifiable execution provenance or explicitly retain status as declared separation only.

### P2 — read-only API duplicates search logic
`recovery_packet` and `search_lessons` duplicate lesson matching. Refactor into one private pure helper to prevent semantic drift while preserving one verified read for recovery_packet.

### P3 — end-to-end observability is missing
Before background autonomy, define trace IDs across source ingestion, claim, critic, adjudication, lesson proposal, transport reads and gated mutations. Trace storage must not become a second uncontrolled authority.

## Correct repair order

1. Canonicalize PR #50 if its exact-head CI remains PASS.
2. Add current-state/authority consistency CI + recovery manifest.
3. Strengthen Owner credential verifier/rotation design and implementation.
4. Add historical-prefix anchor verification and timestamp rules.
5. Establish independent external anchor witness.
6. Install/authenticate the read-only local transport and run fresh-seat E2E.
7. Broaden CI/version/reproducibility controls.
8. Add execution provenance for critic/adjudicator independence.
9. Only then resume Research Adapter and autonomous-learning orchestration.

## Architecture judgment

The architecture is substantially safer than the earlier baseline, but it is not yet ready for autonomous durable mutation. The main structural risk has shifted from obvious write bypasses to **trust-boundary completeness, state consistency, credential strength, and proof that separate components are actually independent in operation**.
