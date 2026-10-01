# OWNER CREDENTIAL V2 MIGRATION — 2026-10-02

**Status:** SECURITY DESIGN / NOT IMPLEMENTED / V1 REMAINS ACTIVE

## Problem
Current Owner Gate uses a declared owner id plus an unsalted SHA-256 verifier. P0 correctly moved authentication inside the mutation boundary, but the verifier is not suitable as the long-term credential design.

## Required properties
Credential v2 must:
- keep authentication inside every durable mutation boundary;
- use a versioned credential record;
- use a password KDF or OS-backed secret mechanism rather than raw SHA-256;
- use per-credential random salt when a KDF is used;
- support credential rotation and explicit revocation;
- compare derived verifiers in constant time;
- never expose the mutation secret to BrainReader/read-only transport;
- fail closed on unknown credential versions or malformed parameters;
- preserve an explicit migration path from v1 without silently weakening the gate.

## Candidate config shape
The exact KDF is an implementation choice after runtime/library review. The stable schema intent is:

```json
{
  "owner_id": "...",
  "credential": {
    "version": 2,
    "scheme": "<approved-kdf-or-os-backed>",
    "parameters": {},
    "salt": "<encoded-random-salt-if-applicable>",
    "verifier": "<encoded-verifier>",
    "credential_id": "<rotation-id>",
    "revoked": false
  }
}
```

Do not store the plaintext secret.

## Migration contract
1. V1 continues to authenticate only while migration is explicitly enabled.
2. A gated migration verifies the existing Owner credential before writing v2 config.
3. After successful v2 verification, v1 fallback is disabled.
4. Unknown version, revoked credential, malformed KDF parameters, or missing verifier => hard FAIL.
5. Rotation creates a new credential_id and invalidates the prior credential.
6. Rollback to an older credential record must be detectable by durable state or an independently protected checkpoint.

## Tests required before promotion
- correct v2 credential passes;
- wrong secret fails;
- malformed/unknown scheme fails closed;
- revoked credential fails;
- v1 migration requires valid existing Owner authentication;
- post-migration v1 fallback fails;
- rotation invalidates previous credential;
- read-only BrainReader/transport works with no mutation credential;
- config-path override remains blocked.

## Gate
Do not replace the active verifier until the implementation dependency and migration/rollback behavior have deterministic tests. This design does not claim real-person identity verification.
