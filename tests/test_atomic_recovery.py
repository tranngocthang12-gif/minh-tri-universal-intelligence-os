import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from minhtri.brain_readonly import BrainReadError, BrainReader
from minhtri.core import Ledger
from tests.support import ledger_apply, write_owner_config


class AtomicRecoveryPacket(unittest.TestCase):
    def test_packet_uses_one_verified_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "brain"
            config = write_owner_config(root)
            ledger = Ledger(home)
            ledger.init()
            def apply(command):
                return ledger_apply(ledger, command, config)
            apply({"type":"register_domain","data":{"id":"youtube","name":"YouTube","risk_class":"NORMAL","measurement_contract":"CTR"}})
            apply({"type":"record_source","data":{"id":"s1","domain_id":"youtube","uri":"owner:focus","captured_at":"2026-01-01T00:00:00Z","kind":"FIRST_PARTY","rights_status":"CLEAR"}})
            apply({"type":"set_learning_focus","data":{"id":"f1","status":"ACTIVE","domain_id":"youtube","source_id":"s1","note":"chat quen, so khong","expected_lesson":"atomic bootstrap","uncertainty":"UNTESTED"}})
            reader = BrainReader(home)
            with patch.object(reader, "_verified", wraps=reader._verified) as verified:
                packet = reader.recovery_packet("nothing")
                self.assertEqual(verified.call_count, 1)
            self.assertEqual(packet["status"], "VALID")
            self.assertEqual(packet["event_count"], 3)
            self.assertEqual(packet["focus"]["id"], "f1")
            self.assertEqual(packet["lesson_matches"], [])

    def test_bad_query_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            reader = BrainReader(Path(tmp) / "missing")
            with self.assertRaises(BrainReadError):
                reader.recovery_packet("")


if __name__ == "__main__":
    unittest.main()
