# AUTONOMY + CRITIQUE + META-LEARNING RUNTIME — 2026-10-02

**Status:** HISTORICAL IMPLEMENTATION SNAPSHOT / MERGED + CI-PROVEN + STAGED; BACKGROUND AUTONOMY REMAINS OFF  
**Branch:** `feature/autonomy-critique-meta-liveness-20261002`

## Scope

This change adds the missing orchestration primitives without granting autonomous durable mutation:

1. `minhtri.autonomy`
   - detects unreviewed claims;
   - produces deterministic structural critique proposals;
   - never emits `ACCEPT_FOR_TRIAL` automatically;
   - computes meta-learning diagnostics from resolved prediction history;
   - emits only `META_LESSON_CANDIDATE` records;
   - plans the next learning actions from verified ledger state;
   - keeps external research fail-closed until the fresh-seat gate is promoted.

2. `minhtri.runtime_supervisor`
   - local-only process watchdog;
   - uses fixed argv with `shell=False`;
   - bounded exponential restart backoff;
   - inherits runtime secrets from the Owner-PC environment instead of persisting them;
   - is not exposed through the read-only MCP server.

3. Tests
   - automatic critique never self-accepts;
   - same-seat critic is rejected;
   - missing critic seat fails closed;
   - meta-learning needs history and only proposes candidates;
   - research remains blocked before its gate;
   - autonomy packet has no write capability;
   - supervisor never invokes a shell and has bounded restart behavior.

## Security invariants

The new autonomy runtime has no call to `Ledger.apply`. Durable mutation remains behind the existing Owner-authenticated ledger boundary.

The runtime cannot:
- mark evidence or claims VERIFIED;
- activate a trial lesson;
- publish externally;
- spend;
- add credentials;
- change stable law;
- expand MCP tools;
- choose a brain filesystem path remotely.

## Research gate

External research remains blocked while:

`research_adapter_gate = BLOCKED_UNTIL_FRESH_SEAT_PASS`

The code can accept a future provenance-preserving adapter only after the gate becomes explicitly promoted. Retrieved material must still enter as unverified research proposals.

## Historical brain transport finding at implementation time

At implementation time, the live read-only connector returned:

`Tunnel-client has not been seen for 300 seconds`

and the Owner PC maintenance connector was offline.

Therefore:
- the read-only MCP design is not changed;
- a local supervisor mechanism is added;
- live persistence is **not** claimed;
- `secure_mcp_tunnel_persistence` remains `NOT_PROVEN`;
- deployment and live recovery must be proven separately on the Owner PC.

## Promotion gates

Do not mark the new runtimes active until:
1. PR CI passes on the exact head;
2. the change is merged;
3. proposal-only runtime is deployed where intended;
4. tunnel supervisor is deployed on the Owner PC;
5. a live reconnect succeeds;
6. fresh-seat recovery passes;
7. only then may Research Adapter activation be reconsidered.

No automatic VERIFIED, automatic trial activation, or autonomous durable write is authorized by this implementation.
