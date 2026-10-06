import unittest

from minhtri.semantic_guard import evaluate_semantic_dependencies


class SemanticGuardTests(unittest.TestCase):
    def test_active_and_uncertain_dependencies_pass(self):
        records = [
            {"id": "A", "status": "ACTIVE"},
            {"id": "B", "status": "UNCERTAIN"},
        ]
        result = evaluate_semantic_dependencies(records=records, dependency_ids=["A", "B"])
        self.assertTrue(result.allowed)

    def test_superseded_refuted_disputed_fail(self):
        for status in ("SUPERSEDED", "REFUTED", "DISPUTED"):
            result = evaluate_semantic_dependencies(
                records=[{"id": "A", "status": status}],
                dependency_ids=["A"],
            )
            self.assertFalse(result.allowed, status)
            self.assertEqual(result.stale_dependency_ids, ("A",))

    def test_pending_review_is_not_established_support(self):
        result = evaluate_semantic_dependencies(
            records=[{"id": "A", "status": "PENDING_REVIEW"}],
            dependency_ids=["A"],
        )
        self.assertFalse(result.allowed)

    def test_missing_dependency_fails_closed(self):
        result = evaluate_semantic_dependencies(records=[], dependency_ids=["MISSING"])
        self.assertFalse(result.allowed)
        self.assertEqual(result.missing_dependency_ids, ("MISSING",))

    def test_duplicate_dependency_id_fails_closed(self):
        result = evaluate_semantic_dependencies(
            records=[{"id": "A", "status": "ACTIVE"}, {"id": "A", "status": "ACTIVE"}],
            dependency_ids=["A"],
        )
        self.assertFalse(result.allowed)
        self.assertEqual(result.ambiguous_dependency_ids, ("A",))

    def test_policy_can_inspect_without_enforcing_freshness(self):
        result = evaluate_semantic_dependencies(
            records=[{"id": "A", "status": "SUPERSEDED"}],
            dependency_ids=["A"],
            require_fresh=False,
        )
        self.assertTrue(result.allowed)

    def test_semantic_staleness_is_independent_of_file_freshness(self):
        result = evaluate_semantic_dependencies(
            records=[{"id": "A", "status": "REFUTED"}],
            dependency_ids=["A"],
        )
        self.assertFalse(result.allowed)


if __name__ == "__main__":
    unittest.main()
