# Kiến trúc MINH TRÍ hiện hành — 2026-10-03

**Status:** CURRENT ARCHITECTURE RECORD / FOUNDATION CORE BUILT / RUNTIME ASSURANCE INCOMPLETE  
**Canonical branch:** `main`  
**Authority:** Owner → stable law → PROJECT_STATE → current architecture → approved GitHub records → domain/history → chat.

## 1. Chốt trạng thái

Nền tảng lõi đã hình thành: GitHub-first authority, ledger/gates, read plane, write plane, maintenance plane, witness/recovery plane, CI/security gate và runtime state model. Project vẫn là `FOUNDATION_PROTOTYPE`; chưa được phép gọi production/autonomous-ready.

## 2. One brain, replaceable seats

Não tổ chức = law + current state + repo + Owner ledger. Chat/model/tool chỉ là ghế thay được. Ghế mới phải fresh-read authority trước việc quan trọng.

## 3. Runtime planes

### Authority plane
Owner → laws → PROJECT_STATE → current architecture → approved records.

### Brain read plane
ChatGPT → Secure MCP Tunnel → dedicated MCP → BrainReader → fixed local brain.
Surface đúng hai tool: `brain.verify`, `brain.recovery_packet`. Không shell, arbitrary filesystem hoặc mutation.

### Brain write plane
Explicit write-authorized workflow → Owner gate → Ledger.apply/repair → local brain.
Read plane không được chạm write plane.

### Maintenance plane
Desktop Commander là break-glass/maintenance, không phải canonical brain transport. PHASE A hardening 2026-10-03 đã thu `allowedDirectories` từ full-filesystem (`[]`) về đúng runtime canonical `C:\\Users\\trann\\OneDrive\\Desktop\\minhtri-runtime-current`; blocked commands không bị nới và telemetry không đổi. Config mutation được thực hiện trong chat maintenance riêng, không trộn terminal/file/reboot operations sau mutation.

### Witness plane
Current GitHub witness chỉ process-separated; chưa độc lập trước full Owner-PC/account compromise.

## 4. Runtime proof và current liveness

Runtime evidence và current liveness là hai lớp khác nhau.

**Current liveness authoritative — fresh sync observation 2026-10-04 02:04:29 +07:00:**  
- Owner PC itself = `UNKNOWN`; remote maintenance-device state cannot prove host power state;
- maintenance plane = `OFFLINE`; Desktop Commander reported WIN-VBIQNFFDKIR offline;
- secure MCP tunnel = `DOWN`; control plane reported tunnel-client not seen for 300 seconds;
- Local Brain connector = `DOWN`; fresh `brain.verify` was unreachable through the tunnel;
- recovery requires maintenance plane online → `/readyz` → `brain.verify` → `brain.recovery_packet`;
- historical PASS evidence below is preserved only as bounded evidence and must not be interpreted as current availability.

Canonical current-liveness source is `PROJECT_STATE.current_runtime_liveness`. Any field whose name contains `live/current/session` but is explicitly marked historical is non-authoritative for liveness.

**Historical bounded observation — AUTO runtime-assurance 2026-10-03 12:42 +07:00:**
- Desktop Commander maintenance plane ping PASS; current maintenance liveness = `ONLINE`;
- tunnel-client process hiện diện, health bind loopback và `/readyz = HTTP 200 ready`; current tunnel liveness = `UP`;
- canonical brain read plane trả `brain.verify = VALID`, event_count=3, head `ef299f726f0b83300df9c91ae9648ca20d643e992e7f20cfb769673382e45927`;
- `brain.recovery_packet` trả cùng head và focus ACTIVE `youtube` / `chat quen, so khong` / `UNTESTED_EXPECTATION`;
- bounded persistence probe không tìm thấy matching Scheduled Task/startup entry/dedicated service cho MINH TRÍ tunnel; persistence vẫn `NOT_PROVEN`;
- Desktop Commander hardening PASS: `allowedDirectories` hiện chỉ cho `C:\\Users\\trann\\OneDrive\\Desktop\\minhtri-runtime-current`; blocked commands giữ nguyên; evidence: `docs/runtime_evidence/DESKTOP_COMMANDER_HARDENING_20261003T125254_PLUS0700.json`;
- Defender realtime/behavior/NIS/on-access đều report off; McAfee được Security Center đăng ký và framework host running, nhưng McAfee realtime protection vẫn `UNKNOWN`;
- BitLocker vẫn `UNKNOWN` vì truy vấn bị access denied nếu không có admin rights;
- old tunnel key revocation vẫn `NOT_VERIFIED` vì chưa có provider-side revocation evidence.

