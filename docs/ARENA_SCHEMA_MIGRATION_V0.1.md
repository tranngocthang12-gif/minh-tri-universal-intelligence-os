# MINH TRÍ — ARENA SCHEMA MIGRATION CONTRACT v0.1

**Status:** `R1 CANDIDATE / SHADOW / NOT MERGED`  
**Date:** 2026-09-29

## Purpose

Preserve AI Commons history across schema upgrades without rewriting old events or allowing old task contracts to bypass current Brain/Law gates.

Supported legacy generations:

- `arena-v1-core-constitution` — PR #2 shape using `core_head` + `constitution_sha256`.
- `arena-v2-github-brain` — PR #3 shape using `runtime_state_head` + `brain_revision` + `brain_fingerprint`.
- current generation: `arena-v3-law-ack` — Project Law + Bootstrap + participant acknowledgement.

## Migration law

```text
OLD EVENTS.JSONL
      │
      ├─ verify legacy hash chain
      ├─ replay with frozen historical reducer
      ├─ verify legacy snapshot equivalence
      ▼
READ-ONLY ARCHIVE
      │
      ├─ copy original events.jsonl byte-for-byte
      ├─ copy original state.json byte-for-byte
      ├─ raw SHA-256 file hashes
      └─ migration manifest
      ▼
CURRENT SYSTEM
      │
      └─ legacy open tasks MUST BE REOPENED
         under current Brain/Law/Bootstrap
```

The migration does **not** append synthetic acknowledgement events to old history and does not recalculate old task fingerprints.

## Why not transform old events in place?

Old fingerprints/hash-chain bodies were calculated under old command shapes. Adding new fields would change event hashes and task fingerprints, destroying the exact history the ledger is supposed to protect.

Therefore:

`HISTORY PRESERVATION > PRETENDING OLD TASKS WERE BORN UNDER NEW LAW`.

## What replay proves

Legacy replay proves only:

- event order is intact;
- `prev` linkage is intact;
- event hashes match;
- historical reducer accepts the original commands;
- historical derived state matches the stored snapshot.

It does **not** prove:

- old AI outputs were semantically correct;
- provider identity was real;
- evidence was true;
- old open tasks satisfy current Project Law.

## Continuation policy

Every legacy task still OPEN after historical replay is marked in the migration report as requiring:

`REOPEN_ACTIVE_TASKS_UNDER_CURRENT_BRAIN`.

Continuation must create a new current task with:

- current `brain_revision`;
- current `brain_fingerprint`;
- current Project Law hash;
- current Bootstrap hash;
- current runtime state head;
- new current task fingerprint;
- participant acknowledgement before work.

Historical proposal/critique/adjudication remains reference evidence only.

## CLI

Verify:

```text
minhtri --home <core-home> arena-migration verify <legacy-arena-home>
```

Archive:

```text
minhtri --home <core-home> arena-migration archive <legacy-arena-home> <archive-root>
```

Optional `--schema` is allowed when a ledger has no `open_task` and automatic detection is impossible.

## Safety / scope

- No migration writes to the source legacy ledger.
- Existing archive path is never overwritten.
- Current-generation ledgers are rejected by the legacy detector.
- R1 opens no provider connection, real-data path, canonical lesson promotion or external action.

## Verification gate

R1 can be called structurally complete only if:

1. PR #2-shaped ledger fixture replays;
2. PR #3-shaped ledger fixture replays;
3. current reducer cannot silently replay legacy history;
4. archive is byte-identical for ledger/snapshot;
5. archived copy replays to same historical head and state digest;
6. CI passes on supported Python versions.

Semantic and real-world effectiveness remain outside R1.
