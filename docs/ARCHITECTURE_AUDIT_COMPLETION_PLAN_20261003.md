# MINH TRÍ — FULL ARCHITECTURE AUDIT + COMPLETION PLAN — 2026-10-03

**Status:** CURRENT AUDIT RECORD / EVIDENCE-BOUNDED  
**Audit base:** live `main` after PR #112 merge  
**Scope:** authority, ledger/write plane, read transport, maintenance, witness/recovery, CI/security, autonomy/learning assurance, documentation consistency, and remaining completion gates.

## 1. Executive finding

The project has a coherent foundation architecture. Authority order, read/write separation, GitHub-first recovery, proposal-only autonomy, and fail-closed learning gates are aligned. No architectural contradiction was found that requires rebuilding the core.

The project is **not complete** and must remain `FOUNDATION_PROTOTYPE`. The largest remaining gaps are runtime assurance and independent evidence, not missing core abstractions.

## 2. Architecture invariants checked

### Authority and durability
PASS at architecture level:
- Owner -> stable law -> PROJECT_STATE -> current architecture -> approved records -> history/chat.
- GitHub is durable project memory; chat is non-canonical.
- current Law Index, architecture pointer, role bootstrap, and recovery manifest agree on the authority route.

### Brain read plane
PASS in bounded live evidence:
- fixed local brain;
- exact remote toolset: `brain.verify`, `brain.recovery_packet`;
- no mutation, shell, arbitrary filesystem, or caller-selected brain path;
- current connector observation returned a valid ledger head and active YouTube focus.

This does not prove reboot persistence or fresh-seat independence.

### Brain write plane
PASS for current canonical boundary:
- `Ledger.apply` authenticates inside the mutation boundary;
- `repair_snapshot` is Owner-gated;
- legacy ungated local runtime is deprecated/non-canonical;
- Owner credential v2 has prior DPAPI runtime evidence.

Remaining limitation: the current Owner gate proves possession of the configured secret, not real-person identity. `owner_identity_verified=false` is therefore correct.

### Maintenance plane
PASS for scope hardening:
- Desktop Commander is maintenance/break-glass only;
- filesystem scope is restricted to the canonical runtime directory;
- it is not accepted as proof of the canonical read-only connector.

### Witness/recovery plane
PARTIAL:
- anchor and witness receipt verification exist;
- same-authority GitHub anchoring is useful provenance but is not an independent witness;
- independent authority/credential is still absent;
- fresh-seat validation remains blocked.

### CI/governance
PASS for current encoded controls:
- main is PR-protected;
- required `test` context is strict;
- no ruleset bypass actors;
- Python 3.10/3.11/3.12 matrix, secret-history scan, dependency audit;
- Actions pinned by immutable SHA;
- PR #112 adds Windows PowerShell parser CI to the required aggregate gate.

Governance hardening still available: required approving reviews/CODEOWNER review are not enforced.

### Learning/autonomy
PASS for fail-closed architecture:
- self-critique, autonomous-learning and meta-learning mechanisms are proposal-only;
- no autonomous durable write;
- no automatic VERIFIED or automatic trial activation;
- research remains blocked until genuine fresh-seat PASS;
- Learning Assurance v1.4 is implemented/CI-proven but has not yet been empirically validated.

## 3. Defect found and fixed during this audit

The deployed tunnel-key provisioner source used an ambiguous PowerShell variable/colon interpolation in the `icacls` grant expression. Existing CI only inspected the script text and did not parse Windows PowerShell syntax.

PR #112:
- replaced the ambiguous grant construction with a formatted grant value;
- added a regression assertion;
- added a `windows-latest` PowerShell parser job;
- made the existing required `test` aggregate depend on that parser;
- passed all required checks and merged through branch protection.

Runtime persistence is still NOT_PROVEN because the corrected source must be deployed before the one-time key provisioning/reboot proof sequence.

## 4. Documentation drift corrected by this audit

- README was a stale early walking-skeleton description and incorrectly implied the current project had no ChatGPT read-only connection.
- security hardening and autonomy implementation records from 2026-10-02 still presented candidate/pre-merge status.
- tunnel persistence design still presented implementation as a candidate despite merge/deployment.

These files are synchronized in the architecture-sync PR while preserving historical observations as historical, not rewriting them into current liveness.

## 5. Foundation completion gates — blocking

