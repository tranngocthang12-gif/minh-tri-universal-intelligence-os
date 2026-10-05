# MINH TRÍ — Universal Intelligence OS

**Current phase:** `FOUNDATION_PROTOTYPE`.  
**Canonical boot root:** [state/bootstrap.json](state/bootstrap.json).  
**Current state:** [state/current.yaml](state/current.yaml).  
**Current architecture/law precedence:** resolve from `state/current.yaml`.  
Legacy `docs/PROJECT_STATE.json`, Recovery Manifest, Law Index and pre-vNext Architecture remain compatibility/history surfaces for unmigrated facts; they must not override migrated vNext state.

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
2. `state/current.yaml`
3. law precedence referenced by current state
4. `docs/LAW_UNIVERSAL_LEARNING_CONTINUITY_20261004.md`
5. architecture referenced by current state
6. role bootstrap referenced by current state
7. `state/tasks.yaml`
8. the active task/domain source

If a legacy surface conflicts with a migrated key in `state/current.yaml`, the migrated vNext state wins. Historical documents remain provenance only after they are superseded.

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

The foundation core is built, but runtime assurance is incomplete. The current blocking gates are maintained in `PROJECT_STATE.json` and summarized in the current architecture. They currently include old tunnel-key revocation evidence, boot/reboot persistence, endpoint-protection/BitLocker unknowns, genuine fresh-seat validation, independent witness authority, real external critic evidence, and empirical validation of Learning Assurance v1.4.

Real provider/domain integration, real-data validation, real business-loop validation, and external actions are not yet production-enabled.

## Security

See [SECURITY.md](SECURITY.md). Never place live API keys, Owner credentials, private brain contents, or other secrets in GitHub records.


## Active learning tracks

The Owner-directed Economics PhD-level self-study track is registered at `docs/learning/ECONOMICS_PHD_AUTO_PROGRAM_20261004.md`, currently `M0.1 STARTED / UNTESTED`. This is evidence-bounded doctoral-level study, not an accredited degree claim.
