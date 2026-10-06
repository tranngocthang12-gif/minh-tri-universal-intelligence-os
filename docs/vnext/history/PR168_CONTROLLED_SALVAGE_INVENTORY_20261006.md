# MINH TRÍ — PR #168 controlled salvage inventory — 2026-10-06

**Status:** CANDIDATE INVENTORY / NO BULK PROMOTION / NO WHOLE-BRANCH MERGE  
**Source PR:** #168  
**Source head:** `80889a3e6b83f1cb4742b1abe3e796ddfc42ce76`  
**Base main:** `9b4bf7f7c2fc89b0d534d2b9f6e71d1832aee598`

## Classification rule

Each changed file is assigned one primary salvage class:

- `SOURCE_INDEX` — structural discourse/verse/reference index.
- `TRANSLATION_AUDIT` — translation cards, contradiction ledgers, comparison records.
- `PARALLEL_ALIGNMENT` — Nikāya/Āgama/parallel-text alignment work.
- `LEXICAL_AUDIT` — term-level lexical or morphology analysis.
- `SYNTHESIS` — project interpretation/integration; cannot be promoted merely by salvage.
- `LATER_PARACANONICAL` — Milindapañha or other later supporting reasoning.
- `PROGRAM_OR_METHOD` — learning program / process design.
- `MEMORY_OR_META_AUDIT` — audit of learning-memory process.
- `OBSOLETE_STATE` — old routing/current-state mutation; not salvageable as present state.

Inventory means preservation priority only. It is not verification.

## Exact file inventory

| File | Class | Salvage disposition |
|---|---|---|
| `docs/PROJECT_STATE.json` | OBSOLETE_STATE | REJECT_AS_CURRENT_STATE |
| `docs/learning/EARLY_BUDDHIST_ANCHOR_DEEP_DIVE_V0_9_20261004.md` | SYNTHESIS | REVIEW_LATER |
| `docs/learning/EARLY_BUDDHIST_ARTHAPADA_AGAMA_MILINDA_STRESS_TEST_V0_1_20261004.md` | PARALLEL_ALIGNMENT | HIGH_VALUE_REVIEW |
| `docs/learning/EARLY_BUDDHIST_ATTHAKAVAGGA_INDEX_V0_1.json` | SOURCE_INDEX | HIGH_VALUE_EXTRACT |
| `docs/learning/EARLY_BUDDHIST_ATTHAKAVAGGA_LEXICAL_PASS_V0_3_20261004.md` | LEXICAL_AUDIT | HIGH_VALUE_REVIEW |
| `docs/learning/EARLY_BUDDHIST_ATTHAKAVAGGA_VERSE_AUDIT_V0_2.json` | SOURCE_INDEX | HIGH_VALUE_EXTRACT |
| `docs/learning/EARLY_BUDDHIST_CANON_AUTO_PROGRAM_20261004.md` | PROGRAM_OR_METHOD | REVIEW_LATER |
| `docs/learning/EARLY_BUDDHIST_CHAT_LEARNING_MEMORY_AUDIT_20261004.md` | MEMORY_OR_META_AUDIT | HISTORICAL_EVIDENCE |
| `docs/learning/EARLY_BUDDHIST_CLAUSE_ALIGNMENT_V0_7_20261004.md` | PARALLEL_ALIGNMENT | HIGH_VALUE_REVIEW |
| `docs/learning/EARLY_BUDDHIST_DIALOGUE_RECONSTRUCTION_V0_5_20261004.md` | SYNTHESIS | REVIEW_LATER |
| `docs/learning/EARLY_BUDDHIST_DISCOURSE_VERSE_PASS_V0_10_20261004.md` | SOURCE_INDEX | HIGH_VALUE_REVIEW |
| `docs/learning/EARLY_BUDDHIST_HARD_CLUSTER_V0_8_20261004.md` | SYNTHESIS | REVIEW_LATER |
| `docs/learning/EARLY_BUDDHIST_MN_DIALOGUE_INDEX_V0_1.json` | SOURCE_INDEX | HIGH_VALUE_EXTRACT |
| `docs/learning/EARLY_BUDDHIST_PARALLEL_TRANSLATION_CONTRADICTION_V0_6_20261004.md` | TRANSLATION_AUDIT | HIGH_VALUE_REVIEW |
| `docs/learning/EARLY_BUDDHIST_REASONING_SYNTHESIS_V0_1_20261004.md` | SYNTHESIS | HISTORICAL_EVIDENCE |
| `docs/learning/EARLY_BUDDHIST_REASONING_SYNTHESIS_V0_2_20261004.md` | SYNTHESIS | HISTORICAL_EVIDENCE |
| `docs/learning/EARLY_BUDDHIST_REASONING_SYNTHESIS_V0_3_ADVERSARIAL_20261004.md` | SYNTHESIS | HISTORICAL_EVIDENCE |
| `docs/learning/EARLY_BUDDHIST_REASONING_SYNTHESIS_V0_4_STRESS_TEST_20261004.md` | SYNTHESIS | HIGH_VALUE_REVIEW |
| `docs/learning/EARLY_BUDDHIST_REFERENCE_STACK_V0_1_20261004.md` | SOURCE_INDEX | HIGH_VALUE_EXTRACT |
| `docs/learning/EARLY_BUDDHIST_SN12_PEYYALA_MATRIX_AUDIT_V0_1_20261004.md` | SOURCE_INDEX | HIGH_VALUE_EXTRACT |
| `docs/learning/EARLY_BUDDHIST_SN22_ID_INDEX_V0_1.json` | SOURCE_INDEX | HIGH_VALUE_EXTRACT |
| `docs/learning/EARLY_BUDDHIST_SN35_ID_INDEX_V0_1.json` | SOURCE_INDEX | HIGH_VALUE_EXTRACT |
| `docs/learning/EARLY_BUDDHIST_SN36_DISCOURSE_INDEX_V0_1.json` | SOURCE_INDEX | HIGH_VALUE_EXTRACT |
| `docs/learning/EARLY_BUDDHIST_SN45_ID_INDEX_V0_1.json` | SOURCE_INDEX | HIGH_VALUE_EXTRACT |
| `docs/learning/EARLY_BUDDHIST_SN46_ID_INDEX_V0_1.json` | SOURCE_INDEX | HIGH_VALUE_EXTRACT |
| `docs/learning/EARLY_BUDDHIST_SN_CORE_INDEX_V0_2_20261004.md` | SOURCE_INDEX | HIGH_VALUE_EXTRACT |
| `docs/learning/EARLY_BUDDHIST_TRANSLATION_CARDS_V0_2.json` | TRANSLATION_AUDIT | HIGH_VALUE_EXTRACT |
| `docs/learning/EARLY_BUDDHIST_TRANSLATION_CONTRADICTION_LEDGER_V0_1.json` | TRANSLATION_AUDIT | HIGH_VALUE_EXTRACT |
| `docs/learning/EARLY_BUDDHIST_WHOLE_CORPUS_INDEX_V0_1.json` | SOURCE_INDEX | HIGH_VALUE_EXTRACT |
| `docs/learning/MILINDAPANHA_REASONING_LAB_V0_1_20261004.md` | LATER_PARACANONICAL | HIGH_VALUE_REVIEW |
| `docs/learning/OWNER_MEMORY_EARLY_BUDDHIST_STUDY_20261004.md` | MEMORY_OR_META_AUDIT | HISTORICAL_EVIDENCE |

