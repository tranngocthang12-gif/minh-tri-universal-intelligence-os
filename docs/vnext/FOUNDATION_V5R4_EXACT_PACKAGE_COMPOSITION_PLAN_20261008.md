# MINH TRI — FOUNDATION V5R4 EXACT PACKAGE COMPOSITION PLAN — 2026-10-08

**CLASS:** F; **TYPE:** proposed merge/review execution plan, evidence-only, not Owner acceptance.
**Status:** DRAFT / NOT_FROZEN. A changed normative tree would invalidate earlier exact-head review.
**Owner instruction:** V4 Option A, keep #319 Draft/unmerged until AFTER Freeze and later controlled Class F reopen.

## Immutable identity ledger

| Object | Identifier | Role |
|---|---|---|
| Protected main at preflight | `d2640da0911940dad7ee2344e7bfa0d20c508bc2` | sole current canonical source; fresh-read before final gates |
| Original repair target | `9bd321410af0b1dff225eb6a5b8d77870698902e` | historical V3 supervised/Claude V4 rereview target |
| Exact substantive integrated target, PR #327 | `c3f7cbe97d68922c822177a3d7ed576a84800fba` | exact review target for fresh Claude+Grok V5R4 |
| Freeze candidate Foundation Law git blob | `2faac92eff36a314fa120a1edf52da697ea04912` | MUST be unchanged, excludes PR #319 amendments |
| Review packet V5R4 git blob | `c5bbd4a1aab8cb293f830bacaa976c35e57acf53` | same-packet input for both critics |
| PR #331 initial packet-only head | `3a8aad1b2df3d682bc4e8bbf2fd09697251064e9` | direct descendant of c3f7cbe; exactly one added packet file |
| Supervisor historical packet/result/receipt | `0489e40357877a66a75afbe33b1c62eb2d50b5bc` / `6067d59978864c292980f4b7765529980e00d52a` / `c48e094bbb6d7bb0a4228e8886e0cccc78c18a7c` | historical PASS for 9bd3214 only |
| Historical V4 rereview packet | `504b4cd4adb2b4e0f9c5300041d6706911c30302` | does NOT bind current c3f7cbe |
| Claude V4 Owner-chat intake | `b380c33aca49d24f48d02b3115ec77a4c618f6fe` | original bytes/provider authorship NOT independently authenticated; historical MATERIAL |
| Grok post-Owner-A Owner-chat intake | `3d48a23b18010edfdfe9f4b3b01439146b082dbc` | source bytes/provider authorship NOT independently authenticated; historical MATERIAL |
| CI on exact substantive head | Security P0 run `37770654628`: completed SUCCESS; required `test` and Python 3.10/3.11/3.12 SUCCESS | CI only, not independent review |
| CI on PR #331 packet-only head | Security P0 run `37770735667`: completed SUCCESS | CI for initial evidence branch head only, recheck whenever head changes |

PR #327 tree is **37 commits ahead of the protected-main preflight SHA** and modifies 32 files against main. It is an integrated repair+records candidate, NOT a thin governance overlay. The repair target is a strict ancestor. PR #331 is an evidence-bearing descendant and is the preferred single potential promotion route after every gate passes; PR #327 and sibling PRs are NOT additional merge steps.

## Required critics and unclosed material issues

Critic set = **two genuinely independent fresh seats, Claude and Grok**, working from the same V5R4 packet blob and exact substantive target `c3f7cbe...`. If either has a CRITICAL/HIGH/MEDIUM finding, stop promotion until material repair and a **new** exact-head review, or an explicit Owner-authorized rejection allowed by current law. No Builder/Architect self-acceptance.

Existing historical material findings:
- `FF-CLAUDE-V4-001` MEDIUM: Owner A PR #319 hold is a candidate, not yet protected-main canonical.
- `FF-CLAUDE-V4-007` MEDIUM elevated by Grok post-Owner-A: prior sibling topology had no unified final head. Integrated PR #327 is a candidate fix, not yet independently accepted.
- Other findings 002–006 were LOW historically; critics may elevate on evidence, never silently downgrade.

No fresh Claude or Grok V5R4 results have been archived as of this plan. Neither the authoring seat nor a GitHub Actions PASS is an independent critic.

## Allowed post-review evidence-only additions (no silent target mutation)

Keep the exact substantive target tree and Law blob fixed. On the **evidence branch only** (PR #331), the expected further additions may include:
1. `docs/vnext/red_team/FOUNDATION_V5R4_CLAUDE_REVIEW_20261008.json` and a receipt;
2. `docs/vnext/red_team/FOUNDATION_V5R4_GROK_REVIEW_20261008.json` and a receipt;
3. a bounded disposition/manifest that **quotes** rather than silently edits historic critic findings and lists review SHA binding;
4. an independent provenance check on earlier Owner-provided review contents, if available.

These are candidate evidence receipts only until Owner has reviewed them. Each new commit changes the Git tree SHA, so check required CI on the resulting **final PR head** before Owner exact-head acceptance. Reviewers must explicitly evaluate the allowlist and whether any append is truly evidence-only; do not automatically waive re-review when it changes interpretation or authority.

**Forbidden under evidence-only allowance:** change `state/bootstrap.json`, `state/current.yaml`, `state/tasks.yaml`, the Foundation Law router, Master Blueprint, original Owner decisions, handoffs, tests, eval scorers/proofs, or the fixed V5R4 packet. Any such change triggers a *new* substantive exact-head target, new CI and a new immutable review packet/review set. No current PR may silently incorporate PR #319 delegated role/merge powers.

## Promotion sequencing; no hidden Owner delegation

1. Fresh-read protected main and PR heads. Confirm exact blob SHAs, #319 Draft/unmerged, zero authority split.
2. Both fresh critics inspect exact substantive target `c3f7cbe...` and V5R4 packet `c5bbd4...`; preserve original results with verifiable receipts on PR #331 evidence branch, subject to review independence.
3. Resolve all material findings by repair and new exact-head reviews if needed. Validate entire final PR tree and strict evidence-only difference between reviewed target and proposed Owner package.
4. Run required CI on **final** PR #331 head and check that the required `test` context succeeds. Do not substitute CI from c3f7cbe for a later changed head.
5. Present the exact PR #331 final SHA, packet blob, complete Claude+Grok verdict set, Law blob, list of post-review evidence append files and their SHAs, unresolved LOW debt and final proposed acceptance statement for Owner. Owner acceptance is reserved; never infer from generic "tiếp" or "AUTO".
6. Once explicit SHA-bound Owner final acceptance exists, pass protected merge for **one** fully accepted candidate (preferred PR #331), never merge #322–#330 as separate sibling changes. Confirm protected-main SHA and every canonical pointer by fresh-read.
7. Declare Foundation `FROZEN` **only if** the Owner has expressly authorized the status transition and the appropriate protected-main state record has been merged/fresh-read. If it requires a later Class F canonicalization PR, run its gates and keep `NOT_FROZEN` until that is complete.

The old Foundation Closure execution delegation authorizes workflow only, not acceptance. Owner final acceptance must explicitly reconcile that history and enumerate the post-2026-10-07 ratification amendments.

## Honest limitations

- This plan is Builder/Architect-authored, not independently endorsed.
- The evidence branch is not protected-main canon.
- Authoring-seat receipts do not authenticate the external providers or the original chat byte sequences.
- Neither material finding is CLOSED by creating this plan or by GitHub mergeability.
