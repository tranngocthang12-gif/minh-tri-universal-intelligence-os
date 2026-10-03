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

## 4. Runtime proof hiện tại

Runtime evidence và current liveness là hai lớp khác nhau.

**Fresh observation trong AUTO runtime-assurance 2026-10-03 12:42 +07:00:**
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

CLOSED on 2026-10-03. Historical architecture experiment PRs #2–#11 and superseded audit PR #81 are closed with history preserved. Learning Assurance v1–v1.4 is merged. PR #116 refreshed/merged the learning backlog and PR #117 refreshed/merged the dependency update; the current audit observed zero open PRs. Backlog hygiene is therefore not a current completion blocker.

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

The dedicated tunnel DPAPI credential is still NOT PROVISIONED, the limited logon task is NOT INSTALLED, and reboot persistence remains NOT PROVEN.

Architecture audit PR #112 fixed an ambiguous PowerShell ACL-grant expression in the provisioner and added a Windows parser job to the required CI aggregate. This closes the source/CI defect only; the corrected runtime script still requires deployment before key provisioning.

Full audit and ordered completion plan:
`docs/ARCHITECTURE_AUDIT_COMPLETION_PLAN_20261003.md`.

## 17. Completion boundary

"Foundation complete" and "project/product complete" are distinct.

Foundation promotion requires the current runtime-assurance, fresh-seat, witness, critic/empirical-validation and backlog gates to close with evidence.

Production/product completion additionally requires later Owner-authorized work for real providers/data/business loops, stronger identity before external actions, operational recovery/observability, and real-world validation. Until those later gates are explicitly defined and passed, `FOUNDATION_PROTOTYPE` remains the truthful phase.


## 16. Post-reboot remote reachability audit — 2026-10-03 15:35 +07:00

Evidence: `docs/runtime_evidence/POST_REBOOT_REMOTE_REACHABILITY_20261003T153500_PLUS0700.json`.

Current bounded observation from this seat:
- canonical GitHub remained reachable and Security P0 for PR #119 was PASS across Python 3.10/3.11/3.12, PowerShell parse, security audit and aggregate `test`;
- the MINH TRÍ read-only connector was UNREACHABLE with the control-plane message that the tunnel-client had not been seen for 300 seconds;
- Desktop Commander reported no currently online device; `WIN-VBIQNFFDKIR` was last seen approximately 41 minutes earlier;
- therefore local Scheduled Task state, tunnel process state and loopback health could not be inspected;
- root cause remains UNKNOWN, and boot/reboot persistence remains NOT_PROVEN.

This newer observation supersedes the 12:42 +07:00 liveness snapshot only for current liveness. It does not erase earlier historical PASS evidence.


## 18. Bounded 24H self-upgrade lease — implementation candidate

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


## 19. Self-upgrade runtime controller and short-proof harness

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


## 21. Lease-bound Codex provider live binding

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


## 22. Owner-PC TEST → CRITIC → FREEZE lifecycle proof — 2026-10-03 21:06 +07:00

Canonical evidence: `docs/runtime_evidence/SELF_UPGRADE_LIFECYCLE_OWNER_PC_20261003T210607_PLUS0700.json`.

After PR #136 and PR #137 corrected the live Codex CLI 0.160.0 restricted-token invocation and src-layout import environment, the bounded Owner-PC lifecycle smoke completed end-to-end:

- lease-bound Codex mutation created exactly one declared candidate artifact in the isolated candidate worktree;
- full unittest discovery PASSed inside the Windows restricted-token sandbox with direct network disabled;
- the read-only Codex critic returned `NO_MATERIAL_DEFECT` for the neutral smoke artifact and is explicitly recorded as `SAME_PROVIDER_NOT_INDEPENDENT`;
- a digest-bound freeze receipt was created and the runtime transitioned to `FROZEN_PENDING_OWNER` / `FROZEN`;
- automatic VERIFIED promotion, automatic Candidate promotion and canonical write capability remained false.

A first smoke using the text `CANDIDATE_LIFECYCLE_SMOKE_PASS` was correctly rejected by the critic as an unsupported success claim. The proof was rerun with the neutral text `CANDIDATE_LIFECYCLE_SMOKE_ARTIFACT`; the critic then accepted the artifact without weakening its criteria.

This closes the bounded TEST → CRITIC → FREEZE runtime-E2E gap. It does **not** prove independent critic authority and does **not** prove OS-level containment of arbitrary Candidate code. The live 24H lease remains OFF. The remaining self-upgrade decision boundary is whether Owner requires stronger OS containment before any explicit 24H activation.