## Structural extraction set

The first extraction wave will preserve exact source/index structures only, as `PENDING_REVIEW` evidence:

1. `EARLY_BUDDHIST_ATTHAKAVAGGA_INDEX_V0_1.json`
2. `EARLY_BUDDHIST_ATTHAKAVAGGA_VERSE_AUDIT_V0_2.json`
3. `EARLY_BUDDHIST_MN_DIALOGUE_INDEX_V0_1.json`
4. `EARLY_BUDDHIST_SN22_ID_INDEX_V0_1.json`
5. `EARLY_BUDDHIST_SN35_ID_INDEX_V0_1.json`
6. `EARLY_BUDDHIST_SN36_DISCOURSE_INDEX_V0_1.json`
7. `EARLY_BUDDHIST_SN45_ID_INDEX_V0_1.json`
8. `EARLY_BUDDHIST_SN46_ID_INDEX_V0_1.json`
9. `EARLY_BUDDHIST_TRANSLATION_CARDS_V0_2.json`
10. `EARLY_BUDDHIST_TRANSLATION_CONTRADICTION_LEDGER_V0_1.json`
11. `EARLY_BUDDHIST_WHOLE_CORPUS_INDEX_V0_1.json`

These files are chosen because their principal value is structured retrieval/provenance rather than broad interpretive synthesis.

## Explicit non-salvage from PR #168

The old `docs/PROJECT_STATE.json` mutation is rejected as present-state authority.

No status phrase such as “complete”, “pass”, “deep dive”, or “whole corpus” inside PR #168 is inherited as a vNext capability claim.

## Review ordering after structural extraction

1. Aṭṭhakavagga structural indexes.
2. SN 22/35/36/45/46 indexes.
3. translation cards + contradiction ledger.
4. Arthapada/Āgama/Milinda stress-test and clause alignment.
5. lexical pass.
6. Milindapañha reasoning lab.
7. synthesis files only if current knowledge still has an unresolved need they can inform.

## Closure condition for PR #168

Do not close PR #168 until:
- high-value structural artifacts are durably preserved with source PR/head/blob provenance;
- high-value non-structural audits are either reviewed, explicitly deferred, or recorded as historical evidence;
- obsolete state is explicitly rejected;
- task registry records final disposition.

## Truth boundary

This inventory proves only that the bundle has been classified and that structural salvage priorities are explicit.

It does not prove:
- index completeness;
- source correctness;
- translation correctness;
- doctrinal correctness;
- memory;
- mastery;
- autonomous learning.
