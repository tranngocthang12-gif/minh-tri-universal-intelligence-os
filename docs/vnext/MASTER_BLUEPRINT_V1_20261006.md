# MINH TRÍ — MASTER ARCHITECTURE / MASTER BLUEPRINT v1 — 2026-10-06

**Status:** FOUNDATION CANDIDATE — REQUIRES INDEPENDENT REVIEW AND OWNER ACCEPTANCE  
**Canonical target:** project-wide organization + law + lifecycle architecture  
**Durable authority:** GitHub protected main after approved merge

## 1. Final system

MINH TRÍ is a long-lived Owner-directed knowledge and execution organization whose state survives replacement of chats, models, providers, tools, and PCs.

The finished system must preserve:
- one constitutional direction;
- one law-precedence system;
- one canonical current-state authority;
- one canonical task registry;
- one current Master Blueprint;
- bounded domain knowledge with provenance and supersession;
- replaceable AI seats;
- independent review and evidence;
- controlled change.

No chat, model, provider, PC, sidecar, hidden memory, or unmerged branch may become a second canonical brain.

## 2. Design principle: structure and law are co-designed

The project does **not** choose “organization first” or “law first” in isolation.

The correct order is:

1. Owner intent and constitutional invariants;
2. Master Blueprint defining structure, boundaries, roles, authority, and lifecycle;
3. laws that govern those structures;
4. implementation under the approved design;
5. supervision against design and law;
6. evidence/validation;
7. acceptance;
8. operation;
9. controlled amendment.

Law without architecture is unenforceable prose.
Architecture without law becomes uncontrolled power.
They are designed together, then versioned and changed under one governance lifecycle.

## 3. Foundation that must remain stable

Foundation invariants:
1. Owner sovereignty.
2. GitHub protected main is durable continuity authority.
3. One boot root.
4. One normative law-precedence router.
5. One current-state authority.
6. One task registry.
7. One Master Blueprint pointer.
8. Chats/seats/tools are replaceable.
9. Material claims require provenance/status.
10. Corrections supersede; history is preserved.
11. No role self-certifies its own material work.
12. Foundation changes require explicit review, evidence, acceptance, and protected merge.
13. No autonomous merge or self-modification in Foundation unless Owner later creates a new explicit constitutional decision.

These are harder to change than modules, workflows, domain knowledge, or tools.

## 4. Extensible zones

May grow without reopening the core architecture when they respect foundation contracts:
- knowledge domains;
- domain-specific rules below foundation law;
- learning programs;
- applications;
- tools/providers;
- local sidecars;
- evaluation fixtures;
- reports and generated views;
- implementation modules.

Growth in these zones must not create new canonical authorities.

## 5. System layers

### Layer A — Constitution & Governance
Owns:
- Owner constitutional decisions;
- law hierarchy;
- role authority;
- amendment rules;
- acceptance/freeze/reopen rules.

Must not own live task state or domain knowledge.

### Layer B — Master Architecture
Owns:
- total system structure;
- component boundaries;
- lifecycle;
- interface contracts;
- stable vs extensible zones;
- role separation;
- canonical-source map.

It does not supersede law; it is governed by law.

### Layer C — Canonical Control State
Owns:
- boot root;
- current state;
- task registry;
- current architecture pointer;
- active handoff pointers.

This is the operational truth for “where the system is now.”

### Layer D — Knowledge Fabric
Owns:
- source/evidence/claim/concept/application/outcome records;
- statuses;
- provenance;
- supersession;
- domain hubs/maps.

Knowledge is not current project control state.

### Layer E — Work & Change Pipeline
Owns:
- task scope;
- branch/base;
- implementation work;
- PR/check/merge workflow;
- handoff and exact next action.

### Layer F — Supervision & Inspection
Compares:
- approved design vs implementation;
- approved law vs implementation;
- task scope vs changed artifacts;
- canonical state vs handoff.

Supervisor reports defects; it does not silently redesign the system.

### Layer G — Independent Critique
Challenges:
- design assumptions;
- contradictions;
- split-brain risks;
- overclaims;
- hidden coupling;
- weak evidence;
- unsafe change.

Critic has no merge authority.

### Layer H — Evidence & Validation
Owns evidence classes:
- static checks;
- deterministic tests;
- fresh-seat recovery proofs;
- independent reproduction;
- runtime evidence where required;
- receipt/provenance binding.

Evidence does not automatically create truth beyond its proof scope.

### Layer I — Execution Sidecars
PC, Local Brain, desktop tools, external providers, APIs, automation.

They execute work but do not hold unique canonical authority.

### Layer J — History & Audit
Preserves:
- superseded law;
- old architecture;
- failed proofs;
- rejected candidates;
- prior receipts;
- decisions and provenance.

History is readable but cannot silently override current authority.

## 6. Role model and separation of duties

### Owner
Final authority for:
- constitutional objectives;
- foundation acceptance;
- foundation exceptions;
- major scope changes;
- explicit rejection of material critic findings.

