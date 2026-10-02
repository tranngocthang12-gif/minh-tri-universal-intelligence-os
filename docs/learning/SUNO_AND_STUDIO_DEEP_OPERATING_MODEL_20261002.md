# MINH TRÍ — SUNO + SUNO STUDIO DEEP OPERATING MODEL

- Snapshot date: 2026-10-02
- Scope: Suno Create / Remix-Edit / Suno Studio 2.0
- Goal: understand what each control is for, how to choose the right tool, what can go wrong, and how to move from brief -> generation -> editing -> stems -> mix -> export.
- Status: DEEP_THEORY_LEARNED / UI_AND_WORKFLOW_MODEL_BUILT / HANDS_ON_NOT_YET_PROVEN
- Important project rule: tool versions are a dated snapshot, not LAW. Suno can change.
- Production boundary: learn now. Do not create/publish channel music unless Owner explicitly orders execution.
- Verification rule: official Suno Help Center, release notes and product pages are primary sources.

---

# 1. The most important distinction

## Suno Create
Purpose:
**Generate, transform and refine the musical identity of a song.**

Use it to decide:
- song concept
- lyrics
- genre/style
- voice direction
- instrumentation
- structure
- model behavior
- reference influence
- variation

Mental model:
**brief -> candidates -> select musical identity -> edit/regenerate**

## Suno Studio 2.0
Purpose:
**Turn musical material into controllable production objects.**

Use it to control:
- tracks
- clips
- stems
- audio/MIDI
- timing
- arrangement
- recording
- effects
- automation
- synth sound design
- mixing
- export

Mental model:
**selected song/material -> separate/control parts -> edit -> arrange -> process -> mix -> export**

Core rule:

> Create chooses WHAT the song becomes.  
> Studio controls HOW the chosen material is constructed and polished.

---

# 2. Current Suno model family

As of this snapshot, Suno's current music family is v6.

## v6
Use when:
- you know what you want
- you need reliable prompt following
- you want polished normal production

Behavior:
balanced, expressive, controlled.

## v6-wild
Use when:
- brief is too obvious
- you need surprise
- you want genre collision or unusual ideas
- you are exploring, not locking

Behavior:
less predictable and more exploratory.

## v6-mini
Use when:
- sketching
- testing many ideas
- high-volume exploration
- early concept triage

Behavior:
lighter/faster.

## Max Mode
Use selectively when:
- track is longer
- cover should remain close
- style transfer needs consistency
- vocal/style consistency matters strongly

Trade-off:
higher credit cost.

Deep rule:
Do not always use the "strongest" mode.
Choose model based on task:
**explore -> converge -> refine**

---

# 3. SIMPLE MODE — when to use it

Simple mode is now more capable than the old "one short prompt" model.

With v6, one prompt can combine:
- desired musical direction
- multiple references
- Suno songs
- playlists
- audio uploads
- images/video
- structural instructions

Use Simple mode when:
- vision is clear in natural language
- you want Suno to choose the internal operation
- speed matters more than micromanaging fields

Do not use Simple mode blindly when:
- lyrics must be exact
- structure needs deliberate section labels
- exclusions matter
- voice/style controls must be isolated
- you want reproducible experiments

For controlled experiments, use Custom.

---

# 4. CUSTOM MODE — control surface

Custom mode is the disciplined production entry point.

Typical control groups:
- Lyrics
- Instrumental toggle
- Style
- Advanced Options
- Vocal Gender
- Exclude
- creative influence controls
- Voice / style persona context
- Title
- Model

## 4.1 Lyrics field

Use for:
- exact human-written lyrics
- structural section markers
- controlled phrasing experiments

Important:
Human-authored lyrics remain a separate rights layer from generated audio.

Operational habit:
Keep lyrics versioned outside the generation result.
Never rely on one Suno output as the canonical lyric source.

## 4.2 Instrumental toggle

Use when:
- no lead vocal is wanted
- preparing backing track
- planning Add Vocals later
- using Studio for instrumental production

## 4.3 Style field

Style should communicate:
- genre family
- era
- instrumentation
- energy
- production texture
- vocal character
- groove
- mood

Better:
"intimate contemporary pop ballad, sparse piano, warm strings, restrained drums, soft male vocal, close-mic emotional delivery"

Worse:
"beautiful emotional hit song"

