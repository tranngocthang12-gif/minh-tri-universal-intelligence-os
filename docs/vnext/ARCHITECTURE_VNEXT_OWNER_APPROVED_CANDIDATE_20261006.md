# MINH TRÍ — Architecture vNext — Current architecture

**Date:** 2026-10-06  
**Status:** CURRENT ARCHITECTURE / MIGRATION ACTIVE  
**Base main:** `a04300f8530c7f8413e8e386c607c7f9938ce32b`  
**Critic gate:** ARCH-VNEXT-CRITIC-01 — three rounds complete  
**Owner decision:** the architecture skeleton is approved; implementation details remain evidence-driven and reversible.

## 1. Purpose

Architecture vNext exists to let MINH TRÍ learn deeply across many domains for years without letting knowledge growth force architecture growth.

The design must preserve:
- Owner authority;
- one durable continuity authority;
- replaceable chats/models/tools;
- self-learning and self-critique as core design intent without false capability claims;
- durable knowledge that can be retrieved, connected, applied, corrected, and revalidated;
- domain-specific epistemic rules without leaking them into global law;
- PC/Local Brain as non-canonical execution/mirror sidecars;
- future transition from learning-heavy work to practice, production, and outcome-based improvement.

Architecture growth is not knowledge growth.

## 2. Eight constitutional principles

These are mechanism-free. They must remain meaningful even if Git, CI, YAML, or the current model provider is replaced.

1. **Owner sovereignty.** The Owner sets purpose, priorities, permissions, and promotion of foundational change.
2. **Single continuity authority.** There is one durable continuity authority. A record stored there is not automatically VERIFIED truth.
3. **Active durable claims require provenance.** A claim cannot be active durable knowledge without provenance, evidence class, and status.
4. **Canonical change requires review and a retained record.** Foundational change cannot silently replace the previous rule or state.
5. **Seats are replaceable.** No chat, model, provider, PC, or hidden provider memory may hold unique canonical state.
6. **Knowledge growth must not force core growth.** New domains are data and domain rules, not new core architecture by default.
7. **Capability claims require proof classes.** MINH TRÍ must not claim a capability merely because code, law, checkpoints, or CI exist.
8. **Corrections supersede; history is not rewritten.** Wrong or narrowed understanding is corrected by explicit supersession while preserving provenance.

## 3. Law hierarchy and precedence

Normative precedence is owned by `docs/vnext/FOUNDATION_LAW_CONSOLIDATED_V1_20261006.md`. This architecture does not duplicate the ladder.

Domain-specific evidence rules are owned by their domain law sources. For Buddhist study, the canonical source hierarchy and Milindapañha rule remain in `docs/LAW_UNIVERSAL_LEARNING_CONTINUITY_20261004.md`.

Architecture may point to law but does not restate or override it.

## 4. Nine core components

### 4.1 Constitution & Law
Owns the eight constitutional rules, Stable Law, Policy, precedence, and amendment/supersession records.

Forbidden:
- domain learning content;
- live task status;
- duplicated current facts.

### 4.2 Current State Core
Owns only a small machine-readable current state:
- phase;
- schema version;
- a small bounded set of global flags.

Target artifact after migration:
`state/current.yaml`

Constraint:
- keep it small;
- no knowledge;
- no task backlog;
- no duplicated prose facts.

### 4.3 Task Registry
Owns the only assignment/task truth.

Target artifact after migration:
`state/tasks.yaml`

Minimum semantics:
- task_id;
- status;
- scope;
- branch;
- holder/seat when applicable;
- lease expiry when applicable;
- base_sha;
- requires: pc|none;
- dependencies/supersession;
- result_ref.

PRs are not tasks. Open PRs may be drafts or work products, but they are never the task registry.

### 4.4 Knowledge Fabric
Uses a hybrid model.

**Typed atoms**:
- source;
- evidence;
- claim;
- passage/argument;
- application;
- outcome.

**Hubs**:
- concept;
- lesson;
- domain map.

