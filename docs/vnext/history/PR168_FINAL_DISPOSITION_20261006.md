# MINH TRÍ — PR #168 final disposition — 2026-10-06

**Status:** CANDIDATE FINAL DISPOSITION / CLOSE ONLY AFTER MERGE  
**Source PR:** #168  
**Source head:** `80889a3e6b83f1cb4742b1abe3e796ddfc42ce76`  
**Base main:** `d87ffa8ab0dea6c538e73686b8a69b047708e66a`

## What has already been durably preserved

Canonical vNext now contains exact preserved evidence from PR #168 for:
- Aṭṭhakavagga structural index;
- Aṭṭhakavagga verse audit;
- MN dialogue index;
- SN 36 structural index;
- SN 22 / SN 35 / SN 45 / SN 46 large structural indexes;
- translation cards;
- translation contradiction ledger;
- whole-corpus structural index;
- Arthapada / Āgama / Milindapañha stress-test;
- clause alignment;
- parallel translation / contradiction audit;
- Aṭṭhakavagga lexical pass;
- Milindapañha reasoning lab.

All remain evidence-level unless separately reviewed and promoted.

## Final disposition of remaining PR #168 files

### REJECT_AS_CURRENT_STATE

- `docs/PROJECT_STATE.json`

Reason:
old branch-local current-state mutation cannot override vNext canonical state.

### SUPERSEDED_METHOD_OR_CONTINUITY

- `EARLY_BUDDHIST_CANON_AUTO_PROGRAM_20261004.md`
- `EARLY_BUDDHIST_CHAT_LEARNING_MEMORY_AUDIT_20261004.md`
- `OWNER_MEMORY_EARLY_BUDDHIST_STUDY_20261004.md`

Reason:
their durable intent survives in the current learning law/source hierarchy, vNext state/task registry, and knowledge fabric.
Their old routing/current-status language is not current authority.

### HISTORICAL_SYNTHESIS_ONLY

- `EARLY_BUDDHIST_REASONING_SYNTHESIS_V0_1_20261004.md`
- `EARLY_BUDDHIST_REASONING_SYNTHESIS_V0_2_20261004.md`
- `EARLY_BUDDHIST_REASONING_SYNTHESIS_V0_3_ADVERSARIAL_20261004.md`
- `EARLY_BUDDHIST_REASONING_SYNTHESIS_V0_4_STRESS_TEST_20261004.md`
- `EARLY_BUDDHIST_DIALOGUE_RECONSTRUCTION_V0_5_20261004.md`
- `EARLY_BUDDHIST_HARD_CLUSTER_V0_8_20261004.md`

Reason:
these are broad historical syntheses and reconstruction exercises.
They remain useful as audit/history evidence in PR #168, but no broad conclusion is promoted merely by branch salvage.

### DEFER_EXTRACT_UNTIL_CURRENT_TASK_NEEDS_IT

- `EARLY_BUDDHIST_ANCHOR_DEEP_DIVE_V0_9_20261004.md`
- `EARLY_BUDDHIST_DISCOURSE_VERSE_PASS_V0_10_20261004.md`
- `EARLY_BUDDHIST_REFERENCE_STACK_V0_1_20261004.md`
- `EARLY_BUDDHIST_SN12_PEYYALA_MATRIX_AUDIT_V0_1_20261004.md`
- `EARLY_BUDDHIST_SN_CORE_INDEX_V0_2_20261004.md`

Reason:
these contain potentially useful domain material, but copying them wholesale would recreate document sprawl.
Their source PR/head remain addressable.
If a current Buddhist task needs a specific claim, source mapping, or matrix, extract that bounded item with provenance and review then.

## Durable principles retained without duplicating old files

The following principles survive the migration:
- early discourse evidence outranks later explanatory material;
- cross-traditional parallels can raise or lower confidence;
- translation divergence is evidence, not noise to erase;
- unresolved contradiction remains unresolved;
- structural coverage is not semantic mastery;
- Milindapañha is a later/paracanonical reasoning aid and never overrides early-discourse evidence;
- broad synthesis must be decomposed into bounded reviewed claims before becoming active knowledge.

## Closure condition

After this disposition record merges:
- PR #168 has no remaining unclassified high-value artifact;
- unique structured/audit materials are durably preserved;
- broad synthesis is retained by Git history as historical evidence;
- obsolete state/method artifacts are explicitly superseded or rejected.

At that point PR #168 may be closed without merge.

Closing PR #168 does not mean:
- all source material is verified;
- the Buddhist corpus is mastered;
- all historical synthesis is accepted;
- all deferred files are useless.

It means PR #168 is no longer a live architecture/knowledge integration candidate.

## Next legacy bundles

Continue controlled salvage on:
1. PR #169
2. PR #170
3. PR #177
while keeping PR #249 as current Buddhist learning draft unless its state changes.

## Truth boundary

This is a migration disposition, not a doctrinal validation document.