**Historical proven evidence vẫn được giữ:**
- connector từng chứng minh đúng hai read-only tools;
- supervisor child restart từng PASS trong cùng session;
- Owner write gate v2 từng PASS wrong-secret fail-closed + DPAPI repair-snapshot E2E;
- boot/reboot persistence: NOT_PROVEN;
- old tunnel key revocation: NOT_VERIFIED;
- fresh-seat recovery: PENDING;
- independent witness: BLOCKED_NO_INDEPENDENT_AUTHORITY_PROVIDER_CREDENTIAL.

Một live check không phải persistence proof; một historical PASS không phải current liveness.

## 5. Host security

- Firewall Domain/Private/Public: enabled.
- Windows Defender engine: enabled; realtime/behavior/NIS reported off.
- McAfee registered in Security Center; framework host Running/Auto.
- McAfee realtime protection itself: UNKNOWN from generic Windows APIs.
- BitLocker: UNKNOWN; both PowerShell/WMI lacked an encryptable-volume result and `manage-bde` returned no usable C: detail.
- Checked runtime secrets are not persisted at User/Machine environment scope.
- Owner DPAPI secret ACL remains Owner read/write only.

UNKNOWN stays UNKNOWN; no promotion from absence of evidence.

## 6. GitHub governance/security

- main requires PR.
- required context: `test`, strict/up-to-date.
- no ruleset bypass actors.
- no force-push/deletion.
- Security P0 includes Python 3.10/3.11/3.12 matrix, history secret scan, pip-audit, and Windows PowerShell syntax parsing for persistence scripts.
- Actions are pinned by immutable commit SHA.
- Dependabot is active.
- Approval count remains 0 and CODEOWNER review is not enforced; this is governance hardening still available, not a current bypass.

## 7. Learning/autonomy

Self-critique, autonomous-learning and meta-learning engines exist/staged, but background autonomous runtime is off. Research adapter stays fail-closed until fresh-seat PASS. No automatic VERIFIED, no automatic trial activation, no autonomous durable mutation.

### Learning Assurance v1

Owner learning strategy now separates **learning capital** from **promoted lessons**:

- external success/failure/mixed cases may be accumulated as `EXTERNAL_CASE_CAPITAL_UNVERIFIED`;
- external cases are not lesson-eligible by themselves and cannot substitute for Owner first-party practice;
- important reviews can freeze a learning packet with target/evidence hashes, counterevidence references, context contract, instruction version and toolset fingerprint;
- critic execution provenance records declared provider/model/run, BLIND/REVEALED mode, output hash and missing evidence;
- `ABSTAIN` is distinct from `REVIEW_INCOMPLETE`;
- negative controls are recorded separately as PASS/FAIL/INCONCLUSIVE and never imply VERIFIED truth;
- meta-learning may summarize patterns and propose candidates, but cannot auto-promote canonical rules or infer cross-domain transfer from case counts.

This layer is additive to the existing ledger. It does not create a multi-agent dependency and does not enable background autonomy.

### Learning Assurance v1.1

- trace links can bind existing artifacts to a durable `trace_id` without rewriting legacy events;
- each trace link records a digest of the linked artifact at link time;
- this is link-based traceability, not yet intrusive full trace propagation through every legacy command;
- lessons may receive future revalidation schedules with explicit staleness conditions;
- revalidation outcomes are `RETAIN / NARROW / RETIRE / INCONCLUSIVE`;
- revalidation remains `PROPOSAL_ONLY`; it cannot mutate lesson status automatically;
- scheduled revalidation cannot occur before its review date, while stale-signal/Owner-request review may happen earlier without automatic mutation.

### Learning Assurance v1.2

- learning failures can be recorded against a concrete artifact with digest-bound provenance;
- machine failure classes include source, scope, unsupported inference, confirmation bias, ignored counterevidence, stale knowledge, critic/eval contamination, reward hacking, tool error, hallucinated source, overconfidence and domain-transfer failure;
- failure records are diagnostic metadata only and cannot repair or rewrite the artifact automatically;
- stratified meta-learning summarizes calibration separately by domain, procedure, source kind and failure class;
- stratified outputs may create bounded meta-lesson candidates only;
- group statistics do not establish causality or cross-domain transfer;
- contamination/reward-hacking classes can be recorded when evidence identifies them, but automatic detection is still NOT_IMPLEMENTED;
- operational independence of declared critic providers remains NOT_PROVEN.

### Learning Assurance v1.3

