# MINH TRÍ — Architecture vNext — Phase 0/1 migration record

**Date:** 2026-10-06  
**Status:** ACTIVE CANDIDATE MIGRATION / NOT CANONICAL UNTIL MERGED  
**Base main:** `a04300f8530c7f8413e8e386c607c7f9938ce32b`  
**Branch:** `owner/architecture-vnext-phase0-1-20261006`

## 1. Owner decision

The Owner approved the Architecture vNext design skeleton after three rounds of independent/cross-adversarial/final adjudication with Claude and Grok.

This record begins implementation without treating chat approval as already-canonical repository state.

## 2. Phase 0 evidence check

### 2.1 PR #251
PR #251 head:
`c6f5f33d6e3c4eebd4e4db1cd6b0f7a3788f8a44`

Live diff inspection shows that #251:
- adds the same learning-core/current-priority facts to Architecture, Bootstrap, Law Index, Universal Learning Law, PROJECT_STATE, and Recovery Manifest;
- adds mandatory `PREWORK RECEIPT` and `MEMORY / APPLICATION` prose gates;
- adds a Philosophy plan;
- strengthens Buddhist source/translation/Pāli discipline;
- formalizes PC/Local Brain as a sidecar.

Conclusion:
`SALVAGE_PARTS / SUPERSEDE_AS_ARCHITECTURE_VNEXT_CANDIDATE`

Do not merge #251 as Architecture vNext.

Salvage:
- Owner intent: self-learning/self-critique remain core;
- durable remember/retrieve/apply/correct requirement;
- Buddhist source discipline;
- philosophy/economics learning portfolio;
- PC/Local Brain sidecar boundary.

Do not carry forward:
- repeated hand-maintained current facts;
- universal checkpoint prose gates as the primary memory mechanism;
- architecture/law/bootstrap copies of mutable facts.

CI evidence:
- Security P0 run #848 on #251 completed with `failure`.

### 2.2 Seat write capability
This ChatGPT seat successfully created:
- branch `owner/architecture-vnext-phase0-1-20261006`;
- the Architecture vNext candidate file on that branch.

Therefore:
- a ChatGPT seat with the connected GitHub capability can perform branch/file writes directly;
- this does **not** prove every external critic/provider can write GitHub;
- seat protocol must distinguish write-capable working seats from read-only/manual external critic seats.

### 2.3 Branch-protection live setting
Direct branch-protection API read returned connector permission `403 Resource not accessible by integration`.

Therefore:
`LIVE_BRANCH_PROTECTION_SETTING = NEED_EVIDENCE_AT_MERGE_TIME`

Do not infer that protection is absent. Do not claim current exact protection settings from this connector result.

### 2.4 Economics location
Economics progress is present on canonical main:
- `docs/learning/ECONOMICS_PHD_AUTO_PROGRAM_20261004.md`;
- PROJECT_STATE records `ACTIVE_DOCTORAL_LEVEL_SELF_STUDY_NOT_ACCREDITED_DEGREE`.

Current evidence does not show economics as a separate canonical brain.

## 3. Open PR inventory — 21 PRs

Rule:
**NO PR IS CLOSED BY THIS PHASE UNTIL SALVAGE REVIEW IS COMPLETE.**

Classification is a migration action, not a truth claim about the PR content.

