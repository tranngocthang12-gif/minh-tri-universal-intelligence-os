# EARLY BUDDHIST DIALOGUE RECONSTRUCTION v0.5 — 2026-10-04

**Status:** MASKED-RECONSTRUCTION PROXY / NOT STRICT BLIND PROOF / REASONING MODEL UPDATED
**Track:** Early Buddhist Canon — reasoning reconstruction
**Critical limitation:** This seat may have prior pretraining exposure to canonical texts. Therefore this exercise can test internal structural consistency and explicit prediction-vs-text comparison, but cannot prove contamination-free blind generalization.

## 1. Evaluation protocol

For each held-out-style dialogue:
1. isolate the interlocutor's question/problem;
2. predict the likely response mode from the current reasoning model;
3. predict the hidden assumption or ambiguity;
4. predict the causal or ethical hinge;
5. compare with the canonical response;
6. record mismatch instead of harmonizing after the fact.

Scoring dimensions:
- RESPONSE_MODE
- HIDDEN_ASSUMPTION
- CAUSAL_HINGE
- PEDAGOGICAL_MOVE
- CLAIM_BOUNDARY

Labels:
- HIGH_MATCH
- PARTIAL_MATCH
- MISMATCH
- NOT_SCORABLE

## 2. Case A — SN 42.6 Asibandhakaputta

### Question
Can a religious teacher or ritual action cause all people to attain a good rebirth regardless of their conduct?

### Model reconstruction before canonical comparison
Predicted:
- COUNTER-QUESTION;
- CAUSAL/ETHICAL REFRAME;
- SIMILE;
- reject the assumption that praise/prayer overrides the causal weight of conduct.

Expected hinge:
- action and mental qualities, not external ritual declaration.

### Canonical comparison
The discourse:
- asks the questioner to judge concrete cases;
- contrasts harmful and wholesome conduct;
- uses a heavy stone sinking and ghee/oil rising as physical analogies;
- shows that collective wishing cannot reverse the causal direction attributed to conduct.

### Score
- RESPONSE_MODE: HIGH_MATCH
- HIDDEN_ASSUMPTION: HIGH_MATCH
- CAUSAL_HINGE: HIGH_MATCH
- PEDAGOGICAL_MOVE: HIGH_MATCH
- CLAIM_BOUNDARY: HIGH_MATCH

### New learning
**CAUSAL INVARIANCE UNDER RITUAL PRESSURE**

When a question assumes symbolic/social declaration can cancel a causal process, the early-Buddhist answer may move to an analogy where causal direction remains stable despite wishes.

## 3. Case B — AN 10.95 Uttiya

### Question
If the Buddha teaches liberation, will all beings, half, or a third be liberated?

### Model reconstruction
Predicted:
- SET-ASIDE or PEDAGOGICAL NON-ANSWER regarding population proportion;
- shift from total-outcome forecasting to necessary conditions of liberation;
- refuse a statistic that does not advance the path.

### Canonical comparison
The Buddha is silent on the proportion question.
Ānanda later explains that the relevant knowledge is not how many will pass, but the route by which those who do pass must go:
- abandon the hindrances;
- establish mindfulness;
- develop awakening factors.

The gate simile makes the distinction between:
- knowing the necessary route;
- predicting the total number who will use it.

### Score
- RESPONSE_MODE: HIGH_MATCH
- HIDDEN_ASSUMPTION: HIGH_MATCH
- CAUSAL_HINGE: HIGH_MATCH
- PEDAGOGICAL_MOVE: HIGH_MATCH
- CLAIM_BOUNDARY: HIGH_MATCH

### New learning
**NECESSARY-PATH KNOWLEDGE IS NOT POPULATION FORECASTING**

The teaching can claim knowledge of the conditions/path required for release without claiming a forecast of how many agents will satisfy those conditions.

## 4. Case C — SN 12.48 Lokāyatika

### Question
Is everything existent?
Is everything non-existent?
Is everything one?
Is everything many?

### Model reconstruction
Predicted:
- reject the offered metaphysical alternatives as extreme views;
- replace entity ontology with dependent arising and cessation.

### Canonical comparison
The discourse explicitly identifies the proposed alternatives as cosmological views and teaches dependent origination/cessation as the middle.

### Score
- RESPONSE_MODE: HIGH_MATCH
- HIDDEN_ASSUMPTION: HIGH_MATCH
- CAUSAL_HINGE: HIGH_MATCH
- PEDAGOGICAL_MOVE: HIGH_MATCH
- CLAIM_BOUNDARY: HIGH_MATCH

### New learning
This strengthens:
**MIDDLE = FRAME REPLACEMENT, NOT MIDPOINT COMPROMISE.**

## 5. Case D — MN 90 Kaṇṇakatthala

