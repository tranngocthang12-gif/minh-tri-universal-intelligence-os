# Secret-safe tunnel autostart design — 2026-10-03

**Status:** IMPLEMENTATION CANDIDATE / CI REQUIRED / RUNTIME NOT YET PROVEN

Goal: provide current-user unattended launch for the canonical read-only tunnel without storing the runtime API key in plaintext or embedding it in Scheduled Task arguments.

Components:
- `provision_tunnel_runtime_key.ps1`: secure prompt -> CurrentUser DPAPI ciphertext at `%LOCALAPPDATA%\MINH_TRI\tunnel.runtime.dpapi`, restricted ACL, no plaintext persistence.
- `run_tunnel_unattended.ps1`: decrypts in memory, sets `CONTROL_PLANE_API_KEY` only in process environment, launches existing `minhtri.runtime_supervisor`, removes env and zeroes BSTR.
- `install_tunnel_logon_task.ps1`: refuses missing prerequisites, creates limited current-user AtLogOn task, and rejects secret-like task arguments.

This is not key rotation and does not revoke old credentials. It does not prove persistence until actual reboot/logon recovery occurs without manual launch.

Promotion sequence:
CI PASS -> deploy scripts -> Owner provisions current tunnel key once through secure prompt -> install limited AtLogOn task -> pre-reboot snapshot -> controlled reboot -> no manual launch -> /readyz PASS -> brain.verify/recovery PASS -> only then consider persistence PROVEN.
