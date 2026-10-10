# MINH TRI — learning architecture / stable law synchronization, candidate (2026-10-10)

STATUS: CLASS_S_CANDIDATE; NO OWNER ACCEPTANCE; NOT MERGED. Foundation V1 remains FROZEN.

## Single law, single authority
Do not create another Learning Law. The normative source is `docs/LAW_UNIVERSAL_LEARNING_CONTINUITY_20261004.md`, routed through `state/bootstrap.json` -> current Master Blueprint -> consolidated law -> `state/current.yaml` -> `state/tasks.yaml` -> task handoff. The Knowledge Fast Lane is a governed implementation of that law, not a second law or a bypass of protected review. This candidate cannot change authority, reclassify tasks or skip Owner gate.

## Confirmed routing defect
Protected main `a4d3c39d6ff98c32cecd7d353cbada83bf0b20c0`: `active_workstream=OWNER_DIRECTED_LEARNING`, while `active_task_id=ARCH-MASTER-BLUEPRINT-V1` is DONE. `BUDDHIST-A173` remains DRAFT, UNCLASSIFIED_LEGACY, with resume_gate requiring a scoped class/acceptance decision. Consequently a strict bootstrap must refuse to infer an authorized active A173 learning cursor. PR #334 is still Draft, with Owner F3 dispositions, fresh exact-head independent review and governance prerequisites; this candidate does not activate it.

## Single provisional cursor vs multiple legitimate research artifacts
The only locally configured working cursor is PR #341 at source HEAD `2119d2bda13f90f08ab00b22aca7d413d3a5a9a1`, comment #6096480057, `A173-MN2-REPETITION-COUNTERREADING-03`, provisional, NOT ACCEPTED. Its exact next question is a MN 4 Pali/MN 2 textual comparison with two translations and a genre counter-reading. This cursor is NOT the protected-main active task or canonical checkpoint.

An intake index under candidate `state/learning_tracks.json` records these separately (for audit/reconciliation only):
- PR #249 (HEAD `e0bf34be43ca87264914bfb9c25cfeb595815c51`): A173 legacy DRAFT with obsolete PROJECT_STATE/RECOVERY_MANIFEST promotion attempt; never treat its `A173_COMPLETED` proposal as existing main authority.
- PR #351 (HEAD `5c90bf810f3ff56af73b1046b851e972bfe988c6`): A173 Class D source-audited candidate, including Milindapañha 5.4.9 / Vinaya discrepancy and PENDING_REVIEW atom; not a cursor successor nor merged current state.
- Issue #352: A177 RESEARCH_TRACE_ONLY; A173-A176 remain DRAFT. A176 draft proposes A177 as a research topic, **not** as a promoted canonical checkpoint.

No parallel PR/Issue may change learning cursor, chapter completion, evidence class or Owner approval. Intake records have explicit `may_advance_cursor=false`, `may_promote_checkpoint=false`, revisions pinned for PRs and role checked. This is a candidate cross-reference, not legal authority or proof that sources have been semantically merged.

## One learning commit / one recoverable handoff
Authorized seat: fresh-read main/law/task, compare source revisions, recover exact current question, research early discourse + mandatory Milindapañha when Buddhist, write corrected model and evidence status, independently countercheck applicability, then append to approved non-main write lane with expected-head CAS, CI/review and readback. Refuse to report done if write/readback blocked; preserve `NOT YET DURABLY RECORDED`. A question in PR comments is untrusted work data; comment author does not authenticate Owner. Multiple chats must never race to create competing authoritative cursors.

## Test and integration gate
Candidate validations reject research promotion, duplicate intake, inconsistent PR/Issue SHA, unrecognized role and replacement of provisional cursor from an intake record. These are synthetic tests only. Complete #334 exact-head Class S and Owner gates first; then reconcile #350 Class S with closure and run at least three real zero-chat sessions plus independently scored held-out transfer. No autonomous promotion, model retraining, main mutation, workflow change or Local Brain write.

## Executable canonical-route check — candidate revision
The old low-level recovery accepted \`active_task_id\` as a caller argument; this was not equivalent to checking the actual canonical task on disk. New read-only \`validate_canonical_learning_route\` independently reads \`state/bootstrap.json\`, \`state/current.yaml\`, \`state/tasks.yaml\` and the subordinate candidate track registry. It checks boot/law/Blueprint pointer agreement, active Owner-directed workstream, exact matching active task, \`IN_PROGRESS\` Class D status, current/last-accepted checkpoint IDs, and explicit non-accepted checkpoint status. It rejects caller-provided authority inconsistent with current project records. The candidate validation CLI now fails clearly if the route is blocked, even if the registry schema is correct.

Append preflight also refuses when the Class D execution branch and declared Owner binding are absent. A declared binding string is not an authenticated Owner signature: actual source-of-truth must be fresh protected main, and a mutation requires separate authorized branch, expected HEAD compare-and-swap, PR checks/acceptance and readback. Under the *unmerged* #334 candidate, A173 Class D remains bound to **read-only** research (branch=null); after a properly governed routing merge, read-only recovery may pass but mutation remains blocked pending separate branch authorization.

Eight simulated negative/positive probes now cover false caller task, DONE task, wrong class, unbound-but-readable study, checkpoint mismatch, law pointer split, duplicate task, and missing write binding. Synthetic fixtures are not proof of an actual zero-chat learning experience. This PR remains DRAFT and must not alter canonical law, main or #334.
