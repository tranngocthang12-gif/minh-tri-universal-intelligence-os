# MINH TRÍ — Universal Intelligence OS

**Current migrated authority root:** `state/bootstrap.json`.  
**Current state:** `state/current.yaml`.  
**Task registry:** `state/tasks.yaml`.  
**Master Blueprint / law / architecture:** resolve dynamically from the boot root and current state. Legacy `docs/PROJECT_STATE.json` and `docs/RECOVERY_MANIFEST.json` are compatibility/history for unmigrated keys and do not override migrated authority.

MINH TRÍ is a provider-neutral, evidence-first learning/control plane built around one durable Owner ledger and replaceable AI seats. GitHub is the durable project authority; chat is not canonical truth.

## Current architecture

The foundation now contains:

- a single-writer JSONL hash-chain ledger with derived state cache;
- an Owner-gated write plane using the canonical `Ledger.apply` / repair boundary;
- a separate read-only brain plane exposed through Secure MCP Tunnel;
- exactly two remote brain tools: `brain.verify` and `brain.recovery_packet`;
- a maintenance plane using Desktop Commander as break-glass tooling, not canonical brain transport;
- external anchor/witness verification contracts;
- proposal-only critique, autonomous-learning and meta-learning engines with no durable write capability;
- GitHub branch protection, required CI, secret-history scanning, dependency audit, and pinned Actions;
- Windows tunnel supervisor and secret-safe autostart components.

The ChatGPT-to-Owner-PC read-only connector has been runtime-proven in bounded historical observations. **Current reachability is not inferred from those proofs.** At the 2026-10-04 synchronization observation, Desktop Commander was offline and the Secure MCP Tunnel/Local Brain read path was down. Current liveness is always read from `PROJECT_STATE.current_runtime_liveness`.

## Authority and recovery

For important work, read in this order:

1. `state/bootstrap.json`
2. the current Master Blueprint
3. the authoritative law-precedence router
4. `state/current.yaml`
5. `state/tasks.yaml`
6. the current architecture
7. the active task handoff
8. task/domain sources and required evidence

Historical documents remain provenance only after they are superseded.

## Core invariants

- Chat statements are not VERIFIED evidence.
- Implemented is not the same as deployed.
- One live check is not persistence proof.
- Read plane must not acquire mutation, shell, or arbitrary filesystem access.
- Background autonomy remains OFF.
- Research remains fail-closed until the genuine fresh-seat gate passes.
- No automatic VERIFIED promotion, automatic trial activation, or autonomous durable mutation.
- Tools/models/providers are replaceable; law/evidence discipline is not.

## Local CLI skeleton

The offline ledger CLI still exists for local development and recovery:

```bat
minhtri.bat init
minhtri.bat status
minhtri.bat verify
```

The simple CLI can operate without the remote connector. Secure MCP/runtime functions use their own declared dependencies and credentials; do not infer current runtime state from this quickstart.

## Foundation status

Foundation status and architecture gates are resolved from `state/current.yaml` and `state/tasks.yaml` through the boot root. Legacy `PROJECT_STATE.json` may still carry unmigrated runtime/liveness fields, but it is not the current authority for migrated Foundation phase, architecture, task, or next-action state.

Real provider/domain integration, real-data validation, real business-loop validation, and external actions are not yet production-enabled.

## Security

See [SECURITY.md](SECURITY.md). Never place live API keys, Owner credentials, private brain contents, or other secrets in GitHub records.


## Active learning tracks

The Owner-directed Economics PhD-level self-study track is registered at `docs/learning/ECONOMICS_PHD_AUTO_PROGRAM_20261004.md`, currently `M0.1 STARTED / UNTESTED`. This is evidence-bounded doctoral-level study, not an accredited degree claim.
