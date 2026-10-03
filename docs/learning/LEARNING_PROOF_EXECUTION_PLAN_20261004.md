# LEARNING PROOF EXECUTION PLAN — 2026-10-04

Status: IMPLEMENTATION HARNESS / OFFLINE-SANDBOX FIRST / NO CLAIM OF LEARNING

## Purpose

Move MINH TRI from proposal governance toward evidence-backed closed-loop learning without
granting autonomous mutation.

## Step 0 — Runtime recovery

Runtime recovery is required before reading/writing the local brain, but not before creating
or testing offline GitHub harnesses.

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
- select/freeze sample before opening original resolution labels;
- second resolver receives the frozen prediction + exact evidence snapshot;
- compare outcome-derived metrics;
- agreement threshold must be preregistered before audit.

No universal agreement threshold is hard-coded yet.

## Step 2 — Canary external critic

Implemented offline scorer: `src/minhtri/critic_canary.py`.

Dataset design:
- clean candidates;
- STRUCTURAL canaries;
- SUBTLE_EPISTEMIC canaries;
- frozen ground-truth defect type + character-span coordinates;
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

Use interleaved randomized A/B assignment on new tasks:
- Control: approved pipeline without trial rule;
- Treatment: same frozen environment plus one bounded TRIAL_RULE;
- independent clean session/process where practical;
- same task distribution and frozen evaluator;
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
