import copy
import unittest
from minhtri.learning_loop_offline_pilot import digest, inspect, target_digest


def fixture():
    sources=[
      {"id":"s1","text":"Primary source snapshot.","sha256":digest("Primary source snapshot."),"locator":"synthetic/early","role":"EARLY_DISCOURSE"},
      {"id":"s2","text":"Supporting reasoning snapshot.","sha256":digest("Supporting reasoning snapshot."),"locator":"synthetic/milinda","role":"MILINDAPANHA"},
    ]
    checks=[]
    for q in ("Apply the distinction to case A?","What would falsify the interpretation in case B?"):
        checks.append({"question":q,"question_hash":digest(q),"frozen_before_answer":True,"answer":"A bounded test answer.","judge":{"id":"critic-other","verdict":"PASS"}})
    packet={"schema":"minhtri-learning-pilot/v1","goal_id":"BUDDHIST-A173","domain":"buddhist","producer_id":"author","sources":sources,
        "understanding":{"record_id":"k1","own_words":"Bounded account.","alternative":"Other reading.","counterexample":"Countercase.","limits":"Not universal.","source_ids":["s1","s2"]},
        "transfer":checks,"policy":{"protected_review":True,"auto_merge":False,"auto_verified":False,"background_runtime":False}}
    packet["critic"]={"id":"independent-critic","verdict":"NO_MATERIAL_DEFECT","target_digest":target_digest(packet)}
    atom={"schema":"minhtri-knowledge-atom/v1","record_type":"claim","id":"k1","domain":"buddhist","class":"SYNTHESIS",
        "status":"PENDING_REVIEW","statement":"Hypothesis, not certified truth.","source_refs":["synthetic/early","synthetic/milinda"],"evidence_refs":[],
        "contradicts":[],"supersedes":[],"depends_on":[],"provenance":{"source_kind":"synthetic-test"}}
    return packet,[atom]


class OfflineLearningPilotTests(unittest.TestCase):
    def check(self,p,records=None,goal="BUDDHIST-A173"):
        if records is None: records=fixture()[1]
        return inspect(p,authorized_goal_id=goal,records=records,domain_rule_refs={"buddhist":["docs/LAW_UNIVERSAL_LEARNING_CONTINUITY_20261004.md"]})

    def test_eligible_proposal_never_becomes_verified_or_durable(self):
        p,r=fixture();out=self.check(p,r)
        self.assertTrue(out["ready_for_review"],out)
        for name in ("understanding_proven","behavioral_learning_proven","durable_written","automatic_verified","background_runtime_enabled"):
            self.assertFalse(out[name])

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

    def test_stale_dependency_is_rejected(self):
        p,r=fixture();r[0]["depends_on"]=["old"]
        r.append(dict(r[0],id="old",status="SUPERSEDED",depends_on=[]))
        self.assertFalse(self.check(p,r)["ready_for_review"])


if __name__=="__main__":
    unittest.main()
