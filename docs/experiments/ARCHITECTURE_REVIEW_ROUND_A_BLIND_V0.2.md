# MINH TRÍ — ROUND A BLIND ARCHITECTURE DISCOVERY PACKET v0.2

**Experiment:** `ARCH-CORE-R4-PRE-R5-2026-09-29-V2`  
**Frozen architecture target:** `50a0444ed20ae2415c9ee31e622a0b6b8575d4c9`  
**Round:** A — blind discovery

## Role

You are an independent architecture critic. Review the frozen repository state without access to any incumbent suspected-blocker list or other reviewer output.

## Core question

> What material architecture defects, unsafe state transitions, governance inconsistencies, continuity failures or missing gates could make it unsafe to begin R5 Skill Lifecycle + Meta-Learning in SHADOW mode?

Do not assume tests passing means the architecture is semantically safe.

## Frozen source set

Read these exact files at the frozen target:

1. `PROJECT_LAW.md`
2. `BOOTSTRAP.md`
3. `docs/PROJECT_STATE.json`
4. `docs/UNIVERSAL_BRAIN_ARCHITECTURE_V0.2_CANDIDATE.md`
5. `docs/PROJECT_LAW_V0.2_RESTORATION_DELTA_CANDIDATE.md`
6. `docs/ARENA_SCHEMA_MIGRATION_V0.1.md`
7. `docs/CANONICAL_TASK_HANDOFF_V0.1.md`
8. `docs/EPISTEMIC_STATE_LEARNING_MATURITY_V0.1.md`
9. `docs/GOAL_DECOMPOSITION_BOTTLENECK_GOVERNOR_V0.1.md`
10. `src/minhtri/brain.py`
11. `src/minhtri/core.py`
12. `src/minhtri/arena.py`
13. `src/minhtri/arena_migration.py`
14. `src/minhtri/tasking.py`
15. `src/minhtri/epistemic.py`
16. `src/minhtri/bottleneck.py`
17. relevant files under `tests/`.

You may inspect a direct dependency outside the list, but disclose it.

## Invariants to verify

These are project requirements, not hints about where bugs exist:

- Owner sovereignty;
- AI/provider replaceability;
- project memory != model memory;
- read before reconstruct;
- evidence before belief;
- prediction before outcome;
- dissent preserved;
- independent logical roles;
- domain isolation;
- fail closed;
- no automatic truth promotion;
- replayable decisions;
- measured learning;
- no silent architecture mutation;
- structural correctness != semantic correctness != effectiveness.

## Output

### Executive result

Choose one:

- `R5_READY_FOR_SHADOW`
- `R4_5_REQUIRED`
- `HOLD_MORE_EVIDENCE`

### Material findings

For each:

```text
finding_id:
severity: BLOCKER | HIGH | MEDIUM | LOW
layer:
claim:
source: exact file/function/test and line/range when available
failure_scenario:
why_material:
minimal_fix:
verification_test:
uncertainty:
scope:
```

### Adversarial traces

Provide at least two concrete current-code traces that attempt to reach an unjustified stronger state.

For BLOCKER/HIGH findings that claim a code/gate defect, provide an executable pytest reproducer against the frozen target when feasible. If no executable reproducer is supplied, mark the finding `NEEDS_TEST` rather than `CONFIRMED`.

### What is already strong

### Unknowns

### Minimal pre-R5 gate

## Blindness rule

Do not read:

- incumbent architecture review;
- suspected blocker lists;
- other provider reviews;
- Round B directed challenge packet;
- synthesized/adjudicated results

until your Round A answer is frozen.
