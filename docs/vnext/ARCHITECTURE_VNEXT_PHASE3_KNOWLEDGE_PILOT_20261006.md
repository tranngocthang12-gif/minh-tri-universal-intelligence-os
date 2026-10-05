# MINH TRÍ — Architecture vNext Phase 3 — Knowledge Schema Pilot

**Date:** 2026-10-06  
**Status:** CANDIDATE / BOUNDED PILOT / NOT PROOF OF MEMORY OR SELF-LEARNING  
**Base main:** `31a789342b3933e4a1fc2882a1b38ecf240c755e`

## Objective

Test the vNext atom+hub representation and generated index on two small, canonical project samples:

1. Buddhist thought — A172.
2. Economics — doctoral-level learning program.

This phase deliberately avoids broad migration.

## Buddhist pilot

Canonical source:
`docs/learning/BUDDHIST_THOUGHT_CHECKPOINT_A172_20261005.md`

The pilot preserves a claim A172 itself labels as cross-text synthesis:
- `bud:a172:identity-shame-synthesis`.

It also creates one `PENDING_REVIEW` uncertainty atom:
- `bud:a172:hiri-lexical-open`.

The concept hub may cite the ACTIVE synthesis atom.
It must not use the pending lexical atom as established support.

This tests the distinction between:
- represented knowledge;
- review state;
- hub synthesis;
- unresolved lexical work.

It does not independently verify the early-discourse claims inside A172.

## Economics pilot

Canonical source:
`docs/learning/ECONOMICS_PHD_AUTO_PROGRAM_20261004.md`

The pilot represents one project learning rule:
- causal claims must state identification assumptions.

This is classed `SECONDARY` because it is a project-program rule, not empirical proof of a causal claim.

## Generated index

`tools/generate_knowledge_index.py` generates:
`knowledge/index.json`

The index is derived.
Atoms/hubs remain the durable knowledge records.

The pilot requires index regeneration to be deterministic.

## Pilot acceptance tests

CI must prove:
- atom IDs are unique;
- hub IDs are unique;
- every hub dependency exists;
- a hub cannot depend on a `PENDING_REVIEW` atom;
- generated index matches repository records exactly;
- both Buddhist and economics domains appear;
- pilot does not claim mastery, memory proof, or autonomous self-learning.

## Truth boundary

Passing this phase means:
`ATOM_HUB_SCHEMA_AND_INDEX_PILOT_CI_PROVEN`

It does **not** mean:
- Buddhist lexical audit completed;
- economics competence proven;
- memory retrieval proven;
- application proven;
- self-learning proven.

## Next

After merge/fresh-read:
- Phase 4 creates a held-out retrieval baseline using a fresh-seat test;
- at least one superseded/false decoy must be present;
- the graded seat must not author the held-out questions.
