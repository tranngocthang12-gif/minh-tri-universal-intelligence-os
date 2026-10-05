# MINH TRÍ — INDEPENDENT SELF-LEARNING / EVALUATION CRITIC — LEARN-CRITIC-01

Review date: 2026-10-05  
Role: independent self-learning / evaluation critic  
Review target: `904e4f3b0bced1fcba760045a65041b80bcdf08d`  
Fresh-read main observed before review: `1f2eef8a0e8ed946020e4de32f099cbbb1a07a72`  
Primary critique reviewed: `docs/critic/PROJECT_ARCHITECTURE_SELF_LEARNING_CRITIQUE_20261005.md` from PR #226 because that file was not present on canonical main/target at review time.  
Independence boundary: result of ARCH-CRITIC-01 was not read.

TASK_ID: LEARN-CRITIC-01

VERDICT: DEFECT_FOUND

## TOP_MATERIAL_DEFECTS

1. **HIGH — Meta-learning does not enforce resolution-provenance eligibility end-to-end.**  
   `meta_learning_report()` and `stratified_meta_learning_report()` consume any resolution row having `interval_hit` and `absolute_midpoint_error`. They do not require `learning_provenance_status == OUTCOME_SOURCE_PREREGISTERED`, an independent provenance-audit PASS, or membership in an audited-resolution allowlist. The tests explicitly demonstrate that 50 bare resolution dictionaries can produce a `META_LESSON_CANDIDATE`. This conflicts with the canonical state claim that invalid provenance is excluded from meta-learning. Because the runtime remains proposal-only, this is not an autonomous mutation bug, but it is an epistemic defect in the candidate-generation path.

2. **HIGH — `AUDITED_LEDGER_DERIVED` lesson provenance is shallow metadata, not a verified audit linkage.**  
   `propose_lesson` checks the status string, nonempty candidate ID, existing resolution IDs, strata, and timestamp. It does not verify an audit receipt, frozen-ledger-export hash, raw-evidence verification receipt, resolver-independence result, derivation procedure/version, or that the stated strata and candidate actually derive from the referenced audited resolutions. `trial_rule_runtime` then treats the same shallow fields as sufficient to set `learning_claim_eligible=true`. Therefore the strongest current learning-claim gate can be satisfied by a structurally valid assertion rather than by a bound proof object.

3. **HIGH — Trial-001's post-run compute-mismatch exclusion can introduce post-treatment selection bias.**  
   The draft says tasks outside B/C telemetry tolerance become ineligible for the primary causal analysis. But token use, retrieval size, and other measured compute can themselves be affected by the treatment. Removing tasks after observing a treatment-dependent variable can change the analyzed task population. The primary analysis should remain intention-to-treat over all valid randomized task units, while budget deviations are reported as protocol deviations/sensitivity analyses, or the executor must hard-enforce budgets before/during execution so eligibility is not decided from downstream behavior.

4. **HIGH BEFORE ACTIVATION — Research Adapter safety is not enforced at the adapter boundary.**  
   The research gate is fail-closed today, which is correct. But if the canonical gate opens and an adapter exists, `build_autonomy_packet` accepts any returned list and labels it `UNVERIFIED_RESEARCH_PROPOSALS`; it does not validate a strict provenance schema, source bytes/content hash, retrieval timestamp, citation locator, redirect/final URL, content type, freshness, deduplication, conflict status, prompt-injection isolation, or secret/privacy constraints. `record_research_trace` is useful downstream metadata, but it is not a safe-ingestion validator. Fresh-seat/liveness proof is therefore necessary but not sufficient to open research.

5. **MEDIUM — Critic canary PASS can be statistically weak at tiny N.**  
   The canary scorer has useful FAR/FRR/localization/subtle-error metrics and distinct-role requirements, but the PASS logic has no minimum defect/clean/subtle counts, confidence interval, or power requirement. The current unit test can pass a dataset containing one bad case and one clean case. A canary PASS should therefore be treated as a measurement result only after sample-size/uncertainty criteria are frozen.

