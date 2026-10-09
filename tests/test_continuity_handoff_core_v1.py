import contextlib
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import mock
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ContinuityHandoffCoreV1Tests(unittest.TestCase):
    def load_json(self, rel):
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_active_task_is_explicit_and_registered(self):
        current = self.load_json("state/current.yaml")
        registry = self.load_json("state/tasks.yaml")
        by_id = {t["task_id"]: t for t in registry["tasks"]}
        self.assertIn(current["active_task_id"], by_id)
        active = by_id[current["active_task_id"]]
        self.assertIn(active["status"], {"IN_PROGRESS", "BLOCKED", "REPORTED", "REVIEWED_REVISE", "STALE"})
        self.assertIn(active["change_class"], {"F", "S", "D", "O"})
        self.assertTrue(active.get("acceptance_authority"))

    def test_active_task_has_machine_checkable_handoff_contract(self):
        registry = self.load_json("state/tasks.yaml")
        task = next(t for t in registry["tasks"] if t["task_id"] == "ARCH-VNEXT-CONTINUITY-HANDOFF-CORE-V1")
        for field in ["scope", "base_sha", "result_ref", "handoff_ref", "next_action", "blocker"]:
            self.assertIn(field, task)
        self.assertEqual(task["status"], "DONE")
        self.assertIsNone(task["blocker"])
        self.assertTrue((ROOT / task["handoff_ref"]).exists())

    def test_handoff_task_id_matches_current_active_task(self):
        current = self.load_json("state/current.yaml")
        registry = self.load_json("state/tasks.yaml")
        task = next(t for t in registry["tasks"] if t["task_id"] == current["active_task_id"])
        text = (ROOT / task["handoff_ref"]).read_text(encoding="utf-8")
        self.assertIn(f"**TASK_ID:** {current['active_task_id']}", text)
        for heading in ["## DONE", "## NOT DONE", "## NEXT ACTION", "## REQUIRED GATES"]:
            self.assertIn(heading, text)

    def test_recovery_entrypoint_is_single_bounded_route(self):
        text = (ROOT / "docs" / "vnext" / "continuity" / "RECOVERY_ENTRYPOINT_V1.md").read_text(encoding="utf-8")
        for token in ["PROJECT_STATE.json", "law_index_catalog", "state/current.yaml", "state/tasks.yaml", "active_task_id", "handoff_ref", "next_action"]:
            self.assertIn(token, text)
        self.assertNotIn("Local Brain is canonical", text)

    def test_validator_passes_repository_candidate(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "validate_continuity_handoff.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("CONTINUITY_HANDOFF_CORE_V1_PASS", proc.stdout)

    def _run_isolated_validator(self, mutate):
        spec = importlib.util.spec_from_file_location(
            "minhtri_continuity_candidate_validator", ROOT / "tools" / "validate_continuity_handoff.py"
        )
        validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validator)
        current = self.load_json("state/current.yaml")
        registry = self.load_json("state/tasks.yaml")
        active = next(t for t in registry["tasks"] if t["task_id"] == current["active_task_id"])

        with tempfile.TemporaryDirectory() as folder:
            fixture_root = Path(folder)
            paths = {
                "state/current.yaml", "state/tasks.yaml",
                "docs/vnext/continuity/RECOVERY_ENTRYPOINT_V1.md",
                current["current_architecture"], current["role_bootstrap"], active["handoff_ref"],
            }
            for rel in paths:
                target = fixture_root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / rel, target)
            mutate(current, active, fixture_root)
            (fixture_root / "state/current.yaml").write_text(
                json.dumps(current, ensure_ascii=False), encoding="utf-8"
            )
            (fixture_root / "state/tasks.yaml").write_text(
                json.dumps(registry, ensure_ascii=False), encoding="utf-8"
            )
            output = io.StringIO()
            with mock.patch.object(validator, "ROOT", fixture_root), contextlib.redirect_stdout(output):
                code = validator.main()
            return code, output.getvalue()

    def test_validator_rejects_six_false_routes_and_accepts_bounded_route(self):
        ok, details = self._run_isolated_validator(lambda *_: None)
        self.assertEqual(ok, 0, details)

        def damage_handoff(current, active, fixture_root):
            file = fixture_root / active["handoff_ref"]
            source = file.read_text(encoding="utf-8")
            old = "## NEXT ACTION\n" + active["next_action"]
            self.assertIn(old, source)
            file.write_text(source.replace(old, "## NEXT ACTION\nCORRUPT ACTION", 1), encoding="utf-8")

        failures = [
            ("DONE task", lambda c, t, r: t.__setitem__("status", "DONE"),
             "active task status is not active: DONE"),
            ("old Blueprint route", lambda c, t, r: c.__setitem__("active_task_id", "ARCH-MASTER-BLUEPRINT-V1"),
             "active task status is not active: DONE"),
            ("unclassified route", lambda c, t, r: t.__setitem__("change_class", "UNCLASSIFIED_LEGACY"),
             "active task change_class is not authorized"),
            ("current/task divergence", lambda c, t, r: c.__setitem__("next_checkpoint", "CORRUPT ACTION"),
             "current.next_checkpoint does not match active task.next_action"),
            ("handoff divergence", damage_handoff,
             "active handoff NEXT ACTION does not match task.next_action"),
            ("unbound legacy branch", lambda c, t, r: t.__setitem__("branch", "learning/buddhist-a173-20261005-2205"),
             "active A173 has an execution branch but is marked unbound"),
            ("builder self-approval", lambda c, t, r: t.__setitem__("acceptance_authority", "Builder"),
             "active task acceptance_authority is missing or self-approving"),
        ]
        for name, mutate, expected in failures:
            with self.subTest(case=name):
                code, details = self._run_isolated_validator(mutate)
                self.assertEqual(code, 1, details)
                self.assertIn(expected, details)

    def test_zero_chat_packet_excludes_gold(self):
        packet = self.load_json("eval/recovery/v1/packet.json")
        self.assertTrue(packet["gold_excluded"])
        self.assertNotIn("eval/recovery/v1/gold.json", packet["canonical_inputs"])
        self.assertEqual(packet["questions_ref"], "eval/recovery/v1/questions.json")
        self.assertTrue(packet["authoring_seat_must_not_self_grade"])

    def test_gold_preserves_unproven_truth_boundary(self):
        gold = self.load_json("eval/recovery/v1/gold.json")
        forbidden = gold["required_facts"]["forbidden_claims"]
        self.assertIn("Core v1 COMPLETE before fresh-seat PASS", forbidden)
        self.assertIn("autonomous learning proven", forbidden)

    def test_blocked_architecture_task_has_continuation_metadata(self):
        registry = self.load_json("state/tasks.yaml")
        task = next(t for t in registry["tasks"] if t["task_id"] == "ARCH-VNEXT-PHASE4-GRADED-RUN")
        self.assertEqual(task["status"], "STALE")
        self.assertEqual(task.get("superseded_by"), "ARCH-RETRIEVAL-APPLICATION-PROOF-V1")
        self.assertTrue(task.get("handoff_ref"))
        self.assertTrue(task.get("next_action"))


if __name__ == "__main__":
    unittest.main()