Owner may delegate execution but not lose final sovereignty.

### Architect
Responsibilities:
- maintain this Master Blueprint;
- define system boundaries and interfaces;
- classify foundation vs extensible change;
- design transitions.

Architect may propose but may not self-approve foundation architecture.

### Builder / Implementer
Responsibilities:
- implement bounded approved work;
- remain inside task scope;
- produce handoff and evidence.

Builder may not mark its own material implementation accepted.

### Supervisor / Inspector
Responsibilities:
- inspect implementation against approved blueprint, law, and task;
- detect design drift, missing controls, stale state, or unauthorized expansion;
- issue PASS/REVISE findings.

Supervisor does not become architect by default.

### Independent Reviewer / Critic
Responsibilities:
- attack assumptions independently;
- identify material defects and contradictions;
- review frozen targets where required.

Critic cannot merge or unilaterally make findings canonical.

### Evidence / Validation Layer
Responsibilities:
- run deterministic validation;
- bind proof target, version, SHA, result, and scope;
- preserve failures;
- distinguish implementation proof from deployment/runtime proof.

### Seat / Operator
Any chat/model/provider instance performing a role.
A seat is replaceable and gets authority only from current canonical records plus explicit Owner instruction.

## 7. Law hierarchy

Normative hierarchy:

1. Durable Constitution-level Owner Decision on protected main.
2. Stable Foundation Law.
3. Policy.
4. Domain Rule.
5. ADR / bounded operational decision.
6. Current State / Task Registry for operational facts within their declared authority.
7. Handoff for task continuity.
8. Generated views / reports.
9. Chat memory / model memory — non-canonical.

A current chat instruction governs the current interaction, but does not durably supersede project-wide Stable Law until recorded through protected governance.

## 8. Conflict resolution

## 8.1 Cross-hierarchy relation: Law vs Master Blueprint vs subsystem architecture

The Master Blueprint is **not a second law-precedence router**.

- Constitution-level Owner decisions and applicable Stable Foundation Law constrain the Master Blueprint.
- The Master Blueprint is the highest structural-design authority for project-wide organization, roles, system layers, lifecycle, and canonical-source topology.
- Current subsystem architecture must conform to the Master Blueprint within structural scope.
- Current State and Task Registry remain operational-fact authorities only within their declared scope.
- If the Master Blueprint conflicts with higher law, higher law wins and the Blueprint must be revised.
- If subsystem architecture conflicts with the accepted Master Blueprint, the subsystem architecture must be revised unless Owner explicitly changes the Blueprint.

This prevents the Blueprint from becoming a second law system while still giving it real architectural authority.


When rules conflict:
1. identify scope;
2. compare authority level;
3. compare explicit supersession;
4. prefer narrower valid rule within its scope if authority level permits;
5. prefer newer only when same-level supersession is explicit;
6. if unresolved, fail closed for the affected mutation;
7. create a durable resolution record;
8. never silently rewrite history.

## 9. Canonical source-of-truth map

Required single routes:

- Boot root: `state/bootstrap.json`
- Master Blueprint: resolved from bootstrap/current-state pointer
- Law precedence: one consolidated normative router
- Current state: `state/current.yaml`
- Task truth: `state/tasks.yaml`
- Current architecture: pointer from current state
- Active handoff: pointer from active task
- Knowledge truth: typed knowledge records + status/provenance
- Evidence truth: immutable receipts/results bound to proof target
- History: preserved historical records, non-current unless explicitly routed

If two current files claim the same authority, this is a defect.

## 10. Build lifecycle

Every material system change follows:

`DESIGN -> LAW CHECK -> TASK AUTHORIZE -> BUILD -> SUPERVISE -> VALIDATE -> INDEPENDENT REVIEW (risk-based) -> OWNER/APPROVER ACCEPT -> PROTECTED MERGE -> FRESH-READ -> OPERATE -> OBSERVE -> CONTROLLED CHANGE`

### Gate 1 — Design
Define objective, boundaries, affected layers, invariants, dependencies, rollback.

### Gate 2 — Law check
Confirm authority, precedence, and no unresolved conflict.

### Gate 3 — Task authorization
Create bounded task with scope, base, holder/role, next action, and required evidence.

### Gate 4 — Build
Implement only the approved scope.

### Gate 5 — Supervision
Inspector checks implementation against design/law/task.

### Gate 6 — Validation
Machine or independent evidence verifies bounded claims.

### Gate 7 — Independent review
Required for foundation, constitution, architecture, major security, or phase transitions.

### Gate 8 — Acceptance
Approver accepts, rejects, or requires revision.
Foundation acceptance remains Owner authority.

### Gate 9 — Protected merge + fresh-read
Only merged protected main becomes durable canonical truth.

### Gate 10 — Operation
Operate under current law/architecture.

### Gate 11 — Controlled change
Observed defects or new Owner objectives start a new lifecycle; they do not justify ad-hoc patching.

## 11. Change classes

