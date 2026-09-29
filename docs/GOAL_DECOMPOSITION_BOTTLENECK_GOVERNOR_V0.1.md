# MINH TRÍ — GOAL DECOMPOSITION & BOTTLENECK GOVERNOR CONTRACT v0.1

**Status:** `R4 CANDIDATE / SHADOW / NOT MERGED`  
**Date:** 2026-09-29

## Purpose

R4 answers one question:

> Given the Owner's target and the current R3 epistemic state, what is the highest-leverage eligible learning/action unit to work on next?

R4 must also be able to return `WAIT` or `HOLD_AMBIGUOUS`.

It does not grant external action authority.

## Flow

```text
OWNER GOAL
→ TARGET STATE
→ SUCCESS CONDITIONS
→ DEPENDENCY / CAPABILITY GRAPH
→ CURRENT GAPS
→ R3 KNOWN / UNKNOWN / MATURITY
→ ELIGIBLE COMPONENTS
→ ORDINAL BOTTLENECK RUBRIC
→ SELECT / WAIT / HOLD_AMBIGUOUS
→ TASK CANDIDATE
```

R4 produces a **task candidate**, not a canonical task. R2 remains the canonical task authority.

## Component contract

Each decomposition component declares:

- success condition(s) it supports;
- dependency IDs;
- target role: `BLOCKER | ENABLER | OPTIMIZER`;
- gap kind;
- Owner impact;
- decision sensitivity;
- expected information gain;
- cost/time/risk bands;
- reversibility;
- R3 epistemic items and/or unknowns;
- allowed evidence;
- leverage hypothesis;
- disconfirming condition;
- bounded next unit;
- acceptance criteria.

A component without any R3 knowledge/unknown linkage is rejected.

## Dependency law

A component is eligible only when all its declared dependencies are `SATISFIED`.

Dependencies can only refer to components already registered in the same plan. This prevents forward-reference cycles in R4 v0.1.

## Selection rubric

R4 uses an explicit ordinal lexicographic rubric:

1. `target_role`;
2. Owner impact;
3. decision sensitivity;
4. epistemic gap;
5. expected information gain;
6. reversibility;
7. lower risk;
8. lower cost;
9. shorter time.

This is deliberately labeled:

`ORDINAL_LEXICOGRAPHIC_NO_CALIBRATED_SCORE`.

R4 does **not** claim a numeric utility score.

The ordering is a candidate decision rule. Its real effectiveness must later be compared against baseline.

## Epistemic gap derivation

R4 derives a coarse gap from R3:

- OPEN HIGH unknown or REOPENED item → HIGH gap;
- L0/L1 item → HIGH gap;
- L2/L3 item → MEDIUM gap;
- L4+ item → LOW gap.

This is a routing heuristic, not a truth measure.

## Tie handling

If multiple eligible components have the same top ordinal tuple:

`HOLD_AMBIGUOUS`.

The governor does not choose alphabetically or randomly.

## WAIT

R4 returns `WAIT` when:

- all components are SATISFIED/NOT_APPLICABLE; or
- unresolved components are blocked by dependencies/HOLD; or
- no eligible unit exists.

WAIT is a valid intelligence outcome.

## Component satisfaction

A component may be set `SATISFIED` only with:

- same-domain evidence; or
- an active R3 item at L2+.

This is a structural gate only. It does not prove the dependency was semantically solved correctly.

## Focus receipt

A committed focus records:

- exact Core head;
- exact Epistemic head;
- exact Governor head before decision;
- candidate IDs;
- selected component if any;
- selection method;
- hash of the recommendation snapshot.

This allows replay of what the governor saw when it focused attention.

## Owner/authority boundary

R4 may recommend:

- LEARN;
- READ_ONLY_ANALYSIS;
- SHADOW_TEST.

It cannot recommend direct publish/trade/spend/irreversible external actions in v0.1.

A SELECT result is not Owner approval.

## Structural verification gate

R4 PASS requires:

1. dependency-blocked work is not selected;
2. upstream completion unlocks downstream work;
3. a BLOCKER can outrank a cheaper optimizer under the declared rubric;
4. exact ties produce HOLD_AMBIGUOUS;
5. no eligible work produces WAIT;
6. closed/blocked Owner goal blocks recommendation;
7. cross-domain R3/evidence links fail closed;
8. SATISFIED requires evidence or L2+ active item;
9. focus receipts pin Core/Epistemic/Governor heads;
10. recommendation does not auto-create a canonical task;
11. Python 3.10/3.12 CI passes.

## Non-claims

R4 does not prove:

- the declared bottleneck is causally the true bottleneck;
- the ordinal ordering is optimal;
- solving the selected component will improve business outcomes;
- AI Commons is needed for every selected unit;
- a selected task is authorized for external execution.

Those remain empirical/authority gates.
