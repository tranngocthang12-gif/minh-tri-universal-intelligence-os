# MINH TRI — ORCHESTRATOR DYNAMIC WORK QUEUE MODEL — 2026-10-05

Status: OWNER-DIRECTED OPERATING MODEL / PENDING PROTECTED INTEGRATION

## Core idea

The orchestrator owns the whole project map and a numbered work queue.
Worker chats are interchangeable. A worker does not own a permanent role; it receives exactly one task at a time.

Example:
- WORK-10: one bounded task -> assign to any available chat.
- WORK-11: another bounded task -> assign to any available chat.
- WORK-12: another bounded task -> assign to any available chat.

When a chat finishes its assigned work, it must report exactly:
- CHAT/WORKER identifier if available;
- TASK_ID completed;
- what was completed;
- durable output location;
- result status;
- unresolved/blockers;
- explicit statement of what task it had been assigned.

Then the orchestrator:
1. verifies/accepts/rejects the result;
2. marks that TASK_ID state;
3. selects the next ready, non-overlapping task;
4. issues a new bounded instruction to that same chat or any other available chat.

## Worker lifecycle

A worker chat is not tied to a domain forever.

Example:
- CHAT-X receives WORK-10.
- CHAT-Y receives WORK-11.
- CHAT-Z receives WORK-12.
- CHAT-Y completes WORK-11 first.
- Orchestrator marks WORK-11 DONE/REVIEWED and immediately assigns CHAT-Y WORK-13.
- CHAT-X may later finish WORK-10 and receive WORK-14.
- CHAT-Z may fail or expire; WORK-12 returns to READY or is reassigned from the last durable point.

## Non-overlap invariant

Before assignment, each task must define:
- TASK_ID;
- objective;
- scope;
- exclusions / do-not-touch;
- dependencies;
- expected output;
- acceptance condition;
- write boundary.

No two ACTIVE tasks may own the same canonical mutation surface unless explicitly coordinated by the orchestrator.

## Suggested task states

READY
-> ASSIGNED
-> IN_PROGRESS
-> REPORTED
-> REVIEWED_ACCEPTED | REVIEWED_REVISE | BLOCKED
-> DONE

If a chat expires before durable report:
ASSIGNED/IN_PROGRESS -> STALE -> READY_FOR_REASSIGNMENT.

## Orchestrator responsibilities

The orchestrator must maintain:
- complete project work map;
- dependency graph;
- READY queue;
- ACTIVE assignments;
- completed tasks;
- reported-but-not-reviewed results;
- blockers;
- next priorities.

The orchestrator alone decides what task is issued next.

## Worker report contract

Every worker final report must contain:

TASK_ID:
ASSIGNED_WORK:
STATUS:
COMPLETED:
OUTPUT:
DURABLE_LOCATION:
BLOCKERS:
OPEN_QUESTIONS:
OUT_OF_SCOPE_FINDINGS:
READY_FOR_NEXT_TASK: YES/NO

The report must make it unambiguous what task was completed and what had been assigned.

## Successor orchestrator rule

If the orchestrator chat expires, a replacement orchestrator must fresh-read the durable task registry and project state, then reconstruct:
- READY;
- ACTIVE;
- REPORTED;
- BLOCKED;
- DONE;
- next assignment order.

It must not rely on memory of the old orchestrator chat.

## Owner interaction

The Owner can operate mainly through the orchestrator.
The orchestrator writes one instruction per task for any available worker chat.
When a worker reports completion, the orchestrator reviews the result and immediately issues the next ready task.

This model replaces permanent worker roles when work can be decomposed into independent bounded tasks.

## Owner clarification — global planner, whole-work-unit assignment

The orchestrator is not merely a dispatcher of small unrelated tickets.

It must first understand:
- the current architecture;
- the full project objective;
- the current learning/work state;
- what remains to be completed;
- the dependency order among remaining work;
- which units can run in parallel and which must wait.

It then decomposes the **whole remaining project** into complete work units and assigns each unit to any available worker chat.

Example for the Buddhist A-sequence:
- CHAT-A may receive the whole checkpoint **A158**;
- after A158 is durably completed and integrated, CHAT-B may receive the whole checkpoint **A159**;
- after A159 is durably completed and integrated, CHAT-C may receive the whole checkpoint **A160**.

The worker chat does the full assigned checkpoint, not merely one tiny sub-step, unless the orchestrator deliberately decides that the checkpoint itself is too large and must be subdivided.

The orchestrator remains responsible for understanding the continuity across A158 -> A159 -> A160 and for ensuring each next worker receives the correct canonical state from the previous completed unit.

### Dependency rule

Different chats may perform consecutive checkpoints, but sequential dependencies must be respected.

A159 must not be treated as canonically complete before A158 is completed and integrated if A159 depends on A158.
A160 must not be treated as canonically complete before A159 is completed and integrated if A160 depends on A159.

Independent workstreams may still run in parallel, for example:
- A158 on one worker;
- SN22 audit on another;
- Atthakavagga lexical audit on another.

Thus the orchestrator manages a dependency graph, not just a flat queue.

### Orchestrator mental model

The orchestrator should think in this order:

PROJECT END STATE
-> REMAINING MAJOR WORK
-> DEPENDENCIES
-> COMPLETE WORK UNITS
-> ASSIGN ONE UNIT PER CHAT
-> RECEIVE REPORT
-> REVIEW / INTEGRATE
-> ASSIGN NEXT UNIT

The chat worker is replaceable.
The orchestrator role persists across chat generations through the durable project state.
