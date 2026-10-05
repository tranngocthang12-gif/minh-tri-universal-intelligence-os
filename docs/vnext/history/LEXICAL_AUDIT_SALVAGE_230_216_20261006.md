# MINH TRÍ — Lexical Audit Salvage #230 / #216 — 2026-10-06

**Status:** CANDIDATE SALVAGE / PENDING_REVIEW EVIDENCE  
**Base main:** `9c511472f80d0eb0b3cbbadd2d4942d5b913b13a`

## Purpose

Preserve unique Aṭṭhakavagga lexical audit work from stale pre-vNext PRs without silently promoting worker conclusions into ACTIVE knowledge.

## PR #216

Source:
- PR #216
- branch `audit/phat-atthaka-lex-01`
- head `6bc822b3361fbb9fa99622073c08cb369053f121`
- original path `docs/learning/PHAT_ATTHAKA_LEX_01_20261005.md`
- original blob `d442d90a88cbbf472a36d84d0e430c86bcb7e796`

Scope reported by the audit:
- `diṭṭhi`
- `sacca`
- bounded Aṭṭhakavagga lexical pass;
- text locations, morphology guardrails, overclaims, counter-readings, uncertainties;
- Milindapañha used only as later/paracanonical reasoning support.

Salvaged evidence:
`knowledge/buddhist/evidence/PHAT_ATTHAKA_LEX_01_PR216_SALVAGED_20261006.md`

Index atom:
`bud:atthaka:lex01:ditthi-sacca-audit-evidence`

Status:
`PENDING_REVIEW`

## PR #230

Source:
- PR #230
- branch `audit/phat-atthaka-lex-02-v2`
- head `a3a254c3b6598484b7165fb8bff86e5755f740fb`
- original path `docs/learning/PHAT_ATTHAKA_LEX_02_20261005.md`
- original blob `a1275558b11b3c89993daef8f015507892d552fb`

Scope reported by the audit:
- `saññā`
- `maññati`
- bounded Aṭṭhakavagga lexical pass;
- morphology traps, text locations, overclaims, counter-readings, uncertainties;
- explicitly not a papañca/nissaya audit;
- Milindapañha used only as later/paracanonical support.

Salvaged evidence:
`knowledge/buddhist/evidence/PHAT_ATTHAKA_LEX_02_PR230_SALVAGED_20261006.md`

Index atom:
`bud:atthaka:lex02:sanna-mannati-audit-evidence`

Status:
`PENDING_REVIEW`

## Why evidence, not ACTIVE claim

Both source audits explicitly state:
- bounded scope;
- not full concordance;
- not automatically verified;
- unresolved morphology/translation questions remain.

Therefore salvage means:
**preserve the audit and its provenance**, not certify every lexical conclusion.

Promotion requires a later Buddhist T1 review against:
- early-text source hierarchy;
- actual cited Pāli locations;
- relevant translation variants;
- morphology where material;
- current project claims that would depend on the audit.

## Closure rule

PR #216 and PR #230 must remain open through this salvage PR.

They may be closed only after:
1. this salvage PR merges;
2. raw evidence and evidence atoms are canonical;
3. their disposition is recorded as `SALVAGED_PENDING_T1_REVIEW`.

Closure does not mean their claims became VERIFIED.

## Next

After merge:
- T1 review these two evidence atoms;
- outcomes may be ACTIVE, NARROWED, DISPUTED, or remain PENDING_REVIEW;
- only then may active hubs depend on promoted claims.
