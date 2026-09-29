# MINH TRÍ — R4.5 ARCHITECTURE STABILIZATION GATE

**Owner:** Trần Ngọc Thắng  
**Status:** `CANDIDATE / UNDER TEST / NOT MERGED`  
**Purpose:** Stabilize the brain, architecture memory, elastic N-AI workcell and cross-chat continuity before R5 Skill Lifecycle + Meta-Learning.

## Why R4.5 exists

R1-R4 added useful structural mechanisms, but architecture review found that governance/Bootstrap, provider-family independence, epistemic revalidation, bottleneck satisfaction, cross-ledger consistency, replay/schema discipline and work handoff needed hardening before lessons can be distilled into reusable skills.

R5 remains `HOLD` until this gate is explicitly closed.

## Owner architecture restored here

The durable interpretation is:

```text
MINH TRÍ = CANONICAL BRAIN
AI = REPLACEABLE COGNITIVE PROVIDER

WORKCELL PARTICIPANTS = N PER TASK
MODEL/PROVIDER = REPLACEABLE
PARTICIPANT COUNT != INDEPENDENT FAMILY COUNT

THREE LOGICAL FUNCTIONS = PROPOSE / CRITIQUE / ADJUDICATE
TRUTH != MAJORITY VOTE

TASK / EVIDENCE / CHECKPOINT / HANDOFF
BELONG TO MINH TRÍ, NOT TO A CHAT
```

## Hardened in the R4.5 candidate

1. Project Law v0.2 candidate records an elastic N-participant AI workcell with replaceable occupants and explicit independence accounting.
2. Bootstrap/AGENTS require v0.2 architecture + continuity contract + exact current handoff before continuation.
3. Brain Manifest pins restored v0.2, continuity, R1, R2, R3 and R4 contracts.
4. Canonical Core provider registry includes `family_id`; proposer/critic/adjudicator family separation is enforced.
5. R3 reopen invalidates the active L2-L6 chain; one evidence-backed revalidation returns only to L1.
6. R4 `SATISFIED` requires resolved linked unknowns and evidence from the component's own allowlist or active linked L2+ state.
7. All primary ledgers share one project writer lock; cross-ledger service validation and append happen under the shared lock.
8. Canonical Task packet exposes a `continuation_fingerprint`; every worker must acknowledge the current packet before acquiring a lease.
9. Explicit handoff records decisions, unknowns, blockers, verification, scope, limitations and exact next action. Terminal completion now creates an equivalent structured fingerprinted completion receipt.
10. The workcell ledger accepts task-specific N participants. Blind freeze requires a contribution from every currently assigned participant; provider-family diversity is measured and reported, not a fixed cardinality gate.
11. Replacement before blind freeze discards the replaced slot's contribution; replacement after reveal is explicitly marked as non-blind.

## Mandatory finish/handoff sequence

```text
WORK
→ TEST / VALIDATE
→ PERSIST DURABLE DELTA
→ CHECKPOINT
→ HANDOFF OR COMPLETION RECEIPT
→ REPLAY / VERIFY
→ REPORT TO OWNER
```

A successor:

```text
READ LAW
→ BOOTSTRAP
→ PROJECT STATE
→ BRAIN MANIFEST
→ CURRENT ARCHITECTURE
→ TASK
→ LATEST HANDOFF
→ ACK CONTINUATION FINGERPRINT
→ ACQUIRE LEASE
→ CONTINUE
```

## Still HOLD before R5

The following must remain visible until closed by evidence:

- **Ledger schema/migration discipline:** `PASS STRUCTURAL FOR CURRENT R4.5 CONTRACTS`. Core pre-`family_id` history has a non-destructive migration verifier; Task/Epistemic/Governor/Workcell command shapes are frozen by schema-tripwire tests. Any future schema edit must deliberately update migration/compatibility evidence; this does not pre-implement future migrations.
- **End-to-end cross-layer continuity:** previous exact-head fixture PASS; the final elastic-N architecture target must rerun Goal/Core outcome+review → R3 L6+Unknown → R4 SELECT → N-AI blind workcell → R2 Task/checkpoint/handoff A→B → R3 unknown resolution → R4 recompute WAIT with all ledgers replayed.
- **Independent architecture review:** current work has strong incumbent/self-review but no completed independent multi-provider blind architecture review.
- **Multi-AI experiment:** v0.1 is superseded/HOLD. The review protocol must be repinned to the final R4.5 architecture target. Collection uses however many eligible independent providers are actually available; actual participant/family counts are provenance, not a truth vote.
- **Official Arena↔Workcell route:** previous service/CLI boundary PASS; the final target must rerun it. `ElasticWorkcellService.submit_arena` and `workcell arena-apply` require a REVEALED session and a current participant. Direct Arena remains a low-level compatibility/replay surface.
- **Provider/Owner identity:** still self-declared/unverified.
- **Real-world effectiveness:** no evidence yet about the optimal participant count or whether multi-AI outperforms simpler baselines on cost/error/outcome.

## R5 opening rule

R5 may begin only in SHADOW after:

1. R4.5 structural tests pass;
2. no unresolved architecture BLOCKER affecting lesson/skill inputs;
3. ledger compatibility policy/fixtures cover current mutable ledgers;
4. end-to-end continuity scenario passes;
5. independent review disputes are either resolved by evidence/test or explicitly HOLD;
6. skill promotion remains OFF until repeated real outcomes + benchmark thresholds exist.

R5 SHADOW readiness is not merge authority, external-action authority, or evidence of real effectiveness.
