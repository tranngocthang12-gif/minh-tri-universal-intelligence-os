# MINH TRÍ — PR #168 controlled salvage inventory kickoff

**Date:** 2026-10-06
**Status:** INVENTORY_STARTED / NO_BULK_PROMOTION / NO_WHOLE_BRANCH_MERGE
**Source PR:** #168
**Source head:** `80889a3e6b83f1cb4742b1abe3e796ddfc42ce76`

## Why bounded salvage is required

PR #168 contains a large early-Buddhist source/audit bundle (31 changed files, roughly 13k added lines) including:
- SN 12/22/35/36/45/46 indexes and deep dives;
- Aṭṭhakavagga indexes and lexical/verse passes;
- translation contradiction ledgers/cards;
- Nikāya/Āgama clause-alignment material;
- Milindapañha reasoning-lab material;
- whole-corpus/reference-stack artifacts.

The branch also contains obsolete PROJECT_STATE routing and old live-status claims.

Therefore:
- whole-branch merge is prohibited;
- no old PROJECT_STATE mutation is salvageable as current state;
- source/audit artifacts must be inventoried file-by-file;
- every salvaged artifact keeps provenance and a review status;
- direct-source claims may be promoted only after T1/domain review;
- large structural indexes may be preserved as PENDING_REVIEW evidence before deeper promotion.

## Salvage order

1. inventory exact changed filenames and classify:
   - SOURCE_INDEX
   - TRANSLATION_AUDIT
   - PARALLEL_ALIGNMENT
   - LEXICAL_AUDIT
   - SYNTHESIS
   - LATER/PARACANONICAL
   - OBSOLETE_STATE
2. extract high-value source/audit artifacts without old routing/state.
3. map preserved artifacts into vNext evidence atoms/hubs.
4. T1-review only the claims needed by current Buddhist knowledge.
5. close PR #168 only after unique material is durably preserved or explicitly rejected.

## Truth boundary

Inventory is not verification.
Structural coverage is not mastery.
A historical PASS or “complete index” label is not automatically accepted as current truth.
