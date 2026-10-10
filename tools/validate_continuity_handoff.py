#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVE_STATUSES = {"IN_PROGRESS", "BLOCKED", "REPORTED", "REVIEWED_REVISE", "STALE"}
A173_DRAFT_REF = "docs/learning/BUDDHIST_THOUGHT_CHECKPOINT_A173_DRAFT_20261005.md"
REQUIRED_F3_KEYS = frozenset(["INTAKE_26D_GROK_HIGH_BRANCH_BASE","INTAKE_26D_CODEX_MEDIUM_BRANCH_BASE","INTAKE_26D_CLAUDE_MEDIUM_BRANCH_BASE","INTAKE_26D_CLAUDE_MEDIUM_DEPENDENT_DRAFTS","INTAKE_26D_CLAUDE_MEDIUM_CLASS_S_AUTHORIZATION","INTAKE_951_CLAUDE_F1_MEDIUM_EXECUTION_REF","INTAKE_951_CLAUDE_F2_MEDIUM_POST_MERGE_RECOVERY","INTAKE_951_CLAUDE_F3_MEDIUM_VERBATIM_INTAKE"])


# Schema seal applies only to the current pre-merge Class S candidate.
CANDIDATE_CURRENT_KEYS = frozenset({
    "schema",
    "project",
    "architecture_generation",
    "phase",
    "durable_continuity_authority",
    "current_architecture",
    "law_precedence",
    "role_bootstrap",
    "active_workstream",
    "next_checkpoint",
    "autonomous_learning_runtime",
    "automatic_self_critique_runtime",
    "meta_learning_runtime",
    "pc_local_brain_role",
    "owner_learning_priority_order",
    "authority_scope",
    "active_task_id",
    "boot_root",
    "task_registry",
    "master_blueprint",
    "foundation_status",
})
CANDIDATE_A173_KEYS = frozenset({
    "task_id",
    "title",
    "status",
    "scope",
    "branch",
    "base_sha",
    "requires",
    "dependencies",
    "supersedes",
    "result_ref",
    "change_class",
    "resume_gate",
    "acceptance_authority",
    "holder",
    "role",
    "handoff_ref",
    "next_action",
    "blocker",
    "branch_binding",
    "role_detail",
    "learning_checkpoint",
})
CANDIDATE_ROUTING_KEYS = frozenset({
    "task_id",
    "title",
    "status",
    "scope",
    "branch",
    "base_sha",
    "requires",
    "dependencies",
    "supersedes",
    "result_ref",
    "handoff_ref",
    "change_class",
    "acceptance_authority",
    "holder",
    "next_action",
    "blocker",
    "resume_gate",
    "review_packet_ref",
    "role",
    "post_merge_validation_gate",
    "prior_review_intake",
    "material_findings_owner_gate",
    "post_merge_witness",
    "candidate_gate_phase",
})
CANDIDATE_BASE_SHA = "a5ed9d8347a60b95503fe2e5de6b95fd8375eb76"


def unsafe_class_d_path(p):
    """Registry scope guard only: deny ambiguous paths and protected root areas.

    This does not compare actual PR changed files to authorized task scopes.
    """
    if not isinstance(p, str) or not p or p.startswith(("/", "~")):
        return True
    if any(ch in p for ch in ('\\', '%', '*', '?', '[', ']', '{', '}')):
        return True
    if ':' in p.split('/', 1)[0]:
        return True
    normalized = (p[:-1] if p.endswith('/') else p).casefold()
    parts = normalized.split('/')
    if any(not part or part in ('.', '..') for part in parts):
        return True
    if len(parts) == 1 and parts[0] in ('docs', 'state', 'tools', 'tests', 'src', 'runtime', '.github'):
        return True
    if parts[0] in ('state', 'tools', 'tests', 'src', 'runtime', '.github'):
        return True
    if parts[0] == 'docs':
        if len(parts) < 2:
            return True
        if parts[1] == 'vnext' or parts[1].startswith((
            'law_', 'owner_', 'one_door_', 'github_first_role_bootstrap_',
            'project_state', 'recovery_manifest', 'architecture_',
        )):
            return True
    return False


