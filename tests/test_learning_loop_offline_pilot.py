import copy
import unittest
from minhtri.learning_loop_offline_pilot import digest, inspect, target_digest, record_digest, dependency_closure


def fixture():
    sources=[
      {"id":"s1","text":"Primary source snapshot.","sha256":digest("Primary source snapshot."),"locator":"synthetic/early","role":"EARLY_DISCOURSE"},
      {"id":"s2","text":"Supporting reasoning snapshot.","sha256":digest("Supporting reasoning snapshot."),"locator":"synthetic/milinda","role":"MILINDAPANHA"},
    ]
    checks=[]
    for q in ("Apply the distinction to case A?","What would falsify the interpretation in case B?"):
        checks.append({"question":q,"question_hash":digest(q),"frozen_before_answer":True,"answer":"A bounded test answer.","judge":{"id":"critic-other","verdict":"PASS"}})
    packet={"schema":"minhtri-learning-pilot/v1","goal_id":"BUDDHIST-A173","domain":"buddhist_thought","producer_id":"author","sources":sources,
        "understanding":{"record_id":"k1","own_words":"Bounded account.","alternative":"Other reading.","counterexample":"Countercase.","limits":"Not universal.","source_ids":["s1","s2"]},
        "transfer":checks,"policy":{"protected_review":True,"auto_merge":False,"auto_verified":False,"background_runtime":False}}
    packet["critic"]={"id":"independent-critic","verdict":"NO_MATERIAL_DEFECT","target_digest":target_digest(packet)}
    atom={"schema":"minhtri-knowledge-atom/v1","record_type":"claim","id":"k1","domain":"buddhist_thought","class":"SYNTHESIS",
        "status":"PENDING_REVIEW","statement":"Hypothesis, not certified truth.","source_refs":["synthetic/early","synthetic/milinda"],"evidence_refs":[],
        "contradicts":[],"supersedes":[],"depends_on":[],"provenance":{"source_kind":"synthetic-test"}}
    packet["atom_sha256"]=record_digest(atom)
    packet["dependency_closure_sha256"]=record_digest(dependency_closure([atom],"k1")[0])
    packet["domain_rules_sha256"]=record_digest({"buddhist_thought":["docs/LAW_UNIVERSAL_LEARNING_CONTINUITY_20261004.md","knowledge/schema/KNOWLEDGE_SCHEMA_V1.md"]})
    packet["critic"]["target_digest"]=target_digest(packet)
    return packet,[atom]


