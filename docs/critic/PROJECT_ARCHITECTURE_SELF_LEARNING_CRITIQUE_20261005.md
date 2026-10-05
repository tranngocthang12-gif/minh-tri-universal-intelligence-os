# MINH TRÍ — PHẢN BIỆN KIẾN TRÚC DỰ ÁN VÀ HỆ THỐNG TỰ HỌC / TỰ PHẢN BIỆN — 2026-10-05

Status: ORCHESTRATOR REVIEW CANDIDATE / ADVERSARIAL / NOT AUTOMATICALLY VERIFIED
Reviewed canonical main: 904e4f3b0bced1fcba760045a65041b80bcdf08d
Scope: whole-project architecture, continuity, governance, runtime, self-learning, self-critique, meta-learning, orchestration
Purpose: identify what is genuinely working, what is overbuilt, what remains unproven, and what should be simplified before stronger autonomy.

## Executive conclusion

MINH TRÍ currently has a stronger evidence/governance shell than a real autonomous learning loop.

The architecture is good at:
- preventing silent promotion of claims;
- preserving provenance and durable state;
- making historical evidence distinguishable from current liveness;
- keeping autonomous durable mutation disabled;
- forcing explicit uncertainty and critique.

But it is still weak at:
- proving that learning changes future behavior;
- proving critic independence;
- closing the loop from outcome to improved policy;
- keeping canonical state simple;
- maintaining operational speed;
- avoiding branch/PR and authority-surface drift.

The current self-learning classification in PROJECT_STATE is accurate:
PROPOSAL_GOVERNANCE_PIPELINE_NOT_AUTONOMOUS_BEHAVIOR_ADAPTATION.

That phrase should remain the truth boundary until a learned rule improves new unseen tasks against a compute-matched control under a frozen evaluation.

## 1. What the architecture genuinely gets right

### 1.1 Evidence humility is real, not decorative

The project repeatedly preserves the difference among:
- chat statement;
- durable record;
- CI proof;
- deployment proof;
- current liveness;
- VERIFIED truth.

This is one of the strongest parts of the architecture.

The rule "recorded does not mean verified" prevents a common AI-system failure: documentation slowly becoming treated as evidence merely because it exists.

### 1.2 Durable continuity is valuable

GitHub-first state plus recovery contracts solves a real problem: chats are replaceable and long conversations fail.

The recent Buddhist-learning workflow shows practical value:
- a worker can complete a bounded audit;
- a later seat can recover it;
- corrections remain durable;
- the project does not have to restart from memory.

This continuity function is already useful even before autonomous learning exists.

### 1.3 Autonomy is currently bounded correctly

Current main says:
- autonomous learning runtime OFF;
- automatic self-critique runtime OFF;
- meta-learning runtime OFF;
- autonomy write capability false;
- no automatic VERIFIED;
- no automatic trial activation.

This is appropriate because empirical proof is not yet complete.

### 1.4 Learning Assurance has several sound design ideas

Useful mechanisms already exist or are specified:
- frozen learning packets;
- counterevidence;
- critic execution provenance;
- negative controls;
- lesson revalidation proposals;
- failure taxonomy;
- stratified meta-learning;
- adaptive deliberation metadata;
- grounded research traces;
- digest-bound context capsules.

These are good assurance primitives when used selectively.

## 2. Central criticism: the project is over-architected relative to proven learning value

MINH TRÍ has accumulated:
- authority plane;
- brain read plane;
- brain write plane;
- maintenance plane;
- witness plane;
- recovery plane;
- fresh-seat protocols;
- tunnel persistence;
- Owner credentials;
- external anchors;
- learning assurance versions;
- critic receipts;
- self-upgrade lease;
- candidate lifecycle;
- negative controls;
- trial preregistration;
- meta-learning statistics;
- context capsules;
- task orchestration concepts.

This is technically interesting, but the core empirical question is still unanswered:

> Does a lesson derived from past experience improve future performance beyond ordinary extra reasoning/computation?

Trial-001 has not yet answered this.

Therefore architecture complexity has advanced faster than demonstrated learning benefit.

The system risks optimizing the machinery for proving learning before proving that the learning mechanism is useful enough to justify the machinery.

## 3. The current self-learning system is not yet self-learning in the behavioral sense

