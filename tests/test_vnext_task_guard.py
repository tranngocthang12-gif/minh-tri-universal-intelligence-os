import unittest

from minhtri.task_guard import evaluate_task_write


def registry_for(task):
    return {"tasks": [task]}


class VNextTaskGuardTests(unittest.TestCase):
    def base_task(self):
        return {
            "task_id": "T1",
            "status": "IN_PROGRESS",
            "generation": 2,
            "scope": ["knowledge/buddhist/", "docs/learning/checkpoint.md"],
            "branch": "owner/task-t1",
            "base_sha": "aaa",
        }

    def test_allows_exact_current_base(self):
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

    def test_rejects_generation_mismatch(self):
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
        self.assertIn("generation mismatch", result.reason)

    def test_rejects_base_sha_mismatch(self):
        result = evaluate_task_write(
            registry=registry_for(self.base_task()),
            task_id="T1",
            expected_generation=2,
            declared_base_sha="bbb",
            current_main_sha="bbb",
            main_changed_paths=[],
            proposed_paths=["knowledge/buddhist/a.json"],
        )
        self.assertFalse(result.allowed)
        self.assertIn("base_sha mismatch", result.reason)

    def test_rejects_out_of_scope_write(self):
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
        self.assertEqual(result.conflicting_paths, ("state/current.yaml",))

    def test_allows_main_advance_outside_scope(self):
        result = evaluate_task_write(
            registry=registry_for(self.base_task()),
            task_id="T1",
            expected_generation=2,
            declared_base_sha="aaa",
            current_main_sha="ccc",
            main_changed_paths=["README.md", "state/current.yaml"],
            proposed_paths=["knowledge/buddhist/a.json"],
        )
        self.assertTrue(result.allowed)
        self.assertIn("no in-scope conflict", result.reason)

    def test_rejects_main_advance_inside_scope(self):
        result = evaluate_task_write(
            registry=registry_for(self.base_task()),
            task_id="T1",
            expected_generation=2,
            declared_base_sha="aaa",
            current_main_sha="ccc",
            main_changed_paths=["knowledge/buddhist/changed.json", "README.md"],
            proposed_paths=["knowledge/buddhist/a.json"],
        )
        self.assertFalse(result.allowed)
        self.assertEqual(result.conflicting_paths, ("knowledge/buddhist/changed.json",))

    def test_rejects_terminal_or_blocked_task(self):
        for state in ("DONE", "STALE", "BLOCKED", "REPORTED", "REVIEWED_ACCEPTED"):
            task = self.base_task()
            task["status"] = state
            result = evaluate_task_write(
                registry=registry_for(task),
                task_id="T1",
                expected_generation=2,
                declared_base_sha="aaa",
                current_main_sha="aaa",
                main_changed_paths=[],
                proposed_paths=["knowledge/buddhist/a.json"],
            )
            self.assertFalse(result.allowed, state)

    def test_rejects_unassigned_branch(self):
        task = self.base_task()
        task["branch"] = None
        result = evaluate_task_write(
            registry=registry_for(task),
            task_id="T1",
            expected_generation=2,
            declared_base_sha="aaa",
            current_main_sha="aaa",
            main_changed_paths=[],
            proposed_paths=["knowledge/buddhist/a.json"],
        )
        self.assertFalse(result.allowed)
        self.assertIn("no assigned branch", result.reason)


if __name__ == "__main__":
    unittest.main()
