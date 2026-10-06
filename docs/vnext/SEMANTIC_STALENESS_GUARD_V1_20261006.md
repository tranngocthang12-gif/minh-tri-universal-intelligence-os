# MINH TRÍ — Semantic Staleness Guard v1 — 2026-10-06

## Purpose

Prevent a task write from relying on retired, refuted, disputed, pending, missing, or ambiguous semantic knowledge when the task requires fresh established dependencies.

This remains a small optimistic-concurrency + semantic-freshness guard. It is not a workflow engine, distributed lock, autonomous agent, or merge authority.

## Two independent checks

1. File/task freshness:
   - task state is writable;
   - generation matches;
   - declared base matches task base;
   - branch exists;
   - proposed paths stay inside task scope;
   - main advancement is rejected only when intervening changes intersect task scope.

2. Semantic dependency freshness:
   - ACTIVE dependency: allowed;
   - UNCERTAIN dependency: allowed as explicitly uncertain, not silently promoted;
   - SUPERSEDED / REFUTED / DISPUTED: rejected when freshness is required;
   - PENDING_REVIEW: rejected as established support;
   - missing dependency: fail closed;
   - duplicate/ambiguous dependency ID: fail closed.

A superseded dependency is not automatically followed to a replacement. The caller must explicitly refresh lineage and declare the replacement dependency.

## Truth boundary

This implementation proves deterministic guard primitives and tests. It does not prove that every possible GitHub write path invokes them. Protected-main review remains required. No autonomous merge or self-modification is enabled.
