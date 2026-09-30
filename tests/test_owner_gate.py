import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from minhtri.cli import main
from minhtri.core import Ledger

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


class OwnerGate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.home = str(root / "brain")
        self.config = root / "owner.json"
        self.config.write_text('{"owner_id": "test-owner"}', encoding="utf-8")
        self.missing = root / "missing.json"
        self.cli("init")
        self.cli("apply", str(EXAMPLES / "01-domain-youtube.json"))

    def tearDown(self):
        self.tmp.cleanup()

    def cli(self, *argv, config=None, owner=None, expect=0):
        prefix = ["--home", self.home]
        if config is not None:
            prefix += ["--owner-config", str(config)]
        if owner is not None:
            prefix += ["--owner-id", owner]
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main([*prefix, *argv])
        self.assertEqual(code, expect, err.getvalue() + out.getvalue())
        return json.loads(out.getvalue() or err.getvalue())

    def events(self):
        return Ledger(self.home).verify()[1]

    def learn_args(self):
        return ("learn", "--domain-id", "youtube", "--uri", "https://example.invalid/x", "--note", "why")

    def test_missing_config_fails_closed_and_writes_nothing(self):
        before = self.events()
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("MINHTRI_OWNER_CONFIG", None)
            result = self.cli(*self.learn_args(), config=self.missing, owner="test-owner", expect=2)
        self.assertEqual(result["reason"], "MISSING_OWNER_CONFIG")
        self.assertEqual(self.cli("unfocus", config=self.missing, owner="test-owner", expect=2)["reason"],
                         "MISSING_OWNER_CONFIG")
        self.assertEqual(self.events(), before)

    def test_owner_mismatch_and_missing_actor_are_blocked_without_ledger_write(self):
        before = self.events()
        self.assertEqual(self.cli(*self.learn_args(), config=self.config, owner="someone-else", expect=2)["reason"],
                         "OWNER_MISMATCH")
        self.assertEqual(self.cli(*self.learn_args(), config=self.config, expect=2)["reason"], "OWNER_ID_REQUIRED")
        self.assertEqual(self.events(), before)

    def test_correct_owner_can_learn_and_unfocus(self):
        result = self.cli(*self.learn_args(), config=self.config, owner="test-owner")
        self.assertEqual(result["status"], "FOCUS_SET")
        self.assertEqual(self.cli("unfocus", config=self.config, owner="test-owner")["status"], "FOCUS_STOPPED")
        self.assertEqual(self.cli("verify")["status"], "VALID")

    def test_env_var_config_path_is_used(self):
        with mock.patch.dict(os.environ, {"MINHTRI_OWNER_CONFIG": str(self.config)}):
            self.assertEqual(self.cli(*self.learn_args(), owner="test-owner")["status"], "FOCUS_SET")

    def test_apply_of_sensitive_types_is_gated_other_types_are_not(self):
        before = self.events()
        source = self.cli("apply", str(EXAMPLES / "05-owner-learn-social-case.json"), config=self.missing)
        self.assertEqual(source["status"], "APPLIED")  # record_source is not an Owner-only command
        focus = EXAMPLES / "06-owner-learn-youtube-mv-market.json"
        self.assertEqual(self.cli("apply", str(focus), config=self.missing, owner="test-owner", expect=2)["reason"],
                         "MISSING_OWNER_CONFIG")
        self.assertEqual(self.cli("apply", str(focus), config=self.config, owner="intruder", expect=2)["reason"],
                         "OWNER_MISMATCH")
        activation = Path(self.tmp.name) / "activate.json"
        activation.write_text(json.dumps({"type": "activate_trial_lesson", "data": {
            "lesson_id": "l1", "owner_ack": "HUMAN_OWNER_APPROVED", "scope": "x"}}), encoding="utf-8")
        self.assertEqual(self.cli("apply", str(activation), config=self.config, owner="intruder", expect=2)["reason"],
                         "OWNER_MISMATCH")
        self.assertEqual(self.events(), before + 1)
        self.assertEqual(self.cli("apply", str(focus), config=self.config, owner="test-owner")["status"], "APPLIED")

    def test_placeholder_or_malformed_config_is_rejected(self):
        placeholder = Path(self.tmp.name) / "placeholder.json"
        placeholder.write_text((Path(__file__).resolve().parent.parent / "config" / "owner.example.json")
                               .read_text(encoding="utf-8"), encoding="utf-8")
        self.assertEqual(self.cli(*self.learn_args(), config=placeholder, owner="doi-ten-owner", expect=2)["reason"],
                         "INVALID_OWNER_CONFIG")
        bad = Path(self.tmp.name) / "bad.json"
        bad.write_text('{"owner_id": "Test Owner", "extra": 1}', encoding="utf-8")
        self.assertEqual(self.cli(*self.learn_args(), config=bad, owner="x", expect=2)["reason"], "INVALID_OWNER_CONFIG")


if __name__ == "__main__":
    unittest.main()
