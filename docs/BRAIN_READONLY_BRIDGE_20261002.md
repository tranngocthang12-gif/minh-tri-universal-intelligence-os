# READ-ONLY BRAIN BRIDGE — 2026-10-02

**Status:** CANDIDATE IMPLEMENTATION / NOT VERIFIED UNTIL EXACT-SHA CI PASSES

## Goal

Recover project learning state after chat/model memory loss without granting the seat any local-brain mutation authority.

## Exposed contract

`BrainReader` exposes only:
- `verify()`
- `get_head()`
- `get_current_focus()`
- `search_lessons(query, limit)`

Every operation first calls the Tier-1 ledger verifier. Returned recovery records include `event_count` and `head` so callers can bind answers to a concrete ledger state.

If verification fails, the bridge fails closed with `BRAIN_VERIFY_FAILED`. It must never repair the ledger automatically.

## Explicitly absent

No:
- `apply`
- `repair_snapshot`
- `init`
- lesson promotion
- network research
- publishing
- secret handling
- autonomous background loop

The bridge is a Python/local contract only. It is **not yet connected to ChatGPT or another remote seat**. A transport adapter such as a tightly scoped local MCP/service remains future work.

## Security dependency

This reconciled branch is based on canonical main after Security P0 PR #40 and governance PR #39 were merged. Security dependency is therefore satisfied at branch creation; exact-head CI is still required.

## Acceptance tests

- empty verified ledger returns a valid head;
- focus is recovered from verified state;
- lesson search does not invent results;
- tampered snapshot fails closed;
- bad search parameters fail closed;
- the facade exposes no known mutation methods;
- full suite passes on exact branch SHA.

## Next recovery test

After CI passes, create a zero-chat-memory bootstrap test:
`bootstrap authority → BrainReader.verify → current focus → relevant lesson search → handoff`.

Passing that test would demonstrate recoverability of learning state, not autonomous learning.
