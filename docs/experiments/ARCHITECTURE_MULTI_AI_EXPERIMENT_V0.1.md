# MINH TRÍ — MULTI-AI CORE ARCHITECTURE REVIEW EXPERIMENT v0.1

**Experiment ID:** `ARCH-CORE-R4-PRE-R5-2026-09-29-V1`  
**Status:** `SHADOW / REVIEW EXPERIMENT / NOT PROJECT LAW / NOT MERGED`  
**Owner:** Trần Ngọc Thắng  
**Target exact head:** `50a0444ed20ae2415c9ee31e622a0b6b8575d4c9`  
**Question:** Is the MINH TRÍ core architecture from restored v0.2 through R4 coherent and safe enough to begin R5 Skill Lifecycle + Meta-Learning?

## Why this experiment exists

R1-R4 are structurally green, but structural tests do not prove semantic correctness or cross-layer consistency.

Before R5 turns lessons into reusable skills, MINH TRÍ needs independent architecture critique from multiple provider families.

The experiment tests whether independent AIs discover:

- the same material blockers;
- different material blockers;
- false positives;
- missing counterexamples;
- unsafe promotion paths;
- cross-layer inconsistencies;
- replay/migration/authority risks.

This is not a popularity vote.

## Frozen review target

Every participant reviews the same exact Git revision:

`50a0444ed20ae2415c9ee31e622a0b6b8575d4c9`

Required artifacts:

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
17. corresponding tests in `tests/`.

Participants may inspect other files only when needed to resolve a direct dependency. They must state any extra file used.

## Independence rule

Blind round participants must not see:

- other participant answers;
- the current ChatGPT architecture review conclusions;
- a synthesized list of suspected blockers;
- any provisional adjudication.

They may see the frozen repository artifacts above.

Different personas or sessions of the same provider family do **not** count as independent evidence.

## Suggested participant configuration

Use 3-5 different provider families where practical.

Example experiment configuration only:

- Participant P1 — Provider Family A
- Participant P2 — Provider Family B
- Participant P3 — Provider Family C
- Participant P4 — Provider Family D

No provider is permanently privileged.

ChatGPT/OpenAI may be retained as the **incumbent-control review**, but because the existing architecture was largely designed and self-reviewed here, it must not be counted as an independent blind reviewer for this experiment.

## Blind round task

Each participant receives exactly the task packet in:

`docs/experiments/ARCHITECTURE_REVIEW_TASK_PACKET_V0.1.md`

Each participant must return findings without seeing other outputs.

## Required finding format

Every material finding must include:

- `finding_id`
- `severity`: BLOCKER / HIGH / MEDIUM / LOW
- `layer`: Governance / Brain / Core / Arena / Migration / Task / Epistemic / Bottleneck / Cross-layer
- `claim`
- `source`: exact file/function/test
- `failure_scenario`
- `why_material`
- `minimal_fix`
- `verification_test`
- `uncertainty`
- `scope`

A participant must distinguish:

- structural defect;
- semantic risk;
- real-world effectiveness unknown.

## Required architecture questions

Participants must answer all:

1. Does the current candidate preserve the Owner's original invariants: Owner sovereignty, AI replaceability, GitHub durable brain, Tier 1/Tier 2 separation, evidence before belief, prediction before outcome, dissent preservation, measured learning?
2. Can any path promote a weak or stale state into a stronger state without the intended evidence?
3. Can provider identity/family separation be bypassed?
4. Can a stale Core/Epistemic/Task/Governor snapshot be committed after dependencies changed?
5. Can a schema upgrade break replay of R2/R3/R4 ledgers?
6. Are Brain Manifest/Bootstrap/Project State synchronized with the implemented candidate surface?
7. Can R4 mark a dependency satisfied without proving the relevant gap was actually resolved?
8. Can R3 revalidation restore maturity too easily after new evidence/regression?
9. Would R5 inherit any unsafe input that could turn a weak lesson into a reusable skill?
10. What is the smallest set of fixes required before R5?

## Adversarial scenario requirement

Each participant must propose at least two adversarial traces such as:

```text
valid-looking events
→ gate accepts them
→ system reaches an unjustified stronger state
```

The trace must use current contracts/code, not hypothetical future features.

## Cross-critique phase

Only after all blind outputs are frozen:

1. reveal all outputs;
2. assign each participant at least one other review;
3. ask it to:
   - confirm or refute material findings;
   - find missing evidence;
   - detect duplicate findings phrased differently;
   - identify contradictions;
   - propose a discriminating test.

A reviewer cannot erase another finding by assertion. Material disagreement remains open until evidence/test resolves it.

## Adjudication

Adjudication must be performed by a participant/provider family not used as proposer for the specific disputed finding when practical.

Allowed per-finding results:

- `CONFIRMED_BLOCKER`
- `CONFIRMED_NON_BLOCKER`
- `NEEDS_TEST`
- `DUPLICATE`
- `OUT_OF_SCOPE`
- `HOLD`

No majority vote.

## Experiment-level decision

The experiment may conclude:

- `R5_READY_FOR_SHADOW`
- `R4_5_REQUIRED`
- `HOLD_MORE_EVIDENCE`

This decision must cite resolved findings and tests.

It must **not** authorize merge, external action, skill promotion, provider ranking, spending, publishing or trading.

## Evaluation metrics

Do not rank providers from a single run.

For this experiment, record descriptive metrics only:

- material defects found;
- unique material defects found;
- confirmed defects after adjudication;
- false positives;
- useful adversarial traces;
- evidence quality;
- time/latency if available;
- cost if available;
- overlap with incumbent review;
- novel confirmed findings.

Repeated experiments are required before any provider scorecard or champion/challenger conclusion.

## Success condition

This experiment succeeds if it produces a better evidence-backed architecture decision than the incumbent self-review alone.

A useful result may be:

- confirmation of existing blockers;
- discovery of new blockers;
- refutation of suspected blockers;
- evidence that R5 can safely begin in SHADOW.

Agreement by itself is not success.

## Current execution boundary

Repository status currently reports:

- `providers_connected = false`
- AI Commons adapter = `MANUAL_SELF_DECLARED_ONLY`
- external actions = closed.

Therefore v0.1 execution is manual: the same frozen task packet is given to independent AIs, and their outputs are imported as evidence with provider/model/version/timestamp provenance.

No output becomes canonical automatically.
