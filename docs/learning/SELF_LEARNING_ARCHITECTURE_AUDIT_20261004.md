# SELF-LEARNING ARCHITECTURE AUDIT — 2026-10-04

**Status:** CURRENT CANONICAL SYNC AUDIT / NO CLAIM OF AUTONOMOUS LEARNING  
**Source main before this sync:** `ffc9ab4762ce53322c5b4bea44b773deeac1d283`

## Scope checked

- `docs/PROJECT_STATE.json`
- `docs/LAW_INDEX_20261003.md`
- `docs/ARCHITECTURE_NOW_20261003.md`
- `docs/RECOVERY_MANIFEST.json`
- `docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md`
- `docs/learning/LEARNING_PROOF_EXECUTION_PLAN_20261004.md`
- `docs/learning/TRIAL001_COUNTEREVIDENCE_PREREGISTRATION_DRAFT_20261004.md`
- `docs/learning/TRIAL001_TASKSET_PROTOCOL_20261004.md`

## Synchronization result

The current authority surfaces agree on the core boundary:

- background autonomous-learning, automatic self-critique and meta-learning runtimes remain OFF;
- the current system is a proposal-governance learning pipeline, not proven autonomous behavior adaptation;
- Research Adapter remains fail-closed until fresh-seat and current-liveness gates pass;
- Trial-001 is a paired four-arm calibration harness: CONTROL / TREATMENT / COMPUTE_MATCHED / PLACEBO;
- `COUNTEREVIDENCE_FIRST` is not currently proven to be a ledger-derived lesson;
- a learning-from-experience claim requires audited lesson provenance bound to an audited meta-lesson candidate, audited resolution IDs and audited strata;
- Trial-001 remains NOT FROZEN and NOT RUN;
- a live isolated executor, provider telemetry capture and blinded evaluator runtime are not yet proven;
- external code review of the TRIAL_RULE reader remains required;
- resolution provenance independence, external critic evidence, empirical v1.4 benefit, multiplicity control/permutation testing and research-ingestion safety remain open.

## Drift found and repaired

`LEARNING_PROOF_EXECUTION_PLAN_20261004.md` still contained an older three-arm A/B/C description and stated that TRIAL_RULE data-plane consumption was not implemented. That conflicted with current `PROJECT_STATE`, current architecture and merged PRs #164/#166.

This sync updates the plan to:

- paired four-arm A/B/C/D semantics;
- implemented read-only fail-closed TRIAL_RULE reader semantics;
- explicit placebo, compute-parity and coverage gates;
- explicit audited lesson-provenance requirement for any learning-from-experience claim;
- current next steps: external reader review, frozen preregistration artifacts, live isolated executor/telemetry/evaluator, then empirical run.

## Runtime note

A fresh Local Brain check during this audit failed because the tunnel client had not been seen for 300 seconds. This is consistent with the canonical current-liveness state being DOWN/OFFLINE. Historical PASS evidence is not current proof.

## Conclusion

Architecture semantics are synchronized after the plan repair. The self-learning subsystem is **not proven as closed-loop learning**. The next valid proof sequence remains: restore/attest runtime as needed, audit resolution provenance, validate the critic/judge path, freeze Trial-001, build live isolated execution telemetry, and only then run the empirical calibration/learning test.
