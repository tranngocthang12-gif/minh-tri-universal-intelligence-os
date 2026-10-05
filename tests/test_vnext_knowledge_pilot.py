import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_generator():
    path = ROOT / "tools" / "generate_knowledge_index.py"
    spec = importlib.util.spec_from_file_location("generate_knowledge_index", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class VNextKnowledgePilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.generator = load_generator()
        cls.index = cls.generator.build_index(ROOT)
        cls.atoms = {a["id"]: a for a in cls.index["atoms"]}
        cls.hubs = {h["id"]: h for h in cls.index["hubs"]}

    def test_index_is_deterministically_generated(self):
        committed = (ROOT / "knowledge" / "index.json").read_text(encoding="utf-8")
        self.assertEqual(committed, self.generator.render_index(ROOT))

    def test_ids_are_unique(self):
        atom_ids = [a["id"] for a in self.index["atoms"]]
        hub_ids = [h["id"] for h in self.index["hubs"]]
        self.assertEqual(len(atom_ids), len(set(atom_ids)))
        self.assertEqual(len(hub_ids), len(set(hub_ids)))
        self.assertTrue(set(atom_ids).isdisjoint(hub_ids))

    def test_hub_dependencies_exist_and_are_not_pending_review(self):
        for hub in self.index["hubs"]:
            for claim_id in hub["depends_on_claims"]:
                self.assertIn(claim_id, self.atoms)
                self.assertNotEqual(self.atoms[claim_id]["status"], "PENDING_REVIEW")

    def test_pending_review_atom_is_indexed_but_not_hub_support(self):
        pending = self.atoms["bud:a172:hiri-lexical-open"]
        self.assertEqual(pending["status"], "PENDING_REVIEW")
        cited = {
            claim_id
            for hub in self.index["hubs"]
            for claim_id in hub["depends_on_claims"]
        }
        self.assertNotIn(pending["id"], cited)

    def test_buddhist_and_economics_pilot_domains_exist(self):
        domains = {a["domain"] for a in self.index["atoms"]}
        self.assertIn("buddhist_thought", domains)
        self.assertIn("economics", domains)

    def test_truth_boundary_stays_unproven(self):
        current = json.loads((ROOT / "state" / "current.yaml").read_text(encoding="utf-8"))
        self.assertFalse(current["autonomous_learning_runtime"])
        self.assertFalse(current["automatic_self_critique_runtime"])
        self.assertFalse(current["meta_learning_runtime"])


if __name__ == "__main__":
    unittest.main()
