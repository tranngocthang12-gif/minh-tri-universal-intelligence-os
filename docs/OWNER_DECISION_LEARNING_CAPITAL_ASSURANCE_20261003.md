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
