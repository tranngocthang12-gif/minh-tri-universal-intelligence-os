# MINH TRÍ — Architecture vNext Phase 4B — Fresh-seat retrieval run handoff

**Date:** 2026-10-06
**Status:** READY_FOR_FRESH_SEAT / NOT YET GRADED
**Canonical base:** `43e1ee36fcf6bd42663dfa1bc2cbc6382b503b55`

## Purpose

Phase 4A is complete. The harness is canonical.

Phase 4B must now be executed by a **different fresh seat**. The current authoring seat is not eligible to be the graded seat.

## Canonical packet

Use only:

`eval/retrieval/v1/packets/ARCH-VNEXT-PHASE4-RETRIEVAL-BASELINE-001.json`

The packet contains:
- instructions;
- five questions;
- canonical knowledge snapshot;
- synthetic decoys.

It does **not** contain:
- gold answers;
- scorer output;
- authoring-seat answers.

## Required graded-seat output

Write a response matching:
`eval/retrieval/v1/response.schema.example.json`

Required result fields:
- qid;
- answer_status;
- record_ids actually used;
- concise answer;
- graded_seat_id.

The result should be returned to the orchestrator for scoring against the sealed gold file.

## Truth boundary

Before a fresh-seat response is scored:
`RETRIEVAL_BASELINE = NOT_RUN`

After scoring, permitted outcomes are:
- `RETRIEVAL_BASELINE_PASS_FOR_THIS_FIXTURE`
- `RETRIEVAL_BASELINE_FAIL_FOR_THIS_FIXTURE`

Neither result by itself proves:
- global memory;
- application;
- correction over time;
- autonomous self-learning.

## Current blocker

This chat cannot honestly act as both:
1. the seat that authored the harness; and
2. the independent graded seat.

Therefore the correct state is READY_FOR_FRESH_SEAT, not PASS.
