# MINH TRÍ — MULTI-AI CORE ARCHITECTURE REVIEW EXPERIMENT v0.2

**Experiment ID:** `ARCH-CORE-R4-PRE-R5-2026-09-29-V2`  
**Status:** `SHADOW / FOUR-SEAT / NOT MERGED`  
**Frozen architecture target:** `50a0444ed20ae2415c9ee31e622a0b6b8575d4c9`  
**Round A packet Git blob SHA:** `b02d98d20961eeb165b2febc74ee66152e85362f`  
**Incumbent baseline Git blob SHA:** `14d7dc97280428188a1445d0a2c9bbef53fa5c91`

## Purpose

Measure whether four genuinely independent AI provider families can improve the evidence-backed architecture decision before R5, without leaking the incumbent suspected-blocker list into the blind discovery round.

This experiment uses the Owner's restored four-seat workcell:

`S1 | S2 | S3 | S4`

The four seats are stable; occupants are replaceable.

## Round A — blind discovery

Every seat receives the exact same:

- frozen target SHA;
- Round A packet identified by the blob SHA above;
- source artifact set;
- no incumbent findings;
- no other provider output.

Each seat must submit a response that is frozen before reveal.

If a seat must be replaced before Round A freeze, the replacement receives only the original frozen Round A packet and must not see any other blind output.

## Freeze barrier

Round A cannot close until:

- all four seats are occupied;
- all four provider families are distinct;
- all four submission hashes are recorded;
- provider/model/version/session provenance is recorded;
- each submission states it did not see other reviews or Round B before completion.

Missing one independent seat => `HOLD / WAIT_FOR_REPLACEMENT`.

## Round B — directed challenge

Only after Round A 4/4 freeze:

1. reveal the frozen incumbent baseline;
2. reveal the Round B directed packet;
3. keep Round A novelty metrics separate from Round B confirmation metrics;
4. ask each participant to CONFIRM / REFUTE / NEEDS_TEST the directed concerns.

The incumbent OpenAI/ChatGPT review is a control baseline, not one of the four independent seats for this experiment.

The Claude session that critiqued protocol v0.1 is classified `PROTOCOL_CRITIC`, not an Anthropic blind-review seat.

## Executable evidence rule

For a BLOCKER/HIGH claim about a code/gate transition:

- executable pytest reproducer against the frozen target is preferred;
- if feasible but absent, disposition defaults to `NEEDS_TEST`;
- semantic/governance findings that cannot be represented as pytest must identify a concrete discriminating evidence/test path.

No AI assertion alone confirms a blocker.

## Cross-critique and adjudication

After Round B:

`FINDING → SOURCE → COUNTEREVIDENCE → REPRO/TEST → ADJUDICATION`

Allowed dispositions:

- `CONFIRMED_BLOCKER`
- `CONFIRMED_HIGH`
- `CONFIRMED_NON_BLOCKER`
- `NEEDS_TEST`
- `DUPLICATE`
- `OUT_OF_SCOPE`
- `HOLD`

No majority vote. A 4-0 opinion without evidence is not truth.

## R5 readiness

`R5_READY_FOR_SHADOW` requires:

1. zero unresolved BLOCKER affecting lesson/skill inputs;
2. zero unresolved HIGH affecting lesson/skill inputs, unless explicitly HOLD with Owner acceptance of the bounded risk;
3. all material disputes have a test/evidence disposition;
4. R3/R4 promotion paths have adversarial coverage;
5. cross-layer continuity tests pass;
6. ledger compatibility gate is explicit for current mutable ledgers;
7. R5 skill promotion remains OFF until repeated real outcomes and benchmark thresholds exist.

Otherwise result is `R4_5_REQUIRED` or `HOLD_MORE_EVIDENCE`.

## Known limitation

Different provider families improve organizational independence but do not prove statistical/cognitive independence: models can share public training data, benchmarks and human prompt routing. Record this as a limitation in every experiment conclusion.

## Authority

Experiment results are evidence/proposals only. They do not merge code, amend Project Law, activate skills, rank providers from one run, or open external actions.
