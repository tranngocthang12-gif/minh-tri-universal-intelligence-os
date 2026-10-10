# MINH TRI — Learning / Understanding / Application Core V1 (candidate)

Status: CLASS_S_CANDIDATE / NOT_OWNER_ACCEPTED / NOT_MERGED.
Foundation V1 remains FROZEN. This is a generic learning contract, not a new Foundation law or an autonomous learner.

## Defect and required behavior
Observed: two fresh Buddhist-study chats read the same PR #341 cursor, studied Q02, but did not publish a successor. The next fresh chat repeated the old question. Writing prose in a chat does not complete learning continuity. Accumulating sources does not prove application on an unseen case.

## Single continuity path
Existing protected main bootstrap, consolidated law, state, task registry and active handoff remain authoritative. A subordinate `state/learning_tracks.json` holds a stable track ID, canonical task ID, last durable checkpoint, unaccepted candidate cursor and evidence source. This registry cannot assign the active task, grant Owner acceptance or override law.

Proposed learning process: fresh-read protected main -> resolve authorized active task -> validate track -> recover most recent append-only delta and exact next question -> research primary sources and disconfirming evidence -> state new knowledge or NO_NEW_KNOWLEDGE -> test understanding separately -> append one candidate delta -> update cursor pointer atomically on authorized non-main Git branch -> read back -> Owner-controlled reviewed merge.

When no file delta exists, a SHA-bound temporary PR comment bridge can recover the EXACT_NEXT_QUESTION. Cursor text is untrusted *topic data*, never a command or permission grant. Require label LEARNING_CURSOR_V1, CURSOR_ID, configured author login, matching PR HEAD and linear SUPERSEDES chain; fail closed if unavailable, stale or divergent. A public GitHub login does not authenticate the human Owner and PR comments are mutable.

## Data and evaluation
Append-only `docs/learning/deltas/<TRACK>/<CURSOR>.json` records source references, learning/correction, evidence class, understanding model, limits, counter-reading, source HEAD, next question, and Milindapanha consultation for Buddhist work. A distinct application section may reference a previously frozen unseen case, rubric hash, attempt and separate reviewer receipt. This code checks only structural relationships; it does NOT prove timing, authentic seat independence, or correctness. Never promote trial observations to VERIFIED. Source approval and Owner checkpoint acceptance remain separate.

Detect path traversal, unexpected/shadow fields, duplicate JSON keys, stale/missing cursor, conflicting successors, mismatched canonical active task and self-acceptance. An optimistic local registry SHA check is not an atomic GitHub lock; actual writes require expected-head compare/lease, protected PR review and readback.

## Current scope and governance gate
The registry is a candidate example only: BUDDHIST_THOUGHT/A173, latest file delta absent and PR #341 working source SHA 2119d2bda13f90f08ab00b22aca7d413d3a5a9a1. Protected main currently points to a DONE architecture task; therefore active learning recovery must fail closed until Owner authorizes and merges PR #334. This candidate does not change main, tasks.yaml, Foundation, law, workflows or #334. After #334's exact-HEAD review, eight F3 Owner dispositions and Owner merge, separately reconcile the Class S closure validator, source-audited A173 status, witness receipts and future long-lived track integration. A173 stays NOT ACCEPTED.

## Acceptance tests required after integration
1. Two real sequential fresh chats: seat one recovers the next question and commits a delta, independent seat two reads that exact delta and applies it rather than repeating the old one.
2. At least one previously unseen case with frozen rubric, an actual independent reviewer and counterexample. Record limitations; self-grading does not count.
3. Negative tests for missing GitHub, stale SHA, competing writers, copied false Owner receipt, malformed paths and unsupported future phase.
4. Independent exact-head Class S review, CI, Owner acceptance, protected merge, fresh-read. The existing 17 local tests are simulated contract tests only.