Reason:
specific musical descriptors are actionable.

## 4.4 Exclude

Use to state what should NOT appear.

Examples:
- trap hi-hats
- distorted guitar
- choir
- aggressive drums
- spoken intro

Deep rule:
Use Exclude only for meaningful blockers.
Too many negative instructions can make the brief internally constrained.

## 4.5 Vocal Gender

Current Custom mode supports Male/Female voice direction.

Use it as:
one control among several.

Also describe vocal character in Style:
- soft
- gritty
- airy
- intimate
- powerful
- youthful
- mature

Do not confuse:
voice gender selection != exact singer identity.

## 4.6 Creative sliders

### Weirdness
Legacy/current creative control documented as range from safer to more chaotic.

Use low when:
- exact brief
- commercial consistency
- structure discipline

Use higher when:
- seeking novel harmony
- unusual instrumentation
- creative escape

### Style Influence
Controls how strongly generation adheres to the entered style.

Use stronger when:
- style is non-negotiable
- production consistency is important

Use looser when:
- prompt feels over-constrained
- you want alternate interpretations

### Audio Influence
Appears in workflows with uploaded/reference audio.

Use higher when:
- melody/timing/reference identity should stay closer

Use lower when:
- source should inspire but not dominate

### Variety in v6
v6 can adjust/update style prompt internally for variation.

If exact style tags must remain under your control:
set Variety toward 0.

Testing rule:
change one major slider per experiment when learning causality.

---

# 5. VOICES, PERSONAS AND CUSTOM MODELS

These are different tools.

## 5.1 Voice
Purpose:
use your verified singing voice profile in generated songs.

Current official workflow:
- record/upload voice
- verify identity with spoken phrase
- confirm rights
- select Voice in Create
- generate with compatible model/workflow

Deep rule:
Voice is an identity/voice source control.
It is not merely a style tag.

Privacy/rights rule:
never create a voice from someone whose voice you are not authorized to use.

## 5.2 Style Persona
Purpose:
reuse the "essence" of an earlier song's style/vocal feel.

Useful for:
- channel sonic continuity
- repeated series
- related tracks

Risk:
over-reliance can make songs feel samey.

## 5.3 Custom Models
Current official feature:
Pro/Premier users can build models from their own tracks.

Key constraint:
you must own rights to uploaded training tracks.

Use when:
- a recurring sonic identity has been proven
- enough owned examples exist
- one-off Persona is too narrow

Do NOT train a custom model before you know what your actual channel sound is.

---

# 6. AUDIO UPLOAD — when sound becomes a prompt

Audio Upload can take:
- rough demo
- voice memo
- melody
- full song
- recorded performance

Current limits differ by plan; paid plans support longer uploads.

Use cases:
- preserve a hummed melody
- use a rhythmic idea
- bring existing original music into Suno
- extend/cover/remix owned material

Deep decision:
Ask what must remain invariant:
- melody?
- rhythm?
- harmony?
- performance?
- timbre?
- structure?

Then choose Audio Influence accordingly.

---

# 7. REMIX / EDIT — choose the correct operation

"Remix" is an umbrella, not one action.

## 7.1 Reuse Prompt

Use when:
the generation is wrong overall but the brief fields are useful.

It reloads:
- lyrics
- styles
- title/context

Best for:
a new generation from the same recipe.

Not best for:
repairing one local section.

## 7.2 Cover

Use when:
you want meaningful transformation while preserving core melodic identity.

Possible changes:
- vocalist
- style
- timing
- instrumentation

Use:
"same song identity, different production interpretation."

Do not use Cover for a tiny mix polish.
Use Remaster instead.

## 7.3 Extend

Use when:
- ending is weak
- song needs another section
- new outro
- continuation from a chosen point

Key control:
choose exactly where original material stops and extension begins.

After choosing an extension:
Get Whole Song stitches the result into a complete version.

Risk:
bad boundary selection causes awkward transition.

## 7.4 Replace Section

Use when:
only part of the song is wrong.

Typical repairs:
- one lyric line
- one verse
- awkward phrase
- local instrumental problem
- insert/remove middle content

Workflow:
- highlight exact region
- Replace
- prompt/lyrics
- audition alternatives
- adjust boundary
- commit chosen result

Deep rule:
Do not regenerate a whole successful song to repair one local defect.

