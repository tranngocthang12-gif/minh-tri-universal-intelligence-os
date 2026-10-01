import tempfile
import unittest
from pathlib import Path

from minhtri.brain_readonly import BrainReader
from minhtri.core import Ledger
from tests.support import ledger_apply, write_owner_config


class ZeroChatRecovery(unittest.TestCase):
    """A fresh seat gets no prior chat transcript; only canonical bootstrap + brain reads."""

    def test_fresh_seat_recovers_learning_state_without_chat_memory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "brain"
            config = write_owner_config(root)
            ledger = Ledger(home)
            ledger.init()

            def apply(command):
                return ledger_apply(ledger, command, config)

            apply({"type": "register_domain", "data": {
                "id": "youtube", "name": "YouTube", "risk_class": "NORMAL",
                "measurement_contract": "CTR"}})
            apply({"type": "record_source", "data": {
                "id": "source-owner", "domain_id": "youtube", "uri": "owner-text:focus",
                "captured_at": "2026-01-01T00:00:00Z", "kind": "FIRST_PARTY",
                "rights_status": "CLEAR"}})
            apply({"type": "set_learning_focus", "data": {
                "id": "focus-youtube", "status": "ACTIVE", "domain_id": "youtube",
                "source_id": "source-owner", "note": "chat quen, so khong",
                "expected_lesson": "recover from durable state", "uncertainty": "UNTESTED"}})

            # Simulate a new seat: construct only the read-only bridge from the brain path.
            fresh_seat = BrainReader(home)
            head = fresh_seat.get_head()
            focus = fresh_seat.get_current_focus()
            lessons = fresh_seat.search_lessons("youtube")

            self.assertEqual(head["status"], "VALID")
            self.assertEqual(head["event_count"], 3)
            self.assertEqual(focus["head"], head["head"])
            self.assertEqual(focus["focus"]["id"], "focus-youtube")
            self.assertEqual(focus["focus"]["domain_id"], "youtube")
            self.assertEqual(lessons["head"], head["head"])
            self.assertEqual(lessons["matches"], [])
            self.assertFalse(hasattr(fresh_seat, "apply"))


if __name__ == "__main__":
    unittest.main()