- critic executions may receive evidence-bound independence receipts recording runtime/session/provider receipt/authority scope and whether Project context was supplied;
- same-runtime or non-blind receipts fail closed;
- even process-separated external evidence is recorded as evidence only, never full-independence proof;
- deterministic eval-integrity assessments may flag configured leakage markers and invariant/score inconsistencies;
- statuses include contamination suspected, reward-hacking suspected, combined suspicion, invariant failure, or clean-no-signal;
- `CLEAN_NO_SIGNAL_NOT_PROOF` is binding: absence of configured signals is not proof of cleanliness;
- autonomy may summarize these records but receives no write power and cannot promote any claim.

### Learning Assurance v1.4

Provider-neutral mechanisms inspired by public Gemini/Claude/Grok documentation:

- adaptive deliberation records a bounded reasoning-effort plan against an artifact; high risk or evidence conflict forces a HIGH floor, while tool-dependent or medium-risk work forces at least MEDIUM;
- deliberation metadata never stores private chain-of-thought;
- grounded research traces bind exact query, source role, claim, citation locator, conflict status and source/claim digests;
- social signals are explicitly non-canonical and cannot acquire truth weight from popularity;
- context capsules compact long-running work into summary + exact artifact references + digests + refresh deadline;
- context capsules are always `CONTEXT_ONLY_NOT_CANONICAL_TRUTH` and cannot overwrite law/evidence/lesson truth;
- autonomy may summarize deliberation/research/context state but has no write or truth-promotion capability.


## 8. Promotion gates còn mở

1. verify/revoke every old tunnel key;
2. establish secure boot persistence design and prove after controlled restart/reboot;
3. resolve endpoint-protection and BitLocker UNKNOWNs with stronger evidence;
4. perform genuine fresh-seat validation;
5. establish independent witness authority/credential;
6. capture a real external critic execution receipt/evidence before claiming operational critic independence;
7. empirically validate Learning Assurance v1.4 against real work before claiming it improves accuracy;
8. only then reconsider closing foundation build phase.

Backlog hygiene is already closed on 2026-10-03; it is not an open foundation gate.

## 9. Backlog hygiene

CLOSED on 2026-10-03. Historical architecture experiment PRs #2–#11 and superseded audit PR #81 are closed with history preserved. Learning Assurance v1–v1.4 is merged. PR #116 refreshed/merged the learning backlog and PR #117 refreshed/merged the dependency update. Later PRs may exist for active Owner work; therefore "zero open PRs" is not a durable architecture invariant and must never be used as a completion proof.

## 10. Bootstrap

Read in order:
1. `docs/PROJECT_STATE.json`
2. `docs/LAW_INDEX_20261003.md`
3. `docs/ARCHITECTURE_NOW_20261003.md`
4. `docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md`
5. task/domain source.

## 11. Non-self-referential deployment evidence

A recorded local deployment SHA is historical evidence only. It must never be interpreted as a requirement that the local clone equal the repository's forever-current main SHA, because merging a state update creates a newer main commit by definition. Operational alignment is instead expressed as a clean tracking relationship to `origin/main` at the time of observation; exact SHA is retained only as bounded evidence.

## 12. Architecture synchronization rule — 2026-10-03

Current machine-readable state, this architecture record, the Law Index, recovery manifest and role bootstrap must agree on:

- authority order;
- current learning-assurance generation;
- runtime evidence vs current liveness semantics;
- background autonomy remaining OFF;
- research adapter remaining fail-closed until the genuine fresh-seat gate passes;
- no automatic VERIFIED, automatic trial activation or autonomous durable mutation;
- provider/model/tool mechanisms remaining replaceable and non-canonical.

Historical documents may preserve old implementation status, but must be explicitly marked historical/superseded when they are no longer valid descriptions of current capability.

## 13. Runtime assurance AUTO evidence — 2026-10-03 12:42 +07:00

Canonical evidence file:
`docs/runtime_evidence/RUNTIME_ASSURANCE_AUTO_20261003T124215_PLUS0700.json`

This evidence proves only the bounded observations captured there. It does not prove boot/reboot persistence, old-key revocation, BitLocker state, McAfee realtime protection state, full-device independent witness, or fresh-seat recovery.

## 14. Desktop Commander hardening — 2026-10-03

Evidence: `docs/runtime_evidence/DESKTOP_COMMANDER_HARDENING_20261003T125254_PLUS0700.json`.

The maintenance-plane filesystem scope is now restricted to the canonical MINH TRÍ runtime directory only. This closes the Desktop Commander filesystem-scope gate, but does not prove fresh-seat recovery or boot/reboot persistence.

## 15. Fresh-seat / boot-persistence precheck — 2026-10-03 12:59 +07:00