def false_a173_positive_claim(value):
    """Bounded textual contradiction alert; NEVER Owner identity authentication."""
    if not isinstance(value, str):
        return False
    expressions = (
        r"\bA173\b\s*(?:[:\u2014-]\s*)?"
        r"(?:(?:is\s+(?:now\s+|both\s+DRAFT\s+and\s+)?|was\s+|"
        r"has\s+been\s+|status\s+is\s+|marked\s+(?:as\s+)?))?"
        r"(?:COMPLETED|ACCEPTED|VERIFIED|GRANTED|complete|DONE)\b",
        r"\bA173\b\s*\(\s*(?:COMPLETED|ACCEPTED|VERIFIED|GRANTED|DONE)\s*\)",
        r"\bA173\b\s+(?:but|yet|and)\s+(?:it\s+)?is\s+"
        r"(?:COMPLETED|ACCEPTED|VERIFIED|GRANTED|DONE)\b",
        r"\bA173\b\s+được\s+(?:nghiệm\s+thu|chấp\s+nhận)\b",
        r"\b(?:Owner\s+)?(?:has\s+)?(?:accepted|approved|verified)"
        r"\s+(?:checkpoint\s+)?\bA173\b",
        r"\bA173\b[^.!?;\n]{0,100}?\b(?:đã\s+(?:được\s+)?(?:Owner\s+)?"
        r"(?:nghiệm\s+thu|chấp\s+nhận|hoàn\s+thành|hoàn\s+tất|"
        r"qua\s+nghiệm\s+thu|duyệt))\b",
        r"\bOwner\s+đã\s+(?:nghiệm\s+thu|duyệt|chấp\s+nhận|hoàn\s+tất)"
        r"(?:\s+và\s+hoàn\s+tất)?\s+(?:checkpoint\s+)?\bA173\b",
    )
    patterns = [re.compile(expr, re.IGNORECASE) for expr in expressions]
    conditional = re.compile(
        r"^\s*(?:[-*]\s*)?(?:(?:before|after|when|if|once|until|only\s+if)\b"
        r"|(?:khi|sau\s+khi|nếu|chỉ\s+khi)\b)", re.IGNORECASE,
    )
    prohibition = re.compile(
        r"(?:không\s+được\s+nói|đừng\s+nói|do\s+not\s+(?:say|claim)"
        r"|never\s+(?:say|claim))\s*$", re.IGNORECASE,
    )
    for line in value.splitlines():
        for clause in re.split(r"[.!?;,]", line):
            clause = clause.replace("\u2019", "\u0027").replace("\u2018", "\u0027")
            # Text is only an advisory contradiction signal, never receipt authority.
            # Strip narrowly recognized negated acceptance before testing positives.
            clause = re.sub(
                r"\bOwner\s+(?:has\s+not|hasn't|has\s+not\s+yet)\s+accepted\s+(?:checkpoint\s+)?A173\b",
                "A173", clause, flags=re.IGNORECASE,
            )
            if conditional.search(clause):
                continue
            for pattern in patterns:
                for match in pattern.finditer(clause):
                    if prohibition.search(clause[:match.start()]):
                        continue
                    return True
    return False


def next_action_line(body):
    """A handoff has one operational action, not a hidden second directive."""
    lines = body.splitlines()
    marks = [i for i, line in enumerate(lines) if line.strip() == "## NEXT ACTION"]
    if len(marks) != 1:
        return None
    section = []
    for line in lines[marks[0] + 1:]:
        if line.strip().startswith("#"):
            break
        if line.strip():
            section.append(line.strip())
    return section[0] if len(section) == 1 else None


def forged_routing_approval(value):
    """Bounded candidate guard; structured receipts remain decisive."""
    if not isinstance(value, str):
        return False
    return bool(re.search(
        r"(?:Owner\s+(?:has\s+)?(?:accepted|approved|authorized)\s+(?:Class\s*S|PR\s*#?334)"
        r"|(?:merge\s+(?:PR\s*#?334\s+)?now|merge\s+authorized|Owner\s+acceptance\s+already\s+given)"
        r"|(?:Owner\s+đã\s+(?:duyệt|nghiệm\s+thu)\s+(?:Class\s*S|PR\s*#?334)))",
        value, re.IGNORECASE,
    ))