6. **MEDIUM — Trial-001 still has Goodhart/leakage pathways despite its four-arm design.**  
   Factual-accuracy-as-a-ratio can be improved by changing claim granularity or saying less; coverage noninferiority helps but depends on a complete frozen gold claim set and stable atomic-claim extraction. Style/structure can reveal arm identity. Judge normalization can itself alter evidence presentation. Replacement and compute exclusions can create selection effects. These must be frozen and audited at the task level, with the task—not individual claims—as the primary independent unit.

7. **MEDIUM — The statistical floor `N=50` is not an inferential guarantee.**  
   It is only an anti-tiny-sample/descriptive floor. It does not control power, minimum detectable effect, dependence, repeated candidate search, multiple strata, multiple endpoints, sequential stopping, or winner's curse. Multiplicity and selection must be handled by a frozen analysis plan; otherwise a 50-resolution candidate can still be a data-mined false pattern.

## LEARNING_CLAIMS_SUPPORTED

- The current classification `PROPOSAL_GOVERNANCE_PIPELINE_NOT_AUTONOMOUS_BEHAVIOR_ADAPTATION` is **correct**.
- The code contains real proposal-only governance primitives: claims, predictions, freeze/resolve mechanics, critic/adjudication records, frozen learning packets, negative controls, lesson lifecycle gates, and a read-only trial-rule plan compiler.
- Core resolution scoring is mechanically stronger than a purely declared score: for an eligible `record_resolution`, interval hit and midpoint error are computed from the frozen prediction and numeric outcome evidence.
- New predictions can preregister an `outcome_source_spec`; legacy predictions without it are explicitly marked not meta-learning eligible at resolution time.
- Critic packets can be blind, redacted, and hash-bound. Current independence semantics are deliberately conservative rather than claiming full independence.
- Trial-001's paired four-arm structure is a materially better causal design than control-vs-treatment alone because B-C targets lesson-specific incremental value beyond generic extra review and D-C probes specificity to true historical labels.
- The current runtime does **not** have autonomous durable write, automatic VERIFIED promotion, or a completed live empirical trial engine.

## LEARNING_CLAIMS_NOT_SUPPORTED

The evidence at the review target does **not** support:

- "MINH TRÍ autonomously self-learns" in the behavioral sense.
- "Meta-learning currently uses only independently audited outcomes."
- "A lesson marked `AUDITED_LEDGER_DERIVED` is cryptographically/evidentially proven to have been derived from audited ledger history."
- "Critic independence is epistemically proven."
- "Learning Assurance v1.4 improves real-world outcomes."
- "Trial-001 has demonstrated causal lesson value."
- "`COUNTEREVIDENCE_FIRST` was learned from project history."
- "Reward hacking or evaluation contamination is generally detected."
- "Research ingestion is safe to activate."
- "Cross-domain behavioral transfer is established."
- "The system can autonomously retain/narrow/retire rules based on replicated outcome evidence."

A defensible future claim after one successful scoped trial is: **evidence-backed behavioral learning for one frozen lesson in one frozen scope**. That is still narrower than a general claim that the whole system "self-learns."

## CRITIC_INDEPENDENCE_ASSESSMENT

Current strength: **PARTIAL / USEFUL AS ADVERSARIAL EVIDENCE / NOT A PROVEN INDEPENDENT ORACLE**.

What is genuinely useful:
- proposer/predictor/critic provider IDs are separated in several ledger paths;
- blind critic packets can omit learner reasoning and prior critic context;
- packets/results can be hash-bound;
- execution-environment/authority receipts can record process separation;
- canary scoring can measure false acceptance, false rejection, localization and subtle-error detection.

What is not established:
- provider/model identity is not cryptographically tied to the actual independent reasoning actor in the manual channel;
- distinct provider IDs do not prove distinct underlying model priors, training corpus, infrastructure, or operator influence;
- shared project framing can create correlated errors;
- process separation is not epistemic independence;
- canary performance measures critic reliability on a frozen distribution, not philosophical independence.

The right claim is therefore: **bounded blind/process-separated adversarial review with recorded provenance**, not "independent truth verification."

For stronger assurance, freeze a single-use canary with adequate defect/clean/subtle counts, uncertainty bounds, predeclared thresholds, and provider-side/external execution evidence. Even then, treat the critic as one noisy measurement channel.

