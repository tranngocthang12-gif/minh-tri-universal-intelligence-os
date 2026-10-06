import unittest

from minhtri.task_guard import evaluate_task_write


def registry_for(task):
    return {"tasks": [task]}


class TaskGuardTests(unittest.TestCase):
    def base_task(self):
        return {
            "task_id": "T1",
            "status": "IN_PROGRESS",
            "generation": 2,
            "scope": ["knowledge/buddhist/", "docs/learning/checkpoint.md"],
            "branch": "owner/task-t1",
            "base_sha": "aaa",
        }

    def test_exact_base_allows(self):
        result = evaluate_task_write(
            registry=registry_for(self.base_task()),
            task_id="T1",
            expected_generation=2,
            declared_base_sha="aaa",
            current_main_sha="aaa",
            main_changed_paths=[],
            proposed_paths=["knowledge/buddhist/a.json"],
        )
        self.assertTrue(result.allowed)

    def test_generation_mismatch_fails(self):
        result = evaluate_task_write(
            registry=registry_for(self.base_task()),
            task_id="T1",
            expected_generation=1,
            declared_base_sha="aaa",
            current_main_sha="aaa",
            main_changed_paths=[],
            proposed_paths=["knowledge/buddhist/a.json"],
        )
        self.assertFalse(result.allowed)

    def test_out_of_scope_fails(self):
        result = evaluate_task_write(
            registry=registry_for(self.base_task()),
            task_id="T1",
            expected_generation=2,
            declared_base_sha="aaa",
            current_main_sha="aaa",
            main_changed_paths=[],
            proposed_paths=["state/current.yaml"],
        )
        self.assertFalse(result.allowed)

    def test_unrelated_main_advance_allows(self):
        result = evaluate_task_write(
            registry=registry_for(self.base_task()),
            task_id="T1",
            expected_generation=2,
            declared_base_sha="aaa",
            current_main_sha="ccc",
            main_changed_paths=["README.md"],
            proposed_paths=["knowledge/buddhist/a.json"],
        )
        self.assertTrue(result.allowed)

    def test_in_scope_main_advance_fails(self):
        result = evaluate_task_write(
            registry=registry_for(self.base_task()),
            task_id="T1",
            expected_generation=2,
            declared_base_sha="aaa",
            current_main_sha="ccc",
            main_changed_paths=["knowledge/buddhist/changed.json"],
            proposed_paths=["knowledge/buddhist/a.json"],
        )
        self.assertFalse(result.allowed)


if __name__ == "__main__":
    unittest.main()
