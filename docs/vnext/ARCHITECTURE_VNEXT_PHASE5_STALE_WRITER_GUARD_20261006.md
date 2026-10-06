# MINH TRÍ — Architecture vNext Phase 5A — Minimal stale-writer guard

**Date:** 2026-10-06  
**Status:** CANDIDATE / GUARD PRIMITIVE / NOT YET GLOBAL WRITE-PATH ENFORCEMENT  
**Base main:** `3c61a37165232c148b4e9efb59423f5789d3a10b`

## Purpose

Implement the smallest useful stale-writer primitive required by Architecture vNext without creating a workflow engine, lease service, or permanent orchestrator.

The guard evaluates one proposed task write using only:

- canonical task registry record;
- `task_id`;
- task `generation`;
- declared `base_sha`;
- current main SHA;
- task write scope;
- files changed on main since the task base;
- files the seat proposes to write.

## Decision rule

Reject when any of these is true:

1. task is not in a writable state;
2. generation differs;
3. declared base SHA differs from task registry;
4. task has no assigned branch;
5. proposed write exceeds task scope;
6. main advanced since base SHA **and** the intervening main changes intersect the task write scope.

Allow when:

- base SHA still equals current main; or
- main advanced only outside the task write scope.

This is optimistic concurrency control, not a distributed lock.

## Why this is intentionally small

Do not add:

- distributed lease server;
- workflow engine;
- service mesh;
- background agent;
- database lock service;
- permanent chat identity.

Git branch + canonical task registry + generation + base SHA + scope are enough for the present project scale.

## Truth boundary

This PR proves only a deterministic guard primitive and its unit tests.

It does **not** yet prove:
- every GitHub write path invokes the guard;
- semantic dependency staleness is fully enforced;
- all current tasks have explicit generation fields;
- autonomous stale-writer rejection exists outside guarded paths.

Global write-path enforcement is a later Phase 5B integration step after this primitive is reviewed.

## Next

1. review/merge this primitive;
2. add explicit `generation` to active vNext tasks;
3. integrate the guard into the protected change path for vNext-managed writes;
4. add semantic dependency staleness for knowledge claims separately;
5. preserve ordinary knowledge throughput and avoid turning every checkpoint into a heavy governance transaction.
