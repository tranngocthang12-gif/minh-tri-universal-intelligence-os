# MINH TRI — Bounded anti-repetition learning gate (candidate, 2026-10-10)

Status: CLASS_S_CANDIDATE / NOT ACCEPTED / NOT MERGED. Stable Universal Learning Continuity Law is unchanged; Foundation V1 FROZEN.

## Observed defect from fourth fresh study chat
Fourth study chat correctly differentiated early-text attestation, synthesis and later Milindapanha support, then repeated previously studied A173 hiri/ottappa, MN 2, MN 4, MN 61 and elephant withdrawal conclusions. It supplied a workplace reporting example and wrote an explicit supplementary comment on PR #351 (#6097675396). It did not answer the exact outstanding PR #341 cursor #6096480057 request to compare Pali lexical expressions in MN 4 and MN 2 sections 2–7 with two translations and a counter-reading. A new example does not mean a new research conclusion or checkpoint completion.

## Design decision
Retain good understanding and encourage deliberate revision/review, but do not confuse repetition or illustrative applications with learning progression. A bounded read-only gate is provided in `src/minhtri/learning_novelty.py`, with independent synthetic unit probes in `tests/test_learning_novelty_v1.py`. Its inputs must be derived from the independently recovered, authority-checked position, and a PINNED reviewed inventory of previously studied claim IDs and primary passage locators. IDs and claimed new evidence are untrusted; this gate checks declared structural difference, not semantic identity. A new label can describe the same claim; that is why all apparently new findings require separate source/semantic review.

For every session: recover active cursor -> list ALREADY_STUDIED and open EXACT_NEXT_QUESTION -> decide whether studying, correction or application is called for -> compare each proposed claim/passage to recorded inventory -> counter-read source and genre -> classify the result. Modes: RESTATEMENT and APPLICATION_EXAMPLE never advance the research cursor; NEW_SOURCE_FINDING and CORRECTION can only become candidate delta eligible when linked to the same exact question digest, a genuinely different *claimed* passage locator, source reference, explicit answer, counter-reading and a declared new/corrected claim. No local selector certifies semantic novelty or Owner acceptance.

If no research progress exists, preserve the exact next question and optionally archive the useful application as application-only evidence; do not increase the checkpoint or pretend that the third-party review succeeded. A valid schema is necessary but not sufficient. This adds NO automatic browser reading, semantic embedding, model training, live GitHub mutation or runtime workflow. Integration into a governed write process and three fresh-chat tests remain future evidence, gated by PR #334 Owner decisions.

## GPT-6.1 option
An available independent model may be a blinded critic for semantic duplicate detection, against source excerpts and inventory. No specific model version is required and no model-only verdict proves truth. A separate seat is useful only if its independence, actual evidence read and disagreement handling are recorded.

## Current legal status
PR #350 is Class S DRAFT; PR #334 routing remains blocked. Do not self-merge, unlock Foundation, claim A173 completed, or write Local Brain. Real-world repetition regression proof is PENDING.
