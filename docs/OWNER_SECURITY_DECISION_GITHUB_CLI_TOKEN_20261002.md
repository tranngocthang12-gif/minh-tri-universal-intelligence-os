# OWNER SECURITY DECISION — GitHub CLI token on Owner PC — 2026-10-02

**Status:** OWNER DECISION / CURRENT SECURITY GATE

Owner decision:
- Do not log out GitHub CLI on the Owner PC.
- Do not revoke, rotate, delete, replace, or otherwise mutate the GitHub CLI credential on the Owner PC.
- Any such credential mutation requires a new explicit Owner instruction.
- Architecture reviews may recommend future hardening, but recommendation alone is not authorization to change the credential.

This gate applies until explicitly superseded by the Owner.
