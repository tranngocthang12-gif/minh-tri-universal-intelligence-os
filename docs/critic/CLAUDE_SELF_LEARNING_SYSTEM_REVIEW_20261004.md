# CLAUDE ADVERSARIAL REVIEW BRIEF — MINH TRI SELF-LEARNING SYSTEM — 2026-10-04

**Purpose:** independent technical critique of the MINH TRI self-learning architecture.  
**Review mode:** adversarial / evidence-bounded / no deference to prior ChatGPT conclusions.  
**Important:** this is not a request to praise the design. Look for material defects, hidden assumptions, missing evidence, circular validation, overclaims, and unsafe or ineffective learning loops.

## 1. System claim to review

MINH TRI is intended to be an evidence-first learning/control system with replaceable AI seats and a durable project brain. The current self-learning layer is deliberately proposal-only:

- automatic critique may produce review proposals;
- autonomous learning may produce read-only action plans;
- meta-learning may summarize historical calibration/failure patterns and propose meta-lesson candidates;
- external cases are learning capital but not lesson proof;
- no automatic VERIFIED promotion;
- no automatic trial activation;
- no automatic durable mutation;
- all durable writes remain behind an Owner-gated ledger boundary;
- Research Adapter is fail-closed until a genuine fresh-seat validation gate passes.

The design goal is to obtain useful learning while preventing an AI from silently rewriting its own law, evidence, or verified state.

## 2. Current implementation facts

Canonical code and tests are on GitHub main.

### Autonomy runtime

`src/minhtri/autonomy.py` defines a proposal-only runtime.

Key properties:

- `ProposalOnlyAutonomyRuntime.tick()` builds and emits an autonomy packet only.
- The packet explicitly sets:
  - `write_capability=false`
  - `automatic_verified_promotion=false`
  - `automatic_trial_activation=false`
- Structural critique refuses to auto-accept a claim and requires a distinct declared critic provider from proposer/predictors.
- Meta-learning creates only `META_LESSON_CANDIDATE` outputs.
- Stratified meta-learning separates domain/procedure/source-kind summaries and explicitly does not establish cross-domain transfer or causality.
- Research remains blocked unless canonical PROJECT_STATE simultaneously proves:
  1. fresh-seat validation PASS,
  2. end-to-end seat/brain transport true,
  3. research adapter gate open.
- Malformed/unreadable canonical state fails closed.

### Learning Assurance

The project records:

- external success/failure/mixed cases as unverified learning capital;
- frozen learning packets;
- critic execution provenance;
- negative controls;
- lesson revalidation as proposal-only;
- learning failure classes;
- critic-independence receipts;
- eval contamination/reward-hacking signals;
- adaptive deliberation metadata;
- grounded research traces;
- context capsules that are explicitly non-canonical.

The current Learning Assurance generation is v1.4. It is implemented and CI-proven but has **not** yet been empirically shown to improve real-world accuracy.

### Candidate self-upgrade path

The self-upgrade path is separate from general self-learning:

- candidate mutation is branch/path constrained;
- test must pass;
- internal critic runs read-only;
- same-provider internal critic is explicitly marked non-independent;
- when an external critic gate is configured, missing/invalid/late external review blocks freeze;
- no automatic candidate promotion, push, merge, or VERIFIED status.

A real Candidate A currently exists with:
- changed path: `src/minhtri/autonomy.py`;
- targeted and full test suites previously PASS;
- status: `PENDING_EXTERNAL_CRITIC`;
- not eligible to freeze until a real external critic response is accepted.

## 3. Current runtime state

Do not confuse code/CI success with a running self-learning service.

Fresh runtime observation at 2026-10-04 02:04:29 +07:00:

- Owner PC host state: UNKNOWN;
- Desktop Commander maintenance plane: OFFLINE;
- Secure MCP Tunnel: DOWN;
- Local Brain connector: DOWN;
- fresh `brain.verify` failed because tunnel-client had not been seen for 300 seconds.

Therefore the current background self-learning runtime is **not running**.

Canonical PROJECT_STATE also says:

- `autonomous_learning_runtime=false`
- `automatic_self_critique_runtime=false`
- `meta_learning_runtime=false`
- `autonomy_write_capability=false`
- `research_adapter_gate=BLOCKED_UNTIL_FRESH_SEAT_PASS`

This is intentional fail-closed behavior, not evidence that the code path is broken.

## 4. Current CI evidence

The latest main push CI completed successfully across:

- Python 3.10 test matrix;
- Python 3.11 test matrix;
- Python 3.12 test matrix;
- PowerShell parse gate;
- security audit;
- real-clock lease-expiry proof;
- aggregate required `test` gate.

