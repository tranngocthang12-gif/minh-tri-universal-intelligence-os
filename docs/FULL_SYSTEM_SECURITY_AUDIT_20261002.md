# FULL SYSTEM SECURITY AUDIT — 2026-10-02

**Status:** CURRENT AUDIT / NO AUTOMATIC REMEDIATION / NO P0 BYPASS FOUND IN REVIEWED MUTATION BOUNDARY
**Reviewed canonical main:** `2a4ca4003ba2f58bce4a206e5ed8898347b047b2`
**Also reviewed:** PR #80 head `212bc778d006d36b9f2b9b603acaaf25d6d7003f` (CI success, not canonical at audit time)

## Executive result

No fresh direct mutation bypass was found in the reviewed Owner-gated `Ledger.apply` / repair path.
The system remains fail-closed for durable writes.

However, several P1 risks remain open:

1. secure MCP tunnel persistence is failing in live operation;
2. Owner-PC runtime config currently lacks a usable credential record;
3. Research Adapter gate is still caller-controlled in the autonomy API surface;
4. fresh-seat proof in PR #80 still relies partly on self-attested metadata;
5. external witness authority is not independent from full Owner-PC compromise;
6. detailed GitHub branch-protection configuration was not independently re-read in this audit.

## P1 — tunnel persistence failure is live, not hypothetical

During this audit both canonical connector calls failed with:
`Tunnel-client has not been seen for 300 seconds`.

Owner-PC process inspection also found no running `tunnel-client.exe`.
The staged supervisor exists and passed a local smoke test, but is not active for the current tunnel session.

Therefore:
- `secure_mcp_tunnel_persistence = NOT_PROVEN` remains correct;
- connector availability is currently transient;
- fresh-seat E2E must not be promoted while the tunnel is not persistently supervised.

## P1 — Owner write plane is fail-closed but operationally unavailable

Current `src/minhtri/owner.py` supports credential v2:
- PBKDF2-SHA256;
- per-credential salt;
- minimum iteration count;
- revocation flag;
- constant-time verifier comparison;
- v1/v2 dual-config rejection.

But the Owner-PC runtime `config/owner.json` currently exposes only `owner_id` and no v1 or v2 credential field.
Under current code this should fail closed on mutation.

This is safer than a bypass, but the write plane is not operationally healthy.
The machine config must be repaired/migrated through the Owner gate before write workflows are considered available.

## P1 — credential documentation drift

Some security/design documents still state that v2 is design-only or that raw SHA-256 is the active design.
Canonical code and `PROJECT_STATE.json` show v2 verifier support is already merged while v1 compatibility remains active.

Risk: a fresh seat may reason from stale docs and make the wrong security decision.

## P1 — Research Adapter gate is not bound to canonical state

`src/minhtri/autonomy.py` accepts a `research_gate` value from its caller.
If a future caller supplies `OPEN_AFTER_FRESH_SEAT_PASS` together with a research adapter, the module itself does not independently verify `PROJECT_STATE.json` or a fresh-seat proof.

Current CLI wiring has no research adapter and therefore still fails closed in practice.
Before Internet research is activated, the gate should be derived from canonical state/proof rather than a caller-supplied string.

## P1 — fresh-seat proof is only partially independent

PR #80 adds useful fail-closed consistency checks and exact toolset checks.
However, `separate_chat_ui=true` and `prompt_seeded_expected_values=false` are self-attested fields in the evidence record.

The validator can prove that supplied runtime reads agree, but cannot by itself cryptographically prove:
- the chat was genuinely separate;
- the prompt was not seeded;
- the record was not fabricated by the same authority.

PR #80 therefore improves consistency but should not be treated as a strong independent identity/seat proof without an external challenge/nonce or connector-origin evidence.

## P1 — witness independence remains incomplete

Anchor/witness verification code is substantially hardened:
- anchor digest verification;
- historical-prefix checking;
- chain continuity;
- UTC/monotonic timestamp checks;
- external witness receipt validation.

But the current witness authority is still reachable from the Owner-PC/GitHub authority domain.
A full device/account compromise can still affect both the ledger writer and present witness authority.

Do not claim full-device-compromise resistance.

## P1/P2 — GitHub governance verification is incomplete in this audit

Repository metadata confirms:
- default branch `main`;
- current connector has admin permission;
- PR-based workflows are active;
- PR #80 exact-head CI completed successfully.

The available connector does not expose branch-protection/ruleset detail, so this audit cannot independently confirm:
- required-check strictness;
- review requirements;
- bypass actors;
- force-push/deletion rules.

Canonical state says strict PR + test enforcement, but this audit marks the detailed settings UNKNOWN rather than re-asserting them.

## P2 — CI and supply-chain controls are narrow

Current workflow:
- runs only Python 3.11;
- runs unit tests only;
- has read-only Actions contents permission.

Gaps:
- no supported-version matrix despite `requires-python >=3.10`;
- no lint/type/static security scan;
- no reproducible dependency lock/hashes;
- `setuptools>=68` is open-ended;
- `mcp>=2,<3` is not exact-pinned;
- GitHub actions use version tags rather than immutable commit SHAs.

These are supply-chain/reproducibility risks, not observed compromise.

## P2 — secret detection is useful but basic

Repository CI scans common plaintext patterns.
A runtime-PC scan of project custom scripts/files found no matching committed/plaintext secret patterns.

Limits:
- encoded/split secrets may evade regex;
- third-party package files can cause false positives;
- pattern scanning is not a full secret-management system.

## Controls that are currently strong

- mutation authentication is inside `Ledger.apply` / repair boundary;
- fixed Owner config path blocks caller-selected authority files;
- v2 credential verifier exists and fails closed on malformed/revoked credentials;
- read-only MCP exposes exactly two brain tools;
- no shell/filesystem/mutation tool is exposed through the canonical brain connector;
- Brain HTTP binds loopback only and requires bearer auth;
- autonomy runtime is proposal-only with `write_capability=false`;
- no automatic VERIFIED or automatic trial activation;
- Research Adapter remains blocked on canonical state;
- no obvious `shell=True`, `os.system`, `eval`, or `exec` use found in the reviewed repo paths;
- staged supervisor uses `shell=False` and bounded restart backoff.

## Priority remediation order

1. activate and observe the tunnel supervisor; prove restart persistence;
2. repair/migrate Owner-PC credential config to v2 and disable v1 fallback after successful migration;
3. bind Research Adapter enablement to canonical state/proof, not a caller argument;
4. strengthen fresh-seat evidence with challenge/nonce or connector-origin proof;
5. establish a witness under truly independent write authority;
6. independently verify GitHub branch protection/rulesets;
7. broaden CI and pin/lock dependencies;
8. synchronize stale security docs with current v2 implementation.

## Bottom line

The system is materially safer than the earlier baseline and still fails closed on durable writes.
The largest current weakness is no longer an obvious write bypass. It is the gap between logical security and operational proof: tunnel persistence, credential deployment, independent witness/seat evidence, and governance/supply-chain verification.