## 7.5 Crop

Use to remove unwanted time/section.

Use for:
- long intro
- bad ending
- redundant segment

## 7.6 Adjust Speed

Use when tempo feel is the main issue.

Do not confuse:
speed/tempo change with re-arrangement.

## 7.7 Add Vocals

Use for:
- generated/uploaded instrumental
- testing toplines
- adding lyric-driven lead vocal

Audio Strength/Influence determines how strongly new result follows source instrumental.

## 7.8 Remaster

Use only when:
structure, lyrics and performance are already basically right.

Current Variation strength:
- Subtle
- Normal
- High

Remaster focuses on:
- mix balance
- production texture
- clarity
- pronunciation polish
- sonic character

Do NOT use Remaster when:
- lyrics are wrong
- chorus is wrong
- arrangement needs major change
- style must transform radically

Decision rule:

**local content error -> Replace Section**  
**ending/length issue -> Extend**  
**big style reinterpretation -> Cover**  
**same recipe, new roll -> Reuse Prompt**  
**sound polish, same song -> Remaster**

---

# 8. SONG EDITOR — timeline repair without full Studio

Song Editor is a useful middle layer.

Controls include:
- timeline sections
- reorder sections
- Quick Replace
- add section
- edit lyrics
- Replace
- Extend
- Crop
- Fade In
- Fade Out
- split/edit section metadata

Use Song Editor when:
a song is mostly correct and needs structural/local edits.

Use Studio when:
you need independent stems/tracks, effects, MIDI or automation.

---

# 9. STEM SEPARATION — current capability

Stem extraction is now a core Suno workflow.

## Auto Split
Produces up to 12 common stem categories.

Common categories include:
- lead vocal
- backing vocal
- drums
- bass
- percussion
- guitar
- keys
- strings
- synth
- brass
- woodwinds
- other/FX

Use:
fast decomposition.

## Split from Mix
Choose one target instrument/voice.

Output:
- target stem
- complement mix without target

Use:
remove/isolate one element without creating a huge session.

## Advanced Split
Premier-level fine selection from a much larger instrument list.

Use:
precise production surgery.

Important:
stem separation is not perfect truth recovery.
It is source separation estimation.
Always listen for:
- bleed
- phasing
- transient damage
- reverb tails
- vocal artifacts

---

# 10. SUNO STUDIO 2.0 — mental model

Studio is a browser-based generative production environment.

It combines:
- DAW timeline
- audio tracks
- MIDI tracks
- recording
- generative audio
- take lanes
- stem splitting
- effects
- automation
- Wavetable synth
- chat-based editing
- export

Current access:
Premier.

Recommended browser:
Chrome.

Important compatibility:
No conventional VST/AU plugin hosting.

---

# 11. STUDIO LAYOUT

Think in five layers:

1. Transport / global project state
2. Track headers
3. Timeline and clips
4. Bottom detail/editor panels
5. Chat / library / lanes

The main question is always:

**What object is selected?**

Because Studio Chat and editing actions are context-aware.

---

# 12. TRANSPORT CONTROLS

Current Studio 2.0 moves common transport controls above timeline.

Important controls:
- Play/Pause
- Record
- Metronome
- Loop
- Follow Playhead
- Tempo
- Clock settings
- Time Signature

Shortcuts include:
- Space = Play/Pause
- Shift+R = Record
- Shift+C = Metronome
- Ctrl/Cmd+L = Loop

Use metronome whenever checking generated timing.

Studio documentation acknowledges that generated parts can sometimes land slightly early/late.
Therefore:
**timing must be verified, not assumed.**

---

# 13. TRACK TYPES

## Audio Track
Contains recorded/generated/imported waveform clips.

Can be:
- edited
- split
- moved
- faded
- processed
- automated
- stem-separated
- regenerated/covered in generative workflows

## MIDI Track
Contains notes, not sound.

MIDI tells an instrument:
- pitch
- timing
- duration
- velocity
- control data

New MIDI tracks load with Wavetable synth ready to play.

Track-level common operations:
- mute
- solo
- arm
- color
- rename
- duplicate
- reorder
- take lanes

---

# 14. RECORDING IN STUDIO

## Arm
"A" on track enables recording target/input selection.

For audio:
choose microphone/interface input.

