# MINH TRÍ — Knowledge PR Salvage Wave 2 Inventory — 2026-10-06

**Status:** CANDIDATE / REVIEW REQUIRED / NO BLIND CLOSE  
**Base main:** `140276378356ee48559879689c64cd1684975d00`

## Purpose

Inventory the remaining pre-vNext knowledge/content PRs after architecture/governance Wave 1.

This wave is intentionally conservative:
- preserve unique knowledge;
- detect semantic collisions;
- distinguish current drafts from historical bundles;
- do not close any PR merely because its number or filename resembles a canonical checkpoint.

## Remaining PRs

### #249 — Buddhist checkpoint A173
Disposition: `ACTIVE_LEARNING_DRAFT`

Unique files not present on main:
- `BUDDHIST_THOUGHT_CHECKPOINT_A173_20261005.md`
- A174–A177 draft files
- compliance audit

Action:
- keep open;
- review as current learning work;
- do not fold into architecture migration.

### #230 — Aṭṭhakavagga lexical audit: saññā / maññati
Disposition: `SALVAGE_PRIORITY_UNIQUE_KNOWLEDGE`

Unique file is not present on main.

Action:
- preserve exact lexical audit;
- review against current Buddhist source hierarchy before promotion;
- do not close before extraction/review.

### #216 — Aṭṭhakavagga lexical audit: diṭṭhi / sacca
Disposition: `SALVAGE_PRIORITY_UNIQUE_KNOWLEDGE`

Unique file is not present on main.

Action:
- preserve exact lexical audit;
- review before promotion;
- do not close before extraction/review.

### #218 — Buddhist master review/work plan
Disposition: `SALVAGE_PRIORITY_PLANNING_EVIDENCE`

Unique file is not present on main.

Action:
- preserve as planning evidence;
- do not automatically promote its conclusions to active knowledge.

### #227 / #232 / #233 / #235 — stacked A162–A165 chain
Disposition: `SEMANTIC_COLLISION_REVIEW_REQUIRED`

Critical finding:
- files with the same checkpoint numbers exist on main;
- exact content is different;
- branch versions contain different primary questions/topics, not just metadata drift.

Therefore:
- these PRs are **not duplicates**;
- checkpoint number alone is not a safe identity key;
- do not close until unique knowledge is extracted or explicitly superseded by content-level review.

Migration implication:
future Buddhist knowledge IDs must not use checkpoint number alone as semantic identity.

### #177 — older Buddhist checkpoint branch
Disposition: `LEGACY_CHECKPOINT_REVIEW_REQUIRED`

The branch is stale relative to current main, but stale chronology does not prove knowledge duplication.

Action:
- inspect unique learning content before closure.

### #170 — Buddhist cross-chat continuity + A6–A30 corpus
Disposition: `LARGE_LEGACY_KNOWLEDGE_BUNDLE_REVIEW_REQUIRED`

Contains many Phase 4 learning files plus continuity/governance edits.

Action:
- separate domain knowledge from obsolete continuity/state changes;
- salvage knowledge by content, not by branch merge;
- do not close blindly.

### #169 — continuous Buddha study program + Phase 2/3 corpus
Disposition: `LARGE_LEGACY_KNOWLEDGE_BUNDLE_REVIEW_REQUIRED`

Contains many early synthesis/study files not currently present on main under the same paths.

Action:
- build content inventory;
- identify what later checkpoints already absorbed;
- preserve unresolved/unique material as historical knowledge evidence.

### #168 — Early Buddhist canon AUTO program
Disposition: `LARGE_LEGACY_SOURCE_AUDIT_BUNDLE_REVIEW_REQUIRED`

Contains:
- discourse/verse indexes;
- lexical passes;
- translation cards;
- contradiction ledgers;
- SN indexes;
- Milindapañha reasoning lab;
- source/reference structures.

This is potentially high-value source-analysis material.

Action:
- highest caution;
- no blind close;
- salvage source/audit artifacts selectively into current knowledge architecture;
- preserve provenance and status.

## Wave 2 architecture findings

### 1. Checkpoint number is not a durable semantic identifier
The A162–A165 collision proves that a reused sequential label can point to different content.

vNext rule:
- durable knowledge identity must be content/domain scoped;
- checkpoint labels are chronology/handoff aids only.

### 2. PR state is not knowledge state
An old/stale PR can still contain unique useful knowledge.
A mergeable PR can still contain unreviewed or superseded claims.

Therefore:
- task registry owns workflow state;
- knowledge atoms/hubs own knowledge status;
- PR open/closed state must not be used as truth classification.

### 3. Large historical branches require indexed salvage
For #168/#169/#170, whole-branch merge is rejected.
Required path:
`inventory -> classify -> extract -> review -> map to atoms/hubs -> supersede/reference`

### 4. No destructive cleanup until knowledge salvage completes
Wave 2 authorizes **zero** PR closures.

## Recommended next salvage order

1. #230 and #216 lexical audits.
2. #218 master review plan.
3. #227/#232/#233/#235 semantic-collision chain.
4. #168 source/audit bundle.
5. #169/#170 large synthesis bundles.
6. #177 legacy checkpoint.
7. #249 stays active as current learning draft.

## Truth boundary

This inventory does not validate the claims inside these PRs.
It only proves they cannot safely be treated as duplicates or discarded based on chronology/filename alone.
