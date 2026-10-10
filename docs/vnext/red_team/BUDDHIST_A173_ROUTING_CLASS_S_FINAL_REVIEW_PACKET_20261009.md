# MINH TRI — PR #334 Class S independent rereview packet

**Status:** BUILDER-PREPARED PACKET / NOT AN INDEPENDENT VERDICT / OWNER ACCEPTANCE PENDING.
**Scope:** canonical A173 recovery routing only, NOT A173 study completion, NOT Foundation reopen.
**Protected main baseline:** `a5ed9d8347a60b95503fe2e5de6b95fd8375eb76`.
**Review target:** live PR #334 HEAD at reviewer start. The final SHA and CI must be bound in PR comments AFTER the packet is committed; no self-referential head SHA is claimed inside this file.
**Reviewer independence:** Fresh different seat, without chat assumptions. Reviewer must read actual protected main, HEAD tree and all current PR diff files. If access is unavailable, verdict BLOCKED rather than inventing evidence.

## Source and authority route

1. `state/bootstrap.json` -> Master Blueprint -> Foundation Law -> Learning Continuity Law -> `state/current.yaml` -> `state/tasks.yaml`.
2. `docs/vnext/handoff/BUDDHIST_A173_ROUTING_CLASS_S_V1.md` is the Class S routing task's own NEXT ACTION, independent from the Class D teaching task.
3. `docs/learning/BUDDHIST_THOUGHT_A173_ACTIVE_HANDOFF_20261009.md` is the Class D active study NEXT ACTION.
4. Main's accepted A172: `docs/learning/BUDDHIST_THOUGHT_CHECKPOINT_A172_20261005.md`. Main's A173 DRAFT remains unaccepted. A174–A176 drafts dependent; legacy PR #249 audit and A173/A177 candidates are history only.
5. `docs/vnext/red_team/BUDDHIST_A173_ROUTING_CLASS_S_FINDINGS_DISPOSITION_20261009.md` summarizes Owner-chat Grok, Codex and Claude defect reports as builder intake only, NOT authenticated independent receipts.

## Changed-scope inventory

At this packet's preparation, Class S PR #334 affects:
- `state/current.yaml`
- `state/tasks.yaml`
- `tests/test_master_blueprint_v1.py`
- `tools/validate_continuity_handoff.py`
- `tests/test_continuity_handoff_core_v1.py`
- `docs/learning/BUDDHIST_THOUGHT_A173_ACTIVE_HANDOFF_20261009.md`
- `docs/vnext/handoff/BUDDHIST_A173_ROUTING_CLASS_S_V1.md`
- `docs/vnext/red_team/BUDDHIST_A173_ROUTING_CLASS_S_FINDINGS_DISPOSITION_20261009.md`
- This packet file itself.

**Reviewer must fetch the live diff:** subsequent files/commits may expand the scope; the list is not an alternative to reading the exact GitHub HEAD diff.

## Specific adversarial assertions to challenge

A. New active A173 branch is `null`; no handoff follows diverged legacy PR #249; main ancestry aligns with `base_sha`.
B. The Class S routing task is separately registered and requires different-seat review and OWNER acceptance, whereas BUDDHIST-A173 study stays Class D.
C. `state/current.yaml.next_checkpoint` == Class D active task `next_action` == its handoff `## NEXT ACTION`; separately, Class S task action == its own separate handoff.
D. Foundation status FROZEN, autonomous/background learning flags false, and PR #319 explicitly HOLD.
E. All referenced source checkpoints/drafts and historical audit salvage are accurately classified. No A173 completion/verification or fresh-seat recovery proof is falsely claimed.
F. Existing CI is synthetic validation, not independent receipt; critic must probe extra failures and historical counterexamples.
G. No implicit Owner Class S acceptance from instruction to *prioritize* or *finalize the review packet*. No protected merge before explicit exact-head Owner gate.

## Integrated audit P0 regression repair — exact final HEAD review