The foundation should not be promoted out of `FOUNDATION_PROTOTYPE` until these are resolved with evidence:

1. **Old tunnel key revocation** — provider-side evidence that obsolete tunnel credentials are revoked.
2. **Boot/reboot persistence** — provision dedicated DPAPI tunnel credential, install limited logon task, capture pre-reboot evidence, controlled reboot/logon without manual launch, then prove tunnel + brain recovery.
3. **Endpoint protection / disk encryption** — resolve McAfee realtime protection and BitLocker UNKNOWN using stronger host/vendor/admin evidence.
4. **Genuine fresh-seat validation** — separate seat, unseeded expected values, exact two read-only tools, independent control verification in the validation window.
5. **Independent witness authority** — credential and storage authority not jointly compromised with the Owner PC/GitHub write authority.
6. **Real external critic execution evidence** — frozen target/evidence packet plus provenance/independence receipt with bounded claims.
7. **Empirical Learning Assurance v1.4 validation** — comparative real-work evidence; implementation/CI is not evidence of improved accuracy.
8. **Backlog hygiene** — CLOSED on 2026-10-03; current audit observed zero open PRs after the refresh/merge work.

## 6. Production-phase gates after foundation

Even after the foundation gates close, the wider project is not a finished production system until Owner explicitly chooses and validates later phases:

- real provider/domain adapters;
- real-data validation;
- real business-loop validation;
- production-grade Owner identity/authentication if external actions are enabled;
- explicit external-action policy, authorization and rollback controls;
- observability, backup/restore and disaster-recovery exercises;
- operational SLOs and failure drills.

Current machine-readable state correctly says `providers_connected=false`, `real_data_validated=false`, `real_business_loop_validated=false`, `external_actions_enabled=false`, and `owner_identity_verified=false`.

## 7. Architecture debt before production

### Ledger crash consistency
The ledger append is fsynced before the derived snapshot is replaced. A crash in between can leave a valid appended event with a stale snapshot; verification then fails closed and Owner-gated repair can rebuild the cache. This is safe against silent acceptance but is not a fully atomic multi-file transaction.

Before production-grade write availability, add crash/fault-injection tests and either:
- formalize this as the intended recoverable transaction model with automated evidence-backed recovery; or
- introduce a journal/checkpoint mechanism that makes event+snapshot recovery deterministic after interruption.

### Owner identity
The shared-secret gate is a possession gate, not real-person identity verification. Keep the current honest state unless/until a stronger OS/hardware-backed identity design is selected and proven.

### Fresh-seat attestation strength
The v1 fresh-seat validator cross-matches runtime reads but still consumes an explicit `separate_chat_ui` attestation. Treat PASS, when obtained, as proof under that protocol's bounded threat model, not cryptographic proof of independent UI/session provenance. A future challenge/receipt protocol can strengthen this if needed.

## 8. Ordered next work

Do not start background autonomy or Research Adapter while the gate is closed.

Execution order:
1. deploy the PR #112 corrected persistence script to the canonical Owner-PC runtime;
2. Owner-only one-time tunnel runtime key provisioning;
3. install limited logon task;
4. capture pre-reboot evidence and execute controlled reboot recovery proof;
5. verify/revoke obsolete tunnel keys;
6. resolve endpoint security/BitLocker unknowns;
7. run genuine fresh-seat validation;
8. establish independent witness;
9. execute external critic + empirical Learning Assurance v1.4 trial;
10. re-audit and decide whether to close the foundation phase.

No step may promote itself to VERIFIED merely because code exists or CI passes.


## 9. Post-reboot update — 2026-10-03 15:35 +07:00

A newer bounded remote observation found the MINH TRÍ read-only connector UNREACHABLE and Desktop Commander offline. GitHub and CI remained reachable. Because the local machine could not be inspected, the root cause of the failed remote recovery is UNKNOWN.

Consequences:
- boot/reboot persistence remains NOT_PROVEN;
- earlier session liveness PASS remains historical evidence only;
- backlog hygiene is CLOSED and is not part of the seven currently open foundation gates;
- the immediate next action is to restore maintenance-plane reachability, inspect Scheduled Task/process/health state, and then either repair the autostart path or capture a successful unattended recovery proof.

Evidence: `docs/runtime_evidence/POST_REBOOT_REMOTE_REACHABILITY_20261003T153500_PLUS0700.json`.