For MIDI:
choose MIDI device.

## Record
Top timeline control or Shift+R.

## Count-In
Provides bars before recording begins.

## Pre-Roll
Plays existing project before record starts.

Difference:
Count-In gives metronome countdown.
Pre-Roll lets performer hear project context.

## Latency Calibration
Studio can measure timing offset.

Use when:
recorded material consistently appears behind/ahead.

Deep rule:
Do latency calibration before judging performer timing.

---

# 15. CLIPS AND TAKE LANES

A generation commonly offers multiple takes.

Studio 2.0 uses Take Lanes/alternate generations.

Use them to:
- audition alternatives
- compare without destroying main arrangement
- commit the best take
- comp ideas

Best practice:
do not delete alternates too early.
First decide:
- performance
- tone
- timing
- arrangement fit

---

# 16. STUDIO CHAT — assistant as command layer

Open via:
- sparkle/chat control
- Enter with context

Chat can:
- inspect project
- edit tracks/clips
- generate audio
- create MIDI
- build effects/plugins
- navigate views
- ask clarification

Crucial behavior:
it is context-sensitive.

"Make this louder"
means selected object/context.

Risk:
wrong selection -> correct command applied to wrong target.

Rule:
Before every chat command, verify:
1. selected track
2. selected clip/range
3. tempo/context
4. desired invariant

Everything chat does uses editable/undoable project operations.
Undo remains important.

---

# 17. HOW TO PROMPT STUDIO CHAT

A good Studio command has four parts:

**target + action + constraint + purpose**

Example:
"On the chorus vocal track, reduce harsh upper mids without making the vocal dull, so it sits behind the lead synth."

Bad:
"Make it better."

For generative part:
"Add a restrained warm electric bass in the second verse, following kick accents but leaving space under the vocal."

For automation:
"Create a slow filter opening across the 8 bars before the chorus."

For plugin:
"Build a subtle tape-style delay with controllable wow, low-pass filtering and tempo-sync."

Deep rule:
Prompt Studio as a collaborator with a concrete production role.

---

# 18. MIDI IN STUDIO

## Add track
Shift+T -> MIDI.

## Piano Roll
Double-click MIDI clip.

Core operations:
- draw notes
- move
- resize
- quantize
- velocity
- scale assist
- pitch bend/modulation where available

## Quantize
Shift+Q.

Use:
tighten timing.

Do not over-quantize:
human groove may be intentional.

## Musical Typing
Ctrl/Cmd+K.

Computer keyboard:
- homerow plays notes
- octave keys shift range
- velocity keys change dynamics

## External MIDI
Web MIDI allows:
- note input
- recording
- MIDI Learn
- transport

Safari limitation:
Web MIDI unavailable; Chrome recommended.

## Audio -> MIDI
Studio can transcribe an audio clip when moved to MIDI context.

Use:
recover musical note structure for re-instrumentation.

## MIDI -> Audio generation
Chat/generation can make audio based on MIDI content.

Use:
write notes first, then ask AI to render musical performance/timbre.

---

# 19. WAVETABLE SYNTH — understand the knobs

Studio 2.0 Wavetable is not just a preset box.

## Oscillator 1/2
Primary waveform sources.

### Wavetable position
Morphs tone through table frames.

### Warp
Distorts waveform playback relationship.

Use:
more harmonics / movement.

### Unison
Adds detuned voices.

Use:
width/thickness.

Risk:
too much can blur pitch and mono image.

### Spread
Controls stereo placement of unison voices.

## Sub Oscillator
Adds low fundamental support.

Use:
bass weight.

## Filter

### Cutoff
Sets frequency boundary.

### Resonance
Emphasizes around cutoff.

High resonance can become tonal/self-oscillating.

## Envelope

### Attack
time to reach level.

### Decay
time from peak to sustain.

### Sustain
held level.

### Release
fade after note ends.

Use envelope language for:
- pluck
- pad
- stab
- bass

## LFO
Repeating modulation.

Use for:
- vibrato
- tremolo
- wobble
- filter movement

## Mod Matrix
Routes source -> destination with amount.

This is the real expressive engine.

## Glide/Portamento
slides between pitches.

Use for:
bass/lead phrasing.