class OfflineLearningPilotTests(unittest.TestCase):
    def check(self,p,records=None,goal="BUDDHIST-A173"):
        if records is None: records=fixture()[1]
        return inspect(p,authorized_goal_id=goal,records=records,domain_rule_refs={"buddhist_thought":["docs/LAW_UNIVERSAL_LEARNING_CONTINUITY_20261004.md","knowledge/schema/KNOWLEDGE_SCHEMA_V1.md"]})

    def test_non_list_sources_return_not_ready(self):
        for x in ({"s1":"bad"},42,"source"):
            p,r=fixture();p["sources"]=x
            result=self.check(p,r)
            self.assertFalse(result["ready_for_review"])
            self.assertIn("missing source snapshots",result["reasons"])

    def test_canonical_domain_rules_cannot_be_laundered(self):
        p,r=fixture()
        outcome=inspect(p,authorized_goal_id="BUDDHIST-A173",records=r,
                        domain_rule_refs={"buddhist_thought":["fake-law.md"]})
        self.assertIn("canonical Buddhist Fast Lane rules mismatch",outcome["reasons"])

    def test_normalized_question_duplicates_rejected(self):
        p,r=fixture()
        p["transfer"][1]["question"]="  Apply  the distinction to case A?  "
        p["transfer"][1]["question_hash"]=digest(p["transfer"][1]["question"])
        p["critic"]["target_digest"]=target_digest(p)
        self.assertIn("duplicate transfer question",self.check(p,r)["reasons"])

    def test_declared_receipts_are_not_independence_proof(self):
        p,r=fixture()
        out=self.check(p,r)
        self.assertTrue(out["ready_for_review"])
        self.assertFalse(out["critic_independence_proven"])
        self.assertFalse(out["transfer_precommitment_proven"])

    def test_eligible_proposal_never_becomes_verified_or_durable(self):
        p,r=fixture();out=self.check(p,r)
        self.assertTrue(out["ready_for_review"],out)
        for name in ("understanding_proven","behavioral_learning_proven","durable_written","automatic_verified","background_runtime_enabled"):
            self.assertFalse(out[name])

    def test_atom_mutated_after_critic_blocks(self):
        p,r=fixture();r[0]["statement"]="Changed after review."
        self.assertIn("knowledge atom integrity mismatch",self.check(p,r)["reasons"])

    def test_atom_source_not_in_snapshot_blocks(self):
        p,r=fixture();r[0]["source_refs"]=["unseen/source"]
        self.assertIn("knowledge atom sources not bound to snapshots",self.check(p,r)["reasons"])

    def test_policy_changed_after_critic_blocks(self):
        p,r=fixture();p["policy"]["background_runtime"]=True
        self.assertIn("exact-target separate critic required",self.check(p,r)["reasons"])

    def test_malformed_inputs_fail_closed(self):
        p,r=fixture()
        self.assertFalse(self.check(None,r)["ready_for_review"])
        p["sources"][0]["role"]=["bad-role"]
        self.assertFalse(self.check(p,r)["ready_for_review"])

    def test_invalid_explanation_source_shape_rejected(self):
        p,r=fixture();p["understanding"]["source_ids"]={"s1":"s2"}
        self.assertIn("explanation source references invalid",self.check(p,r)["reasons"])

    def test_wrong_owner_goal_fails_closed(self):
        p,r=fixture();self.assertFalse(self.check(p,r,goal="OTHER")["ready_for_review"])

    def test_mutated_snapshot_fails_even_with_existing_critic(self):
        p,r=fixture();p["sources"][0]["text"]="tampered"
        self.assertIn("source integrity mismatch",self.check(p,r)["reasons"])

    def test_source_hierarchy_is_required(self):
        p,r=fixture();p["sources"]=p["sources"][:1]
        self.assertIn("Buddhist source hierarchy incomplete",self.check(p,r)["reasons"])

    def test_critic_cannot_be_the_producer(self):
        p,r=fixture();p["critic"]["id"]="author"
        self.assertIn("exact-target separate critic required",self.check(p,r)["reasons"])

    def test_critic_cannot_use_stale_target_digest(self):
        p,r=fixture();p["understanding"]["own_words"]="Changed claim"
        self.assertIn("exact-target separate critic required",self.check(p,r)["reasons"])

    def test_transfer_questions_must_be_frozen(self):
        p,r=fixture();p["transfer"][0]["frozen_before_answer"]=False
        self.assertIn("transfer integrity failure",self.check(p,r)["reasons"])

    def test_policy_never_allows_automatic_merge(self):
        p,r=fixture();p["policy"]["auto_merge"]=True
        self.assertIn("unsafe learning policy",self.check(p,r)["reasons"])

    def test_record_must_remain_pending_review(self):
        p,r=fixture();r[0]["status"]="ACTIVE"
        self.assertIn("one matching pending knowledge atom required",self.check(p,r)["reasons"])

    def test_canonical_buddhist_goal_and_attestation(self):
        p,r=fixture()
        self.assertTrue(self.check(p,r)["ready_for_review"])
        p["understanding"]["source_ids"]=["s2"]
        r[0]["class"]="ATTESTED";r[0]["source_refs"]=["synthetic/milinda"]
        p["atom_sha256"]=record_digest(r[0])
        p["dependency_closure_sha256"]=record_digest(dependency_closure(r,"k1")[0])
        p["critic"]["target_digest"]=target_digest(p)
        self.assertIn("ATTESTED claim lacks cited early discourse",self.check(p,r)["reasons"])
    def test_canonical_alias_rejected(self):
        p,r=fixture();p["domain"]="buddhist";r[0]["domain"]="buddhist"
        p["atom_sha256"]=record_digest(r[0])
        p["dependency_closure_sha256"]=record_digest(dependency_closure(r,"k1")[0])
        p["critic"]["target_digest"]=target_digest(p)
        self.assertIn("Buddhist goal domain mismatch",self.check(p,r)["reasons"])

    def test_unhashable_question_fails_structured(self):
        for q in ([],{},None):
            p,r=fixture();p["transfer"][0]["question"]=q
            out=self.check(p,r)
            self.assertFalse(out["ready_for_review"])
            self.assertIn("transfer integrity failure",out["reasons"])
    def test_nonserializable_atom_without_digest_fails(self):
        p,r=fixture();r[0]["provenance"]["bad"]={"not json"}
        p.pop("atom_sha256",None)
        self.assertIn("knowledge atom integrity mismatch",self.check(p,r)["reasons"])
    def test_buddhist_goal_cannot_be_economics(self):
        p,r=fixture();p["domain"]="economics";r[0]["domain"]="economics"
        p["atom_sha256"]=record_digest(r[0])
        p["dependency_closure_sha256"]=record_digest(dependency_closure(r,"k1")[0])
        p["critic"]["target_digest"]=target_digest(p)
        self.assertIn("Buddhist goal domain mismatch",self.check(p,r)["reasons"])
    def test_unused_early_source_cannot_satisfy_hierarchy(self):
        p,r=fixture();p["understanding"]["source_ids"]=["s2"]
        p["critic"]["target_digest"]=target_digest(p)
        self.assertIn("Buddhist source hierarchy incomplete",self.check(p,r)["reasons"])
    def test_dependency_cycle_cannot_be_accepted(self):
        p,r=fixture();r[0]["depends_on"]=["k2"]
        r.append(dict(r[0],id="k2",status="ACTIVE",depends_on=["k1"]))
        p["atom_sha256"]=record_digest(r[0])
        p["dependency_closure_sha256"]=record_digest(dependency_closure(r,"k1")[0])
        p["critic"]["target_digest"]=target_digest(p)
        self.assertIn("dependency cycle",self.check(p,r)["reasons"])
    def test_critic_normalization(self):
        p,r=fixture();p["critic"]["id"]=" AUTHOR "
        p["critic"]["target_digest"]=target_digest(p)
        self.assertIn("exact-target separate critic required",self.check(p,r)["reasons"])
    def test_stale_dependency_is_rejected(self):
        p,r=fixture();r[0]["depends_on"]=["old"]
        r.append(dict(r[0],id="old",status="SUPERSEDED",depends_on=[]))
        self.assertFalse(self.check(p,r)["ready_for_review"])


if __name__=="__main__":
    unittest.main()
