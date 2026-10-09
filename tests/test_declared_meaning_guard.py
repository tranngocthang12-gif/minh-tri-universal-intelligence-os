import copy
import unittest
from minhtri.declared_meaning_guard import inspect_meaning_annotations

def specimen():
    frame={"claim_id":"k1","proposition":"Under C, O may occur.","conditions":["C"],
           "certainty":"POSSIBLE","relation_type":"CONDITIONAL","scope":"S only",
           "source_refs":["source/v1"],"nonclaims":["O is inevitable"],
           "uncertainties":["rate unknown"],"layer":"INTERPRETATION"}
    atom={"schema":"minhtri-knowledge-atom/v1","record_type":"claim","id":"k1","domain":"buddhist_thought","class":"SYNTHESIS","status":"PENDING_REVIEW","statement":frame["proposition"],"source_refs":["source/v1"],"evidence_refs":[],"contradicts":[],"supersedes":[],"depends_on":[],"provenance":{"fixture":"synthetic"}}
    examples=[
        {"kind":"EXPLANATION","text":"When C holds, O is possible, not certain.","annotations":copy.deepcopy(frame)},
        {"kind":"SHORT_FORM","text":"In S, C may accompany O.","annotations":copy.deepcopy(frame)},
    ]
    return {"schema":"minhtri-declared-meaning/v1","reference":frame,"renderings":examples},atom

class MeaningGuardTests(unittest.TestCase):
    def check(self,pack=None,atom=None):
        if pack is None or atom is None:
            p,a=specimen();pack=p if pack is None else pack;atom=a if atom is None else atom
        return inspect_meaning_annotations(pack,atom=atom)
    def test_synthesis_cannot_be_promoted_to_source_report(self):
        p,a=specimen()
        p["reference"]["layer"]="SOURCE_REPORT"
        for sample in p["renderings"]:
            sample["annotations"]["layer"]="SOURCE_REPORT"
        self.assertIn("MEANING_SOURCE_LAYER_CLASS_MISMATCH",self.check(p,a)["reasons"])

    def test_attested_must_use_source_report(self):
        p,a=specimen()
        a["class"]="ATTESTED"
        self.assertIn("MEANING_SOURCE_LAYER_CLASS_MISMATCH",self.check(p,a)["reasons"])

    def test_uncertain_claim_cannot_assert_certainty(self):
        p,a=specimen()
        a["class"]="UNCERTAIN"
        p["reference"]["certainty"]="ASSERTED"
        for sample in p["renderings"]:
            sample["annotations"]["certainty"]="ASSERTED"
        self.assertIn("MEANING_UNCERTAINTY_CLASS_MISMATCH",self.check(p,a)["reasons"])

    def test_minimal_atom_is_rejected(self):
        p,a=specimen()
        for k in ("record_type","domain","class","provenance"):
            a.pop(k)
        self.assertIn("MEANING_ATOM_INVALID",self.check(p,a)["reasons"])

    def test_valid_annotations_still_do_not_prove_prose(self):
        p,a=specimen();out=self.check(p,a)
        self.assertTrue(out["annotation_contract_pass"],out)
        for k in ("prose_meaning_verified","source_truth_verified","independent_review_proven","durable_written","autonomous_runtime_enabled"):
            self.assertFalse(out[k])
    def test_lost_condition(self):
        p,a=specimen();p["renderings"][0]["annotations"]["conditions"]=[]
        self.assertIn("MEANING_DRIFT_CONDITIONS",self.check(p,a)["reasons"])
    def test_inflated_certainty(self):
        p,a=specimen();p["renderings"][0]["annotations"]["certainty"]="ASSERTED"
        self.assertIn("MEANING_DRIFT_CERTAINTY",self.check(p,a)["reasons"])
    def test_causation_upgrade(self):
        p,a=specimen();p["renderings"][0]["annotations"]["relation_type"]="CAUSAL"
        self.assertIn("MEANING_DRIFT_RELATION_TYPE",self.check(p,a)["reasons"])
    def test_scope_widening(self):
        p,a=specimen();p["renderings"][0]["annotations"]["scope"]="All contexts"
        self.assertIn("MEANING_DRIFT_SCOPE",self.check(p,a)["reasons"])
    def test_source_laundering(self):
        p,a=specimen();p["renderings"][0]["annotations"]["layer"]="SOURCE_REPORT"
        self.assertIn("MEANING_DRIFT_LAYER",self.check(p,a)["reasons"])
    def test_erased_uncertainty(self):
        p,a=specimen();p["renderings"][0]["annotations"]["uncertainties"]=[]
        self.assertIn("MEANING_DRIFT_UNCERTAINTIES",self.check(p,a)["reasons"])
    def test_erased_nonclaim(self):
        p,a=specimen();p["renderings"][0]["annotations"]["nonclaims"]=[]
        self.assertIn("MEANING_DRIFT_NONCLAIMS",self.check(p,a)["reasons"])
    def test_atom_changed_after_annotation(self):
        p,a=specimen();a["statement"]="Altered proposition"
        self.assertIn("MEANING_ATOM_PROPOSITION_MISMATCH",self.check(p,a)["reasons"])
    def test_atom_source_mismatch(self):
        p,a=specimen();a["source_refs"]=["elsewhere"]
        self.assertIn("MEANING_ATOM_SOURCE_MISMATCH",self.check(p,a)["reasons"])
    def test_wrong_rendering_kind(self):
        p,a=specimen();p["renderings"][0]["kind"]="UNKNOWN"
        self.assertFalse(self.check(p,a)["annotation_contract_pass"])
    def test_invalid_annotation_shape(self):
        p,a=specimen();p["renderings"][1]["annotations"]["conditions"]="C"
        self.assertIn("MEANING_ANNOTATION_INVALID",self.check(p,a)["reasons"])
    def test_prose_can_lie_and_structural_pass_does_not_certify(self):
        p,a=specimen();p["renderings"][0]["text"]="O will always happen even without C"
        out=self.check(p,a)
        self.assertTrue(out["annotation_contract_pass"])
        self.assertFalse(out["prose_meaning_verified"])
    def test_malformed_kind_is_structured_failure(self):
        for invalid in ([], {}, None):
            p,a=specimen()
            p["renderings"][0]["kind"]=invalid
            out=self.check(p,a)
            self.assertFalse(out["annotation_contract_pass"])
            self.assertIn("MEANING_KIND_INVALID",out["reasons"])
    def test_nonpending_atom_is_rejected(self):
        for status in ("ACTIVE","SUPERSEDED","REFUTED","VERIFIED"):
            p,a=specimen();a["status"]=status
            self.assertIn("MEANING_ATOM_INVALID",self.check(p,a)["reasons"])
    def test_rendering_count_bound(self):
        p,a=specimen()
        p["renderings"].extend([
          {"kind":"TEACH_BACK","text":"Example.","annotations":copy.deepcopy(p["reference"])},
          {"kind":"EXPLANATION","text":"Repeated.","annotations":copy.deepcopy(p["reference"])}
        ])
        self.assertIn("MEANING_RENDERINGS_REQUIRED",self.check(p,a)["reasons"])
    def test_missing_rendering(self):
        p,a=specimen();p["renderings"]=p["renderings"][:1]
        self.assertIn("MEANING_RENDERINGS_REQUIRED",self.check(p,a)["reasons"])
    def test_invalid_reference(self):
        p,a=specimen();p["reference"]["conditions"]=[{"unexpected":"object"}]
        self.assertIn("MEANING_REFERENCE_INVALID",self.check(p,a)["reasons"])

if __name__=="__main__":
    unittest.main()
