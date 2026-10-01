# INDEPENDENT EXTERNAL WITNESS ADAPTER CONTRACT — 2026-10-02

**Status:** INTERFACE READY / PUBLICATION STILL BLOCKED

## Purpose

Repair 4/5 must not turn the existing GitHub repository or local brain into a fake external witness. The witness is valid only when its write authority is independent from the ledger writer and its history is append-only or immutable.

## Adapter boundary

A future witness adapter must expose only:

- `append(anchor) -> receipt`
- `read(anchor_id) -> anchor`
- `list_chain(project) -> anchors`

The adapter must not receive the Owner mutation secret, local ledger write capability, shell access, or arbitrary filesystem access.

## Activation evidence

Before `external_anchor_publication` may become true, the project must record:

1. Owner-approved target identifier and permission model;
2. proof that witness write credentials are separate from ledger mutation credentials;
3. append-only/immutable-history property;
4. successful publish then exact read-back;
5. successful `verify_anchor_chain` over read-back records;
6. a negative test proving a ledger writer alone cannot rewrite witness history;
7. outage behavior that returns UNKNOWN/FAIL, never PASS.

## Current boundary

No qualifying target or separate credential is available in the current project runtime. Therefore implementation stops at the adapter contract. Same-repository GitHub commits, local files, and `brain/` remain explicitly invalid as external witnesses.

The next activation step requires a real independent storage authority approved by Owner.
