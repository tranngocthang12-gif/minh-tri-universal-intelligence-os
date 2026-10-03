# LEARNING PROOF EXECUTION PLAN — 2026-10-04

Status: IMPLEMENTATION HARNESS / OFFLINE-SANDBOX FIRST / NO CLAIM OF LEARNING

## Purpose

Move MINH TRI from proposal governance toward evidence-backed closed-loop learning without
granting autonomous mutation.

## Step 0 — Runtime recovery

Runtime recovery is not required to begin measurement design or ledger audit preparation.
Historical ledger audit must begin from a frozen verified export created without starting
Brain/autonomy runtimes. Runtime recovery is a separate operational workstream.

Fresh runtime PASS later requires:
1. maintenance plane online;
2. secure tunnel /readyz;
3. brain.verify;
4. brain.recovery_packet;
5. fresh runtime commit/build attestation.

Historical receipts never substitute for current liveness.

## Step 1 — Resolution provenance audit

Implemented offline harness: `src/minhtri/resolution_provenance.py`.

Required provenance fields:
- prediction_id / prediction_hash;
- prediction_created_at / due_at;
- evidence_id;
- evidence_content_hash (SHA-256 of raw evidence snapshot);
- evidence_cutoff_timestamp;
- outcome_captured_at;
- observed_value;
- resolver_actor / resolver_method;
- resolution_created_at;
- deterministic interval_hit / absolute_midpoint_error.

Disqualification:
- outcome captured before due_at;
- prediction not frozen before due_at;
- evidence cutoff before due_at;
- missing/invalid hashes;
- evidence snapshot cannot reproduce evidence_content_hash;
- resolver identity/method absent.

Independent audit:
- export/hash the ledger before audit; do not start Brain or background learning merely to read history;
- select/freeze sample before opening original resolution labels;
- Resolver B receives only frozen prediction + exact RAW_SOURCE_SNAPSHOT;
- Resolver B must not see original resolution, model trace, context capsule, or model-authored evidence summary;
- compare outcome-derived metrics;
- both minimum agreement and maximum OUT rate must be preregistered;
- if OUT rate exceeds the preregistered ceiling, the whole audited corpus is ineligible for meta-learning.

No universal agreement threshold is hard-coded yet.

## Step 2 — Canary external critic

Implemented offline scorer: `src/minhtri/critic_canary.py`.

Dataset design:
- clean hard negatives;
- STRUCTURAL canaries;
- SUBTLE_EPISTEMIC canaries;
- historical real defects where available;
- frozen ground-truth defect type + character-span coordinates;
- trap author, rubric author and human adjudicator must be distinct;
- ground truth must not be included in critic packet.

Critic response extension for canary experiments:
- defect_type;
- target_span = [start, end];
- falsification_reason.

Primary metrics:
- False Acceptance Rate;
- False Rejection Rate;
- localization rate;
- subtle-epistemic detection rate.

Thresholds must be preregistered per experiment. Suggested reviewer values such as FAR <=10%
or subtle detection >=80% are hypotheses, not canonical law until preregistered for a run.

## Step 3 — Empirical Learning Assurance v1.4

Design before execution:
- preregister exactly one primary endpoint and one safety endpoint before unblinding;
- changing an endpoint after unblinding invalidates that run;
- private/fresh task set where possible;
- baseline and treatment outputs generated independently;
- randomized presentation order to judges;
- judge blinded to arm;
- generator cannot be sole judge;
- cost-adjusted utility is preregistered alongside accuracy/calibration/unsupported claims;
- latency/token/API cost retained;
- public benchmark contamination risk explicitly recorded;
- sample size chosen from pilot variance/power, not a magical fixed N.

## Step 4 — Behavioral learning trial

Do not use simple before/after comparison.

Use preregistered interleaved randomized A/B assignment on new tasks:
- Control: approved pipeline without trial rule;
- Treatment: same frozen environment plus one bounded TRIAL_RULE;
- independent clean session/process where practical;
- assignment unit = task_id; same task distribution and frozen evaluator;
- first trial routing may use only system-coded domain_id/procedure_id, never failure_class or post-outcome labels;
- TTL + rollback + Owner veto;
- protected targets remain immutable.

A rule is evidence of learning only if it changes future behavior and the treatment improves
preregistered outcome metrics versus concurrent control.

## Current boundary

- background autonomy OFF;
- automatic VERIFIED OFF;
- automatic learning mutation OFF;
- Research Adapter blocked;
- Local Brain runtime currently DOWN/OFFLINE at last fresh observation.


## Causal-proof hardening update

### Stage 1 provenance
- Every new prediction intended for learning must preregister an `outcome_source_spec` before due time:
  source URI, source kind, value selector, and capture rule.