## RESOLUTION_PROVENANCE_ASSESSMENT

Current state: **NOT YET SUFFICIENT FOR META-LEARNING ADAPTATION**.

The critique underestimates one part of the implementation: core already computes `interval_hit` and `absolute_midpoint_error` mechanically and supports a preregistered outcome-source specification. The principal defect is not the arithmetic; it is provenance binding and downstream enforcement.

Required repairs:
1. Bind each eligible resolution to a frozen-ledger-export hash and exact raw outcome snapshot hash.
2. Verify the raw bytes in the batch audit itself, not only through a separate optional helper.
3. Bind/verify execution of `value_selector` and `capture_rule`, rather than checking only source URI/kind and timestamps.
4. Require independent-resolver evidence beyond a distinct actor string where independence matters.
5. Emit a durable audit receipt listing exactly which resolution IDs passed and which failed.
6. Make meta-learning consume only that audit-passed allowlist; legacy/invalid rows must be impossible to enter candidate statistics.
7. Bind lesson provenance to the audit receipt, synthesis procedure/version/hash, input resolution IDs, strata, candidate artifact hash and derivation timestamp.

Until that is wired end-to-end, historical resolutions are suitable for audit preparation and descriptive diagnostics, not for a strong meta-learning claim.

## TRIAL001_ASSESSMENT

Current assessment: **GOOD CALIBRATION DESIGN / NOT YET A LEARNING PROOF / REQUIRES STATISTICAL AND EXECUTION HARDENING**.

### What the four arms can distinguish

- **A vs B**: total effect of adding the lesson-targeted pipeline versus base.
- **B vs C**: incremental value of the targeted lesson direction beyond generic extra retrieval/review under a compute-matched contract.
- **D vs C**: whether an overlay synthesized from shuffled historical labels produces similar gains; this probes whether real historical label structure is doing useful work or whether the overlay/synthesis family gives generic benefits.

This is substantially better than a simple A/B test.

### What it cannot establish by itself

Even a clean B > C does not establish historical learning unless B's lesson is itself produced from audit-passed historical outcomes by a frozen derivation procedure. Without that, it establishes only that `COUNTEREVIDENCE_FIRST` is a useful intervention.

Also, exact token/call matching does not fully equalize hidden model compute or qualitative retrieval difficulty. The claim should be "compute-contract matched to observed telemetry," not "identical internal compute."

### Remaining failure modes

- **Leakage:** task/gold leakage into generator, overlay-design leakage into task authorship, cache/session/retrieval contamination across arms, judge exposure to arm markers.
- **Judge bias:** style/length/source-count preferences can masquerade as factual quality; one model judge can share generator priors.
- **Arm guessing:** B/C/D instructions can leave lexical/structural fingerprints. Run guessing on both frozen raw judge inputs and any normalized representation; normalization itself must be deterministic and hash-frozen.
- **Verbosity/coverage gaming:** micro factual-accuracy ratios can change when answers split/merge claims or omit difficult claims. Freeze atomic-claim rules, required-gold coverage and preferably task-level paired summaries.
- **Placebo weakness:** a shuffled-label overlay may be incoherent, stylistically distinct, or obviously weaker. Placebo generation must be matched for plausibility, length, specificity, synthesis procedure and compute. D > C should invalidate a claim that correct historical labels caused the gain; it does not necessarily mean the entire harness is broken.
- **Multiple testing:** many lessons/strata/endpoints/guardrails create opportunity to select a winner post hoc.
- **Replacement bias:** current mechanical replacement rules are directionally good, but replacement should occur before any arm outcome is inspected. All replacements and missing arms must be reported.
- **Post-treatment compute filtering:** primary analysis should not drop tasks merely because treatment changed token/retrieval use.
- **Sequential stopping:** safety stopping is justified, but inferential claims must account for planned interim looks/stopping.
- **Model/version drift:** provider/model revision between arms or across the run can invalidate paired comparability.
- **Correlated task families:** many near-duplicate tasks inflate nominal N while effective N stays small.

## META_LEARNING_STATISTICS_ASSESSMENT

### Meaning of minimum N=50