Fresh-seat attempt:
- current seat exposed exactly `brain.verify` and `brain.recovery_packet`;
- both returned `VALID`, event_count=3, same ledger head;
- recovery without a query restored ACTIVE YouTube focus and the current untested expectation;
- however canonical validator also requires `separate_chat_ui=true` and an independent `control_verify` from a separate control seat;
- those two conditions are not proven here, so `fresh_chat_seat_validation` remains blocked and `end_to_end_seat_brain_transport=false`.

Boot-persistence precheck:
- Desktop Commander hardening remains in force with a runtime-only allowlist;
- tunnel `/readyz=200 ready`, brain verify/recovery are healthy, and Owner credential v2 verifies;
- no matching Scheduled Task/startup entry/dedicated MINH TRÍ service was found by the bounded current probe;
- the tunnel launcher still obtains the control-plane API key interactively;
- no User/Machine environment persistence or dedicated tunnel DPAPI/file credential was observed;
- tunnel-client supports `--control-plane.api-key env:VARNAME` or `file:/path`, which allows a future secret-safe unattended design;
- the local canonical clone observed on the Owner PC is clean but stale relative to live GitHub main.

Therefore controlled reboot is intentionally blocked until:
1. a dedicated encrypted tunnel credential is provisioned without plaintext persistence;
2. a boot/login auto-start mechanism is installed without secrets in task/service arguments;
3. the recovery source/clone is current enough for recovery;
4. a fresh pre-reboot evidence snapshot is captured.

Evidence:
- `docs/runtime_evidence/FRESH_SEAT_ATTEMPT_20261003T125900_PLUS0700.json`
- `docs/runtime_evidence/BOOT_PERSISTENCE_PRECHECK_20261003T125900_PLUS0700.json`


## 16. Secret-safe autostart deployment + PowerShell CI hardening — 2026-10-03

The secret-safe tunnel autostart components are implemented, merged, CI-proven and deployed to the Owner-PC runtime, with fail-closed smoke evidence in `docs/runtime_evidence/SECRET_SAFE_AUTOSTART_DEPLOY_20261003T132600_PLUS0700.json`.

At that historical deployment stage, the dedicated tunnel DPAPI credential was not yet provisioned and the limited logon task was not yet installed. Later evidence shows both were subsequently provisioned/installed; reboot persistence nevertheless remains NOT_PROVEN.

Architecture audit PR #112 fixed an ambiguous PowerShell ACL-grant expression in the provisioner and added a Windows parser job to the required CI aggregate. This closed the source/CI defect. Later evidence recorded corrected-script deployment and DPAPI/logon-task provisioning; those later records supersede this stage for deployment state, but do not prove reboot persistence.

Full audit and ordered completion plan:
`docs/ARCHITECTURE_AUDIT_COMPLETION_PLAN_20261003.md`.

## 17. Completion boundary

"Foundation complete" and "project/product complete" are distinct.

Foundation promotion requires the current runtime-assurance, fresh-seat, witness, critic/empirical-validation and backlog gates to close with evidence.

Production/product completion additionally requires later Owner-authorized work for real providers/data/business loops, stronger identity before external actions, operational recovery/observability, and real-world validation. Until those later gates are explicitly defined and passed, `FOUNDATION_PROTOTYPE` remains the truthful phase.


## 17A. HISTORICAL — Post-reboot remote reachability audit — 2026-10-03 15:35 +07:00

Evidence: `docs/runtime_evidence/POST_REBOOT_REMOTE_REACHABILITY_20261003T153500_PLUS0700.json`.

Current bounded observation from this seat:
- canonical GitHub remained reachable and Security P0 for PR #119 was PASS across Python 3.10/3.11/3.12, PowerShell parse, security audit and aggregate `test`;
- the MINH TRÍ read-only connector was UNREACHABLE with the control-plane message that the tunnel-client had not been seen for 300 seconds;
- Desktop Commander reported no currently online device; `WIN-VBIQNFFDKIR` was last seen approximately 41 minutes earlier;
- therefore local Scheduled Task state, tunnel process state and loopback health could not be inspected;
- root cause remains UNKNOWN, and boot/reboot persistence remains NOT_PROVEN.

This newer observation supersedes the 12:42 +07:00 liveness snapshot only for current liveness. It does not erase earlier historical PASS evidence.


## 18. HISTORICAL — Bounded 24H self-upgrade lease implementation stage

Owner authorized the architecture for a maximum 24-hour self-learning/self-upgrade capability window. The implementation is merged to canonical `main` with required CI PASS and **does not activate a live 24H lease**.