| PR | Subject | Initial vNext disposition | Reason |
|---|---|---|---|
| #251 | Core learning architecture + durable memory | SALVAGE_PARTS / SUPERSEDE | Duplicates mutable facts and adds prose gates; Owner intent is valuable |
| #250 | Mandatory learning prework receipt | SUPERSEDE_AFTER_SALVAGE | Governance-first pattern; overlapping #251/vNext |
| #249 | Buddhist checkpoint A173 | ACTIVE_LEARNING_DRAFT | Current-base learning work; do not close during architecture migration |
| #237 | Learning-first / remove fixed 3-chat dispatch | SALVAGE_OWNER_INTENT | Direction remains valuable; branch is non-mergeable/stale |
| #235 | Buddhist A165 stacked chain | SALVAGE_CHECK | Historical stacked knowledge; current main is beyond A165 |
| #234 | Learning preflight/canonical rules | SUPERSEDE_AFTER_SALVAGE | Stale/non-mergeable governance branch |
| #233 | Buddhist A164 stacked chain | SALVAGE_CHECK | Historical stacked knowledge |
| #232 | Buddhist A163 stacked chain | SALVAGE_CHECK | Historical stacked knowledge |
| #230 | Aṭṭhakavagga saññā/maññati lexical audit | SALVAGE_PRIORITY | Material domain knowledge; rebase/extract before close |
| #228 | ARCH-CRITIC-01 report | HISTORICAL_EVIDENCE_SALVAGE | Critic evidence, not current architecture |
| #227 | Buddhist A162 | SALVAGE_CHECK | Historical learning branch, non-mergeable |
| #226 | Architecture/self-learning adversarial review | HISTORICAL_EVIDENCE_SALVAGE | Preserve evidence, do not treat as law |
| #218 | Buddhist master review/work plan | SALVAGE_PRIORITY | Potential cross-check/work-plan value |
| #216 | Aṭṭhakavagga diṭṭhi/sacca lexical audit | SALVAGE_PRIORITY | Material domain knowledge |
| #215 | Persistent orchestrator continuity law | SUPERSEDE_AFTER_SALVAGE | vNext rejects orchestrator-law sprawl |
| #193 | GitHub-primary / PC-optional architecture | SALVAGE_OWNER_INTENT | PC-sidecar principle survives; branch is stale/non-mergeable |
| #177 | Buddhist A38→A39 | SALVAGE_CHECK | Far behind canonical track; verify unique knowledge only |
| #170 | Buddhist cross-chat continuity | SALVAGE_OWNER_INTENT_AND_KNOWLEDGE | Continuity intent survives; old large branch |
| #169 | Continuous Buddha study program | SALVAGE_CHECK | Large old branch; inspect unique knowledge before close |
| #168 | Early Buddhist canon AUTO study | SALVAGE_CHECK | Large old branch; inspect unique material before close |
| #167 | Self-learning semantics sync | SUPERSEDE_AFTER_SALVAGE | Architecture semantics replaced by vNext design |

## 4. Phase 1 — minimal precedence rule

Until full law consolidation:

1. Constitution-level Owner decisions outrank Stable Law.
2. Stable Law outranks Policy.
3. Policy outranks Domain Rule.
4. Domain Rule outranks ADR/current operational preference only inside that domain.
5. Current State is not law.
6. Historical checkpoints and critic packets are evidence, not normative authority.
7. Same-level conflict requires explicit supersession; otherwise create one canonical task.
8. No new parallel law file for a concern already owned by an existing layer.
9. No mutable current fact may be copied into multiple hand-maintained normative files.
10. Domain-specific Buddhist epistemology must not silently bind economics, software, YouTube, or future domains.

This Phase-1 precedence rule is intentionally small. Full law consolidation is Phase 6, after state/task/knowledge migration works.

## 5. Migration safety rules

- Buddhist learning continues during architecture migration.
- No mass rewrite of historical checkpoints.
- No PC dependency for Phases 0–6 unless a specific task truly requires PC.
- No new microservices/vector brain/workflow engine/assurance platform.
- No autonomous merge.
- No closing open PRs before salvage review.
- No promotion of unreviewed salvaged text to ACTIVE knowledge.
- Every migration PR is small and reversible.
- vNext implementation details may change when measured evidence contradicts the current default; the nine-component skeleton and eight constitutional principles require explicit Owner-level reconsideration to change.

## 6. Phase 0/1 completion criteria

Phase 0/1 candidate is reviewable when:
- Owner-approved vNext design is in one consolidated candidate document;
- all 21 open PRs are inventoried without destructive close;
- #251 disposition is explicit;
- economics location is verified;
- seat write capability is recorded;
- live branch-protection uncertainty is recorded rather than guessed;
- minimal precedence is explicit;
- no duplicated PROJECT_STATE/Recovery edits are introduced by this PR;
- existing learning work is not blocked.

## 7. Next migration step after this PR

If this candidate passes CI and is merged/fresh-read:
- Phase 2 creates the small current-state core and one task registry;
- Phase 3 begins the atom+hub knowledge schema on a bounded sample before broad migration.

No Phase 2/3 mutation is included in this PR.