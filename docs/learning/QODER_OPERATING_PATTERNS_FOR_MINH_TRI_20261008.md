# MINH TRÍ — LEARNING CANDIDATE: OPERATING PATTERNS LEARNED FROM QODER — 2026-10-08

**Status:** LEARNING CANDIDATE / NON-CANONICAL UNTIL GOVERNED REVIEW  
**Purpose:** Learn useful architecture/operations ideas without adopting or depending on Qoder.

## Core conclusion

MINH TRÍ should not copy Qoder as a product architecture. The useful lessons are operating patterns that fit inside the existing Master Blueprint. Tools/providers remain replaceable execution seats; protected GitHub main remains canonical authority.

## Patterns worth learning

### 1. Role contract / specialist packet
The current Blueprint already separates Architect, Builder, Supervisor, Critic, Evidence and Owner. Improve operational clarity by giving each task role a compact contract:
- objective;
- allowed scope;
- allowed tools/actions;
- write boundary;
- required evidence;
- stop/escalation conditions;
- completion output.

This is an operational template, not a new authority layer.

### 2. Permission envelope: ALLOW / ASK / DENY
For each task/seat/tool action, explicitly classify capability:
- ALLOW: bounded reversible actions inside task scope;
- ASK: material or sensitive actions requiring the recorded acceptance authority;
- DENY: actions outside role, secrets boundary, direct protected-main bypass, self-certification.

This should refine task execution, not replace law or role authority.

### 3. Event-driven wake-up without event-driven authority
Scheduled triggers, webhooks and external events may wake a worker or create/advance a task, but never create acceptance authority or constitutional decisions.
Event -> task/check -> governed evidence -> recorded acceptance authority -> merge.

### 4. Memory tiers
Keep three distinct memory classes:
- seat working memory: temporary and replaceable;
- shared non-canonical cache/sidecar: convenience only;
- canonical project knowledge/state: protected repository with provenance/status.

A shared worker memory must never become a second canonical brain.

### 5. Checkpoint and rollback discipline
Use Git/protected-main history and immutable receipts as canonical rollback/provenance. Do not add a second proprietary snapshot authority. Local/session checkpoints may improve convenience but are disposable.

### 6. UI / computer operator as a role
Computer/browser automation should be treated as an execution role with isolated profiles, least privilege and explicit task scope. It is not an authority role and cannot approve its own effects.

### 7. Agent-economics telemetry
Evaluate orchestration by outcomes, not number of agents. For real tasks record:
- completion time;
- first-pass success;
- critic defects;
- Owner interventions;
- compute/API/tool cost;
- rework count.

Use this to decide whether multi-seat execution is worth the overhead.

## Ideas not to copy

- persistent AI persona as authority;
- vendor memory as project truth;
- Lead Agent with implicit acceptance/merge authority;
- same-team reviewer treated as independent critic;
- product-specific SDK/runtime in the Foundation;
- schedule/webhook triggers that mutate canonical state without governed task/evidence;
- more agents merely because the product supports them.

## Fit with current Master Blueprint

These patterns should remain inside existing extensible zones and execution/work-pipeline layers. They do not justify a new architecture layer or reopening Foundation by themselves.

Highest-value future experiments after Foundation freeze:
1. role-contract template;
2. permission-envelope template;
3. outcome/cost telemetry for single-seat vs multi-seat execution.

No Qoder dependency is required.
