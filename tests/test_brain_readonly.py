import tempfile
import unittest
from pathlib import Path

from minhtri.brain_readonly import BrainReadError, BrainReader
from minhtri.core import Ledger
from tests.support import ledger_apply, write_owner_config


class BrainReadonlyBridge(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.home = self.root / "brain"
        self.config = write_owner_config(self.root)
        self.ledger = Ledger(self.home)
        self.ledger.init()
        self.reader = BrainReader(self.home)

    def tearDown(self):
        self.tmp.cleanup()

    def apply(self, command):
        return ledger_apply(self.ledger, command, self.config)

    def test_verify_and_head_are_read_only_recovery_records(self):
        before = self.ledger.events.read_bytes()
        self.assertEqual(self.reader.verify(), self.reader.get_head())
        self.assertEqual(self.reader.verify()["event_count"], 0)
        self.assertEqual(self.ledger.events.read_bytes(), before)

    def test_current_focus_recovers_from_verified_state(self):
        self.apply({"type": "register_domain", "data": {
            "id": "youtube", "name": "YouTube", "risk_class": "NORMAL", "measurement_contract": "CTR"}})
        self.apply({"type": "record_source", "data": {
            "id": "source-one", "domain_id": "youtube", "uri": "owner-text:x",
            "captured_at": "2026-10-02T00:00:00Z", "kind": "FIRST_PARTY", "rights_status": "CLEAR"}})
        self.apply({"type": "set_learning_focus", "data": {
            "id": "focus-one", "status": "ACTIVE", "domain_id": "youtube", "source_id": "source-one",
            "note": "chat quen so khong", "expected_lesson": "recover state", "uncertainty": "untested"}})
        recovered = self.reader.get_current_focus()
        self.assertEqual(recovered["focus"]["id"], "focus-one")
        self.assertEqual(recovered["event_count"], 3)

    def test_search_lessons_returns_only_verified_ledger_state(self):
        # Empty verified brain is a valid result, not an invented lesson.
        result = self.reader.search_lessons("youtube")
        self.assertEqual(result["matches"], [])
        self.assertEqual(result["status"], "VALID")

    def test_tampered_snapshot_fails_closed(self):
        self.ledger.snapshot.write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(BrainReadError, "BRAIN_VERIFY_FAILED"):
            self.reader.get_head()

    def test_bad_search_contract_fails_closed(self):
        with self.assertRaises(BrainReadError):
            self.reader.search_lessons("")
        with self.assertRaises(BrainReadError):
            self.reader.search_lessons("x", 0)

    def test_bridge_has_no_mutation_surface(self):
        for forbidden in ("apply", "repair_snapshot", "init", "publish", "write"):
            self.assertFalse(hasattr(self.reader, forbidden), forbidden)


if __name__ == "__main__":
    unittest.main()
