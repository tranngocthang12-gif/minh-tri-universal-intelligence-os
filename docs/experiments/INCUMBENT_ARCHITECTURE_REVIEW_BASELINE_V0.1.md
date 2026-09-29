# MINH TRÍ — INCUMBENT ARCHITECTURE REVIEW BASELINE v0.1

**Reviewer family:** OpenAI  
**Role:** incumbent/self-review control, NOT independent evidence  
**Frozen reviewed target:** `50a0444ed20ae2415c9ee31e622a0b6b8575d4c9`  
**Frozen before external blind architecture reviews:** YES  
**Status:** `BASELINE_ONLY / NOT PROJECT LAW`

This file freezes the incumbent findings that existed before collecting any independent provider review. It must not be rewritten to improve overlap after external results arrive. Corrections must be appended as a new version.

## Incumbent material findings at the frozen target

1. **Brain/Bootstrap drift — BLOCKER.** Mandatory read path and Brain Manifest lagged restored v0.2 and R1-R4 runtime contracts.
2. **Provider-family loophole in canonical Core — BLOCKER.** Core separated provider IDs but did not encode family independence, allowing aliases from one family to appear independent.
3. **R3 revalidation too permissive — BLOCKER.** Reopened L6 state could return to L6 after one evidence-backed revalidation while retaining the old active reasoning chain.
4. **R4 SATISFIED too permissive — BLOCKER.** Same-domain evidence or an L2+ item could close a component without proving relevance to the linked gap.
5. **Cross-ledger race — BLOCKER.** Core/Task/Epistemic/Governor had separate writer locks; a recommendation could be computed from heads that changed before receipt append.
6. **Schema/migration discipline incomplete — BLOCKER.** Arena legacy replay existed, but Task/Epistemic/Governor did not yet have an explicit future compatibility policy/fixture requirement.
7. **No full cross-layer continuity test — HIGH.** Module tests were green but no deterministic Goal→Unknown→Bottleneck→Task→Outcome→R3→R4 loop existed.
8. **No independent architecture review — HIGH.** PR #2 through #9 had no independent review.
9. **External success/failure case learning not yet durable — MEDIUM.** Owner direction existed in chat but was not yet persisted as an architecture rule.
10. **Candidate stack != canonical main — GOVERNANCE HOLD.** Main remained at the foundation commit while later architecture existed only in stacked draft PRs.

## Incumbent conclusion at frozen target

`R4_5_REQUIRED`.

R5 should remain HOLD until architecture stabilization closes the material inputs that could turn weak/stale state into reusable skill candidates.

## Integrity

This is a control baseline. It is not an adjudication, provider ranking or proof that any finding is correct.
