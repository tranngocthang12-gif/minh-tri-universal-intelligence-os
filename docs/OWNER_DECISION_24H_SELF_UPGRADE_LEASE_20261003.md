# OWNER DECISION — 24H SELF-UPGRADE LEASE — 2026-10-03

**Status:** STABLE OWNER LEASE LAW / HISTORICAL INITIAL STATUS BELOW / CURRENT RUNTIME FROM PROJECT_STATE  
**Owner intent:** permit bounded self-learning and candidate self-upgrade for at most 24 hours, then automatically remove upgrade authority and freeze candidates for Owner review.

## Control flow

OWNER
→ 24H LEASE
→ SELF-LEARN
→ SELF-UPGRADE
→ CANDIDATE
→ TEST / CRITIC
→ FREEZE
→ LEASE EXPIRES
→ RIGHTS REVOKED
→ OWNER DECIDES PROMOTION

## Binding rules

- Maximum lease duration is 86,400 seconds.
- Lease issuance requires the existing fixed Owner credential gate.
- No lease renewal method exists. Any later run requires a newly Owner-authorized lease.
- Candidate/child capability inherits the same lease id and expiry with equal-or-less privilege.
- Any wall-clock rollback, monotonic rollback, unknown/invalid time state, expiry, or explicit revocation fails closed.
- Mutation paths must re-check lease immediately before the write.
- Self-upgrade writes are candidate-branch only.
- Candidate code cannot alter Owner authority, lease enforcement, protected canonical state/law/architecture, branch-protection workflows, or the self-upgrade guard tests.
- No automatic VERIFIED.
- No automatic trial activation.
- No automatic candidate promotion.
- Owner promotion records a decision only; it does not merge a branch.
- Existing GitHub PR + required CI + branch protection remain the merge authority.
- On expiry, learning/evidence/candidate history may remain, but autonomous self-upgrade write authority ends.
- A frozen candidate remains `FROZEN_PENDING_OWNER` until Owner promotes, rejects, or authorizes a new lease for revision.
- Historical initial implementation did not itself activate a real 24-hour lease; later Owner-authorized runtime records supersede that initial status.

## Candidate evaluation rule

Parent and Candidate must use the same frozen evaluation packet. Candidate is eligible for Owner review only when:
- no security regression;
- no recovery regression;
- no authority-boundary violation;
- no declared quality metric degrades;
- at least one declared quality metric strictly improves.

Eligibility is not VERIFIED truth and is not promotion.

## Required evidence before a live 24H run

1. CI PASS for lease, generation, evolution and security regression tests.
2. Short-duration runtime test (60–300 seconds).
3. Demonstrated expiry stops mutation.
4. Demonstrated early Owner revoke stops mutation.
5. Demonstrated clock rollback fails closed.
6. Demonstrated child capability cannot extend expiry or scope.
7. Demonstrated protected authority paths cannot be mutated by Candidate.
8. Demonstrated a Candidate freezes pending Owner rather than self-promoting.

Only after these bounded proofs may Owner explicitly activate a real 24-hour lease.


## Explicit activation authorization — 2026-10-03

Owner explicitly accepted the bounded containment evidence already recorded in canonical runtime evidence and issued the command to activate the real 24-hour self-upgrade lease immediately.

Authorization semantics:
- duration: 86,400 seconds maximum;
- no automatic renewal;
- candidate/self-upgrade branch writes only;
- TEST → CRITIC → FREEZE remains mandatory;
- no automatic VERIFIED, trial activation, candidate promotion, push, merge, or canonical write capability;
- expiry/revoke/clock anomalies fail closed;
- existing GitHub PR + required CI + branch protection remain merge authority.

Runtime status at the moment of this record: AUTHORIZED_PENDING_LIVE_OWNER_PC_START. This document must not be interpreted as proof that the lease process is already running; live activation requires Owner-PC runtime evidence.


## Current-state interpretation — 2026-10-04

This file is the stable Owner decision and lease law, not the authority for changing runtime liveness. Later canonical runtime evidence proved activation of an authenticated-worker-handoff 24H lease. At the 2026-10-04 full synchronization observation, its authorization expiry is still in the future, but the live parent process is not currently observable because the maintenance/read planes are down. Therefore current runtime state must be read from `PROJECT_STATE.json` and treated fail-closed when not freshly proven.
