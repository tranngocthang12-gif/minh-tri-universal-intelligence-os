# Retrieval/Application Proof v1 handoff

**TASK_ID:** ARCH-RETRIEVAL-APPLICATION-PROOF-V1

## DONE
- Knowledge Fast Lane v1 passed CI and merged through PR #290.
- Retrieval/Application v1 candidate packet, gold, schema, scorer, tests, and fresh-seat command are on the working branch.

## NOT DONE
- The harness is not canonical until CI PASS and merge.
- No fresh-seat graded run has occurred yet.
- Law consolidation remains downstream.

## NEXT ACTION
- Merge this harness only after CI PASS, then run the canonical fresh-seat command outside the MINH TRI project and return the JSON for deterministic grading.

## REQUIRED GATES
- graded seat must be fresh and independent of the authoring chat context;
- gold must not be provided to the graded seat;
- all structured decisions must PASS;
- stale/superseded/decoy support must be rejected;
- durable response + score + provenance receipt required before the proof task is DONE.