def evaluate_class_s_transition(*, phase, reviewed_head, expected_head, ci_head,
                                owner_receipt=None, merge_receipt=None,
                                witness_receipt=None, closure_receipt=None,
                                verify_owner=None, verify_merge=None,
                                verify_witness=None, verify_closure=None):
    """Evidence gate, not an approval issuer.

    Verifier callbacks must read independently trusted evidence OUTSIDE this
    candidate branch. Fixture callbacks have zero real-world authority.
    """
    if not expected_head or reviewed_head != expected_head or ci_head != expected_head:
        return False, "reviewed HEAD / CI mismatch"
    if not isinstance(owner_receipt, dict) or owner_receipt.get("head_sha") != expected_head:
        return False, "missing or stale Owner receipt"
    if owner_receipt.get("actor_role") == "BUILDER":
        return False, "Builder cannot self-approve"
    if not callable(verify_owner) or not verify_owner(owner_receipt):
        return False, "Owner evidence unverified by independent trust source"
    if phase == "PRE_MERGE":
        return True, "pre-merge prerequisites verified externally, NOT merged"
    if not isinstance(merge_receipt, dict) or merge_receipt.get("reviewed_head_sha") != expected_head:
        return False, "missing/mismatched protected merge receipt"
    if not merge_receipt.get("merged_main_sha") or not callable(verify_merge) or not verify_merge(merge_receipt):
        return False, "merge main SHA unverified externally"
    if phase not in {"POST_MERGE_WITNESS", "CLOSURE"}:
        return False, "unsupported transition phase"
    if not isinstance(witness_receipt, dict) or witness_receipt.get("merged_main_sha") != merge_receipt["merged_main_sha"]:
        return False, "independent witness absent or wrong merged SHA"
    if not callable(verify_witness) or not verify_witness(witness_receipt):
        return False, "witness evidence unverified externally"
    if witness_receipt.get("actor_role") in {"BUILDER", "OWNER"}:
        return False, "witness is not an independent validation seat"
    if phase == "POST_MERGE_WITNESS":
        return True, "post-merge witness evidence eligible, NOT closure"
    if not isinstance(closure_receipt, dict) or closure_receipt.get("merged_main_sha") != merge_receipt["merged_main_sha"]:
        return False, "missing/mismatched closure receipt"
    if closure_receipt.get("actor_id") == witness_receipt.get("actor_id"):
        return False, "witness cannot self-close"
    if not callable(verify_closure) or not verify_closure(closure_receipt):
        return False, "separate protected closure receipt unverified"
    return True, "independent three-phase evidence eligible, not self-authorization"


def _unique_json_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("duplicate JSON key: " + key)
        obj[key] = value
    return obj


def load_json(rel):
    return json.loads(
        (ROOT / rel).read_text(encoding="utf-8"),
        object_pairs_hook=_unique_json_object,
    )

def fail(errors, msg):
    errors.append(msg)

