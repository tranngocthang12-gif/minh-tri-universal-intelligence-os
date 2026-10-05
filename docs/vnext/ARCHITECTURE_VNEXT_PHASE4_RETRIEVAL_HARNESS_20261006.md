# MINH TRÍ — Architecture vNext Phase 4A — Retrieval Evaluation Harness

**Date:** 2026-10-06  
**Status:** CANDIDATE HARNESS / NOT A MEMORY PASS  
**Base main:** `a002cef755e8832c045af422e6ee9da62c375205`

## Goal

Build a reproducible held-out retrieval test without allowing the authoring seat to grade itself.

Phase 4 is split:

- **Phase 4A:** create questions, decoys, packet builder, response schema, and scorer.
- **Phase 4B:** a different fresh seat runs the packet and submits a response artifact.

Only Phase 4B can produce a retrieval baseline result.

## Independence rule

The seat that authored the questions/gold set must not be the graded seat.

The graded seat receives:
- generated eval packet;
- canonical knowledge snapshot embedded in that packet;
- decoys.

The graded seat must not receive:
- `gold.json`;
- scorer internals beyond the response schema;
- prior answers from the authoring seat.

## Decoy design

The harness includes two synthetic non-canonical decoys:

1. a **SUPERSEDED** competing record that falsely promotes the A172 identity-shame synthesis into direct attestation;
2. a synthetic false active-looking record claiming `ottappa = generalized anxiety`.

They live only under `eval/`, never under canonical `knowledge/`.

## What a pass means

A fresh-seat pass can establish only:

`RETRIEVAL_BASELINE_PASS_FOR_THIS_FIXTURE`

It does not prove:
- global memory;
- understanding;
- application;
- correction across time;
- autonomous self-learning.

## Required response

The graded seat returns JSON matching:
`eval/retrieval/v1/response.schema.example.json`

Each answer must include:
- qid;
- answer_status: SUPPORTED / UNSUPPORTED / PENDING_REVIEW;
- record_ids actually used;
- concise answer.

## Next gate

After this harness PR merges:
- generate a packet from canonical main;
- route it to a different fresh seat;
- store the returned response;
- score it against sealed gold;
- record pass/fail honestly.
