import tempfile
import unittest
from pathlib import Path

from minhtri.anchor import make_anchor
from minhtri.core import Ledger
from minhtri.witness import make_witness_receipt, verify_local_history_against_witness
from tests.support import ledger_apply, write_owner_config


class ExternalWitnessRewriteDefense(unittest.TestCase):
    def make_ledger(self, root: Path, domain_name: str) -> tuple[Ledger, Path]:
        home = root / "brain"
        config = write_owner_config(root)
        ledger = Ledger(home)
        ledger.init()
        ledger_apply(ledger, {
            "type": "register_domain",
            "data": {
                "id": "alpha",
                "name": domain_name,
                "risk_class": "NORMAL",
                "measurement_contract": "count",
            },
        }, config)
        return ledger, config

    def test_external_receipt_matches_original_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger, _ = self.make_ledger(root, "Original")
            _, count, head = ledger.verify()
            anchor = make_anchor(count, head, "2026-10-01T20:30:00Z")
            receipt = make_witness_receipt(
                anchor,
                authority="cloud-github-connector",
                locator="github://witness/anchor-1",
                published_at="2026-10-01T20:31:00Z",
            )
            result = verify_local_history_against_witness(ledger.events, receipt)
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["reason"], "LOCAL_HISTORY_MATCHES_EXTERNAL_WITNESS")

    def test_full_valid_local_rewrite_is_detected_by_external_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            original_root = root / "original"
            rewritten_root = root / "rewritten"
            original_root.mkdir()
            rewritten_root.mkdir()

            original, _ = self.make_ledger(original_root, "Original")
            _, count, head = original.verify()
            anchor = make_anchor(count, head, "2026-10-01T20:30:00Z")
            receipt = make_witness_receipt(
                anchor,
                authority="cloud-github-connector",
                locator="github://witness/anchor-1",
                published_at="2026-10-01T20:31:00Z",
            )

            rewritten, _ = self.make_ledger(rewritten_root, "Rewritten")
            # The attacker replaces both event log and derived snapshot with a different,
            # internally valid history. Local Ledger.verify() still succeeds.
            original.events.write_bytes(rewritten.events.read_bytes())
            original.snapshot.write_bytes(rewritten.snapshot.read_bytes())
            original.verify()

            result = verify_local_history_against_witness(original.events, receipt)
            self.assertEqual(result["status"], "FAIL")
            self.assertEqual(result["reason"], "LOCAL_HISTORY_DIVERGES_FROM_EXTERNAL_WITNESS")

    def test_tampered_receipt_fails_before_local_comparison(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger, _ = self.make_ledger(root, "Original")
            _, count, head = ledger.verify()
            anchor = make_anchor(count, head, "2026-10-01T20:30:00Z")
            receipt = make_witness_receipt(
                anchor,
                authority="cloud-github-connector",
                locator="github://witness/anchor-1",
                published_at="2026-10-01T20:31:00Z",
            )
            receipt["locator"] = "attacker://rewritten"
            result = verify_local_history_against_witness(ledger.events, receipt)
            self.assertEqual(result["status"], "FAIL")
            self.assertEqual(result["reason"], "WITNESS_DIGEST_MISMATCH")


if __name__ == "__main__":
    unittest.main()
