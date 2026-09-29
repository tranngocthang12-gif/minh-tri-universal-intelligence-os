# MINH TRÍ — ARCHITECTURE MEMORY & CONTINUITY CONTRACT v0.1

**Owner:** Trần Ngọc Thắng  
**Status:** `OWNER-DIRECTED CANDIDATE / R4.5 / NOT MERGED`  
**Purpose:** Preserve the original architecture intent, work logic and exact continuation state across chats, AI/provider replacements and handoffs.

## 1. Durable architecture memory

The following are durable project invariants, not chat memory:

1. MINH TRÍ is the brain; no AI/model/provider is the brain.
2. GitHub holds durable law, state, evidence, checkpoints, lessons, skills and decision history.
3. Tier 1 owns the universal learning method, not domain expertise.
4. Tier 2 owns domain knowledge.
5. Tier 3 converts validated understanding into controlled action only after authority gates.
6. Learning maturity is L0 MEMORY → L9 TRANSFER; a level must be evidenced, not self-declared.
7. Every material claim must survive evidence, counterevidence and a discriminating test where feasible.
8. Three logical cognitive functions remain universal: PROPOSE / CRITIQUE / ADJUDICATE.
9. AI Commons official workcell has **four cognitive slots**: S1, S2, S3, S4.
10. The four slot identities are **not fixed**. GPT/Claude/Gemini/Grok or any future provider may occupy a slot and may be replaced.
11. One provider family may not impersonate multiple independent slots.
12. All four slots receive the same frozen task/brain/evidence packet before the blind round.
13. Truth is not decided by 4-vote majority. Material disagreement goes to counterevidence/test/HOLD.
14. Task, evidence, checkpoint and accepted durable delta belong to MINH TRÍ, not to a chat/session.
15. A new chat/provider must read current law + architecture + task + latest handoff before continuing.
16. Work is not considered handed off until the durable handoff receipt has been written and can be replayed.
17. A completed unit must checkpoint last: durable delta first, validation second, handoff/completion receipt last.
18. Historical design sources are evidence of Owner intent; accepted current law/revision governs execution.
19. External success/failure cases may improve hypotheses and priors, but do not automatically prove local transfer.
20. Structural PASS != semantic correctness != real-world effectiveness.

## 2. Four-seat AI workcell

The stable abstraction is:

```text
FOUR SLOTS = STABLE
MODEL / PROVIDER IDENTITY = REPLACEABLE

S1  S2  S3  S4
│   │   │   │
└── same Brain / Task / Evidence ──┘
             ↓
       BLIND CONTRIBUTIONS
             ↓
        FREEZE 4/4
             ↓
           REVEAL
             ↓
       CROSS-CRITIQUE
             ↓
  COUNTEREVIDENCE / TEST
             ↓
        ADJUDICATION
             ↓
HOLD / REVISE / OWNER CANDIDATE
```

Three logical roles are applied to each proposal; they are not permanent model identities.

A valid rotation pattern may be:

| Proposal | Proposer | Critics | Adjudicator |
| --- | --- | --- | --- |
| S1 | S1 | S2 + S3 | S4 |
| S2 | S2 | S3 + S4 | S1 |
| S3 | S3 | S4 + S1 | S2 |
| S4 | S4 | S1 + S2 | S3 |

The runtime may use another deterministic rotation if it preserves provider-family separation and all material dissent.

## 3. Replacement law

If a slot occupant disappears:

- Brain does not change merely because the model changes.
- Task/evidence/checkpoint do not belong to the missing model.
- Replacement receives the exact current packet and handoff state.
- Replacement identity/provider family/version and replacement reason are recorded.
- Before blind freeze, a replacement must not see other blind submissions.
- After reveal, the replacement receives the canonical revealed session state; the system must not pretend it remained blind.

If a required independent slot cannot be filled, the official four-seat workcell is `HOLD / WAIT_FOR_REPLACEMENT`.

## 4. Handoff receipt

Every intentional work handoff must preserve at least:

- task_id;
- checkpoint sequence;
- Brain revision/fingerprint;
- Project Law and Bootstrap hashes;
- source worker/chat identifier;
- summary of accepted work;
- decisions made and their authority status;
- artifacts produced;
- evidence used;
- unresolved unknowns;
- blockers;
- exact next action;
- verification already performed;
- verification still required;
- scope and limitations;
- handoff fingerprint.

A new worker/chat must acknowledge the exact latest handoff fingerprint before continuation.

## 5. New chat / new AI entry

```text
READ PROJECT_LAW
→ READ BOOTSTRAP
→ READ PROJECT_STATE
→ VERIFY BRAIN MANIFEST
→ READ CURRENT ARCHITECTURE CONTRACTS
→ READ CANONICAL TASK
→ READ LATEST HANDOFF
→ ACK EXACT BRAIN + HANDOFF
→ ONLY THEN CONTINUE
```

Model/chat memory may help navigation but cannot replace these reads.

## 6. Finish-work order

A work unit is closed in this order:

```text
WORK
→ TEST / VALIDATE
→ PERSIST DURABLE DELTA
→ UPDATE CHECKPOINT
→ WRITE HANDOFF / COMPLETION RECEIPT
→ VERIFY REPLAY
→ REPORT TO OWNER
```

Do not report "done" first and try to reconstruct the handoff later.

## 7. Protection against architecture drift

Any change affecting one of these must stale old official work packets:

- Project Law;
- Bootstrap;
- this continuity contract;
- current universal architecture;
- R1-R4 contracts;
- relevant code/schema;
- exact task/checkpoint/handoff.

Architecture expansion remains blocked unless a proven bottleneck requires it.

## 8. Current limits

This contract does not prove:

- provider identity;
- cognitive independence merely because families differ;
- semantic correctness of a handoff summary;
- real-world superiority of four AI versus fewer AI;
- external-action authority.

Those remain separate evidence/authority gates.
