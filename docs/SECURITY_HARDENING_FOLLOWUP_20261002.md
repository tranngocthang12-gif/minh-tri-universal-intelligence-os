# SECURITY HARDENING FOLLOW-UP — 2026-10-02

**Status:** HISTORICAL IMPLEMENTATION SNAPSHOT / MERGED; CURRENT STATUS LIVES IN PROJECT_STATE + CURRENT ARCHITECTURE  
**Base main:** `832cd09c5537ab7b0a46d76f26c42e53f35a84fe`

## Historical blockers observed before this PR

1. Owner PC maintenance plane: OFFLINE at the latest probe.
2. Local Brain connector: DOWN; tunnel-client had not been seen for more than 300 seconds.
3. Secure MCP Tunnel persistence: NOT PROVEN.
4. Old tunnel runtime key revocation: NOT VERIFIED.
5. Secure write launcher v2: E2E proof blocked while Owner PC is offline.
6. Independent witness: no authority/provider/credential independent from both Owner PC and GitHub.

No historical PASS is promoted to current liveness.

## Independent hardening in this PR

- add a reachable-Git-history secret scanner that redacts secret values;
- add a required security-audit CI job;
- audit installed Python dependencies with `pip-audit==2.10.1`;
- make the existing required `test` context depend on both the Python matrix and security audit;
- enable Dependabot proposals for Python and GitHub Actions;
- add CODEOWNERS metadata without claiming approval enforcement;
- add a repository security policy.

## Promotion rule

Do not merge if the exact PR head does not pass the required Security P0 / `test` context.
A CI PASS proves only the checks encoded here; it does not prove Owner-PC deployment, tunnel
persistence, key revocation, fresh-seat recovery, independent witness, or host hardening.
