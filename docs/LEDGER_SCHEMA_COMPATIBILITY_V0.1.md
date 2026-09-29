# MINH TRÍ — LEDGER SCHEMA & COMPATIBILITY POLICY v0.1

**Status:** `R4.5 CANDIDATE / NOT MERGED`

## Rule

A durable ledger schema is part of project memory. Reducer evolution must not silently reinterpret or destroy historical events.

For every mutable ledger:

- Core
- Arena
- Canonical Task
- Epistemic
- Bottleneck Governor
- Four-seat Workcell
- future Skill/Meta-Learning ledgers

the project must maintain an explicit schema generation and compatibility decision.

## Required change process

Before changing a command shape, initial state shape, reducer meaning or fingerprint input:

1. name the old schema generation;
2. freeze an old-ledger fixture;
3. replay it with the historical reducer;
4. define whether the new reducer can replay it exactly;
5. if not, use a non-destructive archive/migration reader;
6. never rewrite old events to pretend they were created under new law;
7. verify event head + derived historical state before/after archival;
8. require old open work to reopen under current Brain/Law when semantics changed.

## Current generations

| Ledger | Current candidate generation | Compatibility state |
| --- | --- | --- |
| Core | `core-v1-foundation` + R4.5 family semantics | migration fixture REQUIRED before canonical schema change |
| Arena | `arena-v3-law-ack` | PR2/PR3 legacy replay implemented; v3→future fixture still REQUIRED |
| Task | `task-v1-continuity-hardened` | freeze fixture at R4.5 before future change |
| Epistemic | `epistemic-v1-reopen-hardened` | freeze fixture at R4.5 before future change |
| Governor | `governor-v1-relevance-hardened` | freeze fixture at R4.5 before future change |
| Workcell | `workcell-v1-four-seat` | first generation; freeze fixture before v2 |
| Skill/Meta | not created | must start versioned |

## R5 gate

R5 must not alter R2-R4 ledger semantics as a side effect. If R5 needs a schema change, migration/replay work precedes that change.

Structural replay compatibility does not validate semantic truth.


## R4.5 compatibility enforcement

R4.5 adds:

- `src/minhtri/core_migration.py` — read-only verifier for the pre-`family_id` Core provider schema. It verifies the original hash chain, maps legacy provider IDs to deterministic legacy family identifiers in memory, normalizes the old cached state, compares migrated derived state, and does not rewrite source bytes.
- `tests/test_schema_compatibility.py` — frozen schema tripwires for Core provider registration, Task, Epistemic, Governor and Workcell command contracts.

Therefore, a future edit to these command contracts must deliberately update the compatibility test and migration policy; silent schema drift should fail CI.

This is a **forward-change guard**, not evidence that every future migration is already implemented.
