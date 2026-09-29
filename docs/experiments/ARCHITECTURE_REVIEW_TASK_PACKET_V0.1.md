# MINH TRÍ — BLIND CORE ARCHITECTURE REVIEW TASK PACKET v0.1

**Experiment:** `ARCH-CORE-R4-PRE-R5-2026-09-29-V1`  
**Frozen target:** `50a0444ed20ae2415c9ee31e622a0b6b8575d4c9`

## Your role

You are an independent architecture critic.

Do not assume the architecture is correct because tests pass.

Do not optimize for agreement with the author.

Do not invent project requirements that are not supported by the frozen artifacts.

Your job is to find material defects, unsafe promotion paths, stale-state races, governance drift, replay problems, false independence, and missing gates before R5 Skill Lifecycle + Meta-Learning is allowed to build on top.

## Core question

> Is the current MINH TRÍ candidate from restored v0.2 through R4 coherent and safe enough to begin R5 Skill Lifecycle + Meta-Learning in SHADOW mode?

## Read first

Read the frozen artifacts listed in:

`docs/experiments/ARCHITECTURE_MULTI_AI_EXPERIMENT_V0.1.md`

at exact Git head:

`50a0444ed20ae2415c9ee31e622a0b6b8575d4c9`

Do not use later branches/commits.

## Project invariants to preserve

Treat these as architecture constraints to verify, not assumptions that implementation satisfies them:

- Owner sovereignty;
- AI/provider replaceability;
- project memory != model memory;
- read before reconstruct;
- evidence before belief;
- prediction before outcome;
- dissent cannot be hidden;
- proposer/critic/adjudicator separation;
- domain isolation;
- fail closed;
- no automatic truth promotion;
- replayable decisions;
- measured learning;
- no silent architecture mutation;
- structural correctness != semantic correctness != real-world effectiveness.

## Required analysis

### A. Governance/Brain consistency

Check whether:

- mandatory bootstrap artifacts reflect the implemented architecture;
- Brain Manifest pins all material architecture contracts/state needed for safe continuation;
- stale tasks can continue after material architecture drift;
- branch/PR status can be confused with canonical project law.

### B. R1 Migration

Check whether legacy preservation solves only Arena or establishes a reusable schema discipline for later ledgers.

Identify future replay failure modes.

### C. R2 Task/Handoff

Check:

- checkpoint CAS;
- lease/failover;
- stale Brain/Law handling;
- cross-ledger race/atomicity;
- whether worker replacement truly preserves enough context.

### D. R3 Epistemic/Maturity

Try to produce unjustified maturity.

Pay special attention to:

- L1 evidence quality;
- L2 understanding claims;
- L3 preregistration;
- L5 validation;
- L6 critique;
- reopen/revalidation;
- knowledge expiry;
- cross-domain evidence;
- provider-error observations.

### E. R4 Goal/Bottleneck

Try to make the governor:

- select a false bottleneck;
- satisfy a dependency using irrelevant evidence;
- commit a stale recommendation;
- bypass an Owner goal change;
- produce a task candidate inconsistent with R2 authority/evidence.

### F. Pre-R5 contamination risk

R5 would transform validated lessons into reusable skill candidates and compare learning methods.

Find any path where current R1-R4 state could cause:

```text
weak/stale/incorrect input
→ skill candidate
→ benchmark/meta-learning
→ repeated institutional error
```

## Output format

### Executive result

Choose exactly one:

- `R5_READY_FOR_SHADOW`
- `R4_5_REQUIRED`
- `HOLD_MORE_EVIDENCE`

Then explain why in no more than 200 words.

### Material findings

For each finding:

```text
finding_id:
severity: BLOCKER | HIGH | MEDIUM | LOW
layer:
claim:
source:
failure_scenario:
why_material:
minimal_fix:
verification_test:
uncertainty:
scope:
```

### Adversarial traces

Provide at least two exact traces using current commands/state transitions.

### What is already strong

List mechanisms you think are structurally sound. Do not omit strengths merely because the task is adversarial.

### Unknowns

State what cannot be concluded from the frozen repo.

### Minimal pre-R5 gate

Give the smallest set of changes/tests that you believe are required before R5 may start in SHADOW.

## Prohibited shortcuts

Do not:

- vote by number of AI opinions;
- treat green CI as proof of semantic correctness;
- treat one successful scenario as a universal rule;
- assume provider IDs imply provider-family independence;
- assume same-domain evidence is relevant evidence;
- assume a Git branch/PR is canonical law;
- propose opening real trading/publishing/spending authority;
- promote lessons/skills based on this review alone.