Deep rule:
When prompting a synth, translate adjectives into synthesis:
"soft evolving pad" ->
slow attack, long release, moving wavetable/LFO, moderate stereo spread, gentle low-pass.

---

# 20. EFFECTS IN STUDIO

Built-in core effects currently include:
- Compressor
- EQ
- Reverb
- Convolution
- Delay
- Distortion
- Gate

## Effects chain order
Audio passes through devices in order.

Therefore:
EQ -> Compressor
is not equal to
Compressor -> EQ.

Always understand why the order exists.

## EQ
Use:
- remove mud
- reduce harshness
- make room
- tonal balance

Do not EQ by eye only.
Listen in context.

## Compressor
Use:
- control dynamics
- increase consistency
- sidechain/pumping

Do not use compressor as "make louder" button.

## Reverb
Use:
depth/space.

Risk:
vocal loses intimacy/clarity.

## Convolution
Uses captured impulse response.

Use:
realistic spatial character.

## Delay
Use:
echo/rhythm/depth.

## Distortion
Use:
harmonics/edge/saturation.

## Gate
Use:
noise/tightening.

Risk:
cutting natural tails.

## Bypass
Always A/B.

If processed version is not functionally better:
remove effect.

---

# 21. CUSTOM PLUGINS

Studio Chat can design custom audio effects.

Use when:
built-ins cannot express a specific behavior.

Workflow:
- describe behavior
- clarify parameters
- build
- audition
- revise by conversation
- save to personal library

Important:
these are Studio-native effects.
They are not VST/AU plugins.

Do not create a custom plugin to solve a problem a normal EQ/compressor already solves well.

---

# 22. AUTOMATION

Automation = parameter changes over time.

Can automate:
- volume
- pan
- plugin parameters
- synth parameters
- many non-static controls

Open:
Shift+A.

Create:
right-click parameter -> Automate.

Edit:
- add points
- move points
- bend segments

When a parameter is automated:
manual knob behavior changes because automation is the active controller.

Use cases:
- vocal lift in chorus
- reverb throw on last word
- filter opening
- pan movement
- effect intensity
- build/drop transitions

Deep rule:
Do not automate static problems.
First fix the base mix, then automate movement.

---

# 23. ARRANGEMENT EDITING

Timeline discipline:
- rename tracks
- color by role
- group conceptual layers
- keep chorus/verse boundaries visible
- avoid anonymous "Audio 27" sessions

Useful edit operations:
- select
- split
- move
- copy/paste
- duplicate
- fade
- loop
- crop/range select

Before large structural edit:
duplicate/version project.

---

# 24. MIXING IN STUDIO

Mixing objective:
make every element have a role in a coherent stereo result.

Order of thinking:

1. arrangement
2. clip/source quality
3. balance
4. pan
5. EQ
6. dynamics
7. space
8. automation
9. final check

Do not start with effects if arrangement is the real problem.

## Volume
Set relative hierarchy:
- lead vocal
- drums
- bass
- harmonic bed
- hooks
- ambience

## Pan
Create separation.

Do not pan merely because track exists.

## EQ
Solve conflicts.

## Compression
Control movement.

## Effects
Create depth/character.

---

# 25. EXPORT FROM STUDIO

Export dropdown supports:
- Full Song
- Selected Time Range
- Multitrack

Individual audio clip:
right-click -> Download WAV.

Stems:
can also produce MIDI via Get MIDI where supported/credited.

Current documentation states high-quality WAV export; Studio 2.0 help also lists 32-bit WAV or MP3 for project export contexts.

## Full Song
Use:
final listening mix.

## Selected Time Range
Use:
- review section
- sample
- handoff excerpt

## Multitrack
Use:
FL Studio / Ableton / Logic / external engineer.

Deep rule:
For MINH TRÍ post-Suno workflow, Multitrack is the handoff bridge to FL Studio if deeper external repair is needed.

---

# 26. SUNO STUDIO vs FL STUDIO

They overlap but have different strengths.

## Suno Studio strongest at
- generative continuation
- generative tracks/stems
- direct Suno project integration
- chat-based edits
- fast AI variations
- stem separation
- audio<->MIDI generative loop

## FL Studio strongest conceptually at
- mature conventional DAW workflow
- detailed external plugin ecosystem
- deep manual routing/editing
- established production/mixing toolchain

