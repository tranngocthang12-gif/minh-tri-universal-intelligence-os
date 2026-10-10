#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVE_STATUSES = {"IN_PROGRESS", "BLOCKED", "REPORTED", "REVIEWED_REVISE", "STALE"}
A173_DRAFT_REF = "docs/learning/BUDDHIST_THOUGHT_CHECKPOINT_A173_DRAFT_20261005.md"
REQUIRED_F3_KEYS = frozenset(["INTAKE_26D_GROK_HIGH_BRANCH_BASE","INTAKE_26D_CODEX_MEDIUM_BRANCH_BASE","INTAKE_26D_CLAUDE_MEDIUM_BRANCH_BASE","INTAKE_26D_CLAUDE_MEDIUM_DEPENDENT_DRAFTS","INTAKE_26D_CLAUDE_MEDIUM_CLASS_S_AUTHORIZATION","INTAKE_951_CLAUDE_F1_MEDIUM_EXECUTION_REF","INTAKE_951_CLAUDE_F2_MEDIUM_POST_MERGE_RECOVERY","INTAKE_951_CLAUDE_F3_MEDIUM_VERBATIM_INTAKE"])



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
    normalized = p[:-1] if p.endswith('/') else p
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
            'LAW_', 'OWNER_', 'ONE_DOOR_', 'GITHUB_FIRST_ROLE_BOOTSTRAP_',
            'PROJECT_STATE', 'RECOVERY_MANIFEST', 'ARCHITECTURE_',
        )):
            return True
    return False


def false_a173_positive_claim(value):
    """Conservative negative gate for contradictory A173 claims, NOT an acceptance authenticator."""
    if not isinstance(value, str):
        return False
    patterns = (
        re.compile(
            r"\bA173\b\s+(?:checkpoint\s+)?"
            r"(?:(?:is\s+both\s+DRAFT\s+and|status\s+is|is|was|has\s+been|marked\s+as|now)\s+)?"
            r"\b(?:COMPLETED|ACCEPTED|VERIFIED|GRANTED)\b", re.IGNORECASE
        ),
        re.compile(
            r"\bA173\b[^.!?;\n]{0,120}?\bđã\s+(?:được\s+)?"
            r"(?:\w+\s+){0,6}?"
            r"(?:nghiệm\s+thu|chấp\s+nhận|hoàn\s+thành|hoàn\s+tất)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(?:Owner\s+)?đã\s+(?:nghiệm\s+thu|chấp\s+nhận|hoàn\s+tất)"
            r"(?:\s+và\s+hoàn\s+tất)?\s+(?:checkpoint\s+)?\bA173\b",
            re.IGNORECASE,
        ),
    )
    qualifier = re.compile(
        r"(?:\b(?:before|until|unless|if|when)\b|không\s+được\s+nói|"
        r"đừng\s+nói|chưa\s+được|không\s+được)(?:\s+\S+){0,9}\s*$",
        re.IGNORECASE,
    )
    for line in value.splitlines():
        for clause in re.split(r"[.!?;]", line):
            for pattern in patterns:
                for hit in pattern.finditer(clause):
                    if qualifier.search(clause[:hit.start()].strip()):
                        continue
                    if re.search(r"\b(?:NOT|NEVER|NO|chưa|không)\b",
                                 hit.group(), re.IGNORECASE):
                        continue
                    return True
    return False


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
    records = registry["tasks"]
    ids = [t["task_id"] for t in records]
    if len(ids) != len(set(ids)):
        fail(errors, "duplicate task_id in canonical registry")
    tasks = {t["task_id"]: t for t in records}
    for record in records:
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
    if current.get("active_workstream") == "OWNER_DIRECTED_LEARNING" and current.get("active_task_id") != "BUDDHIST-A173":
        fail(errors, "Buddhist learning route cannot silently change its task ID")
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
                sections = text.splitlines()
                next_headings = [i for i, line in enumerate(sections) if line.strip() == "## NEXT ACTION"]
                if len(next_headings) != 1:
                    fail(errors, "active handoff must have exactly one NEXT ACTION heading")
                else:
                    following = sections[next_headings[0] + 1:]
                    first_action = next((line.strip() for line in following if line.strip()), None)
                    if first_action is None or first_action.startswith("## "):
                        fail(errors, "active handoff NEXT ACTION is empty")
                    elif first_action != task.get("next_action"):
                        fail(errors, "active handoff NEXT ACTION does not match task.next_action")


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
            fail(errors, "routing Class S candidate phase is not pending")
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
            lines = body.splitlines()
            heads = [i for i, line in enumerate(lines)
                     if line.strip() == "## NEXT ACTION"]
            if len(heads) != 1:
                fail(errors, "routing Class S handoff must have exactly one NEXT ACTION")
            else:
                tail = lines[heads[0] + 1:]
                first = next((line.strip() for line in tail if line.strip()), None)
                if first != routing.get("next_action"):
                    fail(errors, "routing Class S handoff NEXT ACTION mismatch")

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
