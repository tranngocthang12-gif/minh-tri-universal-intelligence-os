import unittest

from minhtri.anchor import make_anchor, verify_anchor


class ExternalAnchor(unittest.TestCase):
    def setUp(self):
        self.head = "a" * 64
        self.anchor = make_anchor(3, self.head, "2026-10-02T00:00:00Z")

    def test_exact_match_passes(self):
        self.assertEqual(verify_anchor(3, self.head, self.anchor)["status"], "PASS")

    def test_missing_is_unknown_never_pass(self):
        self.assertEqual(verify_anchor(3, self.head, None), {
            "status": "UNKNOWN", "reason": "MISSING_EXTERNAL_ANCHOR"})

    def test_same_count_different_head_is_hard_fail(self):
        self.assertEqual(verify_anchor(3, "b" * 64, self.anchor)["status"], "FAIL")

    def test_rollback_is_hard_fail(self):
        result = verify_anchor(2, self.head, self.anchor)
        self.assertEqual(result, {"status": "FAIL", "reason": "LOCAL_LEDGER_ROLLBACK"})

    def test_local_ahead_requires_new_anchor(self):
        result = verify_anchor(4, "b" * 64, self.anchor)
        self.assertEqual(result, {"status": "UNKNOWN", "reason": "LOCAL_LEDGER_AHEAD_OF_ANCHOR"})

    def test_tampered_anchor_digest_fails(self):
        bad = dict(self.anchor)
        bad["head"] = "b" * 64
        self.assertEqual(verify_anchor(3, "b" * 64, bad), {
            "status": "FAIL", "reason": "ANCHOR_DIGEST_MISMATCH"})

    def test_malformed_anchor_fails_closed(self):
        self.assertEqual(verify_anchor(3, self.head, {"schema": "x"}), {
            "status": "FAIL", "reason": "MALFORMED_ANCHOR"})

    def test_anchor_chain_pointer_is_committed_into_id(self):
        second = make_anchor(4, "b" * 64, "2026-10-02T01:00:00Z", self.anchor["anchor_id"])
        changed = dict(second)
        changed["previous_anchor"] = "c" * 64
        self.assertEqual(verify_anchor(4, "b" * 64, changed)["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
