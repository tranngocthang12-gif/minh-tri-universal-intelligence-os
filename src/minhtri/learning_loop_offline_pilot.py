"""Read-only contract for one Owner-directed learning proposal, not a learner."""
import hashlib
import json
import unicodedata
from minhtri.knowledge_fast_lane import validate_fast_lane_change, REQUIRED_FIELDS, ALLOWED_CLASSES

def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def record_digest(value):
    """Canonical local digest; no guarantee of external-source authenticity."""
    try:
        data=json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(",",":"),allow_nan=False)
    except (TypeError,ValueError,OverflowError):
        return None
    return digest(data)

def normalized_id(value):
    return unicodedata.normalize("NFKC", value).strip().casefold() if isinstance(value,str) else ""

def dependency_closure(records, root):
    """Bounded closure; all supporting atoms need valid status and schema."""
    errors=[]
    if len(records) > 500:
        return {}, ["knowledge graph exceeds safe bound"]
    record_ids = [r.get("id") for r in records]
    if len([x for x in record_ids if isinstance(x,str)]) != len(set(x for x in record_ids if isinstance(x,str))):
        errors.append("duplicate knowledge record id")
    table = {r.get("id"):r for r in records if isinstance(r.get("id"),str)}
    relevant={}
    visiting=set()
    visited=set()
    def walk(key):
        if key in visiting:
            errors.append("dependency cycle")
            return
        if key in visited:
            return
        if len(visiting) >= 60:
            errors.append("dependency depth exceeds safe bound")
            return
        obj=table.get(key)
        if not isinstance(obj,dict):
            errors.append("missing knowledge dependency")
            return
        if obj.get("status") not in ({"PENDING_REVIEW"} if key == root else {"ACTIVE"}):
            errors.append("invalid or stale dependency status")
        if (obj.get("schema") != "minhtri-knowledge-atom/v1"
                or not REQUIRED_FIELDS.issubset(obj)
                or obj.get("class") not in ALLOWED_CLASSES):
            errors.append("malformed supporting knowledge atom")
        visiting.add(key)
        refs=obj.get("depends_on",[])
        if not isinstance(refs,list) or any(not isinstance(v,str) or not v for v in refs):
            errors.append("invalid dependency shape")
        else:
            for child in refs:
                if child != root and table.get(child,{}).get("status") != "ACTIVE":
                    errors.append("nonactive dependency")
                walk(child)
        visiting.remove(key)
        visited.add(key)
        relevant[key]=obj
    walk(root)
    return relevant,sorted(set(errors))

def target_digest(packet):
    if not isinstance(packet,dict):
        return None
    keys=("schema","goal_id","domain","producer_id","sources","understanding",
          "transfer","policy","atom_sha256","critic","dependency_closure_sha256","domain_rules_sha256")
    return record_digest({k:( {"id":packet.get("critic",{}).get("id")} if k=="critic" and isinstance(packet.get("critic"),dict) else packet.get(k)) for k in keys})