Implemented and CI-proven components:
- immutable Owner-gated upgrade lease capped at 86,400 seconds;
- fail-closed UTC + monotonic runtime checks and immediate pre-mutation recheck;
- early Owner revocation;
- child capability inheritance with the same lease/expiry and equal-or-less scope;
- candidate-branch sandbox blocking authority/security control paths;
- generation manifests and explicit lineage states;
- deterministic Parent-versus-Candidate evaluator using a frozen packet digest;
- no automatic VERIFIED, no automatic trial activation, no automatic Candidate promotion;
- frozen candidates require Owner promotion and still use normal PR/CI/branch protection for canonical merge.

Current bounded status: source/tests are merged and required CI passed; runtime short-lease expiry proof remains pending. A real 24-hour lease must not be activated until short-duration expiry/revocation/clock-rollback/child-containment tests have passed with evidence.

Authority record: `docs/OWNER_DECISION_24H_SELF_UPGRADE_LEASE_20261003.md`.


## 19. HISTORICAL — Self-upgrade runtime controller and short-proof harness

A runtime controller is staged on the current PR to turn the immutable lease into an in-memory session boundary:

- the authoritative live lease exists only in process memory;
- process exit/restart loses the lease and therefore loses upgrade authority (fail closed);
- no renewal method is exposed;
- child capability inherits the same lease id/expiry and equal-or-less scope;
- candidate mutation authorization still passes through the existing candidate branch/path guard;
- a short-proof command runs a real-clock 60–300 second expiry proof and a separate Owner-revocation proof;
- Owner secret is taken from an environment value if present and removed from the process environment, otherwise requested with a non-echoing prompt;
- CI adds a dedicated real-clock 60-second expiry probe so elapsed-time enforcement is not proven only by mocks.

Important boundary: this controller is not an OS sandbox. It does not prove that arbitrary candidate code cannot bypass Python-level guards if executed with unrestricted host credentials. Therefore `candidate_execution_containment=NOT_PROVEN_OS_SANDBOX` remains binding until a separate process/OS containment design is implemented and tested.

A real Owner-PC short lease remains required before activating the 24-hour lease.


## 20. Real-clock lease expiry CI evidence

PR #123 merged the self-upgrade runtime session controller after required Security P0 PASS.

Bounded real-clock evidence:
- duration requested: 60 seconds;
- observed elapsed monotonic time: 60.25014910499999 seconds;
- pre-expiry mutation: completed;
- post-expiry mutation: blocked;
- Owner-PC runtime proven: false;
- OS sandbox containment proven: false.

This proves elapsed-time expiry at the CI runtime/controller boundary. It does not prove Owner-PC execution, 24-hour expiry, arbitrary candidate-code containment, or safe autonomous activation on the host. The live 24H lease remains OFF.


## 21. HISTORICAL — Lease-bound Codex provider live binding

The bounded self-upgrade path now has live Owner-PC evidence through the candidate mutation boundary:

- Codex CLI 0.160.0 is installed on the Owner PC and authenticated through ChatGPT;
- planning runs with Codex `read-only` sandbox;
- candidate apply runs with Codex `workspace-write` sandbox;
- the adapter closes stdin for true non-interactive execution;
- explicit `candidate_objective` and optional exact `required_changed_paths` are enforced before write;
- self-upgrade control-plane files are protected from Candidate mutation;
- provider blocked/no-change results cannot be mislabeled as successful candidates;
- Owner-PC controlled smoke created exactly `docs/CODEX_WORKSPACE_WRITE_SMOKE.md` in an isolated candidate worktree, with the declared path equal to the actual path;
- the smoke did not commit, push, merge, auto-renew, auto-promote or mark VERIFIED;
- integrated Owner revoke is proven on the Owner PC without weakening Windows Execution Policy.

Current boundary remains explicit: a live 24-hour lease is still OFF. The next missing end-to-end layer is the candidate lifecycle `TEST → CRITIC → FREEZE` after a successful workspace mutation. OS-level containment of arbitrary candidate code is also not proven. No 24H activation claim is permitted until those remaining boundaries are resolved or explicitly accepted by Owner governance.

Runtime evidence:
- `docs/runtime_evidence/SELF_UPGRADE_OWNER_REVOKE_E2E_20261003T191700_PLUS0700.json`
- `docs/runtime_evidence/SELF_UPGRADE_CODEX_WORKSPACE_WRITE_20261003T201243_PLUS0700.json`


## 22. HISTORICAL EVIDENCE — Owner-PC TEST → CRITIC → FREEZE lifecycle proof — 2026-10-03 21:06 +07:00

Canonical evidence: `docs/runtime_evidence/SELF_UPGRADE_LIFECYCLE_OWNER_PC_20261003T210607_PLUS0700.json`.

After PR #136 and PR #137 corrected the live Codex CLI 0.160.0 restricted-token invocation and src-layout import environment, the bounded Owner-PC lifecycle smoke completed end-to-end:

