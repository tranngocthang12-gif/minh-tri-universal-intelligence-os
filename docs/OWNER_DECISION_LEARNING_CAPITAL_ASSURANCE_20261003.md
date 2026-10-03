# OWNER DECISION — LEARNING CAPITAL + ASSURANCE — 2026-10-03

**Status:** OWNER DECISION / ADDITIVE TO CURRENT LEARNING CONTRACT / NO AUTOMATIC VERIFIED

## 1. Owner decision

MINH TRÍ practices a little each day, so first-party real-world lessons may take a long time to accumulate.

Until enough Owner practice exists:

1. accumulate useful **external success cases** as learning capital;
2. accumulate useful **external failure cases** as learning capital;
3. keep both explicitly unverified for transfer to Owner context;
4. do not convert case counts, popularity, model agreement, or one attractive success into a lesson;
5. first-party Owner practice remains the main promotion path for durable trial lessons.

External cases are capital for questioning, comparison, counterexamples, hypotheses and future test design. They are not proof that the same mechanism will work for Owner.

## 2. Learning Assurance v1

Add an assurance layer without replacing the Tier-1 ledger:

```
SOURCE / EXTERNAL CASE CAPITAL
        ↓
EVIDENCE
        ↓
CLAIM + ALTERNATIVE + FALSIFIER
        ↓
COUNTEREVIDENCE
        ↓
FROZEN LEARNING PACKET
        ↓
PREDICTION / OUTCOME WHEN AVAILABLE
        ↓
CRITIC EXECUTION PROVENANCE
        ↓
NEGATIVE CONTROLS
        ↓
ADJUDICATION
        ↓
LESSON CANDIDATE
        ↓
OWNER GATE
        ↓
TRIAL RULE
```

## 3. External case capital

Machine status:

`EXTERNAL_CASE_CAPITAL_UNVERIFIED`

Allowed outcomes:

- `SUCCESS`
- `FAILURE`
- `MIXED`

Every case must retain:

- domain;
- evidence references;
- context;
- mechanism hypothesis;
- transfer limits;
- uncertainty.

External cases have `lesson_eligible=false` by construction in Learning Assurance v1.

## 4. Frozen learning packet

Before an important critic run, freeze:

- trace ID;
- exact claim;
- supporting evidence references;
- counterevidence references;
- selected external-case references;
- context contract;
- instruction version;
- toolset fingerprint;
- target hash;
- evidence-bundle hash.

A critic finding is about that frozen packet, not about an silently changed target.

## 5. Critic execution provenance

Critic execution records:

- critic provider seat;
- declared provider/model;
- run ID;
- BLIND or REVEALED context mode;
- output hash;
- verdict;
- missing evidence;
- inherited target/evidence hashes.

Allowed assurance verdicts:

- `FINDINGS`
- `NO_MATERIAL_DEFECT`
- `BLOCKED`
- `ABSTAIN`
- `REVIEW_INCOMPLETE`

These are critic metadata, not epistemic truth.

## 6. Negative controls

A claim may be pressure-tested with negative/adversarial cases. Control outcomes are:

- `PASS`
- `FAIL`
- `INCONCLUSIVE`

A control PASS is not VERIFIED truth. A FAIL is evidence requiring narrowing, revision or hold.

## 7. Meta-learning boundary

Meta-learning may summarize historical performance and propose candidates. It may not:

- write canonical rules automatically;
- promote a claim to VERIFIED;
- activate a trial lesson;
- infer cross-domain transfer from case counts;
- treat external success frequency as causal proof.

## 8. No multi-agent dependency

This does not convert MINH TRÍ into a multi-agent system. Critic remains a replaceable seat. Blind/external review is an assurance technique when warranted, not a permanent panel requirement.

## 9. Runtime boundary

Background autonomous learning remains OFF until existing fresh-seat, transport, persistence and security gates pass. Learning Assurance v1 is additive and fail-closed.

## 10. Explicit v1 limits / next gates

Learning Assurance v1 intentionally does **not** claim the following are complete:

- full lifecycle `trace_id` propagation across every legacy source/claim/prediction/resolution/lesson event;
- automatic lesson expiry/revalidation mutation;
- semantic proof that declared critic providers are operationally independent;
- reward-hacking or contamination detection beyond future eval fixtures;
- rich meta-learning by domain/source/method/failure class.

These remain follow-up gates. They must be added with backward-compatible ledger migration and tests rather than silently inferred from the v1 packet trace.


## 11. Learning Assurance v1.1 candidate

Additive contracts:

### Trace links
A `record_trace_link` record may bind an existing artifact to a durable `trace_id` with a typed relation and an artifact digest.

This avoids rewriting historical events while enabling causal debugging across selected source/evidence/claim/prediction/outcome/critic/adjudication/lesson/control/revalidation artifacts.

A trace link proves linkage metadata and the artifact snapshot hash at link time. It does not prove causality.

### Lesson revalidation proposals
A lesson may receive a future review schedule with explicit staleness conditions.

Revalidation outcomes are:
- `RETAIN`
- `NARROW`
- `RETIRE`
- `INCONCLUSIVE`

