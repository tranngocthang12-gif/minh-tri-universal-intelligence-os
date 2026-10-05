# MINH TRÍ — Independent Architecture Critic Report — ARCH-CRITIC-01

Review date: 2026-10-05
Review target: main @ 904e4f3b0bced1fcba760045a65041b80bcdf08d
Critic status: INDEPENDENT TASK REPORT / NOT VERIFIED
Critique reviewed: docs/critic/PROJECT_ARCHITECTURE_SELF_LEARNING_CRITIQUE_20261005.md from PR #226 branch review/architecture-self-learning-20261005-v1
Independence guard: LEARN-CRITIC-01 was not read before this report.
Mutation boundary: this report does not modify law, PROJECT_STATE, RECOVERY_MANIFEST, or merge any PR.

TASK_ID:
ARCH-CRITIC-01

VERDICT:
DEFECT_FOUND

TOP_MATERIAL_DEFECTS:
1. Canonical-state sprawl and duplicated current facts are now an operational defect. At reviewed main, PROJECT_STATE.json has 653 top-level keys, about 86 KB and 762 lines; RECOVERY_MANIFEST.json is about 46 KB and 430 lines; current Architecture is 544 lines. Runtime state, learning state, current/next checkpoints, gates, and historical proof summaries are repeated across multiple manually maintained surfaces. The evidence/liveness distinction is a good design, but update fan-out is too high.
2. Open PRs have become a second state machine. At review time there are 15 open PRs. Only #226, #223 and #221 are direct-to-main PRs based on the current main SHA. #222/#224/#225 are stacked on non-main parents. Nine direct-to-main PRs were opened from older main SHAs. Eight open PRs are currently mergeable=false. A successor seat must infer active/superseded/stacked/blocked state from PR topology because no authoritative machine task registry exists.
3. Persistent orchestration is specified but not implemented as a project-wide durable coordination primitive. Current main already contains docs/WORK_QUEUE_ORCHESTRATOR_MODEL_20261005.md with task states, dependency rules, non-overlap and successor recovery, and the Buddhist track contains one-active-MAIN/stale-as-candidate rules. But no machine-readable project task registry was found, and no project-wide assignment-generation/CAS fence was found. PR #215 attempts law/state integration for the persistent orchestrator but is still open and mergeable=false.
4. The GitHub/PC boundary is not clean enough. GitHub already carries the canonical continuity for most knowledge work, while current runtime liveness records maintenance OFFLINE, tunnel DOWN and Local Brain connector DOWN. Nevertheless the project-wide next checkpoint still prioritizes runtime restoration and autonomous research remains coupled to fresh-seat/current-liveness gates. PC/runtime should gate only work that intrinsically needs local secrets, desktop/filesystem state, persistent services, Local Brain transport, self-upgrade runtime, or empirical executor/telemetry.
5. Assurance and autonomy machinery have grown faster than demonstrated behavioral-learning value. Canonical state itself says PROPOSAL_GOVERNANCE_PIPELINE_NOT_AUTONOMOUS_BEHAVIOR_ADAPTATION and empirical validation remains unproven. The heavy controls are not useless, but they should live behind a risk boundary instead of burdening routine Work OS activity.

CLAIMS_SUPPORTED:
- Yes: the architecture is materially over-engineered relative to current proven Owner-visible learning value, especially on the daily Work OS path.
- Yes: the system is strong at evidence humility, provenance, branch protection, no-automatic-VERIFIED, and bounded mutation.
- Yes: GitHub is already sufficient as the durable knowledge-continuity brain for most non-PC-bound work. It is not sufficient as the entire execution runtime.
- Yes: current-state duplication materially increases drift and recovery cost.
- Yes: the PR backlog has become a parallel state machine outside PROJECT_STATE.
- Yes: behavioral self-learning is not yet proven; the canonical classification already says so.
- Yes: a Work OS / Autonomy Lab separation is directionally correct if both remain under one authority chain.
- Yes: a concrete task registry plus stale-writer fencing is the highest-value missing orchestration primitive.
- Yes: persistent-orchestrator law/state integration is incomplete because PR #215 is not merged.
- Yes: PR #193 represents the desired GitHub-primary/PC-optional simplification, but its current head is mergeable=false and its Security P0 workflow run concluded failure.

