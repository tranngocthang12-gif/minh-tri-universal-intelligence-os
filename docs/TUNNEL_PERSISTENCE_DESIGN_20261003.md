# Secret-safe tunnel autostart design — 2026-10-03

**Status:** IMPLEMENTED + MERGED + DEPLOYED / REBOOT PERSISTENCE NOT YET PROVEN

Goal: provide current-user unattended launch for the canonical read-only tunnel without storing the runtime API key in plaintext or embedding it in Scheduled Task arguments.

Components:
- `provision_tunnel_runtime_key.ps1`: secure prompt -> CurrentUser DPAPI ciphertext at `%LOCALAPPDATA%\MINH_TRI\tunnel.runtime.dpapi`, restricted ACL, no plaintext persistence.
- `run_tunnel_unattended.ps1`: decrypts in memory, sets `CONTROL_PLANE_API_KEY` only in process environment, launches existing `minhtri.runtime_supervisor`, removes env and zeroes BSTR.
- `install_tunnel_logon_task.ps1`: refuses missing prerequisites, creates limited current-user AtLogOn task, and rejects secret-like task arguments.

This is not key rotation and does not revoke old credentials. It does not prove persistence until actual reboot/logon recovery occurs without manual launch.

Promotion sequence:
CI PASS -> deploy scripts -> Owner provisions current tunnel key once through secure prompt -> install limited AtLogOn task -> pre-reboot snapshot -> controlled reboot -> no manual launch -> /readyz PASS -> brain.verify/recovery PASS -> only then consider persistence PROVEN.


## Deployment update — 2026-10-03

The secret-safe autostart scripts were merged, deployed to the Owner-PC runtime, and smoke-tested fail-closed while the dedicated tunnel DPAPI secret is absent. Evidence: `docs/runtime_evidence/SECRET_SAFE_AUTOSTART_DEPLOY_20261003T132600_PLUS0700.json`.

A later architecture audit found and fixed a PowerShell parsing hazard in the provisioner's ACL grant construction. PR #112 added a Windows PowerShell parser CI job and passed the required `test` gate before merge.

Current boundary remains unchanged:
- dedicated tunnel DPAPI secret: NOT PROVISIONED;
- limited AtLogOn task: NOT INSTALLED;
- reboot/logon recovery: NOT PROVEN;
- no plaintext tunnel key is recorded in canonical evidence.

Therefore the next runtime promotion still requires one-time secure key provisioning, task installation, a fresh pre-reboot snapshot, controlled reboot/logon without manual tunnel launch, and post-reboot read-plane verification.
