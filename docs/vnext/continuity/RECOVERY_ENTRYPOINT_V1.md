# MINH TRÍ — ZERO-CHAT RECOVERY ENTRYPOINT v1

A new seat starts here. Do not use old chat memory as authority.

1. Read `docs/PROJECT_STATE.json`.
2. Read current Law Index routed by PROJECT_STATE.
3. Read `docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md`, especially section 8.
4. Read `state/current.yaml`.
5. Read `state/tasks.yaml`.
6. Resolve `active_task_id` from current state.
7. Find that exact task in the task registry.
8. Read its `handoff_ref`.
9. Read its `result_ref` and task/domain sources as needed.
10. Continue from its `next_action` unless fresh canonical evidence proves the handoff stale or Owner redirects.

Before mutation, report internally:
- CURRENT LAW;
- ACTIVE TASK;
- CANONICAL vs CANDIDATE state;
- DONE / NOT DONE;
- BLOCKER;
- NEXT ACTION;
- REQUIRED GATE.

If any required record is missing or conflicting: FAIL CLOSED, reconstruct from GitHub durable evidence, and do not invent.
