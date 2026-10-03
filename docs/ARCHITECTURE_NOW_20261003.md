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
Desktop Commander là break-glass/maintenance, không phải canonical brain transport. Hiện config `allowedDirectories=[]` nghĩa là full-filesystem access; hardening config phải làm trong chat riêng theo safety rule của chính tool.

### Witness plane
Current GitHub witness chỉ process-separated; chưa độc lập trước full Owner-PC/account compromise.

## 4. Runtime proof hiện tại

- Secure tunnel: LIVE, `/readyz=200 ready`.
- Connector: đúng hai read-only tools.
- Brain: `VALID`, event_count=3, head `ef299f726f0b83300df9c91ae9648ca20d643e992e7f20cfb769673382e45927`.
- Supervisor child restart: PASS trong cùng session.
- Boot/reboot persistence: NOT_PROVEN.
- Owner write gate v2: wrong-secret fail-closed + DPAPI positive repair-snapshot E2E PASS.
- Local canonical write clone đã sync sạch với GitHub main sau merge #91.
- Old tunnel key revocation: NOT_VERIFIED.
- Fresh-seat recovery: PENDING.
- Independent witness: BLOCKED_NO_INDEPENDENT_AUTHORITY_PROVIDER_CREDENTIAL.

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
- Security P0 includes Python 3.10/3.11/3.12 matrix, history secret scan and pip-audit.
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

## 8. Promotion gates còn mở

1. verify/revoke every old tunnel key;
2. harden Desktop Commander filesystem scope in a separate config-hardening chat;
3. establish secure boot persistence design and prove after controlled restart/reboot;
4. resolve endpoint-protection and BitLocker UNKNOWNs with stronger evidence;
5. perform genuine fresh-seat validation;
6. establish independent witness authority/credential;
7. clean/resolve remaining active learning and Dependabot PRs;
8. only then reconsider closing foundation build phase.

## 9. Backlog hygiene

Historical architecture experiment PRs #2–#11 and superseded audit PR #81 are closed, with history preserved. Learning PRs and current dependency PRs remain active and must be evaluated on current main before merge.

## 10. Bootstrap

Read in order:
1. `docs/PROJECT_STATE.json`
2. `docs/LAW_INDEX_20261003.md`
3. `docs/ARCHITECTURE_NOW_20261003.md`
4. `docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md`
5. task/domain source.

## 11. Non-self-referential deployment evidence

A recorded local deployment SHA is historical evidence only. It must never be interpreted as a requirement that the local clone equal the repository's forever-current main SHA, because merging a state update creates a newer main commit by definition. Operational alignment is instead expressed as a clean tracking relationship to `origin/main` at the time of observation; exact SHA is retained only as bounded evidence.
