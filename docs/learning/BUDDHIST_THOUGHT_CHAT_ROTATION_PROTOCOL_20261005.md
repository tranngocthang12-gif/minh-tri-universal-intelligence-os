# MINH TRI — Buddhist Chat Rotation and Dead-Chat Recovery Protocol — 2026-10-05

Status: ACTIVE COORDINATION PROTOCOL / SUBORDINATE TO CANONICAL LEARNING LAW

## Problem

Long chats can become slow, lose effective working context, fail to respond reliably, or become unusable. The Buddhist-thought project must not depend on the continued health of any single chat.

## Core design

**Roles persist; chats are disposable workers.**

The three durable logical roles are:

1. MAIN — canonical A-sequence synthesis.
2. EARLY_TEXT_AUDIT — early-discourse/source verification.
3. CRITIC_MILINDAPANHA — adversarial, lexical, parallel, and Milindapanha stress-test.

A chat instance is only one generation of a role:
- MAIN-01, MAIN-02, MAIN-03...
- AUDIT-01, AUDIT-02, AUDIT-03...
- CRITIC-01, CRITIC-02, CRITIC-03...

When a chat becomes long or unreliable, the role moves to a fresh chat. The old chat is not required for recovery.

## Never wait for a chat to die

The project uses **bounded durable units**:

- MAIN: one numbered A checkpoint is a durable unit.
- EARLY_TEXT_AUDIT: one audit packet is a durable unit.
- CRITIC_MILINDAPANHA: one critic packet is a durable unit.

At the end of every durable unit, the seat must record:
- role;
- completed unit ID;
- evidence/claim status;
- corrections;
- open uncertainty;
- next assignment;
- durable file location.

If the chat dies immediately after that, a new chat loses at most the unfinished unit, not the learning history.

## Proactive rotation

Do not use token count as the trigger because the usable limit is not reliably observable from inside a chat.

Default soft-rotation rule:
- MAIN: rotate to a fresh chat after 3 completed A checkpoints, or earlier on degradation.
- EARLY_TEXT_AUDIT: rotate after 3 completed audit packets, or earlier on degradation.
- CRITIC_MILINDAPANHA: rotate after 3 completed critic packets, or earlier on degradation.

Early-rotation triggers:
- repeated tool/context failures;
- the chat begins forgetting current role or checkpoint;
- it contradicts freshly read project state;
- response quality visibly degrades;
- messages become unusually slow or fail;
- the chat can no longer complete normal project reads/writes.

Rotation is not a failure. It is normal lifecycle management.

## Unexpected death rule

If a chat becomes unusable before it can hand off:

1. Do not try to reconstruct truth from remembered chat conversation.
2. Open a fresh chat for the same logical role.
3. Fresh-read canonical project state and the role's durable records.
4. Resume from the last durable completed unit.
5. Treat any unrecorded partial work from the dead chat as **LOST / NOT DURABLE**.
6. Re-do only the unfinished bounded unit.
7. Do not advance current/next routing based on a claim that existed only in the dead chat.

This makes failure cost bounded.

## MAIN role recovery

A replacement MAIN chat must read:
1. PROJECT_STATE;
2. current law index;
3. Universal Learning Continuity Law;
4. current architecture/bootstrap required by project law;
5. active Buddhist checkpoint;
6. this rotation protocol;
7. the three-chat parallel work plan;
8. any accepted audit/critic packets not yet integrated.

It then states:
- recovered current checkpoint;
- recovered next checkpoint;
- open audits;
- last durable A record;
- exact next action.

Only after that may it continue the A-sequence.

## AUDIT role recovery

A replacement AUDIT chat must:
- fresh-read project state and laws;
- inspect current open audits;
- inspect durable audit packets already completed;
- choose the first unresolved audit in the assigned priority order;
- never advance the canonical A-number.

## CRITIC role recovery

A replacement CRITIC chat must:
- fresh-read project state and laws;
- inspect existing critic packets;
- inspect current main checkpoints needing challenge;
- continue the next unresolved lexical/parallel/Milindapanha stress test;
- never advance the canonical A-number.

## Owner-facing recovery commands

The Owner should not need to paste the old conversation.

For a replacement MAIN chat, the Owner can say:

`Tiếp quản vai trò PHẬT MAIN từ project. Không dùng chat cũ. Fresh-read canonical state, phục hồi checkpoint và tiếp tục đúng next checkpoint.`

For a replacement AUDIT chat:

`Tiếp quản vai trò PHẬT EARLY TEXT AUDIT từ project. Không dùng chat cũ. Fresh-read các audit đã hoàn thành và tiếp tục audit chưa xong; không nâng A-number.`

For a replacement CRITIC chat:

`Tiếp quản vai trò PHẬT CRITIC / MILINDAPANHA từ project. Không dùng chat cũ. Fresh-read critic state và tiếp tục stress-test chưa xong; không nâng A-number.`

## Handoff quality rule

A handoff is good only if a fresh chat can answer without old-chat memory:

ROLE
→ LAST DURABLE UNIT
→ CURRENT CANONICAL STATE
→ NEXT ASSIGNMENT
→ OPEN AUDITS / UNKNOWNS
→ DURABLE RECORD LOCATIONS
→ WRITE BOUNDARY

If any of these are missing, the handoff is incomplete.

## Safety against dual-active MAIN

At most one MAIN chat may be treated as the active canonical writer at a time.

When MAIN-N+1 takes over:
- MAIN-N becomes historical/read-only from the coordination perspective;
- if MAIN-N later resumes, it must fresh-read the newer project state and must not continue from its stale local context;
- stale MAIN work must be reconciled as a candidate, never allowed to overwrite newer routing.

## Result

The system does not attempt to make a chat immortal.

It makes any chat replaceable with bounded loss.
