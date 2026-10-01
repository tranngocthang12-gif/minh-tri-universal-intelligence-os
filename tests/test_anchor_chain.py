import unittest

from minhtri.anchor import make_anchor, verify_anchor, verify_anchor_chain


class AnchorChainHardening(unittest.TestCase):
    def test_valid_chain_passes(self):
        a1 = make_anchor(1, "a" * 64, "2026-10-01T00:00:00Z")
        a2 = make_anchor(2, "b" * 64, "2026-10-01T01:00:00Z", a1["anchor_id"])
        result = verify_anchor_chain([a1, a2])
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["head_anchor_id"], a2["anchor_id"])

    def test_broken_pointer_fails(self):
        a1 = make_anchor(1, "a" * 64, "2026-10-01T00:00:00Z")
        a2 = make_anchor(2, "b" * 64, "2026-10-01T01:00:00Z", "c" * 64)
        self.assertEqual(verify_anchor_chain([a1, a2])["reason"], "BROKEN_ANCHOR_CHAIN")

    def test_non_increasing_count_fails(self):
        a1 = make_anchor(2, "a" * 64, "2026-10-01T00:00:00Z")
        a2 = make_anchor(2, "b" * 64, "2026-10-01T01:00:00Z", a1["anchor_id"])
        self.assertEqual(verify_anchor_chain([a1, a2])["reason"], "ANCHOR_COUNT_NOT_INCREASING")

    def test_tampered_record_fails_digest(self):
        a1 = make_anchor(1, "a" * 64, "2026-10-01T00:00:00Z")
        a1["created_at"] = "2026-10-01T02:00:00Z"
        self.assertEqual(verify_anchor_chain([a1])["reason"], "ANCHOR_DIGEST_MISMATCH")

    def test_malformed_anchor_head_fails_closed(self):
        a1 = make_anchor(1, "a" * 64, "2026-10-01T00:00:00Z")
        a1["head"] = "not-sha"
        record = {k: a1[k] for k in ("schema", "project", "event_count", "head", "created_at", "previous_anchor")}
        import hashlib, json
        a1["anchor_id"] = hashlib.sha256(json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
        self.assertEqual(verify_anchor_chain([a1])["reason"], "MALFORMED_ANCHOR")

    def test_verify_anchor_rejects_malformed_local_head(self):
        a1 = make_anchor(1, "a" * 64, "2026-10-01T00:00:00Z")
        self.assertEqual(verify_anchor(1, "bad", a1), {"status": "FAIL", "reason": "MALFORMED_ANCHOR"})

    def test_empty_chain_is_unknown(self):
        self.assertEqual(verify_anchor_chain([]), {"status": "UNKNOWN", "reason": "MISSING_EXTERNAL_ANCHOR"})


if __name__ == "__main__":
    unittest.main()
