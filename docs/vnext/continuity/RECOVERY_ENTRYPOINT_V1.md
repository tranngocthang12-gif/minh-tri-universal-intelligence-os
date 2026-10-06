# MINH TRÍ — ZERO-CHAT RECOVERY ENTRYPOINT v1

A new seat starts from the single boot root. Do not use old chat memory as authority.

1. Read `state/bootstrap.json`.
2. Follow its `current_state` and `task_registry` pointers.
3. Read the Law Index and role bootstrap named by the boot root (currently `docs/LAW_INDEX_20261003.md` and `docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md`).
4. Resolve current architecture and law precedence from `state/current.yaml`.
5. Resolve `active_task_id` from current state.
6. Find that exact task in `state/tasks.yaml`.
7. Read its `handoff_ref`.
8. Read its `result_ref` and task/domain sources as needed.
9. Continue from its `next_action` unless fresh canonical evidence proves the handoff stale or Owner redirects.

Legacy `docs/PROJECT_STATE.json` and `docs/RECOVERY_MANIFEST.json` remain available for unmigrated keys and history only. They cannot override migrated state routed by `state/bootstrap.json`.

Before mutation, report internally:
- CURRENT LAW;
- ACTIVE TASK;
- CANONICAL vs CANDIDATE state;
- DONE / NOT DONE;
- BLOCKER;
- NEXT ACTION;
- REQUIRED GATE.

If any required boot pointer or required record is missing or conflicting: FAIL CLOSED, reconstruct from protected GitHub main and durable evidence, and do not invent.
