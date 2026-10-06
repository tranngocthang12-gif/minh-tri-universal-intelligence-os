# MINH TRÍ — Knowledge Fast Lane v1 — 2026-10-06

## Purpose

Provide a lightweight protected path for ordinary learning updates while keeping the existing knowledge schema, semantic freshness discipline, and protected-main review.

Fast Lane is a validation contract, not a second authority and not a workflow engine.

## Required disciplines

Every changed knowledge record must preserve:
- schema fields;
- provenance;
- status;
- source/evidence references;
- supersession lineage;
- semantic dependency freshness;
- domain-rule references.

Supersession is explicit: when a new record supersedes an old one, the old target must be marked SUPERSEDED in the same protected update. The validator does not silently rewrite or auto-follow lineage.

## Forbidden

- self-VERIFIED promotion;
- autonomous merge;
- bypass of protected-main review;
- second canonical authority;
- workflow-engine requirement.

## Intended learning flow

ordinary learning -> update bounded knowledge atom/hub -> validate Fast Lane contract -> semantic stale check -> protected review/CI -> merge -> regenerate/read index as needed.

Architecture does not grow merely because knowledge volume grows.

## Truth boundary

This proves the bounded validator and contract behavior. It does not claim autonomous learning or universal enforcement across every future write path.
