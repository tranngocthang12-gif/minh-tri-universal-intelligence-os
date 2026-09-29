# MINH TRÍ — FOUR-SEAT ARCHITECTURE REVIEW RESULTS INDEX v0.2

**Experiment:** `ARCH-CORE-R4-PRE-R5-2026-09-29-V2`  
**Frozen target:** `50a0444ed20ae2415c9ee31e622a0b6b8575d4c9`  
**Status:** `AWAITING FOUR BLIND PROVIDER FAMILIES`

Canonical experiment state for collection progress:

`docs/experiments/EXPERIMENT_STATE_V0.2.json`

## Do not use v0.1 for blind collection

The v0.1 packet leaked directed incumbent hypotheses and is retained only as historical experiment design evidence.

## Four-seat collection

| Seat | Provider family | Model/session | Round A frozen | Round B | Adjudicated |
| --- | --- | --- | --- | --- | --- |
| S1 | TBD | TBD | NO | NO | NO |
| S2 | TBD | TBD | NO | NO | NO |
| S3 | TBD | TBD | NO | NO | NO |
| S4 | TBD | TBD | NO | NO | NO |

Rules:

- exactly four independent provider-family seats for the official workcell experiment;
- all four receive the same pinned Round A packet;
- Round A outputs freeze before any reveal;
- one family cannot fill multiple seats;
- replacement before freeze must remain blind;
- no majority vote;
- BLOCKER/HIGH code claims require executable reproduction when feasible or remain `NEEDS_TEST`.

## Non-seat participants

- OpenAI/ChatGPT current architecture review = `INCUMBENT_CONTROL`, not an independent seat.
- The Claude/Anthropic session that critiqued protocol v0.1 = `PROTOCOL_CRITIC`, not a blind seat.
- A fresh Anthropic session that has not seen the critique/incumbent findings may occupy one seat if it receives only the pinned Round A packet.

## Decision

Until all four Round A submissions are frozen and material disputes receive evidence/test disposition:

`R5 = HOLD`.