def inspect(packet, *, authorized_goal_id, records, domain_rule_refs):
    errors=[]
    if (not isinstance(packet,dict) or not isinstance(records,(list,tuple))
            or any(not isinstance(r,dict) for r in records)
            or not isinstance(domain_rule_refs,dict)):
        return {"ready_for_review":False,"reasons":["invalid pilot input shape"],
                "target_digest":None,"understanding_proven":False,
                "behavioral_learning_proven":False,"durable_written":False,
                "automatic_verified":False,"background_runtime_enabled":False,"critic_independence_proven":False,"transfer_precommitment_proven":False}
    if not isinstance(packet.get("producer_id"),str) or not packet["producer_id"].strip():
        errors.append("producer identity declaration missing")
    if (packet.get("schema")!="minhtri-learning-pilot/v1"
            or packet.get("goal_id")!=authorized_goal_id
            or authorized_goal_id != "BUDDHIST-A173"):
        errors.append("unauthorized learning goal")
    expected_rules=[
        "docs/LAW_UNIVERSAL_LEARNING_CONTINUITY_20261004.md",
        "knowledge/schema/KNOWLEDGE_SCHEMA_V1.md",
    ]
    if domain_rule_refs.get("buddhist_thought") != expected_rules:
        errors.append("canonical Buddhist Fast Lane rules mismatch")
    policy=packet.get("policy",{})
    if not isinstance(policy,dict) or policy.get("protected_review") is not True or policy.get("auto_merge") is not False or policy.get("auto_verified") is not False or policy.get("background_runtime") is not False:
        errors.append("unsafe learning policy")
    if authorized_goal_id == "BUDDHIST-A173" and packet.get("domain") != "buddhist_thought":
        errors.append("Buddhist goal domain mismatch")
    source_ids=set()
    roles=set()
    source_roles={}
    sources=packet.get("sources")
    if not isinstance(sources,list) or not sources:
        errors.append("missing source snapshots")
    else:
        for source in sources:
            if not isinstance(source,dict):
                errors.append("invalid source")
                continue
            sid=source.get("id")
            if not isinstance(sid,str) or not sid.strip() or sid in source_ids:
                errors.append("invalid or duplicated source id")
            else:
                source_ids.add(sid)
            text=source.get("text")
            if not isinstance(text,str) or not text or source.get("sha256")!=digest(text):
                errors.append("source integrity mismatch")
            if (not isinstance(source.get("locator"),str) or not source["locator"].strip()
                    or not isinstance(source.get("role"),str) or not source["role"].strip()):
                errors.append("source provenance missing")
            else:
                roles.add(source["role"])
                if isinstance(sid,str): source_roles[sid]=source["role"]
    u=packet.get("understanding")
    if not isinstance(u,dict) or any(not isinstance(u.get(k),str) or not u[k].strip() for k in ("record_id","own_words","alternative","counterexample","limits")):
        errors.append("understanding explanation incomplete")
        rid=""
    else:
        rid=u["record_id"]
        if (not isinstance(u.get("source_ids"),list) or not u["source_ids"]
                or any(not isinstance(x,str) for x in u["source_ids"])
                or not set(u["source_ids"]).issubset(source_ids)):
            errors.append("explanation source references invalid")
    if packet.get("domain") == "buddhist_thought" or authorized_goal_id=="BUDDHIST-A173":
        cited=u.get("source_ids",[]) if isinstance(u,dict) else []
        cited_roles={source_roles.get(sid) for sid in cited if isinstance(sid,str)}
        if not {"EARLY_DISCOURSE","MILINDAPANHA"}.issubset(cited_roles):
            errors.append("Buddhist source hierarchy incomplete")
    if packet.get("domain") == "buddhist" and authorized_goal_id == "BUDDHIST-A173":
        errors.append("legacy Buddhist domain alias not canonical")
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
            if (not isinstance(q,str) or not q.strip()
                or (not isinstance(q,str) or item.get("question_hash")!=digest(q))
                or item.get("frozen_before_answer") is not True
                or not isinstance(item.get("answer"),str) or not item["answer"].strip()):
                errors.append("transfer integrity failure")
            if isinstance(q,str):
                normalized_question=normalized_id(" ".join(q.split()))
                if normalized_question in seen: errors.append("duplicate transfer question")
                seen.add(normalized_question)
            judge=item.get("judge",{})
            if (not isinstance(judge,dict) or not isinstance(judge.get("id"),str)
                    or not judge["id"].strip() or normalized_id(judge.get("id"))==normalized_id(packet.get("producer_id"))
                    or judge.get("verdict")!="PASS"):
                errors.append("separate declared judge required")
    critic=packet.get("critic",{})
    if (not isinstance(critic,dict) or not isinstance(critic.get("id"),str)
            or not critic["id"].strip() or normalized_id(critic.get("id"))==normalized_id(packet.get("producer_id"))
            or critic.get("verdict")!="NO_MATERIAL_DEFECT"
            or target_digest(packet) is None
            or critic.get("target_digest")!=target_digest(packet)):
        errors.append("exact-target separate critic required")
    critic_id=normalized_id(critic.get("id")) if isinstance(critic,dict) else ""
    if isinstance(transfer,list):
        for item in transfer:
            if isinstance(item,dict):
                judge=item.get("judge",{})
                if isinstance(judge,dict) and normalized_id(judge.get("id"))==critic_id:
                    errors.append("critic and transfer judge must be distinct")
    matched=[r for r in records if r.get("id")==rid]
    if len(matched)!=1 or matched[0].get("status")!="PENDING_REVIEW" or matched[0].get("domain")!=packet.get("domain"):
        errors.append("one matching pending knowledge atom required")
    if len(matched)==1:
        atom=matched[0]
        atom_hash=record_digest(atom)
        if atom_hash is None or not isinstance(packet.get("atom_sha256"),str) or len(packet["atom_sha256"])!=64 or any(c not in "0123456789abcdef" for c in packet["atom_sha256"].lower()) or atom_hash!=packet.get("atom_sha256"):
            errors.append("knowledge atom integrity mismatch")
        refs=atom.get("source_refs")
        locators={src["locator"] for src in (sources if isinstance(sources,list) else []) if isinstance(src,dict) and isinstance(src.get("locator"),str)}
        if not isinstance(refs,list) or not refs or any(not isinstance(ref,str) or ref not in locators for ref in refs):
            errors.append("knowledge atom sources not bound to snapshots")
    if len(matched)==1 and matched[0].get("class")=="ATTESTED":
        early={src.get("locator") for src in sources or [] if isinstance(src,dict) and src.get("role")=="EARLY_DISCOURSE"}
        if not (set(matched[0].get("source_refs",[]) if isinstance(matched[0].get("source_refs"),list) else []) & early):
            errors.append("ATTESTED claim lacks cited early discourse")
    if rid:
        closure,closure_errors=dependency_closure(records,rid)
        errors.extend(closure_errors)
        if record_digest(closure) is None or packet.get("dependency_closure_sha256")!=record_digest(closure):
            errors.append("dependency closure integrity mismatch")
        if record_digest(domain_rule_refs) is None or packet.get("domain_rules_sha256")!=record_digest(domain_rule_refs):
            errors.append("domain rules integrity mismatch")
        try:
            gate=validate_fast_lane_change(all_records=records,changed_record_ids=[rid],domain_rule_refs=domain_rule_refs,protected_review_required=True,autonomous_merge=False,self_verified=False)
            errors.extend(gate.reasons)
        except (TypeError,ValueError,KeyError):
            errors.append("malformed knowledge atom rejected by Fast Lane")
    return {"ready_for_review":not errors,"reasons":sorted(set(errors)),"target_digest":target_digest(packet),"understanding_proven":False,"behavioral_learning_proven":False,"durable_written":False,"automatic_verified":False,"background_runtime_enabled":False,"critic_independence_proven":False,"transfer_precommitment_proven":False}