- lease-bound Codex mutation created exactly one declared candidate artifact in the isolated candidate worktree;
- full unittest discovery PASSed inside the Windows restricted-token sandbox with direct network disabled;
- the read-only Codex critic returned `NO_MATERIAL_DEFECT` for the neutral smoke artifact and is explicitly recorded as `SAME_PROVIDER_NOT_INDEPENDENT`;
- a digest-bound freeze receipt was created and the runtime transitioned to `FROZEN_PENDING_OWNER` / `FROZEN`;
- automatic VERIFIED promotion, automatic Candidate promotion and canonical write capability remained false.

A first smoke using the text `CANDIDATE_LIFECYCLE_SMOKE_PASS` was correctly rejected by the critic as an unsupported success claim. The proof was rerun with the neutral text `CANDIDATE_LIFECYCLE_SMOKE_ARTIFACT`; the critic then accepted the artifact without weakening its criteria.

This closes the bounded TEST → CRITIC → FREEZE runtime-E2E gap. It does **not** prove independent critic authority and does **not** prove OS-level containment of arbitrary Candidate code. The live 24H lease remains OFF. The remaining self-upgrade decision boundary is whether Owner requires stronger OS containment before any explicit 24H activation.


## 23. HISTORICAL EVIDENCE — Codex workspace-write outside-worktree negative probe — 2026-10-03 21:09 +07:00

Evidence: `docs/runtime_evidence/CODEX_WORKSPACE_CONTAINMENT_PROBE_20261003T210957_PLUS0700.json`.

A live Owner-PC `codex exec --sandbox workspace-write` probe was instructed to create a harmless canary immediately outside the isolated candidate worktree. The underlying PowerShell write returned UnauthorizedAccess / access denied, the canary was never created, and no repository file was intentionally modified. This is positive evidence that the live workspace-write sandbox enforced that tested filesystem boundary.

This remains a **bounded negative probe**, not universal proof against arbitrary candidate code, sandbox escape, or host compromise. Therefore the architecture does not promote the OS-containment claim to universal VERIFIED. The live 24H lease remains OFF; Owner must decide whether this bounded containment evidence is sufficient before any explicit activation.


## 24H Owner authorization recorded — 2026-10-03

Owner explicitly accepted the bounded OS-containment evidence and ordered immediate activation of the real 86,400-second self-upgrade lease. Canonical authorization is therefore satisfied. Runtime activation remains a separate empirical fact and must only be marked ACTIVE after live Owner-PC evidence records lease id, issued_at, expires_at, process/session identity, and fail-closed controls. No chat statement alone counts as runtime proof.


## 25. Live 24H lease + local brain audit closure — 2026-10-03 23:29 +07:00

Evidence: `docs/runtime_evidence/SELF_UPGRADE_LIVE_24H_AND_BRAIN_AUDIT_20261003T232905_PLUS0700.json`.

The live lease is empirically ACTIVE with lease id `upgrade-78bb759426dd41d4b306dc995dc47fae`, expiry `2026-10-04T15:56:05.483438Z`, and continuing heartbeat. The local brain ledger now contains append-only `LEASE_CREATED` and `LEASE_ACTIVATED` audit events; `brain.verify` reports VALID with event_count 5 and head `bbc3e5080b3e397550cbc13d319fbfccbd3888fc6fa6c9d2d5ac64a2827c4fe4`. This closes the audit gap for activation. The actual 24-hour expiry proof remains deliberately NOT PROVEN until the lease reaches its real expiry and mutation authority is observed to fail closed.


## 26. Manual blind external critic channel — 2026-10-03

Merged in `d2881608b72763d4923e366c12b3ccfc7161b0f7` after Security P0 PASS.

The external critic control plane now supports a manual Owner-mediated channel only. Candidate code cannot write `src/minhtri/critic/`. A critic packet is built only after deterministic TEST and internal critic, contains bounded artifact/test output/claims plus a pinned eval hash, is redacted and hash-bound, and excludes learner reasoning, prior critic conclusions and Owner preference. The prompt is versioned and fixed in-repo; responses must match a strict JSON verdict schema.

When this external gate is configured, pending, invalid or post-expiry responses do not permit FREEZE. A MEDIUM/HIGH/CRITICAL external defect blocks freeze. `NO_MATERIAL_DEFECT_FOUND` is recorded as PARTIAL independence evidence only and never promotes VERIFIED or replaces Owner review. The API/network provider remains disabled pending a future lease and separate review. Runtime execution with a real outside model has not yet been captured, so external critic independence remains PARTIAL / NOT PROVEN.