def main():
    errors = []
    try:
        current = load_json("state/current.yaml")
        registry = load_json("state/tasks.yaml")
    except (ValueError, OSError, UnicodeError) as exc:
        print("CONTINUITY_HANDOFF_CORE_V1_FAIL")
        print(f"- canonical state/task invalid: {exc}")
        return 1
    if set(current) != CANDIDATE_CURRENT_KEYS:
        fail(errors, "current candidate schema has unexpected or missing fields")
    records = registry["tasks"]
    ids = [t["task_id"] for t in records]
    if len(ids) != len(set(ids)):
        fail(errors, "duplicate task_id in canonical registry")
    tasks = {t["task_id"]: t for t in records}
    for record in records:
        record_id = record.get("task_id")
        if record_id in {"BUDDHIST-A173", "ARCH-BUDDHIST-A173-ROUTING-V1"}:
            schema_keys = (CANDIDATE_A173_KEYS if record_id == "BUDDHIST-A173"
                           else CANDIDATE_ROUTING_KEYS)
            if set(record) != schema_keys:
                fail(errors, f"{record_id} candidate schema has unexpected or missing fields")
            base = record.get("base_sha")
            if (not isinstance(base, str) or re.fullmatch(r"[0-9a-f]{40}", base) is None
                    or base != CANDIDATE_BASE_SHA):
                fail(errors, f"{record_id} base_sha is not bound to the approved candidate base")
        if record.get("change_class") == "D":
            scope = record.get("scope")
            if not isinstance(scope, list):
                fail(errors, "Class D requires explicit scope list")
            elif any(unsafe_class_d_path(p) for p in scope):
                fail(errors, "Class D cannot edit canonical architecture or law")
            if record.get("task_id") == "BUDDHIST-A173" and isinstance(scope, list):
                if not scope or any(not isinstance(p, str) or not p.startswith("docs/learning/") for p in scope):
                    fail(errors, "A173 Class D scope must remain inside docs/learning/")
        checkpoint = record.get("learning_checkpoint")
        if checkpoint is not None:
            if record.get("task_id") != "BUDDHIST-A173":
                fail(errors, "shadow A173 learning checkpoint task")
            elif not isinstance(checkpoint, dict) or set(checkpoint) != {
                "current_checkpoint_id", "checkpoint_acceptance",
                "last_accepted_checkpoint_id", "last_accepted_checkpoint_ref",
                "acceptance_receipt_ref"
            }:
                fail(errors, "A173 checkpoint shadow/missing schema fields")
        if re.fullmatch(r"BUDDHIST-A17[3-7](?:[-_].+)?", str(record.get("task_id", ""))):
            if record.get("task_id") != "BUDDHIST-A173" and (
                (isinstance(record.get("status"), str) and record["status"].upper() in {"DONE", "COMPLETED", "ACCEPTED", "VERIFIED", "GRANTED"}) or checkpoint is not None
            ):
                fail(errors, "unreceipted A173-dependent checkpoint promotion")
        if record.get("task_id") == "BUDDHIST-A173":
            if record.get("result_ref") != A173_DRAFT_REF:
                fail(errors, "A173 result_ref must point to the existing canonical A173 DRAFT source")
            else:
                draft_path = ROOT / A173_DRAFT_REF
                if not draft_path.is_file():
                    fail(errors, "A173 result_ref DRAFT source is missing")
                else:
                    draft_text = draft_path.read_text(encoding="utf-8")
                    statuses = [
                        line.split("**Status:**", 1)[1].strip()
                        for line in draft_text.splitlines()
                        if line.lstrip().startswith("**Status:**")
                    ]
                    if (not draft_text.startswith("# Buddhist Thought Checkpoint A173 — DRAFT")
                            or statuses != ["DURABLE DRAFT / NOT CURRENT / NOT AUTOMATICALLY VERIFIED"]):
                        fail(errors, "A173 result_ref is not an unaccepted DRAFT source")
                    if false_a173_positive_claim(draft_text):
                        fail(errors, "A173 DRAFT source falsely claims checkpoint acceptance")
    # No global hard-pin to BUDDHIST-A173: Owner may govern a future track
    # change through protected state/task review. This validator checks shape
    # only; actor separation and acceptance require an external Owner gate.
    if "ARCH-BUDDHIST-A173-ROUTING-V1" not in tasks:
        fail(errors, "Class S routing gate missing")


    active_id = current.get("active_task_id")
    if not active_id:
        fail(errors, "current.active_task_id missing")
    elif active_id not in tasks:
        fail(errors, f"active_task_id not found in registry: {active_id}")
    else:
        task = tasks[active_id]
        if task.get("status") not in ACTIVE_STATUSES:
            fail(errors, f"active task status is not active: {task.get('status')}")
        if task.get("change_class") not in {"F", "S", "D", "O"}:
            fail(errors, "active task change_class is not authorized")
        authority = task.get("acceptance_authority")
        if not isinstance(authority, str) or not authority.strip():
            fail(errors, "active task acceptance_authority is missing")
        elif task.get("holder") == authority or authority.strip().lower() in {"builder", "builder/implementer"}:
            fail(errors, "active task holder/Builder cannot self-approve")
        if current.get("active_workstream") == "OWNER_DIRECTED_LEARNING" and task.get("change_class") != "D":
            fail(errors, "learning workstream must route to Class D study task")
        # No Owner-approved Class D delegate exists in this candidate scope.
        if active_id == "BUDDHIST-A173" and authority != "OWNER":
            fail(errors, "A173 acceptance authority lacks verified Owner designation")
        if task.get("next_action") and current.get("next_checkpoint") != task.get("next_action"):
            fail(errors, "current.next_checkpoint does not match active task.next_action")
        if active_id == "BUDDHIST-A173" and (
                false_a173_positive_claim(task.get("next_action"))
                or false_a173_positive_claim(current.get("next_checkpoint"))):
            fail(errors, "A173 next action falsely claims checkpoint completion")
        if active_id == "BUDDHIST-A173":
            # No branch mutation is authorized by this Class S routing candidate.
            if task.get("branch") is not None:
                fail(errors, "A173 execution branch requires separate Owner-authorized Class D binding")
            if task.get("branch_binding") != "NONE_NO_EXECUTION_REF_UNTIL_OWNER_APPROVED_ASSIGNMENT":
                fail(errors, "A173 unbound routing policy was changed without authorized binding")
            checkpoint = task.get("learning_checkpoint")
            expected = {
                "current_checkpoint_id": "A173",
                "checkpoint_acceptance": "NOT_CURRENT",
                "last_accepted_checkpoint_id": "A172",
                "last_accepted_checkpoint_ref": "docs/learning/BUDDHIST_THOUGHT_CHECKPOINT_A172_20261005.md",
                "acceptance_receipt_ref": None,
            }
            if not isinstance(checkpoint, dict):
                fail(errors, "A173 structured checkpoint state missing")
            else:
                for key, value in expected.items():
                    if checkpoint.get(key) != value:
                        fail(errors, f"A173 checkpoint {key} cannot claim acceptance without Owner receipt")
                checkpoint_ref = checkpoint.get("last_accepted_checkpoint_ref")
                if checkpoint_ref and not (ROOT / checkpoint_ref).is_file():
                    fail(errors, "A172 accepted checkpoint reference is missing")
        for field in ("scope", "base_sha", "result_ref", "handoff_ref", "next_action"):
            if task.get(field) in (None, "", []):
                fail(errors, f"active task missing {field}")
        if task.get("status") in {"BLOCKED", "STALE"} and not task.get("blocker"):
            fail(errors, "blocked/stale active task missing blocker")
        handoff_ref = task.get("handoff_ref")
        if handoff_ref:
            handoff_path = ROOT / handoff_ref
            if not handoff_path.exists():
                fail(errors, f"handoff_ref missing file: {handoff_ref}")
            else:
                text = handoff_path.read_text(encoding="utf-8")
                m = re.search(r"\*\*TASK_ID:\*\*\s*([^\s]+)", text)
                if not m:
                    fail(errors, "handoff missing TASK_ID")
                elif m.group(1).strip() != active_id:
                    fail(errors, f"handoff TASK_ID mismatch: {m.group(1).strip()} != {active_id}")
                for heading in ("## DONE", "## NOT DONE", "## NEXT ACTION", "## REQUIRED GATES"):
                    if heading not in text:
                        fail(errors, f"handoff missing heading {heading}")
                first_action = next_action_line(text)
                if first_action is None:
                    fail(errors, "active handoff must have exactly one NEXT ACTION line")
                elif first_action != task.get("next_action"):
                    fail(errors, "active handoff NEXT ACTION does not match task.next_action")
                if forged_routing_approval(task.get("next_action")):
                    fail(errors, "active task claims unauthorized Owner/merge approval")


    # No static repository field authenticates an external Owner comment or merge.
    # A post-merge Class S closure needs a separately reviewed receipt-bound change.
    routing = tasks.get("ARCH-BUDDHIST-A173-ROUTING-V1")
    if active_id == "BUDDHIST-A173" and routing is None:
        fail(errors, "A173 routing Class S control task missing")
    if routing is not None:
        gate = routing.get("material_findings_owner_gate")
        witness = routing.get("post_merge_witness")
        if routing.get("change_class") != "S" or routing.get("acceptance_authority") != "OWNER":
            fail(errors, "routing Class S authority mismatch")
        if routing.get("holder") == routing.get("acceptance_authority"):
            fail(errors, "routing Builder cannot be Owner acceptance authority")
        if routing.get("candidate_gate_phase") != "PRE_MERGE_UNACCEPTED_SNAPSHOT":
            # DESIGN_ONLY: the static validator has no independently trusted
            # Owner/merge/witness receipt provider. Fail closed without faking
            # a transition call with None inputs or a misleading HEAD error.
            fail(errors, "routing Class S candidate phase is not pending; external evidence verifier not configured (DESIGN_ONLY)")
        if routing.get("status") != "IN_PROGRESS":
            fail(errors, "routing Class S closure requires separate protected evidence")
        if not isinstance(gate, dict) or gate.get("owner_acceptance") != "NOT_GRANTED" or gate.get("status") != "OWNER_PER_FINDING_DISPOSITION_PENDING":
            fail(errors, "routing Class S approval cannot be self-asserted in candidate snapshot")
        if isinstance(gate, dict):
            keys = gate.get("provisional_intake_keys")
            if not isinstance(keys, list) or len(keys) != 8 or set(keys) != REQUIRED_F3_KEYS:
                fail(errors, "routing Class S exact eight historical risk identities changed")
            if set(gate) != {"status","source","provisional_intake_keys","required_disposition_each",
                             "originals_or_attestation","missing_verbatim_originals",
                             "gate_3_build_before_task_authorize","owner_acceptance"}:
                fail(errors, "routing Class S shadow approval/provenance fields forbidden")
            if (gate.get("originals_or_attestation") != "OWNER_REPORTED_ORIGINALS_LOST_NO_SUMMARY_COMPLETENESS_ATTESTATION_FRESH_INDEPENDENT_EXACT_HEAD_REVIEW_AND_OWNER_RESIDUAL_RISK_DECISION_REQUIRED"
                    or gate.get("missing_verbatim_originals") != "OWNER_REPORTED_LOST_HISTORICAL_COMPLETENESS_UNVERIFIABLE_PROVENANCE_LIMITATION_OPEN"):
                fail(errors, "routing Class S lost F3 originals cannot be marked verified")
            if (gate.get("source") != "OWNER_CHAT_BUILDER_SUMMARY_UNVERIFIED_NOT_ORIGINAL_CRITIC_RECEIPTS"
                    or gate.get("required_disposition_each") != "OWNER_REPAIR_CONFIRMED_OR_EXPLICIT_REJECTION_WITH_EVIDENCE"):
                fail(errors, "routing Class S F3 source/disposition cannot claim approval")
            if gate.get("gate_3_build_before_task_authorize") != "OWNER_CHAT_ONE_TIME_GATE3_EXCEPTION_RELAYED_PR334_COMMENT_6076001277_NOT_CLASS_S_ACCEPTANCE":
                fail(errors, "routing Class S Gate 3 exception cannot be expanded")
        if (not isinstance(witness, dict)
                or set(witness) != {
                    "assignment_authority", "evidence_role", "witness_holder",
                    "closure_holder", "assignment_condition", "merge_commit_evidence",
                    "witness_status", "closure_method",
                    "builder_self_certification_allowed", "pre_merge_status_interpretation",
                }
                or witness.get("assignment_authority") != "OWNER"
                or witness.get("evidence_role") != "Evidence/Validation"
                or witness.get("assignment_condition") != "OWNER_MUST_NAME_REPLACEABLE_INDEPENDENT_EVIDENCE_SEAT_AND_CLASS_S_CLOSURE_SEAT_AT_EXACT_HEAD_ACCEPTANCE"
                or witness.get("merge_commit_evidence") != [
                    "reviewed_head_sha", "owner_acceptance_comment_id",
                    "exact_head_ci_run_id",
                ]
                or witness.get("witness_status") != "NOT_CLAIMED_BY_THIS_CANDIDATE"
                or witness.get("witness_holder") is not None
                or witness.get("closure_holder") is not None
                or witness.get("closure_method") != "SEPARATE_PROTECTED_CLASS_S_TASK_STATE_CHANGE"
                or witness.get("pre_merge_status_interpretation") != "AFTER_ACCEPTED_MERGE_HISTORICAL_PRE_MERGE_SNAPSHOTS_SUPERSEDED_BY_DURABLE_OWNER_DECISION_AND_PROTECTED_MERGE_RECEIPT"
                or witness.get("builder_self_certification_allowed") is not False):
            fail(errors, "routing Class S witness/closure cannot be self-certified")
        handoff = routing.get("handoff_ref")
        if not handoff or not (ROOT / handoff).is_file():
            fail(errors, "routing Class S handoff absent")
        else:
            body = (ROOT / handoff).read_text(encoding="utf-8")
            if f"**TASK_ID:** {routing['task_id']}" not in body or "## NOT DONE" not in body:
                fail(errors, "routing Class S handoff contract missing")
            if false_a173_positive_claim(body):
                fail(errors, "routing Class S handoff falsely claims A173 completion")
            first = next_action_line(body)
            if first is None:
                fail(errors, "routing Class S handoff must have exactly one NEXT ACTION line")
            elif first != routing.get("next_action"):
                fail(errors, "routing Class S handoff NEXT ACTION mismatch")
            if forged_routing_approval(routing.get("next_action")):
                fail(errors, "routing Class S next_action claims unauthorized Owner/merge approval")

    if active_id == "BUDDHIST-A173" and active_id in tasks:
        ref = tasks[active_id].get("handoff_ref")
        if ref and (ROOT / ref).is_file():
            body = (ROOT / ref).read_text(encoding="utf-8")
            expected_handoff = {
                "LAST_ACCEPTED_CHECKPOINT": "A172",
                "CURRENT_CHECKPOINT": "A173",
                "CHECKPOINT_ACCEPTANCE": "NOT_CURRENT",
                "CHECKPOINT_ACCEPTANCE_RECEIPT": "NONE",
            }
            for key, value in expected_handoff.items():
                matches = re.findall(rf"^\*\*{key}:\*\*\s*(\S.*?)\s*$", body, flags=re.MULTILINE)
                if matches != [value]:
                    fail(errors, f"A173 handoff {key} disagrees with unaccepted checkpoint")
            acceptance_lines = re.findall(
                r"(?im)^\s*(?:\*\*CHECKPOINT_ACCEPTANCE:\*\*|CHECKPOINT_ACCEPTANCE\s*:)\s*(.*?)\s*$",
                body,
            )
            if acceptance_lines != ["NOT_CURRENT"]:
                fail(errors, "A173 handoff CHECKPOINT_ACCEPTANCE has duplicate or untrusted assertion")
            if false_a173_positive_claim(body):
                fail(errors, "A173 handoff falsely claims checkpoint completion")

    for field in ("current_architecture", "role_bootstrap"):
        ref = current.get(field)
        if not ref or not (ROOT / ref).exists():
            fail(errors, f"current {field} missing/unreadable: {ref}")

    entry = ROOT / "docs/vnext/continuity/RECOVERY_ENTRYPOINT_V1.md"
    if not entry.exists():
        fail(errors, "recovery entrypoint missing")
    else:
        et = entry.read_text(encoding="utf-8")
        for needle in ("state/current.yaml", "state/tasks.yaml", "active_task_id", "handoff_ref", "next_action"):
            if needle not in et:
                fail(errors, f"recovery entrypoint missing route token: {needle}")

    for t in registry["tasks"]:
        if t.get("status") in {"BLOCKED", "STALE"}:
            if not t.get("next_action"):
                fail(errors, f"{t['task_id']} blocked/stale missing next_action")
            if not t.get("handoff_ref") and t["task_id"].startswith("ARCH-"):
                fail(errors, f"{t['task_id']} blocked/stale architecture task missing handoff_ref")

    if errors:
        print("CONTINUITY_HANDOFF_CORE_V1_FAIL")
        for e in errors:
            print(f"- {e}")
        return 1
    print("CONTINUITY_HANDOFF_CORE_V1_PASS")
    print(f"active_task_id={active_id}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
