# Security Policy

## Scope

This repository is a foundation prototype. Security-sensitive paths include the Owner gate,
ledger mutation boundary, local brain transport, tunnel/runtime launchers, credential handling,
witness/anchor verification, and GitHub governance.

## Reporting

Do not place secrets, API keys, Owner credentials, private brain contents, or exploit payloads
containing live credentials in a public issue, pull request, commit, or discussion.

Use an existing private Owner communication channel for sensitive reports. If no private channel
is available, report only a redacted summary publicly and withhold secret material until a private
channel is established.

## Security invariants

- Chat statements and historical PASS records are not runtime proof.
- Security-sensitive mutation must fail closed.
- The read-only brain connector must not expose shell, arbitrary filesystem, or ledger mutation.
- Canonical project memory is GitHub-first, but GitHub evidence is not an independent witness.
- No autonomous VERIFIED promotion, publish, spend, delete, or durable write without the required
  Owner/governance gate.


## Current-state security rule

- `PROJECT_STATE.current_runtime_liveness` is the only authority for current maintenance/tunnel/brain reachability.
- Historical PASS evidence must never be used to infer that a process or connector is currently running.
- An unexpired self-upgrade authorization timestamp does not prove the in-memory lease runtime is alive.
- If runtime observability is lost, mutation authority is UNKNOWN and must be treated fail-closed until fresh proof.