- The old FROZEN/DONE exception in the live continuity validator is removed; active task MUST have an active status, recognized change class and non-builder acceptance authority.
- The current NEXT ACTION is checked against the active task and the actual next-action line in the routed handoff; conflicting mirrors must fail closed.
- Isolated negative-control fixtures must reject the DONE Blueprint route, unclassified task, mismatched mirrors, mismatched handoff, unbound A173 legacy branch, and Builder self-approval. A valid A173 task IN_PROGRESS does NOT mean A173 checkpoint COMPLETED.
- The old test relying on the exact historical phrase "Gate 3 authorization-after-build" is replaced by a check of the actual Gate 3 status, recorded comment ID, eight provisional finding keys, and missing-original F3 risk.
- Candidate assertions no longer universally pin the active task, witness to null, or review flag NOT_GRANTED as a permanent future truth. A GitHub green CI does NOT supply a missing Owner approval.
- Review ALL live changed files. The continuity validator and tests are candidate Class S compliance checks under the existing Foundation; no Foundation authority or law has been reopened. Claude subsequently completed R2 and reported HR-01..HR-08 on old HEAD 9aed814; old Grok verdict is for the earlier HEAD and neither is an independent final-head approval.
- Only final exact-head CI, fresh different-seat critique, per-key Owner dispositions and separate exact-head Class S decision permit protected integration. Foundation stays FROZEN; PC ledger remains unwritten.

## HR-01..HR-08 scoped anti-forgery and truthful-study guards

- **Phase-bound candidate**: routing task IN_PROGRESS; candidate_gate_phase PRE_MERGE_UNACCEPTED_SNAPSHOT; Owner status NOT_GRANTED. Forged GRANTED/DONE, witness or changed phase must FAIL. Genuine later Owner acceptance is a separate authenticated exact-head receipt; separate protected Class S closure after post-merge independent recovery requires a different reviewed state transition.
- Owner-directed learning must route to an active Class D study task. This study task has OWNER as recorded approver and a distinct non-Owner holder. No delegated approver is authorized by this candidate; a future Owner delegation must be reviewed and recorded, never inferred from arbitrary text.
- A173 study task IN_PROGRESS does not imply checkpoint COMPLETED: machine state and handoff explicitly bind A172 accepted, A173 NOT_CURRENT, no accepted A173 receipt. Structured status and receipts remain authoritative; the validator rejects bounded known completion-prose contradictions and duplicate CHECKPOINT_ACCEPTANCE lines, but is not a comprehensive natural-language verifier. An A173 execution branch still needs separate Owner Class D authorization.
- PR #341/#336/#345 are unaccepted study candidates. Updated Class S handoff now has TASK_ID and NOT DONE.
- Static tests **cannot authenticate an actual GitHub account's identity**, prove missing F3 originals, or substitute for different-seat review and protected merge. An independent critic should deliberately challenge combined text+structured edits and actor-impersonation, and report any novel bypass.
- HR-05 Class S-vs-Class F concern is explicitly OPEN for competent independent and Owner review. If a proposed change would alter Foundation law or powers, stop for separate Class F authorization; this candidate does not assert Foundation V2 or thaw.

## Machine evidence required

- PR head and base SHAs fresh-read live.
- GitHub comparison ancestry (merge-base and ahead/behind).
- GitHub Actions exact-head run, every job conclusion, with failures disclosed.
- `test_master_blueprint_v1.py` and full state/task law checks under exact HEAD.
- Fresh-zero-chat route exercise independent of builder fixture, with explicit pass/fail and source locators.

## Reviewer output contract

Return JSON containing `reviewer`, `independence`, `pr`, `verified_head_sha`, `verified_base_sha`, `changed_files`, `checks`, `findings` (severity and precise evidence references), `limitations`, and `verdict` (`NO_MATERIAL_DEFECT_FOUND`, `MATERIAL_DEFECTS_FOUND`, or `BLOCKED`).

A reviewer may flag a material issue on the final HEAD. Builder repair then invalidates older-head acceptance. Only an explicitly distinct Owner acceptance and protected merge can make the Class S routing canonical.

**CURRENT GATE:** INDEPENDENT_EXACT_HEAD_REREVIEW_PENDING. OWNER_ACCEPTANCE_NOT_GRANTED. MAIN_UNCHANGED. MACHINE_LEDGER_NOT_WRITTEN.
