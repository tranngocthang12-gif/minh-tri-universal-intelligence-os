"""Read-only contract for one Owner-directed learning proposal, not a learner."""
import hashlib
import json
from minhtri.knowledge_fast_lane import validate_fast_lane_change

def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def target_digest(packet):
    content={k:packet.get(k) for k in ("goal_id","domain","sources","understanding","transfer")}
    return digest(json.dumps(content,sort_keys=True,ensure_ascii=False,separators=(",",":")))

def inspect(packet, *, authorized_goal_id, records, domain_rule_refs):
    errors=[]
    if packet.get("schema")!="minhtri-learning-pilot/v1" or packet.get("goal_id")!=authorized_goal_id or not authorized_goal_id:
        errors.append("unauthorized learning goal")
    policy=packet.get("policy",{})
    if not isinstance(policy,dict) or policy.get("protected_review") is not True or policy.get("auto_merge") is not False or policy.get("auto_verified") is not False or policy.get("background_runtime") is not False:
        errors.append("unsafe learning policy")
    source_ids=set()
    roles=set()
    sources=packet.get("sources")
    if not isinstance(sources,list) or not sources:
        errors.append("missing source snapshots")
    else:
        for source in sources:
            if not isinstance(source,dict):
                errors.append("invalid source")
                continue
            sid=source.get("id")
            if not isinstance(sid,str) or not sid or sid in source_ids:
                errors.append("invalid or duplicated source id")
            else:
                source_ids.add(sid)
            text=source.get("text")
            if not isinstance(text,str) or not text or source.get("sha256")!=digest(text):
                errors.append("source integrity mismatch")
            if not source.get("locator") or not source.get("role"):
                errors.append("source provenance missing")
            else:
                roles.add(source["role"])
    u=packet.get("understanding")
    if not isinstance(u,dict) or any(not isinstance(u.get(k),str) or not u[k].strip() for k in ("record_id","own_words","alternative","counterexample","limits")):
        errors.append("understanding explanation incomplete")
        rid=""
    else:
        rid=u["record_id"]
        if not u.get("source_ids") or not set(u["source_ids"]).issubset(source_ids):
            errors.append("explanation source references invalid")
    if packet.get("domain")=="buddhist" and not {"EARLY_DISCOURSE","MILINDAPANHA"}.issubset(roles):
        errors.append("Buddhist source hierarchy incomplete")
    transfer=packet.get("transfer")
    if not isinstance(transfer,list) or len(transfer)<2:
        errors.append("two frozen transfer questions required")
    else:
        seen=set()
        for item in transfer:
            if not isinstance(item,dict):
                errors.append("invalid transfer check")
                continue
            q=item.get("question")
            if not isinstance(q,str) or not q or item.get("question_hash")!=digest(q) or item.get("frozen_before_answer") is not True or not item.get("answer"):
                errors.append("transfer integrity failure")
            if q in seen:
                errors.append("duplicate transfer question")
            seen.add(q)
            judge=item.get("judge",{})
            if not isinstance(judge,dict) or not judge.get("id") or judge.get("id")==packet.get("producer_id") or judge.get("verdict")!="PASS":
                errors.append("separate declared judge required")
    critic=packet.get("critic",{})
    if not isinstance(critic,dict) or critic.get("id") in (None,"",packet.get("producer_id")) or critic.get("verdict")!="NO_MATERIAL_DEFECT" or critic.get("target_digest")!=target_digest(packet):
        errors.append("exact-target separate critic required")
    matched=[r for r in records if r.get("id")==rid]
    if len(matched)!=1 or matched[0].get("status")!="PENDING_REVIEW" or matched[0].get("domain")!=packet.get("domain"):
        errors.append("one matching pending knowledge atom required")
    if rid:
        gate=validate_fast_lane_change(all_records=records,changed_record_ids=[rid],domain_rule_refs=domain_rule_refs,protected_review_required=True,autonomous_merge=False,self_verified=False)
        errors.extend(gate.reasons)
    return {"ready_for_review":not errors,"reasons":sorted(set(errors)),"target_digest":target_digest(packet),"understanding_proven":False,"behavioral_learning_proven":False,"durable_written":False,"automatic_verified":False,"background_runtime_enabled":False}