Current project doctrine:
**Suno generates and performs generative reconstruction.  
Suno Studio controls and decomposes the Suno material.  
FL Studio is optional deeper conventional post-production.**

Tool choice is dynamic, not LAW.

---

# 27. RIGHTS / COMMERCIAL USE — production gate

Current Suno official guidance distinguishes:
- free-plan outputs: generally non-commercial
- paid Pro/Premier creations: commercial use rights granted under current terms
- ownership/commercial rights are not the same as copyright eligibility

Important:
commercial permission from Suno does NOT guarantee copyright registration/protection.

Human-authored lyrics are a separate human-created layer.

Before channel monetization:
record:
- plan/status at creation time
- source lyrics provenance
- uploaded audio rights
- voice authorization
- sample provenance
- collaborator permissions
- download/export date if relevant to current terms

Do not monetize:
- another person's lyrics without permission
- unauthorized voice material
- remixes that you do not own rights to monetize
- uploaded music you do not control

Terms can change.
Re-check before commercial release.

---

# 28. CURRENT DOWNLOAD / WORKFLOW LIMIT AWARENESS

As of current 2026 documentation:
download rules changed in September 2026.

Do not hardcode quotas into project LAW.

Operational principle:
before batch export, check current account entitlement.

Studio professional workflow downloads are treated differently in current Suno documentation from normal library download limits.

---

# 29. FAILURE MODES — CREATE

## 29.1 Prompt too vague
Symptom:
generic song.

Fix:
add concrete musical variables.

## 29.2 Prompt too overloaded
Symptom:
model ignores some instructions.

Fix:
rank must-have vs optional.

## 29.3 Wrong tool
Symptom:
regenerating whole track for one lyric error.

Fix:
Replace Section.

## 29.4 Wrong variation level
Symptom:
Remaster unexpectedly changes song.

Fix:
lower variation.

## 29.5 Reference influence too low/high
Symptom:
melody lost OR result too trapped.

Fix:
adjust Audio Influence deliberately.

## 29.6 Style drift
Symptom:
genre elements appear that violate brief.

Fix:
Style Influence / Variety / Exclude.

---

# 30. FAILURE MODES — STUDIO

## 30.1 Wrong selection + Chat
Symptom:
correct edit on wrong track.

Fix:
verify context before Enter.

## 30.2 Timing drift
Symptom:
generated stem feels off-grid.

Fix:
metronome + solo + inspect alignment.

## 30.3 Over-processing
Symptom:
mix becomes dull/harsh/washed.

Fix:
bypass and compare.

## 30.4 Stem artifacts
Symptom:
bleed/phasing.

Fix:
choose another stem mode or keep original mixed context.

## 30.5 Automation confusion
Symptom:
knob does not stay at manual value.

Fix:
check automation lane.

## 30.6 Too many alternatives
Symptom:
decision paralysis.

Fix:
define acceptance criteria before generating more takes.

---

# 31. BRIEF -> SUNO OPERATING LOOP FOR MINH TRÍ

## Gate A — Editorial/music brief
Write:
- listener
- emotion
- story purpose
- genre range
- tempo feel
- voice
- instrumentation
- structure
- must-have hook
- prohibited elements
- rights constraints

## Gate B — Exploration
Use:
v6-mini or v6-wild where appropriate.

Goal:
discover directions.

## Gate C — Convergence
Use:
v6.

Goal:
produce 2-4 serious candidates.

## Gate D — Selection
Judge:
- emotional truth
- lyric delivery
- hook
- arrangement
- sonic identity
- editability

Do not select only by first impression.

## Gate E — Local repair
Choose:
- Replace Section
- Extend
- Cover
- Remaster

## Gate F — Studio
Open chosen song.

## Gate G — Separation/control
- stem if needed
- organize tracks
- timing check
- choose best takes

## Gate H — Production
- arrangement
- effects
- automation
- MIDI/generative layers

## Gate I — Mix
- balance
- pan
- EQ
- dynamics
- space

## Gate J — Export
- Full Song review WAV
- Multitrack if FL Studio handoff needed

## Gate K — Verification
Listen outside Studio.
Check:
- headphones
- normal speakers
- phone
- mono compatibility when relevant
- lyrics/pronunciation
- start/end
- loudness consistency

---

# 32. ONE-SONG PRACTICAL EXAM

