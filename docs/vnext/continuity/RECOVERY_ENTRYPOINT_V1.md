# MINH TRÍ — ZERO-CHAT RECOVERY ENTRYPOINT v1

A new seat starts from the single boot root. Do not use old chat memory as authority.

1. Read `state/bootstrap.json`.
2. Read the `master_blueprint` routed by the boot root.
3. Read the authoritative `law_precedence`; `law_index_catalog` is discovery/catalog only and has no independent precedence authority.
4. Follow the boot root's `current_state` and `task_registry` pointers.
5. Resolve current architecture from `state/current.yaml`; confirm the current-state law and Master Blueprint pointers agree with the boot root.
6. Resolve `active_task_id` from current state.
7. Find that exact task in `state/tasks.yaml`.
8. Read its `handoff_ref`.
9. Read its `result_ref` and task/domain sources as needed.
10. Continue from its `next_action` unless fresh canonical evidence proves the handoff stale or Owner redirects.

## Learning-seat cold-start addendum (subordinate to existing law)

For every material learning request, after the ten recovery steps above, read **`docs/LAW_UNIVERSAL_LEARNING_CONTINUITY_20261004.md` §2A** (seven activities and three gates), and for Buddhist study also §7A (early discourse priority and mandatory *specific* Milindapañha consultation). The non-normative `docs/learning/LEARNING_SEAT_WORKSHEET_V1.md` is a concise execution aid. Resolve CURRENT/NEXT only from accepted routed state, task, handoff and checkpoint; distinguish unmerged PRs or chat-only A-numbers as candidates. If an active task is DONE/stale or the learning route conflicts, disclose the conflict and block promotion; continue appropriately scoped provisional study and request a governed Class S routing repair. Never fill missing checkpoints by guessing. Record G1/G2/G3 status honestly. Independent recovery is demonstrated only after protected merge and a separate zero-chat reader; do not claim it after merely rereading an author's draft.

Legacy `docs/PROJECT_STATE.json` and `docs/RECOVERY_MANIFEST.json` remain available for unmigrated keys and history only. They cannot override migrated state routed by `state/bootstrap.json`.

Before mutation, recover internally:
- CURRENT MASTER BLUEPRINT;
- CURRENT LAW;
- CURRENT STATE;
- ACTIVE TASK;
- CANONICAL vs CANDIDATE state;
- DONE / NOT DONE;
- BLOCKER;
- NEXT ACTION;
- REQUIRED GATE.

If any required Blueprint/Law/State/Task pointer or required record is missing or conflicting: FAIL CLOSED, reconstruct from protected GitHub main and durable evidence, and do not invent.
