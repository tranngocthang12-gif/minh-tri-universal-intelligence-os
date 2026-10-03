# TRIAL-001 INDEPENDENT TASK-SET PROTOCOL

**Status:** PREPARATION ONLY / RAW TASKS NOT YET CREATED IN PROJECT CONTEXT  
**Trial:** COUNTEREVIDENCE_FIRST paired four-arm calibration trial

## Goal

Prepare a fresh task population without leaking task answers or gold labels to the execution generator before assignment.

## Non-contamination rule

This chat/model MUST NOT author the final raw task texts or gold answers for the primary trial and then later serve as the execution generator.

Therefore this repository stores:
- protocol;
- slot IDs;
- metadata schema;
- content hashes after sealing;
- gold hashes after sealing.

It does **not** store raw primary task text before execution in the public repository.

## Task roles

Keep these roles distinct where practical:
- Task Author;
- Gold/Rubric Author;
- Execution Generator;
- Blinded Judge;
- Final Adjudicator.

The execution generator must not be Task Author or Gold/Rubric Author for the primary trial.

## Slot plan

Provision tasks in complete blocks of six.

Initial capacity:
- 10 primary blocks = 60 task slots;
- 2 reserve blocks = 12 reserve slots;
- total reserved IDs = 72.

This is capacity, not a frozen final N. Final primary block count is set after a separate power pilot.

IDs:
- `TRIAL001-B01-T01` ... `TRIAL001-B10-T06`
- reserve: `TRIAL001-R01-T01` ... `TRIAL001-R02-T06`

## Diversity

Each completed block should avoid clustering all difficult/easy tasks in one narrow subtopic.

Before execution-order randomization, each task receives frozen system-coded metadata:
- domain_id;
- procedure_id;
- difficulty_band;
- source_packet_id;
- scorable_claim_count_band.

These metadata must be assigned before outcomes are generated. Post-outcome labels such as failure_class are prohibited from routing.

## Raw task packet

Each sealed task packet should contain:
- task_id;
- task_text;
- domain_id;
- procedure_id;
- source packet references;
- allowed tools;
- answer constraints;
- created_at;
- task_author;
- task_content_sha256.

## Gold packet

Stored separately from the generator:
- task_id;
- gold factual claims;
- acceptable variants;
- supporting raw-source spans;
- unsupported-claim rubric;
- false-positive-counterclaim rubric;
- directness/conciseness rubric;
- gold_author;
- adjudicator;
- gold_sha256.

Gold labels must be complete and hash-frozen before answer generation.

## Source freshness

Prefer:
- Owner-private task material;
- newly assembled source packets;
- synthetic-but-auditable data generated from project-specific constraints and then human-checked.

Avoid:
- famous benchmark questions;
- commonly published answer keys;
- tasks already discussed in project chat;
- tasks used to design the overlay or assurance framework.

## Sealing process

1. Create raw tasks outside execution-generator context.
2. Complete gold packets, including required-claim coverage rubric.
3. Hash every task and gold packet.
4. Freeze manifest.
5. Commit only manifest/hashes to canonical GitHub.
6. Generate execution-order secret and commit only its hash.
7. Freeze A/B/C/D prompts/overlays, placebo provenance, evaluator rubric and compute telemetry schema.
8. For each eligible task, execute all four arms A/B/C/D in isolated process/cache/state contexts; randomize only arm order.
9. Freeze each arm output and actual compute telemetry before judging.
10. Normalize judge-facing representation enough to reduce avoidable stylistic arm leakage.
11. Run arm-guessing leakage diagnostic under the frozen protocol.
12. Judge primary/safety/coverage endpoints blinded to arm labels.
13. Reveal arm labels only after all scores are frozen.

## Replacement policy

A task can be replaced before unblinding only for a preregistered mechanical reason:
- corrupted packet;
- hash mismatch;
- impossible/missing raw source;
- duplicate task;
- scoring rubric objectively non-executable.

Replacement uses reserve slots. The reason is logged. A task may not be replaced because its answer looks surprising or harms an arm.

## Leakage audit

Before execution each task must certify:
- not present in project chat;
- not present in context capsules;
- not used in v1.4 design;
- not used in canary design;
- not previously executed by the generator seat;
- raw gold not exposed to generator.

Any failed leakage check makes the task ineligible.


## Paired four-arm invariant

Every eligible primary task must produce exactly four outputs:
- A CONTROL;
- B TREATMENT;
- C COMPUTE_MATCHED;
- D PLACEBO.

A missing arm invalidates that task for paired primary analysis. Retrieval caches, session state, tool state, and generated artifacts must be isolated by arm. No arm may consume another arm's output or retrieval result.

## Placebo task-set rule

The D overlay comes from shuffled historical resolution labels using the same synthesis procedure family as the candidate lesson. Its text and provenance hash are frozen before any primary task is executed. The execution generator does not see why D is the placebo.

## Coverage and answer-completeness gold

The gold packet must identify required answer claims separately from optional claims so that `GOLD_CLAIM_COVERAGE` can detect a treatment that appears more accurate only because it says less.

## Domain/risk freeze

`domain_id`, `procedure_id`, and risk classification are assigned by the Task/Gold preparation side and frozen before execution. The runtime does not infer these fields from the generated answer. Unknown risk is ineligible for automatic trial routing.
