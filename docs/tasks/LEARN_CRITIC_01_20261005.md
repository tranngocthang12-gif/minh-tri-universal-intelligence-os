# TASK ASSIGNMENT — LEARN-CRITIC-01 — 2026-10-05

Status: ASSIGNED / INDEPENDENT CRITIC / NO CANONICAL MUTATION

TASK_ID: LEARN-CRITIC-01
Role: independent self-learning / evaluation critic
Review target main commit: 904e4f3b0bced1fcba760045a65041b80bcdf08d
Primary critique draft to challenge:
docs/critic/PROJECT_ARCHITECTURE_SELF_LEARNING_CRITIQUE_20261005.md
Review mode: adversarial, evidence-bounded, independent from the architecture critic.

Objective:
Attack the self-learning, self-critique, meta-learning, Learning Assurance, Trial-001 and research-ingestion design for causal validity, evaluation contamination, independence, statistics, Goodhart/reward-hacking risk, and false claims of learning.

Required questions:
1. Is PROPOSAL_GOVERNANCE_PIPELINE_NOT_AUTONOMOUS_BEHAVIOR_ADAPTATION the correct current classification?
2. What exact evidence would be required to claim behavioral self-learning?
3. Can resolution provenance currently support meta-learning?
4. Is critic independence adequate for any strong assurance claim?
5. Is paired four-arm Trial-001 sufficient to distinguish learned-value from extra compute/placebo?
6. What failure modes remain: leakage, judge bias, arm identification, verbosity/coverage tradeoff, placebo weakness, multiple testing, selective task replacement?
7. Is minimum N=50 meaningful without multiplicity/power evidence?
8. What should the permutation test and multiplicity control actually protect?
9. What research-ingestion gates are mandatory before autonomous search?
10. Which claims in the orchestrator critique are too strong or too weak?
11. Propose the minimal empirical sequence that could legitimately upgrade the system from proposal-governance to evidence-backed behavioral learning.

Required output:
- VERDICT: DEFECT_FOUND / NO_MATERIAL_DEFECT_FOUND
- TOP_MATERIAL_DEFECTS with severity
- LEARNING_CLAIMS_SUPPORTED
- LEARNING_CLAIMS_NOT_SUPPORTED
- CRITIC_INDEPENDENCE_ASSESSMENT
- RESOLUTION_PROVENANCE_ASSESSMENT
- TRIAL001_ASSESSMENT
- META_LEARNING_STATISTICS_ASSESSMENT
- RESEARCH_INGESTION_ASSESSMENT
- STRONGEST_COUNTERARGUMENTS_TO_MAIN_CRITIQUE
- MINIMUM_PROOF_LADDER
- FINAL_ADVICE
- DURABLE_LOCATION
- READY_FOR_NEXT_TASK

Constraints:
- Fresh-read canonical main before review.
- Do not rely on chat memory.
- Do not read the result of ARCH-CRITIC-01 before submitting your own report.
- Do not modify law, PROJECT_STATE, Recovery Manifest, or current checkpoints.
- Do not merge PRs.
- Do not call any pipeline VERIFIED from design documents alone.