CLAIMS_OVERSTATED_OR_WRONG:
- The critique overstates absence of orchestrator design. Current main already contains the dynamic work-queue model with explicit task states, dependencies, non-overlap and successor-orchestrator recovery. What is missing is the durable machine registry and enforcement.
- The critique overstates the stale-writer gap if read globally. The Buddhist rotation protocol already defines one active MAIN writer and stale work as candidate-only; self-upgrade uses leases/generation lineage and pre-mutation checks; protected main requires PR plus the strict test gate. The defect is project-wide coordination fencing, not total absence of stale-writer thinking.
- “PC/Local Brain is optional” is only correct for most knowledge continuity. It is not optional for tasks requiring local secrets, private local files, desktop apps, Local Brain transport/write, persistent runtime, self-upgrade execution, or runtime attestation.
- “Research Adapter is a missing organ” is correct for a broad autonomous learner, but overstated for the ordinary Work OS. Supervised chat/tool research can continue without the autonomous Research Adapter.
- “2 heavy + 1 light/standby” is a reasonable scheduling heuristic, not yet an evidence-backed architectural invariant. Do not hard-code it as law without throughput telemetry.
- The strategic statement that security/assurance is “becoming the product” is plausible but not quantitatively proven because the project does not yet measure engineering time/cost versus Owner-visible outcome value.
- Work OS / Autonomy Lab must not become two canonical brains. If the split creates separate law/current-state authorities, it would worsen the exact split-brain risk it is meant to reduce.

MISSING_COUNTEREVIDENCE:
- Current main already has docs/WORK_QUEUE_ORCHESTRATOR_MODEL_20261005.md.
- Current main already has docs/learning/BUDDHIST_THOUGHT_CHAT_ROTATION_PROTOCOL_20261005.md with bounded recovery and one-active-MAIN semantics.
- GitHub main has PR-required strict test protection, which is a real canonical integration fence even though it is not a task-assignment fence.
- Self-upgrade already has lease IDs, generation IDs, authenticated handoff and parent-lease rechecks; these primitives should be reused conceptually rather than rebuilt everywhere.
- PROJECT_STATE deliberately separates historical proof from current liveness. The defect is size/duplication/manual fan-out, not the existence of historical evidence.
- The critique does not provide measured cost telemetry: no task-cycle time distribution, token/tool cost per output, recovery time, PR lead time, or quantified Owner-value delta. “Over-engineered” is therefore a strong architectural judgment, not a measured economic result.

MINIMUM_VIABLE_ARCHITECTURE:
Use one authority chain, not one giant runtime:

OWNER
-> normative laws
-> protected GitHub main
-> slim machine current state + one machine task registry
-> replaceable orchestrator/workers/critics
-> immutable result/evidence packets
-> PR + required CI integration

Minimum retained components:
1. Owner authority and stable normative law router.
2. One slim current-state file containing only current pointers, active workstreams/checkpoints, current runtime-liveness summary, safety mode, and open gates. Historical receipts stay in referenced evidence files, not copied into the current state.
3. One machine task registry as the sole truth for READY / ASSIGNED / IN_PROGRESS / REPORTED / REVIEWED / BLOCKED / DONE, dependencies, write scope and integration status.
4. Protected GitHub main with required CI. Chat is never canonical.
5. Source/provenance/uncertainty discipline and the rule that recorded does not mean VERIFIED.
6. Workers produce immutable result packets or PRs; workers do not own the canonical task registry.
7. A project-wide stale-writer fence using:
   - registry_revision or orchestrator_epoch;
   - per-task assignment_generation;
   - expected_main_sha / expected registry blob SHA;
   - declared write_scope;
   - stale results preserved as candidate-only, never silently promoted.
   GitHub's existing blob-SHA/update and PR-base semantics can supply much of the compare-and-swap behavior; a new distributed-lock subsystem is not required.
8. PC/Local Brain as an optional execution sidecar for PC-bound tasks, not the continuity authority.
9. Autonomy Lab as proposal-only experimental sidecar: research ingestion, trials, telemetry, self-upgrade, external critic/witness and runtime attestation may live there, but it has no direct path to silent Work OS canonical mutation.
10. Human-readable Architecture and Recovery views should be generated from, or automatically validated against, the machine state/registry rather than independently storing CURRENT/NEXT facts.

