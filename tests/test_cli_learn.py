import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from minhtri.cli import main
from minhtri.core import Ledger


class CliLearn(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = str(Path(self.tmp.name) / "brain")
        self.run_cli("init")

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *argv, expect=0):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(["--home", self.home, *argv])
        self.assertEqual(code, expect, err.getvalue())
        return json.loads(out.getvalue() or err.getvalue())

    def test_learn_focus_unfocus_keeps_history_and_verifies(self):
        self.assertEqual(self.run_cli("focus")["focus"], "NO_ACTIVE_FOCUS")
        self.run_cli("learn", "--uri", "https://example.invalid/case", "--note", "x", expect=2)  # no domain yet
        self.assertEqual(Ledger(self.home).verify()[1], 0)  # blocked request appended nothing
        result = self.run_cli("learn", "--domain-id", "alpha", "--domain-name", "Alpha", "--id", "case-one",
                              "--uri", "https://example.invalid/case", "--text", "Fictional case",
                              "--note", "Why", "--expected-lesson", "Lesson", "--uncertainty", "High")
        self.assertEqual((result["status"], result["events_appended"], result["event_count"]), ("FOCUS_SET", 4, 4))
        state = Ledger(self.home).verify()[0]
        self.assertEqual(state["sources"]["case-one-src"]["kind"], "THIRD_PARTY")
        self.assertEqual(state["sources"]["case-one-src"]["rights_status"], "UNKNOWN")
        self.assertEqual(state["evidence"]["case-one-ev"]["verification"], "DECLARED_UNVERIFIED")
        self.assertEqual(self.run_cli("focus")["focus"]["id"], "case-one")
        stopped = self.run_cli("unfocus", "--reason", "Done for now")
        self.assertEqual(stopped["focus"]["status"], "STOPPED")
        self.assertEqual(self.run_cli("focus")["focus"], "NO_ACTIVE_FOCUS")
        self.run_cli("unfocus", expect=2)
        state, count, _ = Ledger(self.home).verify()
        self.assertEqual(count, 5)
        self.assertIn("case-one", state["learning_focuses"])
        self.assertIn("case-one-src", state["sources"])

    def test_domain_switch_uses_same_core_and_default_domain(self):
        self.run_cli("learn", "--domain-id", "alpha", "--domain-name", "Alpha", "--uri", "https://example.invalid/a",
                     "--note", "Today")
        second = self.run_cli("learn", "--uri", "https://example.invalid/a2", "--note", "Same domain by default")
        self.assertEqual(second["focus"]["domain_id"], "alpha")
        self.assertEqual(second["focus"]["expected_lesson"], "CHƯA NÊU")
        third = self.run_cli("learn", "--domain-id", "beta", "--domain-name", "Beta", "--uri", "https://example.invalid/b",
                             "--note", "New profession")
        state = Ledger(self.home).verify()[0]
        statuses = sorted(f["status"] for f in state["learning_focuses"].values())
        self.assertEqual(statuses, ["ACTIVE", "SUPERSEDED", "SUPERSEDED"])
        self.assertEqual(state["learning_focuses"][third["focus"]["id"]]["domain_id"], "beta")
        self.assertEqual(set(state["domains"]), {"alpha", "beta"})

    def test_unknown_domain_without_name_and_missing_input_are_blocked(self):
        self.run_cli("learn", "--domain-id", "alpha", "--uri", "https://example.invalid/a", "--note", "x", expect=2)
        self.run_cli("learn", "--domain-id", "alpha", "--domain-name", "Alpha", "--note", "x", expect=2)
        self.assertEqual(Ledger(self.home).verify()[1], 0)


if __name__ == "__main__":
    unittest.main()
