# MINH TRÍ — CONTINUITY & HANDOFF CORE v1

**Status:** OWNER-APPROVED BUILD / STATIC GATE CANDIDATE  
**Authority:** implements the foundation law in `docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md` section 8.  
**Canonical authorities remain:** `state/current.yaml` for bounded current state and `state/tasks.yaml` for task truth.

## Purpose

Guarantee that loss/replacement of a chat does not destroy the ability to continue material work.

Core v1 adds no second canonical brain. It adds machine-checkable continuity around the existing current-state + task-registry model.

## Recovery chain

A fresh seat must enter through:

```text
RECOVERY_ENTRYPOINT
→ LAW ROUTER
→ state/current.yaml
→ state/tasks.yaml
→ active_task_id
→ active task handoff_ref
→ task/domain sources
→ NEXT ACTION
```

## Active-task contract

`state/current.yaml.active_task_id` identifies exactly one active foreground task.

For an active task in `IN_PROGRESS`, `BLOCKED`, `REPORTED`, `REVIEWED_REVISE`, or `STALE`, the task record must include:
- `task_id`;
- `status`;
- `scope`;
- `base_sha`;
- `result_ref`;
- `handoff_ref`;
- `next_action`;
- `blocker` (null is allowed only when not blocked/stale);
- branch when work is branch-bound.

The active task handoff must name the same `TASK_ID`.

## Fail-closed rules

Validator failure blocks architecture mutation when:
- active_task_id is missing or not found;
- active task status is not active;
- active task lacks handoff_ref or next_action;
- referenced handoff file is missing;
- handoff TASK_ID disagrees with active_task_id;
- BLOCKED/STALE task lacks blocker;
- current architecture pointer or role bootstrap file is missing;
- recovery entrypoint omits canonical state/task/handoff route.

## Truth boundary

Static validation proves record consistency, not behavioral recovery by a model.

Core v1 is COMPLETE only after:
1. STATIC PASS on canonical main; and
2. GENUINE ZERO-CHAT FRESH-SEAT PASS using the recovery packet without relying on prior chat history.

The authoring seat must not self-grade the genuine fresh-seat result.
