# LOCAL BRAIN HTTP CONNECTOR — 2026-10-02

**Status:** IMPLEMENTED REFERENCE HOST + E2E TEST / OWNER-PC DEPLOYMENT NOT VERIFIED

## Purpose
Provide a real process boundary between a replaceable AI seat/connector process and the local MINH TRÍ brain without exposing mutation rights.

## Runtime boundary
- bind only to literal loopback addresses;
- fixed brain directory configured when the host starts;
- bearer token required at the HTTP boundary;
- only `brain.verify` and `brain.recovery_packet` are exposed;
- no remote filesystem path selection;
- no mutation method;
- request and response sizes are bounded;
- transport failures and ledger verification failures fail closed;
- default HTTP handler logging is suppressed to avoid leaking bearer tokens, queries or brain metadata.

## Proven in repository tests
A fresh client process can recover the verified focus/head from a temporary local ledger over the authenticated loopback HTTP boundary. Tests also cover wrong-token rejection, path redirection rejection, mutation rejection, non-loopback bind rejection and tampered-snapshot failure.

## Not yet proven
This repository test does **not** prove that the Owner's actual PC currently has the host process running, nor that the current ChatGPT product session has an installed connector route to that loopback endpoint.

Therefore:
- `brain_http_host`: IMPLEMENTED_AND_MERGED after this change;
- `brain_http_e2e_test`: CI_PROVEN after exact-head CI;
- `owner_pc_brain_http_host_running`: UNKNOWN until observed on Owner runtime;
- `chatgpt_to_owner_pc_brain_connector`: NOT_CONNECTED until product connector installation is observed.

Do not upgrade `end_to_end_seat_brain_transport` to true merely from repository CI.