All revalidation records are `PROPOSAL_ONLY` and set `automatic_lesson_mutation=false`.

A scheduled review cannot be recorded before its `review_after` time. A `STALE_SIGNAL` or `OWNER_REQUEST` may trigger earlier review, but still cannot mutate the lesson automatically.

## 12. Learning Assurance v1.2 candidate

### Failure taxonomy

MINH TRÍ may record bounded learning failures against a concrete artifact. Initial machine classes:

- `SOURCE_ERROR`
- `SCOPE_OVERREACH`
- `UNSUPPORTED_INFERENCE`
- `CONFIRMATION_BIAS`
- `COUNTEREVIDENCE_IGNORED`
- `STALE_KNOWLEDGE`
- `CRITIC_CONTAMINATION`
- `EVAL_CONTAMINATION`
- `REWARD_HACKING`
- `TOOL_ERROR`
- `HALLUCINATED_SOURCE`
- `OVERCONFIDENCE`
- `DOMAIN_TRANSFER_FAILURE`

A recorded failure is metadata/evidence for diagnosis. It does not automatically rewrite or repair the underlying artifact.

### Stratified meta-learning

Meta-learning should compare bounded historical strata instead of one global average:

- domain;
- procedure/method;
- outcome source kind;
- failure class;
- failure class within domain.

Minimum history still applies. Group summaries are descriptive calibration evidence only.

No group statistic proves causality or transfer to another domain. Meta-learning may produce `META_LESSON_CANDIDATE` records only and cannot change rules automatically.

### Contamination and reward hacking boundary

v1.2 can **record** `EVAL_CONTAMINATION`, `CRITIC_CONTAMINATION`, and `REWARD_HACKING` when evidence identifies them. It does not claim automatic detection is solved. Automatic detection remains a separate eval-hardening gate.

## 13. Learning Assurance v1.3 candidate

### Critic execution independence receipts

A critic execution may receive a separate receipt that records:

- execution environment ID;
- project runtime ID;
- session ID;
- provider receipt hash;
- authority scope;
- whether Project context was supplied;
- verification method;
- bounded supporting evidence.

Machine status is deliberately conservative:

- same runtime -> `BLOCKED_SAME_RUNTIME`;
- not blind / Project context supplied -> `BLOCKED_NOT_BLIND`;
- process-separated + separate approved authority + external evidence -> `PROCESS_SEPARATED_EXTERNAL_EVIDENCE_RECORDED_NOT_FULL_INDEPENDENCE_PROOF`;
- otherwise -> `EVIDENCE_BOUND_NOT_INDEPENDENCE_PROOF`.

No receipt automatically proves full independence.

### Eval integrity assessment

A deterministic assessment may record:

- output hash;
- configured forbidden-marker hits;
- invariant failures;
- whether the candidate claimed a pass;
- evaluator kind.

Bounded statuses:

- `EVAL_CONTAMINATION_SUSPECTED`;
- `REWARD_HACKING_SUSPECTED`;
- `EVAL_CONTAMINATION_AND_REWARD_HACKING_SUSPECTED`;
- `INVARIANT_FAILURE_RECORDED`;
- `CLEAN_NO_SIGNAL_NOT_PROOF`.

This is a guard for explicit signals, not a solved universal detector. A clean result means only that configured signals were not observed.

## 14. Learning Assurance v1.4 candidate — provider-neutral reasoning/context patterns

Research basis: public provider documentation only. This does not claim access to private model internals or that any provider continuously retrains itself from a user's conversation.

### Adaptive deliberation

MINH TRÍ may record a deliberation plan against a concrete artifact.

Inputs:
- risk level;
- evidence conflict;
- tool dependency;
- requested effort;
- rationale.

Deterministic floor:
- HIGH/CRITICAL risk or conflicting evidence -> minimum HIGH;
- MEDIUM risk or tool dependency -> minimum MEDIUM;
- otherwise minimum LOW.

The effective effort can be raised above the request but not below the deterministic minimum.

This mechanism stores no private chain-of-thought. It stores only bounded planning metadata.

### Grounded research trace

A research trace binds:
- exact query;
- source;
- source role;
- claim;
- citation locator;
- conflict status;
- note;
- source and claim digests.

Source roles:
- PRIMARY
- SECONDARY
- SOCIAL_SIGNAL
- REFERENCE
- COUNTEREVIDENCE

SOCIAL_SIGNAL is always `NON_CANONICAL_SIGNAL`; popularity or social visibility cannot promote truth.

### Context capsules

Long-running work may create a bounded context capsule containing:
- exact artifact references;
- digest of every referenced artifact;
- summary;
- purpose;
- refresh deadline;
- capsule digest.

A capsule status is always `CONTEXT_ONLY_NOT_CANONICAL_TRUTH`.

Compaction/summary is a retrieval aid only. It cannot overwrite source/evidence/law/lesson truth and cannot automatically promote a claim.

### Provider-neutral rule

Gemini/Claude/Grok mechanisms may inspire implementation patterns, but no provider-specific hidden reasoning state, memory format, or proprietary runtime becomes canonical Tier-1 truth.
