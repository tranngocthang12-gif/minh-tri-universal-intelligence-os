# MINH TRÍ — EPISTEMIC STATE & LEARNING MATURITY CONTRACT v0.1

**Status:** `R3 CANDIDATE / SHADOW / NOT MERGED`  
**Date:** 2026-09-29

## Purpose

Make the brain explicitly track:

- what it currently treats as remembered/known/understood;
- what remains unknown;
- what has prediction/outcome/critique support;
- what knowledge is stale or reopened;
- what provider errors have been observed;
- the highest demonstrated and currently effective learning maturity.

R3 does not let an AI self-declare “I understand” or “I am L9”.

## Learning maturity

```text
L0 MEMORY
L1 KNOWLEDGE
L2 UNDERSTANDING
L3 PREDICTION
L4 ACTION
L5 VALIDATION
L6 SELF-CRITICISM
L7 META-LEARNING       [FUTURE GATE]
L8 SELF-REPAIR         [FUTURE GATE]
L9 TRANSFER            [FUTURE GATE]
```

R3 can structurally demonstrate only L0-L6.

L7-L9 remain represented in the data model but cannot be reached because their required engines/benchmarks belong to R5/R8.

## Evidence gates

### L0 — MEMORY
A durable epistemic item exists with source/origin reference and scope.

### L1 — KNOWLEDGE
The item has one or more Core evidence references in the same domain.

### L2 — UNDERSTANDING
After L1, the system records all four practical signals:

- explanation;
- distinction from a nearby alternative;
- expected pattern;
- falsifier.

These are evidence of a demonstrated explanation, not proof of semantic truth.

### L3 — PREDICTION
The item links to a Core prediction that is already `FROZEN` or `RESOLVED`.

A merely registered/unfrozen prediction cannot claim L3.

### L4 — ACTION
R3 permits only:

- `SHADOW_TEST`;
- `READ_ONLY_ANALYSIS`.

No external effect is granted by R3.

### L5 — VALIDATION
The application links to the Core resolution of the exact linked prediction and to its observed outcome evidence.

Synthetic outcome evidence is not accepted for L5.

This validates a measured outcome relation only; causal attribution remains whatever Core states.

### L6 — SELF-CRITICISM
The item links to a Core review of the exact claim behind the linked prediction.

The review may be ACCEPT/HOLD/REVISE. L6 means the item has been exposed to independent criticism, not that criticism approved it.

## Highest vs effective maturity

Each item keeps:

- `highest_demonstrated_level` — historical maximum demonstrated under recorded evidence;
- `effective_level` — level currently allowed for use;
- `maturity_status`.

When reopened by:

`NEW_EVIDENCE | STALENESS | REGRESSION | OWNER_REOPEN | DEPENDENCY_CHANGE | POLICY_CHANGE | ENVIRONMENT_CHANGE`

the effective level falls to `L0_MEMORY` with:

`SUSPENDED_PENDING_REVALIDATION`.

The historical maximum is not erased.

After evidence-backed revalidation, the effective level can return to the level still supported by the retained chain.

## Unknown registry

A material unknown records:

- question;
- domain;
- materiality;
- Owner impact;
- optional review due time;
- OPEN / RESOLVED_DECLARED_EVIDENCE;
- evidence-backed resolution;
- reopen history.

Resolving an unknown requires evidence.

## Knowledge lifecycle

Items and unknowns may have `review_due_at`.

Status can surface items due for review, but R3 does not automatically declare them false merely because time passed.

Expiry is a trigger for review/reopen, not proof of invalidity.

## Provider error observations

R3 records provider/actor error observations with:

- actor reference;
- task class;
- severity;
- description;
- evidence references;
- domain.

Status is:

`OBSERVED_NOT_SCORED`.

R3 does not yet compute provider rankings, champion status or routing scores. Those belong to R6 after repeated evidence.

## Domain isolation

Evidence, prediction, resolution and review links cannot cross domain boundaries.

This prevents finance evidence from being silently used as YouTube evidence or vice versa.

## Non-claims

R3 does not prove:

- that explanations are semantically correct;
- that a prediction demonstrates causality;
- that a provider is objectively good/bad;
- that L6 implies high intelligence;
- meta-learning, self-repair or cross-domain transfer.

## Structural gate

R3 PASS requires tests proving:

1. no maturity jump over missing evidence;
2. L1 requires evidence;
3. L2 requires L1;
4. L3 requires a frozen/resolved preregistered prediction;
5. L4 is bounded to no-effect modes;
6. L5 binds to the actual resolution/outcome and rejects synthetic outcome evidence;
7. L6 binds to the exact claim critique;
8. reopen suspends effective maturity while retaining history;
9. evidence-backed revalidation restores supported maturity;
10. unknowns require evidence to resolve and may reopen;
11. cross-domain links fail closed;
12. provider errors are observations, not fake scores;
13. Python 3.10/3.12 CI passes.
