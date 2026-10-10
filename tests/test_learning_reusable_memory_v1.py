"""Memory selector negative controls. Synthetic only: NOT a real AI application test."""
import copy
import unittest
from minhtri.learning_reusable_memory import MemorySelectionError, select_memory, validate_memory

def item(ident="MEM-01", kind="SEMANTIC", status="ACCEPTED", track="BUDDHIST_THOUGHT"):
    return {"schema":"minhtri-learning-reusable-memory/v1","memory_id":ident,"track_id":track,
            "kind":kind,"status":status,"revision_sha":"a"*40,
            "claim":"Source-grounded bounded interpretation, not a direct quotation.",
            "context_tags":["fear"],"applicability_tags":["fear","safe_setting"],
            "exclusion_tags":["physical_danger"],
            "source_refs":["mn2:6"],"counterevidence_refs":["mn4:genre"],
            "limits":"Do not generalize to active physical danger.",
            "supersedes":[],"procedure_steps":["Check sources"] if kind=="PROCEDURAL" else [],
            "outcome_ref":"outcome:001" if kind=="EPISODIC" else None,
            "review_receipt_ref":"review:001" if status=="ACCEPTED" else None}

class ReusableMemoryTests(unittest.TestCase):
    def test_01_accepted_relevant_memory(self):
        self.assertEqual(select_memory([item()],track_id="BUDDHIST_THOUGHT",context_tags=["fear","safe_setting"])["selected_ids"],["MEM-01"])
    def test_02_no_keyword_only_match(self):
        self.assertEqual(select_memory([item()],track_id="BUDDHIST_THOUGHT",context_tags=["fear"])["selected_ids"],[])
    def test_03_exclusion_wins(self):
        self.assertEqual(select_memory([item()],track_id="BUDDHIST_THOUGHT",context_tags=["fear","safe_setting","physical_danger"])["selected_ids"],[])
    def test_04_different_domain_isolated(self):
        self.assertEqual(select_memory([item()],track_id="PC_WORKSHOP",context_tags=["fear","safe_setting"])["selected_ids"],[])
    def test_05_unaccepted_is_not_default_truth(self):
        self.assertEqual(select_memory([item(status="CANDIDATE")],track_id="BUDDHIST_THOUGHT",context_tags=["fear","safe_setting"])["selected_ids"],[])
    def test_06_candidate_may_be_read_as_explicit_working_material(self):
        r=select_memory([item(status="CANDIDATE")],track_id="BUDDHIST_THOUGHT",context_tags=["fear","safe_setting"],permitted_statuses=["CANDIDATE"])
        self.assertEqual(r["selected_ids"],["MEM-01"]);self.assertFalse(r["owner_acceptance_created"])
    def test_07_retracted_memory_not_retrievable(self):
        with self.assertRaisesRegex(MemorySelectionError,"invalid permitted"):
            select_memory([item(status="RETRACTED")],track_id="BUDDHIST_THOUGHT",context_tags=["fear","safe_setting"],permitted_statuses=["RETRACTED"])
    def test_08_replaced_memory_skipped(self):
        a=item(status="SUPERSEDED");b=item(ident="MEM-02");b["supersedes"]=["MEM-01"]
        self.assertEqual(select_memory([a,b],track_id="BUDDHIST_THOUGHT",context_tags=["fear","safe_setting"])["selected_ids"],["MEM-02"])
    def test_09_broken_supersession_blocks_all(self):
        a=item();a["supersedes"]=["MISSING"]
        with self.assertRaisesRegex(MemorySelectionError,"broken"):
            select_memory([a],track_id="BUDDHIST_THOUGHT",context_tags=["fear","safe_setting"])
    def test_10_cross_domain_supersession_blocks(self):
        a=item();b=item(ident="MEM-02",track="PC_WORKSHOP");b["supersedes"]=["MEM-01"]
        with self.assertRaisesRegex(MemorySelectionError,"cross-track"):
            select_memory([a,b],track_id="PC_WORKSHOP",context_tags=["fear","safe_setting"])
    def test_11_duplicate_memory_blocks(self):
        with self.assertRaisesRegex(MemorySelectionError,"duplicate"):
            select_memory([item(),item()],track_id="BUDDHIST_THOUGHT",context_tags=["fear","safe_setting"])
    def test_12_procedure_needs_steps(self):
        a=item(kind="PROCEDURAL");a["procedure_steps"]=[]
        with self.assertRaisesRegex(MemorySelectionError,"procedure must"):
            validate_memory(a)
    def test_13_experience_needs_actual_outcome_reference(self):
        a=item(kind="EPISODIC");a["outcome_ref"]=None
        with self.assertRaisesRegex(MemorySelectionError,"outcome"):
            validate_memory(a)
    def test_14_accepted_record_needs_review_reference(self):
        a=item();a["review_receipt_ref"]=None
        with self.assertRaisesRegex(MemorySelectionError,"review"):
            validate_memory(a)
    def test_15_shadow_field_rejected(self):
        a=item();a["owner_override"]=True
        with self.assertRaisesRegex(MemorySelectionError,"invalid memory fields"):
            validate_memory(a)
    def test_16_duplicate_tags_rejected(self):
        a=item();a["context_tags"]=["fear","fear"]
        with self.assertRaisesRegex(MemorySelectionError,"invalid context_tags"):
            validate_memory(a)
    def test_17_conflicting_tags_rejected(self):
        a=item();a["exclusion_tags"]=["safe_setting"]
        with self.assertRaisesRegex(MemorySelectionError,"contradictory"):
            validate_memory(a)
    def test_18_selected_is_never_self_verified(self):
        a=item(kind="PROCEDURAL")
        r=select_memory([a],track_id="BUDDHIST_THOUGHT",context_tags=["fear","safe_setting"])
        self.assertFalse(r["procedure_executed"]);self.assertEqual(r["status"],"RETRIEVAL_CANDIDATES_NOT_TRUTH")
    def test_19_unmerged_live_predecessor_rejected(self):
        a=item();b=item(ident="MEM-02");b["supersedes"]=["MEM-01"]
        with self.assertRaisesRegex(MemorySelectionError,"live predecessor"):
            select_memory([a,b],track_id="BUDDHIST_THOUGHT",context_tags=["fear","safe_setting"])
    def test_20_zero_context_rejected(self):
        with self.assertRaisesRegex(MemorySelectionError,"context"):
            select_memory([item()],track_id="BUDDHIST_THOUGHT",context_tags=[])
if __name__=="__main__":
    unittest.main()
