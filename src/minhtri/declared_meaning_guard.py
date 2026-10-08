"""Validate declared meaning invariants for a learning proposal.

This is a structural guard, NOT a natural-language understanding evaluator.
Human/model semantic review of the actual prose remains a separate gate.
No source ingestion, model calls, persistence, authority or autonomy.
"""
from __future__ import annotations

FIELDS = frozenset({
    "claim_id", "proposition", "conditions", "certainty", "relation_type",
    "scope", "source_refs", "nonclaims", "uncertainties", "layer",
})
LIST_FIELDS = ("conditions", "source_refs", "nonclaims", "uncertainties")
TEXT_FIELDS = ("claim_id", "proposition", "certainty", "relation_type", "scope", "layer")
MODALITIES = frozenset({"UNKNOWN", "POSSIBLE", "CONDITIONAL", "ASSERTED"})
RELATIONS = frozenset({"UNSPECIFIED", "ASSOCIATION", "SEQUENCE", "CONDITIONAL", "CAUSAL", "DEFINITION"})
LAYERS = frozenset({"SOURCE_REPORT", "INTERPRETATION", "APPLICATION"})
KINDS = frozenset({"EXPLANATION", "SHORT_FORM", "TEACH_BACK"})


def _text(value):
    return isinstance(value, str) and bool(value.strip()) and len(value) <= 2400


def _string_list(value, *, nonempty=False):
    return (
        isinstance(value, list) and len(value) <= 40
        and (not nonempty or bool(value))
        and all(_text(item) for item in value)
        and len(set(value)) == len(value)
    )


def _valid_frame(frame):
    return (
        isinstance(frame, dict)
        and set(frame) == FIELDS
        and all(_text(frame[field]) for field in TEXT_FIELDS)
        and all(_string_list(frame[field], nonempty=field == "source_refs")
                for field in LIST_FIELDS)
        and frame["certainty"] in MODALITIES
        and frame["relation_type"] in RELATIONS
        and frame["layer"] in LAYERS
    )


def inspect_meaning_annotations(pack, *, atom):
    """Compare declared annotations to the proposed atom and reference.

    Equal annotations cannot prove the displayed prose preserves the meaning.
    A separate independently inspected prose specimen remains mandatory.
    """
    errors = []
    if not isinstance(atom, dict):
        errors.append("MEANING_ATOM_INVALID")
    if not isinstance(pack, dict) or set(pack) != {"schema", "reference", "renderings"}:
        errors.append("MEANING_PACK_INVALID")
        return _out(errors)
    if pack["schema"] != "minhtri-declared-meaning/v1":
        errors.append("MEANING_SCHEMA_INVALID")
    ref = pack["reference"]
    if not _valid_frame(ref):
        errors.append("MEANING_REFERENCE_INVALID")
        return _out(errors)
    if isinstance(atom, dict):
        if ref["claim_id"] != atom.get("id"):
            errors.append("MEANING_CLAIM_ID_MISMATCH")
        if ref["proposition"] != atom.get("statement"):
            errors.append("MEANING_ATOM_PROPOSITION_MISMATCH")
        atom_sources = atom.get("source_refs")
        if not _string_list(atom_sources, nonempty=True) or set(ref["source_refs"]) != set(atom_sources):
            errors.append("MEANING_ATOM_SOURCE_MISMATCH")
    samples = pack["renderings"]
    if not isinstance(samples, list) or not 2 <= len(samples) <= 4:
        errors.append("MEANING_RENDERINGS_REQUIRED")
        return _out(errors)
    used = set()
    for sample in samples:
        if not isinstance(sample, dict) or set(sample) != {"kind", "text", "annotations"}:
            errors.append("MEANING_RENDERING_INVALID")
            continue
        kind = sample["kind"]
        if kind not in KINDS or kind in used:
            errors.append("MEANING_KIND_INVALID")
        elif isinstance(kind, str):
            used.add(kind)
        if not _text(sample["text"]):
            errors.append("MEANING_RENDERING_TEXT_INVALID")
        annotation = sample["annotations"]
        if not _valid_frame(annotation):
            errors.append("MEANING_ANNOTATION_INVALID")
            continue
        for field in sorted(FIELDS):
            if field in LIST_FIELDS:
                different = set(annotation[field]) != set(ref[field])
            else:
                different = annotation[field] != ref[field]
            if different:
                errors.append("MEANING_DRIFT_" + field.upper())
    if not {"EXPLANATION", "SHORT_FORM"}.issubset(used):
        errors.append("MEANING_REPHRASE_KINDS_MISSING")
    return _out(errors)


def _out(errors):
    return {
        "annotation_contract_pass": not errors,
        "reasons": sorted(set(errors)),
        "prose_meaning_verified": False,
        "source_truth_verified": False,
        "independent_review_proven": False,
        "durable_written": False,
        "autonomous_runtime_enabled": False,
    }
