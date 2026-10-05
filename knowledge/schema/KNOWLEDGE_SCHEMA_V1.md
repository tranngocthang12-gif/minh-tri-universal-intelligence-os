# MINH TRÍ — Knowledge Schema v1 — Phase 3 pilot

**Status:** PILOT / CANDIDATE  
**Purpose:** prove the atom+hub contract on a bounded Buddhist + economics sample before broad migration.

## Atom types

- source
- evidence
- claim
- passage_argument
- application
- outcome

Pilot files use JSON.

Minimum claim fields:
- `schema`;
- `record_type`;
- `id`;
- `domain`;
- `class`;
- `status`;
- `statement`;
- `source_refs`;
- `evidence_refs`;
- `contradicts`;
- `supersedes`;
- `depends_on`;
- `provenance`.

Generic classes:
- `ATTESTED`
- `SYNTHESIS`
- `SECONDARY`
- `UNCERTAIN`
- `REFUTED`

Statuses:
- `ACTIVE`
- `PENDING_REVIEW`
- `UNCERTAIN`
- `DISPUTED`
- `SUPERSEDED`
- `REFUTED`

Domain rules map domain-specific terminology to these generic classes. Buddhist `TEXT_ATTESTED` may map to generic `ATTESTED`, but a project checkpoint that merely reports such a claim is not silently promoted to direct source attestation.

## Hub contract

A hub is Markdown with a machine-readable JSON metadata block:

```
<!-- MINHTRI_META
{...json...}
MINHTRI_META -->
```

Required hub metadata:
- `schema`;
- `hub_type`;
- `id`;
- `domain`;
- `aliases`;
- `depends_on_claims`;
- `status`.

Rules:
- hubs carry nuance, interpretation, argument structure, and open questions;
- hubs do not create active claims that have no atom;
- hubs may cite ACTIVE/UNCERTAIN/DISPUTED atoms;
- hubs must not cite `PENDING_REVIEW` atoms as established support;
- superseding a depended-on claim must make the hub reviewable/stale.

## Dependency safety

- `depends_on` is a semantic dependency between knowledge atoms, not a provenance pointer;
- an `ACTIVE` claim must not semantically depend on an atom whose status is `PENDING_REVIEW`;
- raw/pending audit material may still appear in `source_refs`, `evidence_refs`, or `provenance` without becoming an established dependency;
- promotion review should create a new reviewed claim atom rather than upgrading a whole pending audit by implication.

## Pilot truth boundary

This pilot validates **representation and retrieval mechanics**, not mastery.

The pilot does not:
- rewrite A172;
- upgrade A172 evidence classes;
- verify the full hiri/ottappa lexical question;
- prove economics competence;
- prove system memory;
- prove self-learning.