Why hybrid:
- atom-only representation loses argument structure and nuance;
- prose-only representation cannot reliably support provenance, supersession, retrieval, and contradiction checks.

A material hub interpretation must cite typed atoms.

### 4.5 Retrieval & Memory
Memory is not storage.

The memory ladder is:
1. STORED;
2. INDEXED;
3. RETRIEVED;
4. APPLIED;
5. CORRECTED_AFTER_SUPERSESSION.

Definitions:
- STORED: durable record exists.
- INDEXED: record is discoverable through generated index/working set.
- RETRIEVED: a fresh seat surfaces the correct active record and avoids superseded/false decoys.
- APPLIED: a task uses the record correctly within scope.
- CORRECTED_AFTER_SUPERSESSION: a later fresh seat uses the replacement and recognizes that the old claim is retired/narrowed.

No same-session self-written quiz is sufficient proof of memory.

### 4.6 Seat Protocol
Every material seat is replaceable.

Boot target:
`state/bootstrap.json -> current state -> task registry -> authoritative law precedence -> current architecture -> active task handoff -> domain working set as needed`

Required properties:
- fresh read;
- base SHA;
- write scope;
- stale-writer rejection;
- semantic dependency check for superseded claims;
- schema compatibility;
- structured handoff for interrupted work.

A mid-task handoff may live on a pushed task branch, but it never outranks canonical state/task truth.

### 4.7 Change Pipeline
Normal path:
`branch -> PR -> required checks -> merge -> fresh-read main`

Architecture vNext does **not** authorize autonomous merge.

A knowledge fast lane may use a smaller check set than architecture/law changes, but it may not bypass:
- source/provenance;
- evidence/status requirements;
- scope checks;
- stale checks.

Any future delegated merge requires an explicit Owner policy decision after measured throughput evidence.

### 4.8 Critique & Learning Evaluation
Critique is tiered by blast radius.

- **T0:** self-check on ordinary records.
- **T1:** second pass for synthesis, supersession, promotion, or reusable lessons.
- **T2:** Owner + external critic for constitution, Stable Law, architecture, or phase changes.

No standing critic bureaucracy is required for ordinary checkpoints.

Learning Assurance, witness, and trial machinery are not a separate platform in vNext. Future evaluation is a fixture/test capability inside Retrieval & Memory.

### 4.9 Decisions & Execution Boundary
ADRs preserve architectural decisions:
- context;
- decision;
- alternatives;
- consequences;
- supersedes.

PC / Local Brain / desktop tools are execution sidecars:
- local secrets;
- UI automation;
- runtime experiments;
- telemetry;
- PC-bound files/apps.

They must not become a second canonical brain.

## 5. Self-learning truth model

Self-learning is split into six layers:

1. **Owner intent:** CORE.
2. **Architectural invariant:** the system must provide a common interface for durable recording, retrieval, supersession, and application.
3. **Learning data model:** build now.
4. **Seat learning protocol:** manual/seat-driven learning is allowed and is the present execution mode.
5. **Autonomous runtime:** OFF unless separately proven and authorized.
6. **Empirical capability claim:** NOT PROVEN until an explicit proof class is satisfied.

Allowed current statement:
MINH TRÍ has an architecture and protocol for durable learning work.

Forbidden current statement:
MINH TRÍ has proven autonomous behavioral self-learning merely because the architecture exists.

## 6. Knowledge status model

Generic evidence classes must be domain-neutral enough to scale, with domain-specific mappings where necessary.

Minimum status semantics:
- ACTIVE;
- UNCERTAIN;
- DISPUTED;
- SUPERSEDED;
- REFUTED;
- PENDING_REVIEW.

Unreviewed salvaged material must not become ACTIVE merely because it is merged.

## 7. Transition to practice and production

Per-domain progression:

`LEARNING -> PRACTICE -> PRODUCTION -> CLOSED-LOOP IMPROVEMENT`