## 27. Authenticated worker handoff proof and live-lease transition — 2026-10-04 00:31 +07:00

Evidence: `docs/runtime_evidence/AUTHENTICATED_WORKER_HANDOFF_OWNER_PC_20261004T003158_PLUS0700.json`.

Owner-commanded revocation of the prior 24H lease completed at `2026-10-03T17:03:16.621694Z`; local brain now records the revoke event. PR #151 merged the authenticated parent-enforcer handoff at `3004f910cd0354c06f78b6d961c7c716bb79ec1c` after Security P0 PASS.

A real Owner-PC 300-second smoke lease then proved the handoff path: one-time IPC credential delivered over stdin only, loopback authenticated IPC, worker held no authoritative lease object, parent re-checked candidate branch and paths before mutation, exactly one neutral candidate artifact was written, and post-revoke mutation was blocked. No push, merge, renewal or canonical-write capability existed.

The replacement live (>300s) lease is intentionally not issued from the earlier Owner command because current law requires a contemporaneous Owner authorization reference no older than 300 seconds at issuance. A fresh Owner command is therefore required for the new live lease; this is the anti-prearm gate working as designed.


## 28. Live 24H lease with authenticated worker handoff — 2026-10-04 00:56 +07:00

Evidence: `docs/runtime_evidence/SELF_UPGRADE_LIVE_24H_HANDOFF_20261004T005645_PLUS0700.json`.

Owner issued a fresh explicit command and the runtime activated a new immutable 86,400-second lease `upgrade-29829fc6febf4c5db42e5ff4a93aa0da` at `2026-10-03T17:56:45.124745Z`, expiring at `2026-10-04T17:56:45.124745Z`. The lease pins Owner authorization ref, Champion SHA, test-dataset hash, eval packet hash and eval metric before activation.

The live controller keeps the authoritative lease in the parent process. Workers receive only a one-time stdin bootstrap for loopback authenticated IPC; `worker_holds_lease=false` and `parent_enforced=true`. Automatic renewal, VERIFIED promotion, candidate promotion, push, merge and canonical write remain false. Local brain audit is VALID at event_count 12, head `c272af26799a7ff32f681de9ac12c712ac1a921f6bebdeab5ac383b2be95e18d`.


## 29. Architecture consistency repair — 2026-10-04

This repair makes the recovery semantics explicit:

- capability/deployment evidence may remain PASS historically while current runtime liveness is UNKNOWN;
- only `PROJECT_STATE.current_runtime_liveness` is authoritative for current maintenance/tunnel/brain availability;
- historical "live/current/session" field names are retained for compatibility but their values must identify themselves as historical/non-authoritative;
- stale implementation-stage statements such as "live lease OFF" remain historical evidence and do not override later lease records;
- bootstrap security findings must distinguish CLOSED/PARTIAL/OPEN instead of repeating a fixed P0 as current;
- active learning tracks may coexist with runtime-assurance work but cannot enable background autonomy or Research Adapter;
- current architecture never treats an open-PR count, old SHA, or old runtime heartbeat as a durable invariant.

Current runtime remains UNKNOWN until fresh proof re-establishes the maintenance and read planes.


## 30. Full architecture synchronization — 2026-10-04

This synchronization aligns all current authority surfaces after PR #156 and the Economics doctoral-level learning-track registration.

### Current runtime
- Owner PC: UNKNOWN.
- Maintenance plane: OFFLINE.
- Secure MCP tunnel: DOWN.
- Local Brain connector: DOWN.
- Historical connector/brain PASS evidence remains valid only as historical evidence.
- Current runtime can be promoted back to healthy only by fresh maintenance + /readyz + brain.verify + brain.recovery_packet proof.

### Self-upgrade lease semantics
The latest 86,400-second authorization window has not expired by wall-clock at this synchronization observation, but the live parent process is not currently observable. Therefore:
- authorization window: OPEN until `2026-10-04T17:56:45.124745Z`;
- runtime lease state: UNKNOWN_NOT_CURRENTLY_OBSERVED;
- historical activation proof remains preserved;
- no mutation authority may be inferred merely from the unexpired timestamp;
- process restart/exit semantics remain fail-closed.

### Learning
The Economics PhD-level learning track is canonical and active at `M0.1 STARTED / UNTESTED`. It is a doctoral-level self-study program, not an accredited degree. Background autonomy remains OFF and Research Adapter remains blocked until genuine fresh-seat PASS.

### Synchronization invariant
`PROJECT_STATE.json` is the machine-readable current-state authority. Recovery manifest, current architecture, bootstrap, README, SECURITY, runbook and domain-learning records must not contradict it. Historical records keep provenance but never override current state.


