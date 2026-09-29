# MINH TRÍ — CANONICAL TASK / HANDOFF CONTRACT v0.1

**Status:** `R2 CANDIDATE / SHADOW / NOT MERGED`  
**Date:** 2026-09-29

## Purpose

Ensure work belongs to MINH TRÍ rather than to one AI/chat. A worker may disappear, fail or be replaced without losing the task, last accepted checkpoint or next exact action.

## Core model

```text
OWNER GOAL
   ↓
CANONICAL TASK
   │
   ├─ brain/law pins
   ├─ allowed evidence
   ├─ acceptance
   ├─ risk
   ├─ checkpoint_seq
   ├─ checkpoint
   └─ lease
        ↓
     WORKER A
        ↓
     CHECKPOINT
        ↓
 release / expiry / failure
        ↓
     WORKER B
        ↓
 continues from same checkpoint
```

## Task ownership

The task is owned by the task ledger, not by a worker.

A task stores:

- goal/domain;
- current Brain revision/fingerprint;
- Project Law/Bootstrap hashes;
- Core state head at creation for provenance;
- evidence allowlist;
- acceptance contract;
- risk class;
- checkpoint sequence;
- last accepted checkpoint;
- current lease;
- structured handoff history;
- continuation acknowledgements.

A deterministic `continuation_fingerprint` binds the current Brain pins, checkpoint and latest handoff. A worker/chat must acknowledge the exact current fingerprint before acquiring a lease.

## Checkpoint law

Checkpoint writes are compare-and-set:

`expected_checkpoint_seq == current checkpoint_seq`.

A stale writer cannot overwrite a newer checkpoint.

Checkpoint contains:

- summary of accepted work;
- artifact references;
- permitted evidence references;
- exact next action;
- worker that wrote it;
- timestamp.

## Lease law

A worker may write/complete only while holding the current non-expired lease.

An active lease blocks a second worker.

When a lease has expired, a new worker may claim the task **only from the same current checkpoint sequence**. The reducer records:

`from_worker → to_worker → LEASE_EXPIRED → checkpoint_seq`.

A voluntary release records a checkpoint-derived handoff and leaves the task OPEN.

For normal intentional transfer, use the structured `handoff_task` path after checkpointing. It records decisions, unknowns, blockers, verification, scope, limitations and the exact next action, then fingerprints the receipt and releases the lease.

For terminal completion, `complete_task` must likewise create a structured `completion_receipt` containing the accepted checkpoint, artifacts/evidence, decisions, remaining unknowns/blockers, verification, scope, limitations and completion summary. Completion without this fingerprinted receipt is not a valid terminal handoff.

The finish order is:

```text
PERSIST DURABLE DELTA
→ TEST / VALIDATE
→ CHECKPOINT
→ STRUCTURED HANDOFF RECEIPT
→ REPLAY / VERIFY
→ REPORT
```

A successor must read the packet and submit an exact continuation acknowledgement before acquiring the task.

## Brain and Owner gates

Continuation is blocked if:

- the underlying Owner goal is blocked/closed;
- Brain revision/fingerprint changed;
- Project Law hash changed;
- Bootstrap hash changed.

The task must then be reopened from current authority/context. This prevents a long-running task from silently continuing under obsolete law.

The `core_state_head_at_open` is provenance, not a requirement that every unrelated Core event invalidates the task.

## Worker identity

R2 worker IDs are identifiers only. Identity/provider authentication is **not solved in R2**. Provider registry/scorecards belong to later phases.

## External actions

R2 does not dispatch models and does not grant tool, publish, trade, spend or irreversible-action authority.

## CLI

```text
minhtri --home brain tasks --brain-root . init
minhtri --home brain tasks --brain-root . apply command.json
minhtri --home brain tasks --brain-root . status
minhtri --home brain tasks --brain-root . packet task1
minhtri --home brain tasks --brain-root . verify
```

## Structural verification gate

R2 PASS requires:

1. checkpoint survives worker replacement;
2. every worker acknowledges the exact current continuation fingerprint before lease acquisition;
3. structured handoff preserves decisions/unknowns/blockers/verification/scope/next action;
4. stale continuation acknowledgement is rejected after checkpoint/handoff changes;
5. active lease blocks a second worker;
6. expired lease permits failover from durable checkpoint state;
7. stale checkpoint writes fail closed;
8. wrong worker cannot checkpoint/complete;
9. blocked goal or stale Brain blocks continuation;
10. terminal completion contains a structured fingerprinted completion receipt;
11. completed task is terminal and no continuation acknowledgement is required;
12. Python 3.10/3.12 CI passes.

## Not yet implemented

- automatic background lease expiry notification;
- provider API dispatch;
- retry policy by error class;
- provider health scoring;
- identity attestation;
- cross-process atomic transaction between Core and Task ledgers;
- real-world task outcomes.

These remain later gates.
