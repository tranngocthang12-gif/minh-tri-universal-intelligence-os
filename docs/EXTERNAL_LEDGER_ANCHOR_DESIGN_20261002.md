# EXTERNAL LEDGER ANCHOR — DESIGN v0.1 — 2026-10-02

**Status:** VERIFIER CANDIDATE IMPLEMENTED / PUBLICATION NOT IMPLEMENTED / NOT VERIFIED

## Threat addressed

The local event hash chain detects accidental edits and partial tampering, but an attacker with full write access to `events.jsonl` and `state.json` can rewrite all events and recompute the chain. A trustworthy copy of a prior ledger head must exist outside that writable set.

## Security invariant

For checkpoint `N`, preserve externally:

```text
project_id + event_count + ledger_head_sha256 + created_at + anchor_version
```

Verification compares the locally replayed `event_count/head` with a previously published external anchor. A mismatch is a hard security failure. A missing anchor is UNKNOWN, never PASS.

## Boundary

The anchor writer must not share the same write authority as the local ledger writer. Otherwise a compromised process can rewrite both and the anchor adds no security.

Therefore:
- local `brain/` remains outside Git;
- anchor publication is a separate gated action;
- historical anchors are append-only;
- normal ledger repair must never rewrite an old anchor;
- rollback to a head older than the latest external anchor is rejected;
- no secret is stored in an anchor.

## Candidate record

```json
{
  "schema": "minhtri-ledger-anchor/v1",
  "project": "MINH_TRI_UNIVERSAL_INTELLIGENCE_OS",
  "event_count": 123,
  "head": "<64 hex sha256>",
  "created_at": "<UTC timestamp>",
  "previous_anchor": "<digest or null>"
}
```

The canonical JSON digest of each anchor becomes its anchor id. `previous_anchor` forms an independent append-only anchor chain.

## Publication targets

Preferred order:
1. a separately protected remote/branch or release/attestation store whose write permission is stricter than ledger write;
2. a second independent storage/account;
3. signed offline Owner checkpoint.

A file beside `events.jsonl` is **not** an external anchor.

## Proposed commands

Read-only:
- `anchor status`
- `anchor verify <anchor-record>`

Gated mutation:
- `anchor publish`

`verify` must be usable without mutation and return machine-readable PASS / FAIL / UNKNOWN.

## Promotion gates

Implementation cannot be promoted until:
- deterministic unit tests cover exact match, mismatch, rollback, malformed anchor and missing anchor;
- CI passes on exact commit;
- anchor target permissions are reviewed;
- Owner approves the external publication boundary.

This design deliberately does not select a provider yet. Provider choice is replaceable; the invariant is not.


## Implementation checkpoint — 2026-10-02

A provider-neutral pure verifier now exists as `src/minhtri/anchor.py` with deterministic tests for exact match, missing anchor, mismatch, rollback, local-ahead, malformed/tampered records, and chained anchor pointers.

This does **not** complete the security control. No independent external publication target has been selected or permission-reviewed, and no `anchor publish` mutation exists. Until an anchor is actually stored outside the local-ledger write authority, runtime protection against full local rewrite remains incomplete.