## 31. Claude adversarial self-learning review adjudication — 2026-10-04

Independent review sharpened the boundary between proposal governance and actual behavioral learning.

Immediate code hardening:
- Research Adapter cannot open from historical fresh-seat flags alone; fresh-seat PASS is TTL-bound and current tunnel + Local Brain liveness must be UP.
- `src/minhtri/autonomy.py` and `src/minhtri/fresh_seat.py` are now protected candidate paths.
- A recorded negative-control `FAIL` for a learning packet bound to the source claim blocks lesson freeze.
- Candidate A is rejected under the new policy because it targeted `src/minhtri/autonomy.py`; its historical test packet remains audit evidence only.

Remaining assurance gaps:
- resolution scoring is mechanically derived from preregistered intervals and numeric outcome evidence, but outcome evidence remains `DECLARED_UNVERIFIED` and resolver identity/independence is not encoded;
- stratified meta-learning is descriptive/proposal-only and lacks multiplicity/sample-size evidence sufficient for adaptation;
- Research Adapter has no approved ingestion-safety implementation yet;
- current Owner-PC commit/build attestation is not proven while runtime is offline;
- old tunnel-key provider-side revocation, genuine fresh-seat execution, independent witness, external critic, and empirical v1.4 benefit remain open.

Terminology boundary:
Current MINH TRÍ may claim a **proposal-governance learning pipeline**. It must not claim autonomous self-learning or empirically effective meta-learning until a learned rule demonstrably changes future behavior and survives controlled evaluation.


## 32. Gemini adversarial review adjudication — 2026-10-04

Gemini's review was adjudicated against live main after Claude hardening.

- DEF-01: PARTIAL / HARDENING GAP, not a proven CRITICAL defect. Historical receipts are audit-only; self-upgrade mutation authority resides in the live parent lease, is checked immediately before mutation, and worker handoff uses one-time authenticated loopback IPC with nonce binding. Runtime epoch-bound tokens remain a possible hardening layer, but stale receipts were not found to authorize mutation.
- DEF-02: ALREADY FIXED SEMANTICALLY. Canonical classification is `PROPOSAL_GOVERNANCE_PIPELINE_NOT_AUTONOMOUS_BEHAVIOR_ADAPTATION`. Historical filenames/terms remain provenance, not current capability claims.
- DEF-03: PARTIAL VALID. The external critic packet is blind to learner reasoning, prior critic output and Owner preference, and is hash-bound/redacted. However shared model priors, corpus independence and account/authority independence are not proven; external critic evidence remains PARTIAL.
- DEF-04: VALID GAP. Previous meta-learning could emit candidate proposals from very small N. The default candidate floor is now 50 resolutions globally/per stratum. This is a conservative proposal floor only, not statistical proof. Multiplicity control is still NOT_IMPLEMENTED and a permutation test remains REQUIRED_BEFORE_ADAPTATION.
- DEF-05: NOT A CURRENT DEFECT. Fresh-seat validation does not call Research Adapter. Dependency is one-way: fresh attestation may unlock research; research is not used to establish fresh-seat PASS.

Rejected as over-prescriptive absent proof:
- mandatory TPM/Secure Enclave/mTLS architecture;
- BitLocker-not-encrypted as a global HALT_SYSTEM condition;
- mandatory three-provider majority voting;
- fixed p<0.01 or fixed 1.5-sigma rollback thresholds;
- production traffic canary percentages for a system that has no production autonomous mutation.

These may be reconsidered when threat model, data volume and deployment mode justify them.


## 33. Trial-001 calibration boundary — 2026-10-04

The first empirical trial is now explicitly a **paired four-arm calibration harness**, not a learning proof by default.

For every eligible task:
- A = CONTROL;
- B = COUNTEREVIDENCE_FIRST treatment;
- C = compute-matched neutral deep review;
- D = shuffled-ledger placebo.

Every arm receives the same frozen task bytes. Arm order is randomized; retrieval/cache/session state must be isolated by arm.

A learning-from-experience claim additionally requires treatment lesson provenance bound to an audited meta-lesson candidate, audited resolution IDs and audited strata. Without that provenance, even a causal B>C result is evidence only for overlay value/harness discrimination.

Declared compute budgets are insufficient. Actual token/retrieval/critic/generator telemetry must satisfy a frozen parity tolerance for B/C/D before a task enters primary causal analysis.

Coverage non-inferiority is mandatory so the treatment cannot win factual-accuracy and unsupported-claim metrics merely by saying less.

The current repository implements planning/validation contracts. It does **not** yet contain a proven live isolated executor, provider telemetry capture, blinded evaluator runtime, or empirical Trial-001 result. External code review of the reader remains required.