The old project hypothesis said:
"one correct brief -> stem -> repair one layer -> export."

Now this can be upgraded into a real competence test.

## Phase 1 — Create
1. Write one precise brief.
2. Make controlled generations.
3. Explain why one candidate wins.
4. Repair one local problem with correct Suno tool.
5. Document settings/decision.

## Phase 2 — Studio
6. Open in Studio.
7. Identify transport and track controls.
8. Separate appropriate stems.
9. Detect stem artifacts.
10. Correct one arrangement issue.
11. Add one MIDI/generative layer.
12. Apply one EQ decision.
13. Apply one compression or dynamics decision.
14. Add one space effect.
15. Create one automation lane.
16. Compare processed/unprocessed.

## Phase 3 — Export
17. Export full mix.
18. Export multitrack.
19. Import handoff stems into FL Studio only if needed.
20. Inspect exported file and listen.

## Phase 4 — Diagnosis
Deliberately introduce:
- wrong chat selection
- timing drift
- over-reverb
- too-strong remaster variation

Then diagnose and recover.

Passing this is practical evidence.

---

# 33. CURRENT UNDERSTANDING LEVEL

## L0 — names
PASS

## L1 — explain core functions
PASS

## L2 — choose correct Suno/Suno Studio operation for a problem
PASS conceptually

Examples:
- local lyric defect -> Replace Section
- wrong ending -> Extend
- same song, new genre -> Cover
- polish -> Remaster
- isolate vocal -> Stem
- detailed production -> Studio

## L3 — diagnose trade-offs/failures
PARTIAL-STRONG

Can reason about:
- prompt overconstraint
- style drift
- influence balance
- stem artifacts
- timing mismatch
- effect order
- automation
- selection/context
- rights gates

## L4 — hands-on speed and production proof
NOT PROVEN

Requires actual logged session and exported artifact.

Current status:

**SUNO_UNDERSTANDING = L2_STRONG / L3_PARTIAL_STRONG**  
**SUNO_STUDIO_UNDERSTANDING = L2_STRONG / L3_PARTIAL**  
**HANDS_ON_PRODUCTION_MASTERY = NOT_VERIFIED**

---

# 34. OFFICIAL SOURCES USED

Suno v6:
https://help.suno.com/en/articles/13924801

v6 FAQ:
https://help.suno.com/en/articles/13924481

Creative Sliders:
https://help.suno.com/en/articles/6141377

Audio Upload:
https://help.suno.com/en/articles/6141569

Song Editor:
https://help.suno.com/en/articles/6141505

Replace Section:
https://help.suno.com/en/articles/3271873

Extend:
https://help.suno.com/en/articles/2409601

Remaster:
https://help.suno.com/en/articles/8105281

Remix/Edit:
https://help.suno.com/en/articles/6050497

Add Vocals:
https://help.suno.com/en/articles/6882817

Voices:
https://help.suno.com/en/articles/11362369

Personas:
https://help.suno.com/en/articles/3484161

Custom Models:
https://help.suno.com/en/articles/11362497

Stem Separation:
https://help.suno.com/en/articles/13925185

Studio 2.0:
https://help.suno.com/en/articles/13670529

Studio Chat:
https://help.suno.com/en/articles/13670721

MIDI:
https://help.suno.com/en/articles/13670593

Wavetable:
https://help.suno.com/en/articles/13670657

Effects:
https://help.suno.com/en/articles/13670785

Automation:
https://help.suno.com/en/articles/13674305

Recording:
https://help.suno.com/en/articles/13671041

Export:
https://help.suno.com/en/articles/13925249

Studio shortcuts:
https://help.suno.com/en/articles/13680385

Rights:
https://help.suno.com/en/articles/9601665
https://help.suno.com/en/articles/2746945

---

# 35. FINAL DOCTRINE

Do not think:
"Suno writes song, then I accept/reject."

Think:

**brief -> generate -> diagnose -> use the smallest correct transformation -> decompose into controllable parts -> edit -> automate -> mix -> export -> listen -> learn**

And do not think:
"Studio is just Suno with more buttons."

Think:

**Suno Create is a generative composer/performer.  
Suno Studio is a generative production environment.**

The most valuable skill is not prompt writing.

It is:
**knowing what must stay unchanged, what is allowed to vary, and which tool changes only the intended layer.**