Current canonical classification already admits this.

What exists today is primarily:

SOURCE / EVIDENCE
→ CLAIM
→ CRITIC
→ PREDICTION / RESOLUTION
→ LESSON CANDIDATE
→ OWNER GATE
→ TRIAL RULE

That is a governed proposal pipeline.

Behavioral self-learning requires an additional demonstrated loop:

PAST EXPERIENCE
→ DERIVED LESSON
→ FUTURE BEHAVIOR CHANGES
→ NEW UNSEEN TASKS
→ MEASURABLY BETTER OUTCOME
→ RETAIN / NARROW / RETIRE

The final causal portion has not been empirically proven.

Until it is, "autonomous self-learning" would be an overclaim.

## 4. Trial-001 is well-hardened conceptually but still not a learning proof

The paired four-arm design is a substantial improvement:

- A: control;
- B: candidate lesson treatment;
- C: compute-matched neutral deep review;
- D: shuffled-ledger placebo.

This directly attacks two important confounds:
- B may win only because it gets more reasoning effort;
- any plausible-looking overlay may improve answers irrespective of historical learning.

However, major blockers remain:

1. Trial-001 status is CALIBRATION_PREPARATION_NOT_FROZEN_NOT_RUN.
2. Final N is not frozen.
3. Live isolated executor is not proven.
4. Actual provider telemetry capture is not proven.
5. Blinded evaluator runtime is not proven.
6. Runtime commit/build attestation is not proven currently.
7. Resolution provenance independence remains open.
8. COUNTEREVIDENCE_FIRST is not currently an audited ledger-derived lesson.

Therefore even a future B > C result with the current candidate would first prove overlay value, not necessarily "the system learned from its own historical experience."

That distinction is correct and must remain.

## 5. Critic independence remains weaker than the project language sometimes suggests

The architecture records critic provider/model/run identity and can use BLIND packets.

That is useful provenance.

But it does not prove independent reasoning.

Open problems include:
- provider IDs can be declared rather than cryptographically tied to independent actors;
- two seats may share the same model priors/training corpus;
- process separation does not prove epistemic independence;
- project/account authority may still be shared;
- historical self-upgrade critic evidence includes same-provider reviews explicitly marked not independent.

Therefore critic output should be treated as adversarial evidence, not an oracle.

The project is right to use "PARTIAL / NOT PROVEN" for independence.

## 6. Resolution provenance is a major epistemic bottleneck

A learning system is only as good as its outcomes.

Current review history already identifies that:
- interval hit/error can be mechanically computed;
- outcome evidence may still be DECLARED_UNVERIFIED;
- resolver identity and resolver independence are incomplete.

If outcome labels are weak, meta-learning simply learns patterns in weak labels.

This is more serious than many architecture details.

Priority should be:
prediction provenance
→ immutable outcome source
→ independent resolution
→ reproducible raw evidence snapshot
→ only then meta-learning.

Without this, sophisticated meta-learning creates sophisticated summaries of uncertain history.

## 7. Meta-learning is still statistically immature

The system now has a conservative minimum candidate floor of 50 resolutions.

That is an improvement over tiny-N candidate generation.

But:
- multiplicity control is NOT_IMPLEMENTED;
- permutation test is still REQUIRED_BEFORE_ADAPTATION;
- strata can become small quickly;
- many candidate patterns can be searched;
- cross-domain transfer remains unproven.

Thus meta-learning should continue to generate hypotheses only.

It should not adapt runtime policy automatically.

## 8. Research Adapter is a missing organ, not a minor feature

A system that cannot safely ingest current external knowledge cannot become a broad autonomous learner.

Current state:
- Research Adapter remains blocked;
- research ingestion safety is BLOCKED_NOT_IMPLEMENTED.

This means the self-learning architecture can reason over existing records, but it cannot yet safely perform the full:
question
→ fresh external search
→ source provenance
→ evidence
→ critique
→ learning
loop autonomously.

The current block is appropriate, but it demonstrates that autonomous learning is not operational yet.

## 9. Runtime architecture is carrying too much weight for work that already succeeds through GitHub

Current runtime liveness on main says:
- maintenance plane OFFLINE;
- tunnel DOWN;
- Local Brain connector DOWN.