Learning:
- source/evidence/claim/concept;
- retrieval proof;
- application opportunities may be recorded.

Practice:
- real application records cite knowledge used.

Production:
- real-world outcome records exist;
- work may affect publication, money, systems, or other people only under explicit Owner/tool scope.

Closed-loop improvement:
`knowledge -> decision -> action -> outcome -> evaluation -> correction/lesson`

Outcome records are not fabricated before real outcomes exist.

## 8. Deferred technologies / non-goals

Do not build now:
- microservices;
- service mesh;
- Kubernetes;
- distributed database;
- vector database as canonical brain;
- graph database as canonical brain;
- workflow engine;
- permanent autonomous agents as canonical writers;
- automatic self-modification;
- autonomous merge;
- extra witness/assurance/trial platforms;
- full event sourcing of every file.

A deferred technology may be reconsidered only after a measured failure plus ADR.

## 9. Fitness requirements for migration

Architecture vNext is not complete until it can demonstrate:

**Law-first foundation gate:** before any remaining architecture-completion claim, project-wide continuity/handoff law must be canonical and enforced. A new zero-chat seat must recover law → current state → task registry → exact NEXT ACTION without Owner recap. Missing/stale/conflicting handoff must fail closed.

1. cold-start recovery from canonical main without chat memory;
2. one current-state authority;
3. one task registry;
4. generated views cannot silently drift from canonical sources;
5. stale writer is rejected;
6. superseded dependency is detected;
7. knowledge PR cannot become active without provenance/status;
8. quarantined/pending material is not treated as active;
9. domain rules do not leak upward;
10. PC outage does not block non-PC knowledge learning;
11. fresh seat can retrieve an active Buddhist claim and avoid a superseded/false decoy;
12. old history remains addressable after migration.

## 10. Owner-approved migration order

### Phase 0 — inventory and salvage
- classify all open PRs;
- no close before salvage review;
- preserve sources/reviewed claims;
- quarantine unreviewed material;
- read #251 rather than merging it by intent.

### Phase 1 — precedence and freeze
- establish hierarchy/precedence;
- stop new law sprawl;
- do not rewrite all old law yet;
- keep Buddhist learning running.

### Phase 2 — current state + task registry
- introduce one small current state and one task registry;
- convert duplicated narrative state into generated views over time.

### Phase 3 — knowledge schema v1
- add atom + hub schema to new work;
- progressively map existing Buddhist/economics material without rewriting historical bodies.

### Phase 4 — retrieval/memory proof
- fresh-seat held-out tests;
- superseded/false decoys;
- later application/correction tests.

### Phase 5 — seat/stale enforcement and fast knowledge lane
- enforce base/scope/semantic staleness;
- measure Owner merge throughput before any delegated merge decision.

### Phase 6 — law consolidation
- consolidate only after the new state/knowledge model works;
- supersede old law explicitly;
- preserve history.

### Phase 7 — practice/outcome loop
- begin when real practical work exists.

## 11. PR #251 disposition

PR #251 is **not** Architecture vNext.

Salvage:
- Owner intent that self-learning/self-critique remain core;
- learning must be remembered/retrieved/applied/corrected;
- Buddhist source discipline;
- philosophy/economics learning portfolio;
- PC/Local Brain sidecar boundary.

Do not preserve as vNext:
- duplicated current-state facts across multiple hand-maintained files;
- new universal prose gates that increase checkpoint bureaucracy without proving retrieval/application;
- architecture/law/bootstrap copies of the same mutable facts.

Disposition:
`SALVAGE_PARTS / SUPERSEDE_AS_ARCHITECTURE_VNEXT_CANDIDATE`

## 12. Canonicalization and migration rule

This architecture became canonical only after protected PR/CI/merge and fresh-read main. Subsequent migration still follows:
`branch -> PR -> required CI -> merge -> fresh-read main`

Migration phases proceed through small reversible PRs. Historical candidate wording or pre-merge base SHAs are provenance only, not current-state authority.