### Problem 1: reported claim about omniscience
The king reports that the Buddha denied the possibility of all-knowing/all-seeing knowledge without exception.

### Model reconstruction
Predicted:
- SOURCE/PARAPHRASE CORRECTION before doctrinal exposition;
- preserve the exact scope of the original statement;
- distinguish simultaneous cognition from a broader claim about possible knowledge.

### Canonical comparison
The Buddha first rejects the inaccurate report.
He then recalls the narrower statement:
- no ascetic or brahmin knows and sees everything all at once.

### Score
- RESPONSE_MODE: HIGH_MATCH
- CLAIM_BOUNDARY: HIGH_MATCH

### New learning
**CORRECT THE QUOTATION BEFORE CORRECTING THE DOCTRINE**

When a dispute rests on reported speech, the first task can be reconstructing the exact proposition rather than debating a distorted paraphrase.

## 6. MN 90 — conventional inequality vs liberative equality

### Question
Are there differences among social classes?

### Canonical response pattern
The discourse first acknowledges a conventional social distinction:
- some classes receive greater public honor.

When the king clarifies that he means spiritual/future consequence, the answer changes:
- five factors of exertion become relevant;
- differences track training and exertion;
- where right exertion is equal, liberation is not different by caste.

### New learning
**CONVENTIONAL DESCRIPTION AND LIBERATIVE NORM MUST NOT BE COLLAPSED**

The Buddha can:
- acknowledge an existing social convention descriptively;
while
- denying that convention determines spiritual capacity or release.

This is a major guard against reading every discourse as either simple social conservatism or simple modern egalitarianism.

## 7. MN 90 — clarify the intended question before answering ontology

When the king asks:
- "Are there devas?"

the Buddha first asks why he is asking.

The king clarifies:
- he wants to know whether they return to this life.

The answer then addresses that practical distinction.

### New response mode
Add:

**INTENT-CLARIFY**
- use when a broad ontological question may hide a narrower practical concern;
- ask what distinction the interlocutor actually needs;
- answer that question rather than rewarding ambiguity with speculative excess.

This mode differs from COUNTER-QUESTION:
- COUNTER-QUESTION can expose an assumption;
- INTENT-CLARIFY resolves ambiguous intent before selecting the doctrinal tool.

## 8. Revised response-mode taxonomy v0.5

Current modes:
- DIRECT
- ANALYTICAL
- CONDITIONAL
- DE-APPROPRIATIVE
- COUNTER-QUESTION
- INTENT-CLARIFY
- REFRAME
- METHOD-SELECTION
- GRADUAL
- SIMILE
- SPEECH-GATED
- RISK-ASYMMETRY
- SET-ASIDE
- UNCERTAINTY
- SOURCE-CORRECTION

## 9. Generalized reasoning update

The current model now adds four explicit controls:

### A. SOURCE PRECISION
Before debating a claim:
- verify what was actually asserted;
- narrow the scope;
- separate direct wording from hearsay/paraphrase.

### B. INTENT PRECISION
Before answering an ambiguous ontology:
- ask why the distinction matters;
- recover the operational question.

### C. NECESSARY-CONDITION VS OUTCOME-COUNT
Distinguish:
- knowing how an outcome can occur;
from
- knowing how many agents will achieve it.

### D. CONVENTIONAL VS LIBERATIVE LEVEL
Distinguish:
- social/conventional facts;
- causal/ethical training;
- final liberative equivalence.

## 10. Meta-evaluation result

The current reasoning architecture remains coherent across this dialogue cluster.

However, **no strict blind-generalization claim is allowed**, because:
- the underlying model may have encountered these texts in pretraining;
- this seat has now explicitly inspected the source responses.

Allowed claim:
> The current synthesis reconstructs the response structure of this dialogue cluster with high explicit agreement and identifies new distinctions that improve future reasoning.

Forbidden claim:
> The assistant has proven it can independently reproduce the Buddha's answers from unseen scripture.

## 11. Next stronger test

A stronger future test requires an external evaluator or dataset construction process that:
- selects dialogue passages unknown to this seat;
- provides only context/question first;
- stores the canonical answer outside the model context;
- scores the prediction after commitment;
- records source hashes and contamination caveats.

Until such a test exists, continue:
- whole-corpus breadth;
- Agama parallel auditing;
- translation-card work;
- contradiction hunting;
- source-grounded applied-question tests.

## 12. Current conclusion

Dialogue study strengthens the following characterization:

> The Buddha's response strategy is frequently not "answer the sentence as asked." It first checks the quotation, the intent, the causal assumptions, the practical stakes, and whether the offered categories are fit for the problem.

This makes the discourse method:
**precision-first, condition-sensitive, pedagogically adaptive, anti-speculative, and practice-directed.**