- Historical predictions without immutable preregistered outcome-source proof are pilot-only and are not eligible for meta-learning.
- Resolver B must retrieve/inspect the raw preregistered source snapshot, not a model-authored bundle.
- Report both raw agreement and Cohen's kappa for interval-hit labels.
- Eligibility criteria, minimum agreement, and maximum OUT rate are frozen before opening outcomes.
- If OUT rate exceeds the preregistered ceiling, the audited corpus fails as a whole.

### Stage 2 canary
- Canary datasets are single-use per critic.
- At least half of canary provenance should come from Owner-contributed or historical real defects when available; this is a target for the frozen dataset, not a retroactive claim.
- Do not publish per-defect-type performance when sample size is too small; only aggregate metrics are inferential unless type-specific power was preregistered.
- Candidate A remains rejected by policy hardening and is not revived as an enforcement-path candidate.

### Stage 3 v1.4 benchmark
- Baseline must be named before execution: `V1_3` or `NO_ASSURANCE`; mixing baselines invalidates the run.
- Use paired tasks: the same frozen task goes through baseline and treatment.
- Gold labels and evaluator rubric are completed and hashed before generation.
- Primary endpoints are frozen before unblinding. For the first benchmark use factual accuracy as primary and unsupported-claim rate as safety; all other metrics are secondary/descriptive.
- Cost-adjusted utility, latency, and token/API cost are retained as deployment constraints, not post-hoc winning metrics.

### Stage 4 causal behavioral trial
- Trial-001 uses a paired four-arm design on every eligible frozen task:
  A = control,
  B = lesson-targeted treatment,
  C = compute-matched non-targeted control,
  D = shuffled-ledger placebo synthesized by the same procedure family.
- B must outperform C on the preregistered primary endpoint while satisfying the frozen safety and coverage endpoints.
- D must not materially outperform C; otherwise the learning-specific interpretation is invalid even if B > C.
- B > A alone only shows that extra compute or review may help.
- A learning-from-experience claim additionally requires frozen audited lesson provenance binding the treatment to an audited meta-lesson candidate, audited resolution IDs and audited strata.
- Rollback threshold, evaluation window, compute-parity tolerance and arm-leakage threshold are numeric and frozen before unblinding.
- Outcome scoring must use the Stage-1 resolver contract.
- The first trial may route only by system-coded domain_id/procedure_id.
- Read-only fail-closed TRIAL_RULE consumption is implemented in `src/minhtri/trial_rule_runtime.py`; this proves only plan compilation/data-plane gating, not a live isolated executor or closed-loop learning.

## Operational order

1. Hash/preregister Stage 1 and Stage 2 criteria before observing results.
2. Obtain provider-side proof that the old tunnel key is revoked.
3. When filesystem access is available, create a frozen verified ledger export without starting Brain/autonomy.
4. Run provenance audit on the export.
5. Build a frozen, single-use canary set with Owner/historical contributions and independent human adjudication.
6. Run blind external critics.
7. Run paired v1.4 benchmark with frozen baseline/gold labels/endpoints.
8. Complete external code review of the fail-closed TRIAL_RULE reader and freeze the Trial-001 preregistration/task-set/compute/placebo receipts.
9. Build and validate the live isolated four-arm executor, provider telemetry capture and blinded evaluator path.
10. Only then run the paired A/B/C/D calibration trial; a learning claim additionally requires audited lesson provenance.


## TRIAL_RULE data-plane reader implementation

Implemented components:
- `src/minhtri/trial_rule_runtime.py` compiles a task into one preregistered arm without mutating the ledger.
- Owner-activated lessons may carry a structured `trial_spec` with experiment hash, domain, procedure, overlay and expiry.
- Legacy text-only `scope` remains non-executable.
- Exactly one fresh matching TRIAL_RULE is required; zero or multiple matches fail closed.
- High-stakes domains are blocked.
- Treatment and compute-matched arms must have identical compute budgets.
- Only treatment receives the learned overlay; compute-matched receives equal compute without the lesson-targeted overlay.
- The initial supported overlay is `COUNTEREVIDENCE_FIRST`.
- Runtime plan always declares `write_capability=false`, `automatic_verified_promotion=false`, and `automatic_rule_promotion=false`.

Causal criterion:
- The preregistered primary success rule must require `treatment > compute_matched` on the frozen primary endpoint.
- The shuffled-ledger placebo must not materially outperform compute-matched control under the frozen placebo criterion.
- Actual B/C/D compute telemetry must satisfy the frozen parity tolerance, and coverage must satisfy the frozen non-inferiority endpoint.
- A/B/C/D planning or execution infrastructure existing is not evidence of learning.
- Without audited treatment lesson provenance, a causal Trial-001 PASS is calibration/overlay-value evidence only.
- MINH TRI may claim evidence-backed behavioral learning only after unseen tasks pass the paired four-arm frozen protocol and the treatment lesson is provenance-bound to audited historical resolutions/strata.
