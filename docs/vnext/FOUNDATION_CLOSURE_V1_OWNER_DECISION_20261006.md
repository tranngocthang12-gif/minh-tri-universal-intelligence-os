# MINH TRÍ — OWNER DECISION — FOUNDATION CLOSURE v1 — 2026-10-06

**Decision:** APPROVED  
**Owner command:** `DUYỆT FOUNDATION CLOSURE v1 — TIẾN HÀNH THEO THỨ TỰ ĐỀ XUẤT`

## Purpose

Close the minimum architectural foundation required for MINH TRÍ to learn across many domains for years without allowing continuity drift, split authority, stale knowledge dependencies, or architecture growth to scale with knowledge growth.

## Approved execution order

1. **Continuity & Handoff Core v1 proof**
   - finish genuine zero-chat fresh-seat recovery proof;
   - deterministic scorer PASS is necessary but not sufficient;
   - preserve independent fresh-seat execution provenance;
   - only then mark Core v1 DONE.

2. **Single Boot Root v1**
   - one canonical boot entrypoint;
   - route new seats through law -> current state -> task registry -> handoff -> domain/knowledge sources;
   - old compatibility surfaces may remain, but may not override the boot root;
   - salvage/rebase existing PR #265 where useful rather than duplicating architecture.

3. **Semantic Staleness Guard v1**
   - reject writes based on superseded/refuted/disputed semantic dependencies when policy requires freshness;
   - bind task generation/base/scope plus knowledge dependency lineage;
   - fail closed on ambiguous dependency freshness;
   - no workflow-engine expansion.

4. **Knowledge Fast Lane v1**
   - lightweight path for ordinary learning updates;
   - preserve provenance, evidence/status discipline, supersession, domain rules, stale checks, and protected-main review;
   - no self-VERIFIED promotion and no autonomous merge.

5. **Retrieval/Application proof**
   - fresh-seat retrieval against active and superseded/false decoys;
   - later application/correction tests.

6. **Law consolidation**
   - consolidate only after the new mechanisms work;
   - explicit supersession, preserved history.

## Explicit non-goals during Foundation Closure v1

Do not introduce:
- autonomous agents as canonical writers;
- autonomous merge;
- vector/graph database as canonical brain;
- workflow engine;
- microservices/Kubernetes;
- self-modifying runtime;
- additional assurance bureaucracy unless a measured failure requires it.

## Truth boundary

Owner approval authorizes the work sequence. It does not prove any capability.

Current active task remains `ARCH-VNEXT-CONTINUITY-HANDOFF-CORE-V1` until its genuine fresh-seat proof is durably recorded. Later phases may be prepared as bounded candidates, but must not be promoted out of order.

## PC boundary

Foundation Closure v1 steps 1-4 are designed not to require Owner PC unless a specific implementation fact proves otherwise. Local Brain remains a non-canonical sidecar.