Yet the project continues useful work:
- Buddhist research;
- audits;
- branch creation;
- PRs;
- canonical GitHub recovery.

This reveals an important architectural fact:

> GitHub is already the practical continuity brain for most knowledge work.

The PC/Local Brain runtime should therefore be treated as an optional execution/support plane for tasks that truly require local compute, secrets, persistent runtime, or desktop interaction.

PR #193 attempted this GitHub-primary / PC-optional simplification but remains open and failed CI.

The unresolved architecture decision is costly: main still carries strong runtime dependencies while actual work proves many workstreams do not need them.

Recommendation:
separate "knowledge continuity" from "local autonomous runtime" explicitly.

## 10. Canonical authority is too duplicated

The same state is often represented across:
- PROJECT_STATE;
- RECOVERY_MANIFEST;
- current Architecture;
- Law Index;
- role bootstrap;
- learning checkpoint files;
- consistency tests.

Redundancy gives safety, but it also creates update fan-out.

The project has already experienced continuity/routing drift.

The current design often requires one conceptual change to update multiple files correctly.

This creates a paradox:
the system built many layers to prevent forgetting, but the number of synchronized surfaces itself becomes a source of forgetting.

Recommendation:
- one machine-readable canonical state registry;
- other human-readable views generated or validated from it;
- laws remain separate because they are normative;
- avoid storing the same CURRENT/NEXT fact independently in many manually edited documents.

## 11. Open PR backlog is now an architectural defect

At review time, open PRs included old and new architecture/learning branches such as:
- #167 self-learning architecture sync;
- #193 GitHub-primary / PC-optional;
- #215 persistent orchestrator law;
- #216 Aṭṭhakavagga lexical audit 1;
- #218 Buddhist master plan;
- #221 / #222 / #224 stacked Buddhist checkpoints;
- #223 lexical audit 2;
plus older open Buddhist PRs.

Some are mergeable, some conflict, some have failed or stale CI, some are stacked on non-main parents.

This means the durable history is strong but the integration queue is becoming a second state machine outside PROJECT_STATE.

A new seat must now understand not only main, but also which open PRs are:
- active;
- stale;
- superseded;
- blocked;
- stacked;
- candidates awaiting review.

That information is not yet cleanly centralized.

Recommendation:
create an explicit PR/task integration registry and aggressively close superseded branches.

## 12. Persistent orchestrator is the right direction but not yet canonical

The Owner's new model is strong:

OWNER
→ ĐIỀU HÀNH
→ work queue
→ replaceable workers
→ reports
→ integration
→ next work

This solves the "chat lifespan" problem better than trying to preserve one immortal conversation.

But PR #215 remains open and currently unmergeable.

Therefore the logical role names and persistent orchestrator rules are not yet fully canonical on main.

More importantly, a permanent orchestrator requires implementation primitives, not only a law:
- task registry;
- assignment status;
- dependency graph;
- worker slot state;
- single-writer generation/epoch;
- stale-writer rejection;
- reported-but-not-integrated queue.

Without those, successor recovery still depends too much on reading scattered PRs and chat reports.

## 13. Three workers should be capacity, not default concurrency

The recent observation that three simultaneous heavy chats are slow is operational evidence.

The architecture should model worker capacity by cost:
- HEAVY: broad source reading / many tools / CI / large synthesis;
- MEDIUM;
- LIGHT.

Recommended default:
- at most 2 HEAVY workers simultaneously;
- third slot LIGHT or STANDBY;
- refill dynamically when a heavy worker becomes blocked on CI or review.

Parallelism should maximize throughput, not the number of chats doing something.

## 14. Security and assurance are becoming the product instead of supporting the product

Security controls are important, especially before autonomous mutation.

But the project has spent substantial effort on:
- lease mechanics;
- external witness design;
- tunnel key state;
- runtime attestation;
- candidate sandboxing;
- critic independence receipts;
- persistence proofs.

Meanwhile Owner-visible learning value still mostly comes from ordinary supervised research and reasoning.

The solution is not to remove security.

The solution is to separate two architectures:

### MINH TRÍ WORK OS
For useful daily work:
- GitHub-first continuity;
- orchestrator;
- workers;
- source discipline;
- review;
- simple task registry.

