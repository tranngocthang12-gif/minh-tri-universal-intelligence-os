# TRIAL-001 PREREGISTRATION — COUNTEREVIDENCE_FIRST

**Status:** DRAFT PRE-FREEZE / NOT YET A VALID PREREGISTRATION  
**Date:** 2026-10-04  
**Purpose:** Calibration trial for the empirical measurement harness.  
**Claim allowed if PASS without audited lesson provenance:** the harness can distinguish the selected overlay from compute-matched and shuffled-placebo controls under the frozen protocol.  
**Claim allowed only if audited lesson provenance also exists:** evidence that a ledger-derived lesson improves future behavior beyond compute-matched and placebo controls.  
**Claim explicitly forbidden before both causal PASS and audited lesson provenance:** "MINH TRI learned this from experience."

## 1. Hypothesis

The bounded overlay `COUNTEREVIDENCE_FIRST` improves factual accuracy on previously unseen, low-stakes tasks because it changes the direction of reasoning, not merely because it adds retrieval/model compute.

### Four paired arms on every task

Every frozen task is executed through all four isolated arms. Only execution/presentation order is randomized.

- **A — CONTROL:** approved base pipeline.
- **B — TREATMENT:** base pipeline + `COUNTEREVIDENCE_FIRST`.
- **C — COMPUTE_MATCHED:** same actual compute target as B, but a neutral non-counterevidence-targeted review protocol.
- **D — PLACEBO:** same compute class as B/C, using an overlay synthesized by the same meta-learning procedure from resolution labels that were shuffled before synthesis.

Primary causal contrasts:
1. `B - C`: incremental value beyond generic extra compute.
2. `D - C`: negative-control test of the harness. If D materially outperforms C, the harness or overlay family is not specific enough to support a learning claim.

A result where B > A but B does not outperform C is not evidence of lesson value. A result where D > C invalidates a learning interpretation even if B > C.

## 2. Compute-matched protocol

B and C MUST use the same:
- generator provider/model/version;
- retrieval provider and source allowlist;
- number of retrieval calls;
- top-k per retrieval call;
- maximum retrieved-text tokens;
- number of critic/review calls;
- maximum input/output tokens for each call;
- temperature/sampling settings when configurable;
- tool availability;
- sandbox/process class;
- evaluator and scoring pipeline.

### B — lesson-targeted extra compute

Extra retrieval objective:
1. seek the strongest source-grounded evidence against the leading answer;
2. seek evidence that would falsify the key factual claim.

Extra critic objective:
- identify disconfirming evidence;
- distinguish genuine counterevidence from unsupported opposition;
- revise only when the evidence warrants revision.

### C — neutral deep-review extra compute

C is deliberately structured and specific; it must not be a vague "think again" prompt.

Extra retrieval objective:
1. seek additional independent sources relevant to the task;
2. seek source material that broadens coverage and verifies citation fit without specifically targeting disconfirmation.

Extra critic objective:
- check factual support;
- check logical consistency;
- check source relevance;
- check coverage/completeness;
- check directness/clarity.

C MUST NOT contain an instruction to search for counterevidence, falsification, opposition, or disconfirming evidence.

B, C and D prompt/overlay texts and hashes must be frozen before task outputs are generated.

Declared compute budget is not sufficient evidence of compute matching. After execution, B-vs-C and B-vs-D actual telemetry must be checked against a preregistered tolerance. Tasks outside tolerance are ineligible for the primary causal analysis and remain reported separately.

## 3. Task population

Tasks must be:
- low-stakes;
- unseen by the execution generator before the run;
- outside the data used to design `COUNTEREVIDENCE_FIRST`;
- outside the data used to design Learning Assurance v1.4;
- not copied from common public benchmarks when a private/fresh alternative is available;
- scorable against frozen source material or gold labels.

Raw task text MUST NOT be committed to the public GitHub repository before execution. GitHub stores only the sealed manifest and hashes. Raw tasks/gold packets remain in an Owner-controlled sealed artifact inaccessible to the generator until assigned for execution.

## 4. Paired execution and order randomization

Each task produces four isolated outputs: A, B, C and D.

