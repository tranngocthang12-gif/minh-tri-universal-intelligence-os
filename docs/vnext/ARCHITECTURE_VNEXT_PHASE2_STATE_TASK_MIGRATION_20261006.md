# MINH TRÍ — Architecture vNext Phase 2 — Current State + Task Registry

**Date:** 2026-10-06  
**Status:** CANDIDATE / NOT CANONICAL UNTIL MERGED  
**Base main:** `d1bc70b04ff38108d5162f0b6a9d99f02db9b566`

## Objective

Create the first real vNext state boundary without creating a second brain.

Phase 2 introduces:

- `state/current.yaml` — a deliberately small current-state authority for a bounded list of migrated keys;
- `state/tasks.yaml` — the single task/assignment truth for vNext work;
- CI tests that enforce the authority boundary.

## Transitional authority rule

This migration is scoped, not a big-bang rewrite.

### Migrated keys
For keys explicitly listed in `state/current.yaml.authority_scope.this_file_is_authoritative_for`:

- `state/current.yaml` is authoritative after this PR merges;
- any matching value still present in `docs/PROJECT_STATE.json` is compatibility-only and must not outrank `state/current.yaml`;
- future migration may generate or remove those legacy duplicates.

### Unmigrated keys
For keys not yet migrated:

- `docs/PROJECT_STATE.json` remains the legacy authority until a later migration names and moves them;
- Phase 2 does not rewrite hundreds of historical/runtime facts.

This avoids a dangerous all-at-once state rewrite while preventing ambiguity about which copy wins.

## Task-registry rule

After merge:

`state/tasks.yaml` is the only vNext assignment/task truth.

Open PRs are not task truth.
Chat memory is not task truth.
Narrative architecture docs are not task truth.

A PR may be referenced by a task, but the task registry decides whether it is READY, DRAFT, BLOCKED, DONE, or superseded.

## Imported tasks

Phase 2 imports only the small set needed to preserve continuity:

1. `ARCH-VNEXT-PHASE2` — this migration.
2. `BUDDHIST-A173` — current learning draft, so architecture migration does not erase or silently close it.
3. `ARCH-VNEXT-PR-SALVAGE` — salvage review of the 21 pre-vNext PRs.
4. `RUNTIME-ASSURANCE-PC` — PC-bound work remains visible without blocking knowledge learning.

The registry is not a dump of every historical checkpoint.

## Why JSON-compatible YAML

The initial `.yaml` files intentionally use JSON syntax, which is valid YAML 1.2.

Reasons:
- standard-library JSON parsing is deterministic in current CI;
- no new YAML dependency is required merely to establish the authority boundary;
- later formatting can change without changing the schema contract.

Serialization is an implementation detail, not architecture.

## Safety properties

Phase 2 must prove:

- current state remains small;
- task registry has unique task IDs;
- every task has status, scope, base SHA, and PC requirement;
- only allowed task states are used;
- migrated-state authority is explicit;
- legacy PROJECT_STATE remains available for unmigrated facts;
- Buddhist A173 remains visible as a draft;
- PC-bound runtime work does not block architecture/learning work.

## Out of scope

This PR does not:

- implement the atom+hub knowledge schema;
- close old PRs;
- rewrite PROJECT_STATE or Recovery Manifest;
- add autonomous merge;
- add workflow-engine machinery;
- add new assurance/witness layers;
- claim self-learning is empirically proven.

## Next

After merge and fresh-read:

Phase 3 runs a bounded atom+hub pilot on a small Buddhist/economics sample before broad migration.
