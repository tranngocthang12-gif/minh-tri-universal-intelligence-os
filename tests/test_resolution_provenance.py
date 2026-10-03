import unittest

from minhtri.resolution_provenance import (
    audit_batch,
    compare_independent_resolution,
    sha256_text,
    validate_resolution_provenance,
    verify_evidence_content,
)


def valid_record(actor="resolver-a"):
    return {
        "prediction_id": "p1",
        "prediction_hash": "a" * 64,
        "prediction_created_at": "2026-10-01T00:00:00Z",
        "due_at": "2026-10-02T00:00:00Z",
        "evidence_id": "e1",
        "evidence_content_hash": sha256_text("raw outcome snapshot"),
        "evidence_cutoff_timestamp": "2026-10-02T00:00:01Z",
        "outcome_captured_at": "2026-10-02T01:00:00Z",
        "observed_value": 10.0,
        "resolver_actor": actor,
        "resolver_method": "BLIND_NUMERIC_EXTRACTION",
        "resolution_created_at": "2026-10-02T01:01:00Z",
        "interval_hit": True,
        "absolute_midpoint_error": 0.5,
    }


class ResolutionProvenanceTests(unittest.TestCase):
    def test_valid_record_is_eligible(self):
        result = validate_resolution_provenance(valid_record())
        self.assertEqual(result["status"], "VALID_PROVENANCE")
        self.assertTrue(result["eligible_for_meta_learning"])

    def test_outcome_before_due_is_disqualified(self):
        record = valid_record()
        record["outcome_captured_at"] = "2026-10-01T23:00:00Z"
        result = validate_resolution_provenance(record)
        self.assertEqual(result["status"], "INVALID_PROVENANCE")
        self.assertIn("OUTCOME_CAPTURED_BEFORE_DUE", result["reasons"])

    def test_evidence_hash_mismatch_is_disqualified(self):
        result = verify_evidence_content(valid_record(), "modified page")
        self.assertEqual(result["status"], "HASH_MISMATCH")
        self.assertFalse(result["eligible_for_meta_learning"])

    def test_blind_resolver_must_be_distinct(self):
        first = valid_record("same")
        second = valid_record("same")
        result = compare_independent_resolution(first, second)
        self.assertEqual(result["status"], "DISAGREE")
        self.assertFalse(result["distinct_resolver"])

    def test_batch_uses_preregistered_threshold(self):
        pair = (valid_record("a"), valid_record("b"))
        report = audit_batch([pair], preregistered_min_agreement=1.0)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["agreement_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