`N=50` has a legitimate but narrow meaning: it blocks candidate generation from trivially tiny histories and can stabilize descriptive summaries somewhat.

It does **not** establish:
- adequate power;
- a meaningful minimum detectable effect;
- Type-I error control;
- multiplicity control;
- independence/effective sample size;
- robustness across strata;
- validity after searching many candidate patterns.

The actual sample size must be derived from the frozen estimand, paired variance/base rate, minimum meaningful effect, desired power, and stopping/multiplicity plan.

### What the permutation test should test

There are two distinct useful permutation tests:

1. **Meta-learning selection test.** Under the null that historical predictors/procedure/strata contain no outcome signal beyond chance, shuffle resolution/outcome labels within the appropriate frozen strata, rerun the **entire candidate-selection/synthesis procedure**, and compare the observed candidate statistic against the null distribution. Re-running candidate selection is essential; otherwise the test ignores winner's curse from searching many candidate lessons. If many candidates/strata are searched, use a max-statistic/Westfall-Young style familywise procedure or another preregistered multiplicity method.

2. **Trial-001 paired randomization inference.** For the frozen primary B-C contrast, swap/sign-flip B and C labels **within task** under the paired null, preserving blocks/strata and using the preregistered task-level statistic. Do not permute individual factual claims as if they were independent observations.

If D-C is used inferentially, preregister it as a separate negative-control family or hierarchical gate. If interim efficacy looks are allowed, the randomization/permutation analysis must honor the sequential design or use a separate alpha-spending/always-valid plan.

## RESEARCH_INGESTION_ASSESSMENT

Current state: **CORRECTLY BLOCKED; DO NOT OPEN ON FRESH-SEAT/LIVENESS ALONE**.

Mandatory gates before activation:

1. **Strict typed ingress schema**: query, requested URL/source ID, final URL, retrieval timestamp, provider/tool, status, content type, source kind/role, rights/privacy classification, citation locator, exact content hash and bounded raw snapshot.
2. **Untrusted-content isolation**: retrieved text is data, never executable instruction; page content cannot change system/tool policy, request secrets, broaden permissions, or cause writes/actions.
3. **Source policy**: domain/source allow/deny controls, size/content-type limits, redirects recorded, private/authenticated sources explicitly scoped.
4. **Freshness/versioning/deduplication**: repeated or changed sources retain separate hashes and timestamps; stale material is marked rather than silently overwritten.
5. **Conflict/counterevidence capture**: ingestion records support/contradiction/unknown status without converting popularity or search rank into truth.
6. **No promotion on ingestion**: all external material enters as unverified research evidence; claim, critic, lesson and trial gates remain separate.
7. **Reproducibility/audit receipts** where source persistence permits; if a source cannot be snapshotted/replayed, that limitation is explicit.
8. **Adversarial test suite**: prompt-injection pages, poisoned/citation-spoofed pages, stale/changed pages, redirects, malformed documents, hidden instructions, duplicate sources and unavailable sources.
9. **Budget/kill switch**: bounded calls/tokens/data volume, timeout/failure behavior, and Owner-controlled scope expansion.
10. **Privacy/secret guard**: no leakage of project secrets or private context into external queries unless explicitly authorized.

Only after these pass should the canonical research gate move from blocked to bounded read-only research.

## STRONGEST_COUNTERARGUMENTS_TO_MAIN_CRITIQUE

The main critique is directionally strong, but several points need narrowing.

### Claims that are somewhat too strong

1. **Research Adapter is not a prerequisite to prove behavioral learning.**  
   A valid learning proof can be run entirely on sealed first-party/private/synthetic auditable data. Research ingestion is required for broad autonomous current-knowledge learning, not for the first causal proof that a ledger-derived lesson improves future behavior.

2. **Resolution provenance is stronger than the critique suggests at the mechanical level.**  
   The core already supports outcome-source preregistration and computes forecast metrics mechanically. The open problem is independent/raw-source provenance and its enforcement through meta-learning, not absence of scoring machinery.

3. **Full epistemic critic independence is not required for every useful assurance claim.**  
   A critic with strong, preregistered single-use canary performance can be valuable even when shared priors prevent a proof of total independence. The system should measure critic reliability rather than wait for an impossible absolute-independence standard.