### MINH TRÍ AUTONOMY LAB
For experimental self-learning/autonomous behavior:
- local runtime;
- trial executor;
- telemetry;
- critic canaries;
- research adapter;
- self-upgrade lease;
- witness/attestation;
- causal learning trials.

The Work OS should not be blocked because the Autonomy Lab is offline.

The Autonomy Lab should not be allowed to mutate the Work OS without its gates.

## 15. Self-critique needs a clearer economic rule

Not every output deserves the full assurance stack.

If every normal task requires:
freeze packet
→ blind critic
→ negative control
→ adjudication
→ revalidation
then the system may spend more effort validating than learning.

Use risk-tiered assurance.

Suggested policy:

LOW:
- direct source check;
- local self-critique;
- durable record if material.

MEDIUM:
- independent worker critique;
- counterevidence;
- explicit uncertainty.

HIGH:
- frozen packet;
- blind critic;
- negative controls;
- adjudication;
- protected promotion.

CRITICAL / autonomy-changing:
- external critic evidence;
- independent resolution;
- preregistered experiment;
- Owner gate.

This preserves rigor without making every learning step expensive.

## 16. The next version should optimize for learning throughput, not architecture count

The project needs fewer new mechanisms and more completed empirical loops.

A strong next milestone is not "Learning Assurance v1.5".

A stronger milestone is:

1. take one genuine historical lesson with clean provenance;
2. freeze it;
3. run it on unseen tasks;
4. compare with compute-matched control;
5. use blinded scoring;
6. inspect failure modes;
7. retain/narrow/retire;
8. show that a later task is better because of that lesson.

One valid closed loop is more valuable than another ten governance concepts.

## 17. Recommended priority order

### P0 — simplify canonical control

1. Decide and integrate the persistent orchestrator model.
2. Create a real task/integration registry.
3. Resolve whether GitHub-primary / PC-optional is the intended architecture.
4. Close or supersede stale/conflicting PRs.
5. Reduce manually duplicated state surfaces.

### P1 — prove one learning loop

1. Audit resolution provenance.
2. Obtain independent critic/judge canary evidence.
3. Build the isolated executor + telemetry + blinded evaluator.
4. Freeze Trial-001 correctly.
5. Run calibration.
6. Do not call it historical learning unless lesson provenance is genuinely ledger-derived.

### P2 — improve worker throughput

1. 2 heavy + 1 light/standby default.
2. Task cost classes.
3. Bounded source packets/context capsules.
4. Work is decomposed by ĐIỀU HÀNH, not by Owner.

### P3 — safe research ingestion

Only after provenance/research safety is implemented:
- open a bounded Research Adapter;
- preserve exact source/citation/conflict records;
- external material starts unverified;
- no automatic lesson promotion.

### P4 — background autonomy last

Only after:
- recovery;
- single-writer protection;
- learning proof;
- research safety;
- rollback;
- audit trail;
- Owner revoke;
are demonstrated.

## 18. Proposed architecture target

A simpler target:

OWNER
→ ĐIỀU HÀNH
→ CANONICAL TASK/STATE REGISTRY
→ WORKERS / CRITICS
→ RESULT PACKETS
→ REVIEW + INTEGRATION
→ GITHUB MAIN

Optional experimental sidecar:

AUTONOMY LAB
→ research
→ candidate lessons
→ trials
→ evidence
→ proposals back to ĐIỀU HÀNH

Never:

AUTONOMY LAB
→ silent canonical mutation.

## 19. Final assessment

### Architecture quality
Strong in safety thinking and auditability.
Weak in simplicity and operational integration.

### Self-learning quality
Good proposal/assurance framework.
Not yet proven behavioral learning.

### Self-critique quality
Useful bounded mechanism.
Independent epistemic critique remains partial.

### Operational quality
GitHub work succeeds.
Local runtime is not currently reliable enough to be central.
Open PR and duplicated-state management are becoming major friction.

### Recommended strategic move
Stop expanding architecture breadth for a short period.
Consolidate.
Close the integration backlog.
Canonicalize the orchestrator.
Build the task registry.
Then prove one real learning loop end-to-end.

The project should now optimize for:

LESS ARCHITECTURE DRIFT
+ FEWER MANUAL STATE SURFACES
+ MORE CLOSED EMPIRICAL LOOPS
+ CLEARER OWNER VALUE.