Tests include explicit checks that:

- same-seat critique is blocked;
- structural critique never auto-accepts;
- meta-learning needs history;
- meta-learning only proposes candidates;
- external cases remain capital-only;
- autonomy packets have no write power;
- research fails closed before its gate;
- callers cannot open research via CLI override;
- runtime tick emits a packet but performs no durable mutation;
- critic independence is not overclaimed;
- context capsules do not become canonical truth.

## 5. Known unclosed gates

The project itself currently admits these major gaps:

1. genuine fresh-seat validation not PASS;
2. independent witness authority absent;
3. real independent external critic execution evidence incomplete;
4. empirical validation of Learning Assurance v1.4 not done;
5. boot/reboot persistence not proven;
6. endpoint protection and BitLocker state partly UNKNOWN;
7. old tunnel-key revocation lacks provider-side proof;
8. runtime is currently offline/down.

## 6. Questions for your critique

Please review this as if you were trying to break the design.

### A. Is this actually a self-learning system?

Determine whether the current design is meaningfully “self-learning,” or whether it is only a reporting/proposal framework.

Identify exactly what would have to be added for learning to change future behavior without creating an unsafe self-modifying loop.

### B. Epistemic loop

Analyze the chain:

SOURCE → EVIDENCE → CLAIM/HYPOTHESIS → CRITIC → PREDICTION/TEST → RESOLUTION → LESSON CANDIDATE → OWNER/GOVERNANCE → TRIAL RULE

Look for:
- circular validation;
- self-confirmation;
- weak falsification;
- proxy gaming;
- excessive dependence on manually declared metadata;
- ways bad evidence could accumulate while all gates technically pass.

### C. Critic independence

Provider IDs are declared identities, not cryptographic proof that two reasoning processes are independent.

Assess whether current separation rules are sufficient and propose a stronger practical independence model.

### D. Meta-learning validity

The current system computes descriptive calibration/failure summaries and creates meta-lesson candidates.

Evaluate:
- whether the statistics are too weak to justify adaptation;
- minimum sample sizes and stratification requirements;
- multiple-comparison / selection-bias risks;
- survivorship bias;
- domain-transfer errors;
- how to prevent the system from learning from its own measurement mistakes.

### E. Research gate design

Research is blocked until fresh-seat validation passes.

Assess whether tying research capability to fresh-seat recovery is:
- a sound safety dependency;
- unnecessarily coupled;
- or missing another prerequisite.

Propose a safer and more useful gate structure if needed.

### F. Proposal-only architecture

The current runtime cannot durably write any learned lesson.

Analyze whether this creates a system that is safe but operationally inert.

If you recommend limited automatic mutation, specify:
- exactly which artifact may change;
- privilege boundary;
- reversible mechanism;
- evidence threshold;
- rollback;
- expiry;
- Owner override;
- conditions that must still require human approval.

### G. Learning Assurance v1.4

The implementation exists but empirical benefit is unproven.

Design a credible experiment to test whether v1.4 improves:
- factual accuracy;
- calibration;
- unsupported-claim rate;
- source quality;
- error discovery;
- task utility.

Avoid an evaluation where the same model both produces and judges the outputs.

### H. Runtime/canonical consistency

Evaluate the architecture's separation of:
- historical capability proof;
- current runtime liveness;
- authorization;
- durable canonical state.

Find any remaining ways stale historical PASS evidence could accidentally be treated as present capability.

## 7. Required response format

Return a technical review with these sections:

1. **Material defects**
   - ID
   - severity: CRITICAL / HIGH / MEDIUM / LOW
   - exact defect
   - why it matters
   - evidence needed to confirm/refute

2. **Architectural strengths that are actually supported by evidence**
   - only include strengths justified by the facts above;
   - do not infer production readiness.

3. **Overclaims or ambiguous terminology**
   - especially around “self-learning,” “independent critic,” “verified,” and “autonomous.”

4. **Missing experiments**
   - rank by information value, not ease.

5. **Recommended architecture changes**
   - separate required fixes from optional improvements.

6. **Adversarial scenarios**
   - at least five concrete ways the learning system could produce a wrong lesson while apparently following its rules.

7. **Bottom line**
   - state what the system can legitimately claim today;
   - state what it cannot legitimately claim today;
   - state the single most important next proof.

Do not rely on prior conclusions from ChatGPT. If the information supplied is insufficient for a claim, say **INSUFFICIENT EVIDENCE** rather than guessing.
