import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from minhtri.arena import ArenaService
from minhtri.bottleneck import BottleneckService
from minhtri.brain import BRAIN_ARTIFACTS
from minhtri.core import Ledger, canonical, digest, evolve, initial_state
from minhtri.epistemic import EpistemicService
from minhtri.tasking import TaskService
from minhtri.workcell import FourSeatWorkcellService


def command(command_type, **data):
    return {"type": command_type, "data": data}


def build_resolved_core(home: Path) -> None:
    events = [
        ("2026-01-01T00:00:00Z", command(
            "register_domain", id="media", name="Media", risk_class="NORMAL",
            measurement_contract="Observed outcome",
        )),
        ("2026-01-01T00:01:00Z", command(
            "register_provider", id="maker", name="Maker", kind="MODEL", family_id="family-maker",
        )),
        ("2026-01-01T00:02:00Z", command(
            "register_provider", id="critic", name="Critic", kind="MODEL", family_id="family-critic",
        )),
        ("2026-01-01T00:03:00Z", command(
            "register_provider", id="judge", name="Judge", kind="HUMAN", family_id="family-judge",
        )),
        ("2026-01-01T00:04:00Z", command(
            "open_goal", id="goal1", domain_id="media", objective="Find repeatable format fit",
            priority=5, owner_boundary="Shadow/read-only only",
        )),
        ("2026-01-01T00:05:00Z", command(
            "frame_problem", id="problem1", goal_id="goal1", reality="Format fit is uncertain",
            conditions=[{"description": "Audience response may vary", "role": "CONDITION", "status": "HYPOTHESIS"}],
            target="Resolve one bounded format-fit unknown", intervention="Read-only analysis",
            unknowns=["Repeatability"], control="Frozen method", influence="Audience mix",
            responsibility="Owner keeps authority", harm_checks=["No external action"],
        )),
        ("2026-01-01T00:06:00Z", command(
            "record_source", id="source1", domain_id="media", uri="internal://baseline",
            captured_at="2026-01-01T00:06:00Z", kind="FIRST_PARTY", rights_status="CLEAR",
        )),
        ("2026-01-01T00:07:00Z", command(
            "record_evidence", id="evidence1", domain_id="media", source_id="source1",
            statement="Observed baseline", observed_at="2026-01-01T00:07:00Z",
        )),
        ("2026-01-01T00:08:00Z", command(
            "register_procedure", id="procedure1", domain_id="media", provider_id="maker",
            version="1", method="Pre-register range",
        )),
        ("2026-01-01T00:09:00Z", command(
            "propose_claim", id="claim1", problem_id="problem1", provider_id="maker",
            statement="Rate will land between 5 and 7", evidence_ids=["evidence1"],
            alternative="Rate may fall outside range", falsifier="Observed rate outside range",
        )),
        ("2026-01-01T00:10:00Z", command(
            "register_prediction", id="prediction1", claim_id="claim1", procedure_id="procedure1",
            metric="rate", unit="percent", lower=5, upper=7,
            due_at="2026-01-03T00:00:00Z", resolution_method="First-party report",
        )),
        ("2026-01-02T00:00:00Z", command("freeze_prediction", prediction_id="prediction1")),
        ("2026-01-04T00:00:00Z", command(
            "record_source", id="source2", domain_id="media", uri="internal://outcome",
            captured_at="2026-01-04T00:00:00Z", kind="FIRST_PARTY", rights_status="CLEAR",
        )),
        ("2026-01-04T00:01:00Z", command(
            "record_evidence", id="outcome1", domain_id="media", source_id="source2",
            statement="Observed final rate", observed_at="2026-01-04T00:01:00Z",
            value=6.0, metric="rate",
        )),
        ("2026-01-05T00:00:00Z", command(
            "record_resolution", id="resolution1", prediction_id="prediction1", evidence_id="outcome1",
        )),
        ("2026-01-06T00:00:00Z", command(
            "review_claim", id="review1", claim_id="claim1", critic_provider_id="critic",
            verdict="HOLD", reason="One outcome is not enough for a reusable rule",
        )),
    ]
    home.mkdir(parents=True, exist_ok=True)
    state = initial_state()
    previous = "0" * 64
    lines = []
    for seq, (at, cmd) in enumerate(events, start=1):
        state = evolve(state, cmd, at)
        body = {"seq": seq, "prev": previous, "at": at, "command": cmd}
        event = {**body, "hash": digest(body)}
        previous = event["hash"]
        lines.append(canonical(event).decode("utf-8"))
    (home / "events.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (home / "state.json").write_bytes(canonical({
        "event_count": len(events), "head": previous, "state": state,
    }) + b"\n")


class ArchitectureContinuityEndToEndTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.home = root / "brain"
        self.brain_root = root / "repo"
        for index, relative in enumerate(BRAIN_ARTIFACTS, start=1):
            path = self.brain_root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"artifact-{index}\n", encoding="utf-8")
        build_resolved_core(self.home)
        self.revision = "a" * 40

    def test_goal_to_four_ai_to_handoff_to_recomputed_wait(self):
        core = Ledger(self.home)

        epistemic = EpistemicService(self.home)
        epistemic.init()
        epistemic.apply(command(
            "register_item", id="item1", domain_id="media", subject="Bounded format relation",
            kind="HYPOTHESIS", scope="Pilot only", origin_ref="claim1",
        ))
        epistemic.apply(command(
            "support_item", item_id="item1", evidence_ids=["evidence1"], support_note="Observed support",
        ))
        epistemic.apply(command(
            "demonstrate_understanding", item_id="item1",
            explanation="The pattern is conditional on this bounded setup.",
            distinction="It is not a universal causal law.",
            expected_pattern="A comparable observation should remain near the frozen range.",
            falsifier="Comparable outcomes repeatedly fall outside the range.",
        ))
        epistemic.apply(command("link_prediction", item_id="item1", prediction_id="prediction1"))
        epistemic.apply(command(
            "record_application", item_id="item1", mode="READ_ONLY_ANALYSIS",
            description="Use the frozen relation in a no-effect analysis.", artifact_refs=["artifact://analysis"],
        ))
        epistemic.apply(command(
            "record_validation", item_id="item1", resolution_id="resolution1",
            quality_note="First-party observed outcome.",
        ))
        epistemic.apply(command("link_critique", item_id="item1", review_id="review1"))
        epistemic.apply(command(
            "register_unknown", id="format-unknown", domain_id="media",
            question="Is this enough to close the bounded format dependency?", materiality="HIGH",
            owner_impact="Blocks the next learning unit",
        ))
        self.assertEqual(epistemic.item("item1")["effective_level"], "L6_SELF_CRITICISM")

        governor = BottleneckService(self.home)
        governor.init()
        governor.apply(command(
            "create_plan", id="plan1", goal_id="goal1", target_state="Bounded format gap resolved",
            success_conditions=["format-gap"], owner_constraints=["No publish", "No spend"],
        ))
        governor.apply(command(
            "add_component", id="format-gap", plan_id="plan1", name="Format gap",
            supports_conditions=["format-gap"], dependency_ids=[], target_role="BLOCKER",
            gap_kind="DECISION_GAP", owner_impact="HIGH", decision_sensitivity="DECISION_CHANGING",
            information_gain="HIGH", cost_band="LOW", time_band="SHORT", risk_band="LOW",
            reversibility="REVERSIBLE", epistemic_item_ids=["item1"], unknown_ids=["format-unknown"],
            allowed_evidence_ids=["evidence1"], leverage_hypothesis="Closing this gap unlocks the next unit.",
            disconfirming_condition="Closing it does not change the next decision.",
            next_unit_type="READ_ONLY_ANALYSIS", next_unit="Resolve the bounded format gap.",
            acceptance="Resolve the linked unknown with allowed evidence.",
        ))
        first = governor.recommend("plan1")
        self.assertEqual(first["decision"], "SELECT")
        self.assertEqual(first["component_id"], "format-gap")

        # Same frozen Arena task is acknowledged by four distinct provider families.
        arena = ArenaService(self.home, self.brain_root, self.revision)
        arena.init()
        for n in range(1, 5):
            arena.apply(command(
                "register_participant", id=f"actor{n}", family_id=f"family{n}",
                model=f"model-{n}", version="test", adapter="MANUAL",
                capabilities=["PROPOSE", "CRITIQUE", "ADJUDICATE"],
            ))
        expiry = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        arena_state = arena.apply(command(
            "open_task", id="arena-task", goal_id="goal1", brief="Blind review the selected gap",
            acceptance="Four independent contributions", allowed_evidence_ids=[], expires_at=expiry,
        ))["state"]
        arena_task = arena_state["tasks"]["arena-task"]
        for n in range(1, 5):
            arena.apply(command(
                "acknowledge_brain", id=f"arena-ack{n}", task_id="arena-task",
                participant_id=f"actor{n}", task_fingerprint=arena_task["fingerprint"],
                brain_revision=arena_task["brain_revision"], brain_fingerprint=arena_task["brain_fingerprint"],
                architecture_law_sha256=arena_task["architecture_law_sha256"],
                bootstrap_sha256=arena_task["bootstrap_sha256"],
            ))

        workcell = FourSeatWorkcellService(self.home, self.brain_root, self.revision)
        workcell.init()
        workcell.apply(command("open_session", id="session1", arena_task_id="arena-task"))
        for n, seat in enumerate(("S1", "S2", "S3", "S4"), start=1):
            workcell.apply(command(
                "assign_slot", session_id="session1", seat_id=seat, participant_id=f"actor{n}",
                family_id=f"family{n}", model=f"model-{n}", version="test",
            ))
            workcell.apply(command(
                "submit_blind", session_id="session1", seat_id=seat, participant_id=f"actor{n}",
                contribution_ref=f"artifact://blind-{seat}", contribution_sha256=str(n) * 64,
            ))
        workcell.apply(command("freeze_blind", session_id="session1"))
        workcell.apply(command("reveal", session_id="session1"))
        self.assertEqual(workcell.status("session1")["round_state"], "REVEALED")

        # Canonical work belongs to MINH TRI; worker B continues from worker A's durable handoff.
        tasks = TaskService(self.home, self.brain_root, self.revision)
        tasks.init()
        tasks.apply(command(
            "create_task", id="task1", goal_id="goal1", brief=first["task_candidate"]["brief"],
            acceptance=first["task_candidate"]["acceptance"], allowed_evidence_ids=["evidence1"],
        ))
        packet_a = tasks.packet("task1")
        tasks.apply(command(
            "acknowledge_continuation", id="continue-a", task_id="task1", worker_id="worker-a",
            continuation_fingerprint=packet_a["continuation"]["fingerprint"],
        ))
        tasks.apply(command(
            "acquire_lease", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expires_at=expiry, expected_checkpoint_seq=0, continuation_ack_id="continue-a",
        ))
        tasks.apply(command(
            "checkpoint_task", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expected_checkpoint_seq=0, summary="Four-seat review packet completed",
            artifact_refs=["artifact://blind-round"], evidence_ids=["evidence1"],
            next_action="Resolve the bounded unknown and recompute bottleneck",
        ))
        tasks.apply(command(
            "handoff_task", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expected_checkpoint_seq=1,
            decisions=["Four-seat blind round completed; no truth by vote."],
            unknowns=["format-unknown remains open until evidence-backed resolution is recorded."],
            blockers=[],
            verification=["Workcell reached REVEALED with four distinct families."],
            scope="R4.5 continuity integration fixture",
            limitations=["Structural fixture; no real-world effectiveness claim."],
        ))
        packet_b = tasks.packet("task1")
        self.assertEqual(
            packet_b["continuation"]["latest_handoff"]["next_action"],
            "Resolve the bounded unknown and recompute bottleneck",
        )
        tasks.apply(command(
            "acknowledge_continuation", id="continue-b", task_id="task1", worker_id="worker-b",
            continuation_fingerprint=packet_b["continuation"]["fingerprint"],
        ))
        tasks.apply(command(
            "acquire_lease", task_id="task1", worker_id="worker-b", lease_id="lease-b",
            expires_at=expiry, expected_checkpoint_seq=1, continuation_ack_id="continue-b",
        ))

        epistemic.apply(command(
            "resolve_unknown", unknown_id="format-unknown",
            answer="Resolved for this bounded fixture.", evidence_ids=["evidence1"],
        ))
        governor.apply(command(
            "set_component_status", component_id="format-gap", status="SATISFIED",
            reason="Linked unknown resolved with component-allowlisted evidence.", evidence_ids=["evidence1"],
        ))
        final = governor.recommend("plan1")
        self.assertEqual(final["decision"], "WAIT")
        self.assertEqual(final["reason"], "ALL_COMPONENTS_SATISFIED_OR_NOT_APPLICABLE")

        # All durable ledgers share the same writer lock and replay independently.
        project_locks = {
            str(core.project_lock),
            str(epistemic.ledger.project_lock),
            str(governor.ledger.project_lock),
            str(tasks.ledger.project_lock),
            str(arena.ledger.project_lock),
            str(workcell.ledger.project_lock),
        }
        self.assertEqual(len(project_locks), 1)
        for ledger in (core, epistemic.ledger, governor.ledger, tasks.ledger, arena.ledger, workcell.ledger):
            ledger.verify()


if __name__ == "__main__":
    unittest.main()