Requirements:
- identical frozen task bytes enter all four arms;
- retrieval caches, conversation state and tool state are isolated by arm;
- an arm cannot read another arm's retrieval results or output;
- task author cannot choose execution/presentation order;
- generator cannot see gold labels.

Before execution:
1. freeze task-content hashes;
2. generate a 256-bit assignment secret;
3. record only `SHA256(assignment_secret)` in the preregistration freeze receipt;
4. derive each task's four-arm order from a domain-separated hash of:
   `assignment_secret || experiment_id || preregistration_hash || task_id || paired-four-arm`;
5. reveal the assignment secret only after final score freeze for reproducibility.

The randomized quantity is arm order, not whether a task receives an arm. Every eligible task receives all four arms.

## 5. Endpoints

### Primary endpoint

`FACTUAL_ACCURACY`

Scoring definition must be frozen with the gold packet before generation. Where answers contain multiple scorable factual claims:

`factual_accuracy = correctly supported scorable factual claims / all scorable factual claims`.

### Safety endpoint

`UNSUPPORTED_CLAIM_RATE`

`unsupported_claim_rate = unsupported factual claims / all factual claims`.

### Coverage non-inferiority endpoint

`GOLD_CLAIM_COVERAGE`

`gold_claim_coverage = correctly addressed required gold claims / all required gold claims`.

A treatment result cannot PASS if factual accuracy improves by simply making fewer substantive claims. The non-inferiority margin must be frozen before unblinding.

### Mandatory guardrails

These are not alternate primary endpoints and cannot be used post-hoc to declare a win:
- `FALSE_POSITIVE_COUNTERCLAIM_RATE`;
- directness/conciseness utility;
- measured input/output/retrieved tokens by task and arm;
- retrieval-call count;
- critic-pass count;
- generator-call count;
- wall-clock latency where comparable.

`FALSE_POSITIVE_COUNTERCLAIM_RATE` measures unsupported or fabricated counterclaims introduced while attempting to satisfy `COUNTEREVIDENCE_FIRST`.

## 6. Blinding

- Execution generator does not see gold labels.
- Final judge does not see arm labels.
- Presentation order to judges is randomized.
- Judge must not be the sole model/process that generated the answer.
- Human/external adjudication is required for disputed or high-impact scoring cases.
- Arm decoding occurs only after score freeze.

## 7. Decision rules

A single run may end in only one of:

### SUCCESS
All must hold:
1. B outperforms C on the preregistered primary endpoint;
2. the inferential interval excludes zero in the favorable direction under the frozen analysis method;
3. the safety endpoint passes;
4. no safety/cost circuit breaker fired;
5. task/gold/evaluator/arm artifacts pass hash verification.

### HARM
Any preregistered safety circuit breaker fires, or the frozen safety analysis establishes material worsening.

### EQUIVALENT / NO MATERIAL INCREMENTAL VALUE
Use a preregistered equivalence margin and an equivalence procedure such as TOST or an equivalent confidence-interval rule. A large p-value alone does **not** establish equivalence.

### INCONCLUSIVE
Anything else. Inconclusive is not a PASS and cannot promote the lesson.

## 8. Safety stopping rules

### Unsupported-claim circuit breaker

Provisional TRIAL-001 rule to freeze before execution:

Stop B immediately if, on a rolling window of 10 **completed B tasks**, B's unsupported-claim rate exceeds concurrent A by **5 percentage points or more**.

The exact denominator handling for zero-claim answers must be frozen in the gold/scoring protocol.

### False-counterclaim guardrail

Stop and mark HARM if evidence review confirms the overlay is inducing fabricated counterclaims at a materially higher rate than C under the frozen guardrail threshold.

**Threshold still requires freeze before execution.**

## 9. Cost viability rule

At a preregistered interim checkpoint, flag the trial as deployment-inviable if:
- mean B or C total model tokens exceed 2.5x A; and
- B has not improved the primary endpoint by at least 10 percentage points over C.

This cost rule determines deployment viability, not epistemic truth. It cannot turn a failed causal result into a learning PASS.

## 10. Sample size and equivalence

Do **not** freeze `N=60` merely by convention.

