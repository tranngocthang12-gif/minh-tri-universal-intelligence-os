import unittest

from minhtri.knowledge_fast_lane import validate_fast_lane_change


def base_record(record_id="A", status="ACTIVE", depends_on=None, supersedes=None, domain="economics"):
    return {
        "schema": "minhtri-knowledge-atom/v1",
        "record_type": "claim",
        "id": record_id,
        "domain": domain,
        "class": "SECONDARY",
        "status": status,
        "statement": "A bounded learning claim.",
        "source_refs": ["docs/source.md"],
        "evidence_refs": [],
        "contradicts": [],
        "supersedes": list(supersedes or []),
        "depends_on": list(depends_on or []),
        "provenance": {"source_kind": "test"},
    }


class KnowledgeFastLaneV1Tests(unittest.TestCase):
    def test_valid_lightweight_change_passes(self):
        records = [base_record()]
        result = validate_fast_lane_change(
            all_records=records,
            changed_record_ids=["A"],
            domain_rule_refs={"economics": ["knowledge/schema/KNOWLEDGE_SCHEMA_V1.md"]},
            protected_review_required=True,
            autonomous_merge=False,
            self_verified=False,
        )
        self.assertTrue(result.allowed, result)

    def test_provenance_is_required(self):
        record = base_record()
        record["provenance"] = {}
        result = validate_fast_lane_change(
            all_records=[record],
            changed_record_ids=["A"],
            domain_rule_refs={"economics": ["knowledge/schema/KNOWLEDGE_SCHEMA_V1.md"]},
            protected_review_required=True,
            autonomous_merge=False,
            self_verified=False,
        )
        self.assertFalse(result.allowed)

    def test_domain_rule_reference_is_required(self):
        result = validate_fast_lane_change(
            all_records=[base_record()],
            changed_record_ids=["A"],
            domain_rule_refs={},
            protected_review_required=True,
            autonomous_merge=False,
            self_verified=False,
        )
        self.assertFalse(result.allowed)

    def test_stale_dependency_is_rejected(self):
        old = base_record("OLD", status="SUPERSEDED")
        new = base_record("NEW", depends_on=["OLD"])
        result = validate_fast_lane_change(
            all_records=[old, new],
            changed_record_ids=["NEW"],
            domain_rule_refs={"economics": ["knowledge/schema/KNOWLEDGE_SCHEMA_V1.md"]},
            protected_review_required=True,
            autonomous_merge=False,
            self_verified=False,
        )
        self.assertFalse(result.allowed)
        self.assertEqual(result.stale_dependency_ids, ("OLD",))

    def test_supersession_requires_old_target_marked_superseded(self):
        old = base_record("OLD", status="ACTIVE")
        new = base_record("NEW", supersedes=["OLD"])
        result = validate_fast_lane_change(
            all_records=[old, new],
            changed_record_ids=["NEW"],
            domain_rule_refs={"economics": ["knowledge/schema/KNOWLEDGE_SCHEMA_V1.md"]},
            protected_review_required=True,
            autonomous_merge=False,
            self_verified=False,
        )
        self.assertFalse(result.allowed)

        old["status"] = "SUPERSEDED"
        result = validate_fast_lane_change(
            all_records=[old, new],
            changed_record_ids=["OLD", "NEW"],
            domain_rule_refs={"economics": ["knowledge/schema/KNOWLEDGE_SCHEMA_V1.md"]},
            protected_review_required=True,
            autonomous_merge=False,
            self_verified=False,
        )
        self.assertTrue(result.allowed, result)

    def test_autonomous_merge_is_forbidden(self):
        result = validate_fast_lane_change(
            all_records=[base_record()],
            changed_record_ids=["A"],
            domain_rule_refs={"economics": ["knowledge/schema/KNOWLEDGE_SCHEMA_V1.md"]},
            protected_review_required=True,
            autonomous_merge=True,
            self_verified=False,
        )
        self.assertFalse(result.allowed)

    def test_self_verified_promotion_is_forbidden(self):
        result = validate_fast_lane_change(
            all_records=[base_record()],
            changed_record_ids=["A"],
            domain_rule_refs={"economics": ["knowledge/schema/KNOWLEDGE_SCHEMA_V1.md"]},
            protected_review_required=True,
            autonomous_merge=False,
            self_verified=True,
        )
        self.assertFalse(result.allowed)

    def test_protected_review_remains_required(self):
        result = validate_fast_lane_change(
            all_records=[base_record()],
            changed_record_ids=["A"],
            domain_rule_refs={"economics": ["knowledge/schema/KNOWLEDGE_SCHEMA_V1.md"]},
            protected_review_required=False,
            autonomous_merge=False,
            self_verified=False,
        )
        self.assertFalse(result.allowed)


if __name__ == "__main__":
    unittest.main()