### Class F — Foundation
Examples: constitution, law precedence, Master Blueprint, canonical authority, role powers, freeze/reopen rule.
Requires:
- Architect proposal;
- Supervisor inspection;
- independent critic review;
- evidence;
- Owner acceptance;
- protected merge;
- fresh-seat recovery proof where continuity changes.

### Class S — Structural
Examples: task registry schema, knowledge schema, core pipeline interfaces.
Requires design review, supervision, validation, protected merge.

### Class D — Domain
Examples: Buddhist/economics domain rules and knowledge structures.
Must obey foundation; cannot alter foundation authority.

### Class O — Ordinary
Examples: bounded knowledge updates, routine implementation, reports.
May use streamlined checks but never bypass provenance, scope, or canonicality.

## 12. New-seat recovery protocol

A completely new AI/chat/model must be able to recover the same system state without Owner recap.

Mandatory order:

1. `state/bootstrap.json`
2. Master Blueprint pointer
3. normative law-precedence router
4. `state/current.yaml`
5. `state/tasks.yaml`
6. current architecture
7. active task handoff
8. task/domain sources
9. relevant evidence receipts

It must output/recover:
- current constitutional authority;
- current law precedence;
- current architecture generation;
- active task;
- exact next action;
- blockers;
- canonical vs candidate vs historical boundaries.

If any required pointer is missing/conflicting, fail closed.

## 13. Acceptance model

Nothing is accepted merely because:
- an AI says it is correct;
- code exists;
- a file exists;
- CI passed;
- a critic agreed;
- a fresh chat reproduced one fixture.

Acceptance requires evidence appropriate to the claim.

Foundation acceptance requires:
- architecture consistency;
- law consistency;
- role separation;
- cold-start recovery;
- bounded capability truth;
- durable critic dispositions;
- Owner acceptance.

## 14. Freeze and reopen

Once Foundation is ACCEPTED/FROZEN:
- normal learning and implementation continue;
- foundation architecture does not reopen for ordinary growth;
- no new foundational mechanism is added merely because it seems useful.

Reopen only when:
1. measured evidence/test failure shows a foundation defect;
2. unresolved operational contradiction appears;
3. security/continuity failure invalidates an invariant;
4. Owner explicitly changes a foundation objective.

Every reopen creates a new versioned foundation change.

## 15. Mapping current project to this blueprint

Already substantially present:
- Owner sovereignty;
- protected-main continuity authority;
- single boot root;
- current state;
- task registry;
- consolidated law router;
- knowledge fabric;
- bounded capability truth;
- fresh-seat recovery testing;
- critic receipts;
- PR/CI/protected merge discipline.

Missing or previously implicit:
- one document explicitly serving as project-wide Master Blueprint;
- formal Architect / Builder / Supervisor / Critic / Evidence role separation;
- explicit no-self-certification rule across all material work;
- one lifecycle from design through operation and controlled change;
- change classes tied to review/approval requirements;
- explicit Master Blueprint pointer in boot recovery;
- foundation freeze conditioned on blueprint acceptance.

Therefore the prior vNext architecture is a strong subsystem/foundation architecture, but it is **not by itself a complete Master Blueprint for the whole organization**.

## 16. Transition plan

1. Hold prior Foundation Freeze.
2. Make this Master Blueprint candidate durable.
3. Route bootstrap/current state to a Master Blueprint pointer.
4. Register a dedicated Master Blueprint task.
5. Reconcile stable law language with this role/lifecycle model without duplicating law.
6. Run Supervisor inspection against existing architecture and laws.
7. Freeze a review packet.
8. Independent Claude + Grok review the same packet.
9. Resolve material findings.
10. Owner accepts v1.
11. Merge canonical Master Blueprint + final routing.
12. Run fresh-seat recovery proving the new seat recovers Blueprint -> Law -> State -> Task -> exact next action.
13. Only then resume Foundation Freeze.

## 17. Total Architect operating contract

Owner-approved operating contract: `docs/vnext/OWNER_DECISION_AUTO_TOTAL_ARCHITECT_20261006.md`.

The short command `AUTO TỔNG CÔNG TRÌNH SƯ` means: execute the full governed architecture lifecycle, automatically continue routine authorized work, review the whole system after each major stage, select the logically-next architecture task, and stop only at explicit Owner-level foundation decisions or unresolved material defects.

This does not grant self-acceptance. The Total Architect may propose and execute within the approved envelope but cannot redefine Owner objectives, change foundation authority, or self-freeze the Master Blueprint/Foundation.

## 18. Definition of success

MINH TRÍ has a valid Master Blueprint only when a fresh seat can identify, without chat memory:
- what the whole system is;
- who has which authority;
- which law outranks which;
- where current truth lives;
- what is stable vs extensible;
- how changes move from proposal to acceptance;
- who builds, supervises, criticizes, validates, and approves;
- how conflicts fail closed;
- how the system continues after every chat/model/tool is replaced.

Until that is independently demonstrated, Master Blueprint v1 remains a candidate.