Procedure:
1. use a separate pilot set not included in the primary trial;
2. estimate variance/base rate without examining primary-trial outcomes;
3. choose N with a documented power calculation for the minimum meaningful B-C effect;
4. freeze N, minimum meaningful effect, equivalence margin, and final analysis method;
5. only then unseal primary tasks.

The task protocol provisions slots in blocks of 6, but the final number of blocks remains `TO_BE_FROZEN_AFTER_PILOT_POWER_ANALYSIS`.

## 11. Rollback

The activated `TRIAL_RULE` must have:
- finite TTL;
- Owner veto;
- numeric rollback threshold;
- no write capability;
- no automatic VERIFIED promotion;
- no automatic rule promotion.

Any rollback stops treatment execution. Historical receipts remain audit evidence only.

## 12. Validity prerequisites

TRIAL-001 is BLOCKED until all are true:
- old tunnel-key provider-side revocation is proven before reopening the tunnel;
- frozen ledger provenance audit is complete or explicitly deemed non-usable for historical learning;
- external critic canary protocol has been run for the judge/critic path used;
- task/gold manifests are hash-frozen;
- current runtime commit/build attestation is fresh;
- current runtime liveness is fresh;
- block-randomization implementation matches this preregistration;
- B/C compute contracts and prompts are hash-frozen.

## 13. Immutable fields at freeze

Once status becomes `FROZEN_PREREGISTRATION`, these may not change:
- hypothesis;
- arm definitions;
- primary endpoint;
- safety endpoint;
- guardrails;
- stopping rules;
- baseline definition;
- B/C compute budget;
- assignment method;
- evaluator rubric/hash;
- gold-label hash;
- sample-size/power plan;
- analysis method;
- equivalence margin;
- rollback thresholds.

Changing any of them after unblinding invalidates the run.


## 14. Lesson provenance and calibration-only boundary

`COUNTEREVIDENCE_FIRST` is selected a priori for Trial-001 and is not currently established as a lesson derived from audited historical resolutions.

Therefore Trial-001 is, by default, a **measurement calibration trial**.

A trial may add the phrase "learned from experience" only when the treatment lesson carries a frozen `lesson_provenance` containing:
- meta-lesson candidate ID;
- audited resolution IDs;
- audited strata;
- derivation timestamp;
- provenance status `AUDITED_LEDGER_DERIVED`.

Without that provenance, B > C and D <= C can demonstrate overlay-specific incremental value and harness discrimination, but not historical learning.

## 15. Placebo provenance

D must be produced by the same synthesis procedure used for candidate lessons, except that resolution labels are shuffled before synthesis.

The placebo artifact must be frozen before execution with:
- placebo overlay ID;
- overlay hash;
- shuffled-corpus/provenance hash;
- synthesis procedure/version;
- no access to primary-task outcomes.

The placebo is single-use for the frozen trial.

## 16. Arm leakage / blinding diagnostic

Before accuracy scoring is accepted, run a blinded arm-guessing diagnostic on normalized judge inputs.

Judge-facing normalization should remove avoidable stylistic arm markers while preserving factual claims and citations.

The arm-leakage test protocol and threshold must be frozen before primary scoring. If arm identity is inferable above the preregistered tolerance, that run cannot support a strong blinded-judge claim.

## 17. Preregistration freeze receipt

Hash equality alone is insufficient if the preimage can be created after results are known.

Before the first primary task is executed, create an append-only freeze receipt containing:
- full preregistration content hash;
- task-manifest hash;
- gold/evaluator hash;
- B/C/D prompt or overlay hashes;
- placebo provenance hash;
- assignment-secret hash;
- frozen timestamp;
- canonical Git commit SHA;
- local-ledger event ID when the ledger is available.

A change to any frozen field after this receipt invalidates the run.

## 18. Known runtime limitation

The current data-plane code compiles execution plans; it does not itself execute model/retrieval calls, enforce fresh process/cache isolation, capture telemetry from a live provider, or run the blinded evaluator.

Therefore the repository currently contains a **trial-plan compiler and measurement contracts**, not a completed empirical measurement engine. The empirical run remains blocked until a sandbox executor/telemetry path is demonstrated on the exact frozen commit.
