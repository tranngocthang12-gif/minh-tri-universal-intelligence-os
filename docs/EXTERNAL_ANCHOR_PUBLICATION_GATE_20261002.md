# EXTERNAL ANCHOR PUBLICATION BOUNDARY GATE — 2026-10-02

**Status:** BLOCKED ON INDEPENDENT AUTHORITY / DO NOT FAKE EXTERNALITY
**Canonical prerequisite:** anchor verifier + chain hardening merged through `f6a68b0c67ef29cdb89330fde92b814389dfcdbb`.

## Finding

The code can create and verify anchor records, including chain continuity. The project still does not have a publication target whose write authority is proven independent from the local ledger writer.

Publishing an anchor into:
- the same local filesystem;
- the same writable `brain/`;
- a normal repo path controlled by the same automation credential

does not satisfy the threat model. It would let one compromised writer alter both the ledger and its supposed witness.

## Required boundary before implementation

An external target must demonstrate all of these:
1. separate write authority from the local ledger writer;
2. append-only or immutable historical records;
3. read-back verification available to the verifier;
4. credential not stored in the local ledger;
5. Owner-approved target and permission model;
6. documented recovery if the target is unavailable;
7. publication failure never becomes PASS.

## Safe implementation contract once target exists

`anchor publish` may:
- verify the local ledger first;
- construct the next anchor with the previous external anchor id;
- publish through the separately authorized adapter;
- read it back;
- run chain verification;
- return PASS only after exact read-back match.

It must not:
- silently fall back to a local file;
- rewrite old anchors;
- share local-ledger mutation credentials;
- convert unavailable storage into success.

## Current decision

Do not implement a fake publisher against the existing same-authority GitHub/local boundary. Keep `external_anchor_publication=false`.

This is a security gate, not unfinished coding disguised as success.
