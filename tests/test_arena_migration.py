import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from minhtri.arena_migration import (
    LEGACY_SCHEMA_PR2,
    LEGACY_SCHEMA_PR3,
    archive_legacy_arena,
    detect_legacy_schema,
    legacy_arena_evolve,
    legacy_initial_state,
    verify_legacy_arena,
)
from minhtri.core import GateError, Ledger


def command(command_type, **data):
    return {"type": command_type, "data": data}


class ArenaMigrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.expiry = (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()

    def build_legacy(self, schema: str) -> Path:
        home = self.root / schema
        reducer = lambda state, command, at: legacy_arena_evolve(schema, state, command, at)
        ledger = Ledger(home, reducer=reducer, initial=legacy_initial_state)
        ledger.init()

        for n in range(1, 4):
            ledger.apply(command(
                "register_participant",
                id=f"actor{n}",
                family_id=f"family{n}",
                model=f"legacy-model-{n}",
                version="legacy",
                adapter="MANUAL",
                capabilities=["PROPOSE", "CRITIQUE", "ADJUDICATE"],
            ))

        if schema == LEGACY_SCHEMA_PR2:
            open_data = dict(
                id="task1",
                goal_id="goal1",
                domain_id="media",
                core_head="1" * 64,
                constitution_sha256="2" * 64,
                brief="Legacy task",
                acceptance="Evidence and critique",
                allowed_evidence_ids=[],
                expires_at=self.expiry,
                risk_class="NORMAL",
                sensitivity="PUBLIC",
                mode="SHADOW",
                budget_cap=0,
            )
        else:
            open_data = dict(
                id="task1",
                goal_id="goal1",
                domain_id="media",
                runtime_state_head="3" * 64,
                brain_revision="a" * 40,
                brain_fingerprint="4" * 64,
                brief="Legacy task",
                acceptance="Evidence and critique",
                allowed_evidence_ids=[],
                expires_at=self.expiry,
                risk_class="NORMAL",
                sensitivity="PUBLIC",
                mode="SHADOW",
                budget_cap=0,
            )

        receipt = ledger.apply(command("open_task", **open_data))
        fp = receipt["state"]["tasks"]["task1"]["fingerprint"]
        ledger.apply(command(
            "submit_proposal",
            id="proposal1",
            task_id="task1",
            participant_id="actor1",
            task_fingerprint=fp,
            claim="Legacy proposal",
            alternative="Legacy alternative",
            uncertainties=["Legacy uncertainty"],
            evidence_ids=[],
            discriminating_test="Legacy test",
            method_ref="legacy-method",
        ))
        ledger.apply(command(
            "submit_critique",
            id="critique1",
            proposal_id="proposal1",
            participant_id="actor2",
            task_fingerprint=fp,
            verdict="CHALLENGE",
            reason="Legacy challenge",
            evidence_ids=[],
            test="Legacy counter-test",
        ))
        ledger.apply(command(
            "submit_adjudication",
            id="decision1",
            proposal_id="proposal1",
            participant_id="actor3",
            task_fingerprint=fp,
            critique_ids=["critique1"],
            outcome="HOLD",
            reason="Legacy hold",
        ))
        return home

    def test_detect_and_replay_pr2_legacy_ledger(self):
        home = self.build_legacy(LEGACY_SCHEMA_PR2)
        self.assertEqual(detect_legacy_schema(home), LEGACY_SCHEMA_PR2)
        report = verify_legacy_arena(home)
        self.assertEqual(report["status"], "LEGACY_ARENA_VERIFIED")
        self.assertEqual(report["source_schema"], LEGACY_SCHEMA_PR2)
        self.assertEqual(report["event_count"], 7)
        self.assertEqual(report["counts"]["participants"], 3)
        self.assertEqual(report["counts"]["tasks"], 1)
        self.assertEqual(report["counts"]["proposals"], 1)
        self.assertEqual(report["counts"]["critiques"], 1)
        self.assertEqual(report["counts"]["adjudications"], 1)
        self.assertEqual(report["active_tasks"], ["task1"])
        self.assertEqual(report["continuation_policy"], "REOPEN_ACTIVE_TASKS_UNDER_CURRENT_BRAIN")

    def test_detect_and_replay_pr3_legacy_ledger(self):
        home = self.build_legacy(LEGACY_SCHEMA_PR3)
        self.assertEqual(detect_legacy_schema(home), LEGACY_SCHEMA_PR3)
        report = verify_legacy_arena(home)
        self.assertEqual(report["source_schema"], LEGACY_SCHEMA_PR3)
        self.assertEqual(report["event_count"], 7)
        self.assertEqual(len(report["head"]), 64)
        self.assertEqual(len(report["state_digest"]), 64)

    def test_archive_is_non_destructive_and_replay_equivalent(self):
        home = self.build_legacy(LEGACY_SCHEMA_PR2)
        before_events = (home / "events.jsonl").read_bytes()
        before_state = (home / "state.json").read_bytes()
        archived = archive_legacy_arena(home, self.root / "archive")
        destination = Path(archived["archive_path"])

        self.assertEqual((home / "events.jsonl").read_bytes(), before_events)
        self.assertEqual((home / "state.json").read_bytes(), before_state)
        self.assertEqual((destination / "events.jsonl").read_bytes(), before_events)
        self.assertEqual((destination / "state.json").read_bytes(), before_state)

        manifest = json.loads((destination / "migration_manifest.json").read_text(encoding="utf-8"))
        replay = verify_legacy_arena(destination, LEGACY_SCHEMA_PR2)
        self.assertEqual(manifest["head"], replay["head"])
        self.assertEqual(manifest["state_digest"], replay["state_digest"])
        self.assertEqual(manifest["history_policy"], "ARCHIVE_READ_ONLY_DO_NOT_REWRITE")

    def test_current_law_ack_reducer_cannot_silently_replay_legacy_history(self):
        home = self.build_legacy(LEGACY_SCHEMA_PR3)
        from minhtri.arena import arena_evolve, initial_arena_state

        with self.assertRaises(GateError):
            Ledger(home, reducer=arena_evolve, initial=initial_arena_state).replay()

    def test_unknown_or_current_generation_is_not_migrated_as_legacy(self):
        home = self.root / "current"
        home.mkdir()
        event = {
            "seq": 1,
            "prev": "0" * 64,
            "at": datetime.now(timezone.utc).isoformat(),
            "command": {
                "type": "open_task",
                "data": {
                    "id": "task1",
                    "architecture_law_sha256": "1" * 64,
                    "bootstrap_sha256": "2" * 64,
                },
            },
        }
        from minhtri.core import digest
        body = {k: event[k] for k in ("seq", "prev", "at", "command")}
        event["hash"] = digest(body)
        (home / "events.jsonl").write_text(json.dumps(event) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(GateError, "current law-acknowledgement generation"):
            detect_legacy_schema(home)


if __name__ == "__main__":
    unittest.main()