4. **D > C should not automatically be called a broken harness.**  
   It is strong evidence against the claim that correct historical resolution labels uniquely caused B's advantage. But it can also reveal that the synthesis family produces a generic useful regularizer. That invalidates the historical-learning interpretation for that run, not necessarily the measurement apparatus.

5. **Architecture complexity and PR backlog are operational concerns, not direct causal-learning falsifiers.**  
   They may reduce reliability and throughput, but a scoped learning experiment can still be valid if its frozen execution boundary is clean.

### Claims that are too weak / miss material implementation defects

1. The critique does not identify that current meta-learning code actually consumes unaudited/legacy resolution rows despite the state-level exclusion claim.
2. It does not identify that `AUDITED_LEDGER_DERIVED` is currently a shallow asserted metadata gate rather than a receipt-bound proof.
3. It does not identify post-treatment selection bias created by excluding B/C compute-mismatch tasks from primary analysis.
4. It under-specifies statistical requirements: power/MDE, task-level dependence, multiplicity, winner's curse, sequential stopping and replication.
5. It under-specifies critic-canary sample-size uncertainty; tiny datasets can currently satisfy the PASS predicate.

## MINIMUM_PROOF_LADDER

The shortest defensible path from proposal-governance to evidence-backed behavioral learning is:

1. **Freeze one eligible historical corpus.** Export/hash the ledger; verify preregistered outcome-source specs, raw snapshot hashes, selectors/capture rules, timing and independent resolution; produce an immutable allowlist of audit-passed resolution IDs.
2. **Derive one lesson mechanically/procedurally from only that allowlist.** Freeze synthesis code/prompt/version, input IDs/strata, candidate hash, derivation timestamp and audit-receipt hash. Owner may approve/veto, but the lesson content used for the learning claim must be traceable to the frozen derivation rather than manually substituted.
3. **Prove the rule changes execution behavior.** On frozen sandbox fixtures, show that B receives/uses the lesson overlay and A/C/D do not; prove arm/cache isolation and live provider telemetry capture on the exact build.
4. **Pilot only for design parameters.** Use a disjoint pilot to estimate paired variance/base rates and freeze N, MDE, equivalence/coverage margin, compute limits, leakage threshold, stopping plan and multiplicity method. Pilot tasks never enter the primary trial.
5. **Run the primary paired four-arm trial on fresh unseen tasks.** Primary estimand is task-level B-C under intention-to-treat; safety and coverage are frozen gates; D-C is the negative-control specificity test; judges are blinded and arm-guessing is audited.
6. **Freeze scores before unblinding and report everything.** Effect size, interval, permutation/randomization result, safety/coverage, placebo result, all protocol deviations, missing arms, replacements and compute mismatches. HARM/INCONCLUSIVE remain valid outcomes.
7. **Replicate once on a new frozen task set.** If the effect replicates, permit the scoped claim: `EVIDENCE_BACKED_BEHAVIORAL_LEARNING_FOR_<lesson>_<scope>`.
8. **Only broaden to "the system self-learns" after at least one additional independently derived lesson completes the same lifecycle and the system demonstrates evidence-based RETAIN/NARROW/RETIRE behavior without bypassing Owner governance.**

## FINAL_ADVICE

Keep the current conservative classification. Do not spend the next cycle adding another assurance layer before fixing the two provenance wiring defects.

Priority order for the learning subsystem:

1. make audited-resolution eligibility machine-enforced in meta-learning;
2. replace self-asserted lesson provenance with receipt-bound provenance;
3. change Trial-001 primary analysis to task-level intention-to-treat or hard-enforced compute budgets;
4. freeze powered statistics/multiplicity/canary sample rules;
5. build the live isolated executor + telemetry + blinded scoring path;
6. run one genuine ledger-derived lesson through the proof ladder;
7. open Research Adapter only after its own bounded ingestion gates pass.

One replicated, audit-bound causal learning episode is more valuable than another version number on Learning Assurance.

## DURABLE_LOCATION

`docs/critic/LEARN_CRITIC_01_20261005.md` on branch `critic/learn-critic-01-20261005-v1`.

## READY_FOR_NEXT_TASK

YES
