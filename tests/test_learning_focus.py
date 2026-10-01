import json
import tempfile
import unittest
from pathlib import Path

from minhtri.core import GateError, Ledger, current_focus, evolve, initial_state
from tests.support import ledger_apply, ledger_repair, write_owner_config


def cmd(command_type, **data):
    return {"type": command_type, "data": data}


class LearningFocus(unittest.TestCase):
    def setUp(self):
        self.state = initial_state()
        self.at = "2026-01-01T00:00:00Z"

    def apply(self, command_type, at=None, **data):
        self.state = evolve(self.state, cmd(command_type, **data), at or self.at)

    def domain_with_source(self, domain, source, kind="THIRD_PARTY"):
        self.apply("register_domain", id=domain, name=domain, risk_class="NORMAL", measurement_contract="Learning log only")
        self.apply("record_source", id=source, domain_id=domain, uri=f"https://example.invalid/{source}",
                   captured_at=self.at, kind=kind, rights_status="UNKNOWN")

    def focus(self, fid, domain, source, at=None):
        self.apply("set_learning_focus", at=at, id=fid, status="ACTIVE", domain_id=domain, source_id=source,
                   note="Why the Owner learns this", expected_lesson="Expected lesson", uncertainty="HIGH: one case")

    def test_state_without_focus_events_has_no_new_key(self):
        self.domain_with_source("alpha", "s1")
        self.assertNotIn("learning_focuses", self.state)
        self.assertIsNone(current_focus(self.state))

    def test_active_focus_records_untested_expectation(self):
        self.domain_with_source("alpha", "s1")
        self.focus("f1", "alpha", "s1")
        focus = current_focus(self.state)
        self.assertEqual(focus["id"], "f1")
        self.assertEqual(focus["expectation_status"], "UNTESTED_EXPECTATION")
        self.assertEqual(focus["started_at"], self.at)

    def test_domain_switch_supersedes_but_keeps_history(self):
        self.domain_with_source("alpha", "s1")
        self.focus("f1", "alpha", "s1")
        self.domain_with_source("beta", "s2")
        self.focus("f2", "beta", "s2", at="2026-01-02T00:00:00Z")
        self.assertEqual(current_focus(self.state)["id"], "f2")
        old = self.state["learning_focuses"]["f1"]
        self.assertEqual((old["status"], old["superseded_by"]), ("SUPERSEDED", "f2"))
        self.assertIn("s1", self.state["sources"])

    def test_stop_keeps_history_and_only_active_can_stop(self):
        self.domain_with_source("alpha", "s1")
        self.focus("f1", "alpha", "s1")
        self.apply("set_learning_focus", id="f1", status="STOPPED", reason="Owner changed plans")
        self.assertIsNone(current_focus(self.state))
        self.assertEqual(self.state["learning_focuses"]["f1"]["stop_reason"], "Owner changed plans")
        with self.assertRaises(GateError):
            self.apply("set_learning_focus", id="f1", status="STOPPED", reason="Again")

    def test_invalid_focus_commands_are_blocked(self):
        self.domain_with_source("alpha", "s1")
        self.domain_with_source("beta", "s2")
        with self.assertRaises(GateError):
            self.focus("f1", "alpha", "s2")  # cross-domain source
        with self.assertRaises(GateError):
            self.apply("set_learning_focus", id="f1", status="ACTIVE", domain_id="alpha", source_id="s1",
                       note="n", expected_lesson="e", uncertainty=" ")
        with self.assertRaises(GateError):
            self.apply("set_learning_focus", id="f1", status="PAUSED", reason="x")
        with self.assertRaises(GateError):
            self.apply("set_learning_focus", id="f1", status="STOPPED", reason="x", note="extra")
        with self.assertRaises(GateError):
            self.apply("set_learning_focus", id="nope", status="STOPPED", reason="x")

    def test_ledger_verify_and_snapshot_stay_consistent(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Ledger(Path(tmp) / "brain")
            config = write_owner_config(tmp)
            ledger.init()
            ledger_apply(ledger, cmd("register_domain", id="alpha", name="Alpha", risk_class="NORMAL", measurement_contract="Log"), config)
            ledger_apply(ledger, cmd("record_source", id="s1", domain_id="alpha", uri="https://example.invalid/a",
                             captured_at="2026-01-01T00:00:00Z", kind="THIRD_PARTY", rights_status="UNKNOWN"), config)
            before = json.loads(ledger.snapshot.read_text(encoding="utf-8"))
            self.assertNotIn("learning_focuses", before["state"])
            ledger_apply(ledger, cmd("set_learning_focus", id="f1", status="ACTIVE", domain_id="alpha", source_id="s1",
                             note="n", expected_lesson="e", uncertainty="u"), config)
            ledger_apply(ledger, cmd("set_learning_focus", id="f1", status="STOPPED", reason="done"), config)
            state, count, _ = ledger.verify()
            self.assertEqual(count, 4)
            self.assertEqual(state["learning_focuses"]["f1"]["status"], "STOPPED")
            ledger.snapshot.write_text("{}", encoding="utf-8")
            ledger_repair(ledger, config)
            self.assertEqual(ledger.verify()[0], state)


if __name__ == "__main__":
    unittest.main()