If the Owner PC/runtime is dead for one month:
- Still works: GitHub law/state/history, code/docs, PR review, task planning, source audits, supervised research/critique using non-PC tools, chat replacement, durable handoffs, and canonical continuity.
- Does not work: Local Brain connector/mirror/write, Desktop Commander/PC files and apps, DPAPI/local secrets operations, tunnel services, persistent local scheduler, live self-upgrade runtime, local runtime attestation, and any empirical trial executor/telemetry that depends on the PC.
Therefore GitHub is enough for most knowledge continuity, but not for all execution.

PR_BACKLOG_RECOMMENDATION:
1. Temporarily stop creating non-emergency architecture PRs until the integration queue is classified.
2. Create exactly one task/PR registry entry per open PR with ACTIVE / SUPERSEDED / SALVAGE / STACKED_WAIT / BLOCKED, owning TASK_ID, dependency, base SHA and intended disposition.
3. #177 is clearly stale relative to main A160 and should be reviewed for salvage then superseded/closed rather than treated as live state.
4. #168/#169/#170/#167 are likely substantially superseded by later integrated continuity/self-learning records; compare unique content first, salvage anything still unique, then supersede/close. Do not close blindly.
5. #193 and #215 contain strategically useful ideas but are stale/conflicted branches. Do not merge them as-is. Re-express the surviving minimum changes in small fresh PRs from current main if the Owner chooses those directions.
6. Treat #221 -> #222 -> #224 -> #225 as one serialized dependency chain. Integrate/rebase sequentially or consolidate future continuation; do not let the stack become durable current state.
7. #216/#218 may contain distinct audit/planning material; salvage/rebase unique content rather than allowing them to remain indefinitely stale.
8. #223 and #226 are based on the reviewed current main and are clean candidates for normal review.
No PR was merged by this task.

ORCHESTRATOR_RECOMMENDATION:
The current orchestrator doctrine is good enough for supervised/manual operation but not enough for durable multi-worker orchestration.

Keep the orchestrator logically persistent but make each chat generation stateless:
- fresh-read slim PROJECT_STATE + TASK_REGISTRY;
- acquire/advance one orchestrator_epoch or registry revision;
- assign a bounded task with assignment_generation + expected_main_sha + write_scope;
- worker writes only result artifact/branch;
- orchestrator reviews result and updates registry using compare-and-swap;
- stale generation cannot change task state or canonical routing;
- stale result remains reviewable candidate evidence.

Do not build an “immortal orchestrator process” just to preserve continuity. The durable registry is the orchestrator memory; the chat is a replaceable planner.

RISKS_OF_SIMPLIFICATION:
- Removing duplicate files without preserving immutable history could destroy auditability and recovery evidence.
- Treating PC as optional for every task could weaken secret handling, local-data boundaries, runtime safety and self-upgrade controls.
- Splitting Work OS and Autonomy Lab into separate law/state authorities would create a worse split-brain.
- Adding a task registry without retiring PR topology/checkpoint duplication as task truth would merely create a third state machine.
- Closing stale PRs before content-salvage review could discard unique findings.
- Risk-tiered assurance must not weaken HIGH/CRITICAL gates for autonomy-changing, security-sensitive or canonical-mutation work.
- A slim current state must retain pointers to historical evidence so simplification does not become amnesia.

FINAL_ADVICE:
The architecture should be simplified, but not by deleting its safety core.

For daily work, make MINH TRÍ a small GitHub-first Work OS:
Owner authority + stable law + protected main + slim current state + one task registry + replaceable workers + reviewed result packets.

Keep the PC/Local Brain/runtime machinery only as an execution sidecar for tasks that genuinely need it.

Keep the autonomy/self-learning/security machinery in an Autonomy Lab that can propose but cannot silently mutate canonical Work OS state.

The next architecture milestone should not add another assurance layer. It should close three loops:
1. PR backlog triage and removal of stale second-state-machine ambiguity.
2. A real machine task registry with project-wide stale-writer fencing.
3. Reduction of manually duplicated CURRENT/NEXT/runtime state, with generated/validated recovery views.

After that, prove one genuine historical lesson improves unseen work against compute-matched and placebo controls. One closed causal learning loop is more valuable than another layer of architecture.

This report finds material architecture defects, but it does not claim the project is unsafe or failed. The strongest existing safety/provenance primitives should be retained and moved out of the routine daily path when they are not needed.

DURABLE_LOCATION:
docs/critic/ARCH_CRITIC_01_REPORT_20261005.md on branch critic/arch-critic-01-20261005-v1; protected integration is proposed by the report PR and remains unmerged at task completion.

READY_FOR_NEXT_TASK:
YES
