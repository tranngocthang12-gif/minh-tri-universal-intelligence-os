# MINH TRÍ — FL STUDIO 2026: DEEP FEATURE + BUTTON ATLAS

- Date: 2026-10-02
- Product: FL Studio 2026
- Learning goal: understand the interface deeply enough to know what the major buttons do, when to use them, how signal/data flows through the application, and which controls are risky to misuse.
- Status: THEORY_DEEPENED / UI_BUTTON_MAP_LEARNED / HANDS_ON_NOT_YET_PROVEN
- Scope: learning only. Do not publish music, generate Suno output, or claim production mastery unless Owner explicitly orders execution.
- Evidence policy: official Image-Line documentation and FL Studio 2026 release notes are the primary sources.
- Important limitation: this document proves structured understanding from current official documentation, not muscle-memory or hands-on speed inside the application.

---

## 1. Mental model first: what each main window really does

### Browser
Finds and loads projects, samples, presets, plugins, current-project objects, favorites and FL Cloud content.

### Channel Rack
Holds instruments/generators and pattern data. Each row is a sound source or internal generator.

### Piano Roll
Edits detailed note timing, pitch, duration and note properties.

### Playlist
Arranges Pattern Clips, Audio Clips and Automation Clips on the song timeline.

### Mixer
Receives audio from Channels, processes it through FX, changes level/pan/stereo, routes it to other tracks and finally to Master/output.

### Edison
Wave editor/recorder for destructive sample editing, repair, trimming, normalization, denoise and time/pitch processing.

### NewTone
Pitch and timing editor for vocals/instruments.

### Automation Clips
Move parameters over time.

### Export
Renders the final audio or stems to files.

Core signal model:

**Instrument / Audio Clip -> Channel -> Mixer Insert -> FX chain -> routing/sends -> Master -> Export**

Core sequencing model:

**Pattern / Audio / Automation data -> Playlist timeline -> playback engine**

Critical FL Studio concept:
**Playlist tracks are not automatically the same thing as Mixer tracks.**
Routing from Channel Rack to Mixer determines where instrument/audio signal is processed unless Track Mode is deliberately used.

---

# 2. GLOBAL TOOLBAR — WHAT EVERY IMPORTANT BUTTON MEANS

## 2.1 PAT / SONG
Shortcut: L

### PAT
Plays only the currently selected pattern.

Use when:
- building a drum loop
- programming one musical phrase
- editing a pattern without hearing the whole arrangement

Common mistake:
- pressing Play and wondering why the whole song is not playing.

### SONG
Plays the Playlist arrangement.

Use when:
- arranging
- mixing
- reviewing transitions
- exporting the finished sequence

---

## 2.2 PLAY / PAUSE
- Space: play/stop behavior
- Ctrl+Space: pause/resume behavior

Meaning:
Starts playback from the current play position.

When Record is armed:
Play also starts recording.

---

## 2.3 STOP
Stops playback/recording.

Important:
- double-click Stop = panic / stop hanging notes.
- useful if a synth note becomes stuck.

---

## 2.4 RECORD
Shortcut: R

Master recording enable.

Right-click exposes the recording filter:
- Automation
- Notes
- Audio
- Clips
- recording behavior options

Important reasoning:
If Automation is enabled and you move controls while recording, those moves can become recorded automation.

Risk:
Accidental automation can make a project appear to "fight" your knob changes later.

---

## 2.5 TEMPO
Sets project BPM.

Useful actions:
- type exact BPM
- tap tempo
- create tempo automation
- temporarily use half-speed for easier performance

For imported audio:
tempo and time-stretch settings determine whether pitch changes when timing changes.

---

## 2.6 TIME DISPLAY
Shows either musical position or real time.

Use:
- bars/beats for arrangement
- minutes/seconds for delivery length

---

## 2.7 PATTERN SELECTOR
Selects the active Pattern.

F4:
find/create next empty pattern.

Best habit:
separate major musical ideas into meaningful patterns rather than putting everything into one giant pattern.

---

## 2.8 METRONOME
Shortcut: Ctrl+M

Plays beat click.

Use for:
- MIDI recording
- vocal/instrument tracking
- timing checks

Right-click:
metronome sound/routing options.

---

## 2.9 COUNT-IN
Shortcut: Ctrl+P

Plays metronome before recording begins.

Use:
performer gets time to enter before bar 1.

---

## 2.10 RECORDING BLEND / OVERDUB
Shortcut: Ctrl+B

Allows newly recorded MIDI notes to blend with existing notes instead of replacing them.

Audio use:
supports sound-on-sound loop recording behavior.

---

## 2.11 RECORDING LOOP
Repeats the selected region while recording.

Useful for:
- multiple takes
- loop performance
- repeated MIDI passes

---

## 2.12 ONE-CLICK AUDIO RECORDING
Opens guided audio-recording workflow.

Important:
Do not record an external source through the Master track because Master contains the whole mix.

---

## 2.13 RENDER AS AUDIO
Shortcut: Ctrl+R

Opens audio render/export.

Right-click can provide quick MP3-related render access.

---

## 2.14 SAVE AS
Shortcut: Ctrl+Shift+S

Creates a new project save/version.

Good practice:
use versions before destructive editing or major mix changes.

---

## 2.15 UNDO
Shortcut: Ctrl+Z

Right-click:
history access.

Learning rule:
before destructive work in Edison, know where Undo/History is.

---

## 2.16 MAIN WINDOW BUTTONS

- F5 Playlist
- F6 Channel Rack
- F7 Piano Roll
- F8 Plugin Picker
- F9 Mixer
- Alt/Opt+F8 Browser
- F11 Project Info

These are navigation anchors.

---

## 2.17 GLOBAL SNAP
Controls the time grid used when a local editor's Snap is set to Main.

Meaning:
decides where Clips/notes/events naturally lock.

Alt while dragging:
temporarily bypass snap in many editing contexts.

Common mistake:
thinking an object is "stuck" when Snap is simply forcing grid alignment.

---

## 2.18 MASTER VOLUME
Controls listening/output level for the project.

Important:
do not confuse this with disciplined Mixer gain staging.

---

## 2.19 MASTER PITCH
Changes global pitch for channels that allow it.

Use carefully:
time-stretch mode determines whether audio length and pitch interact.

---

# 3. BROWSER — BUTTONS AND BEHAVIOR

Shortcut: Alt/Opt+F8

Default concepts:
- All
- Current Project
- Plugin Database
- Online Content
- Starred
- Presets
- Sounds / FL Cloud, depending on view/version

## 3.1 SEARCH
Shortcut: Ctrl+F

Find files/content.

F3:
next search match.

## 3.2 COLLAPSE STRUCTURE
Closes expanded folder branches.

Use:
clean up a crowded Browser.

## 3.3 REFRESH CONTENT
Re-reads folders.

Use after:
- adding files outside FL Studio
- changing sample directories

## 3.4 STAR / FAVORITE
Marks files/plugins/content as favorites.

Use:
build a trusted small working library.

## 3.5 CURRENT PROJECT
Shows:
- Patterns
- Effects
- Generators
- Automation
- Initialized controls
- Samples

High-value use:
diagnose unwanted automation.

## 3.6 PLUGIN DATABASE
Organized list of installed plugins.

Important:
plugin scan/classification controls where plugins appear.

## 3.7 SOUNDS / FL CLOUD
Can audition and load online content.

Relevant controls include:
- search
- genre/tag filters
- favorites
- auto time stretch
- auto pitch shift
- sync downloaded sounds

Risk:
automatic time/pitch options can change how a sample behaves on import.

---

# 4. CHANNEL RACK — EACH CONTROL IN A CHANNEL ROW

Shortcut: F6

From left to right the important controls are:

## 4.1 MUTE / SOLO LED
Left-click:
mute/unmute.

Solo:
Ctrl-click, Alt-click or right-click menu depending workflow.

Meaning:
silences pattern/Piano Roll playback for that channel.

Important:
live MIDI input can still behave differently from pattern playback.

---

## 4.2 PAN
Channel-level pan sent to the plugin.

Best understanding:
this is pre-Mixer behavior.

Usually:
Mixer pan is more useful for final mix placement.

---

## 4.3 VOLUME
Channel-level volume before Mixer processing.

Useful as:
pre-effect / source level control.

Important:
Mixer fader is post-effect, so Channel Volume and Mixer Fader are not interchangeable in every case.

---

## 4.4 MIXER TRACK DESTINATION
Routes the Channel to a Mixer Insert.

Fast routing:
Ctrl+L can link selected Channel(s) to selected Mixer track.

Meaning:
this is the bridge from sound generation to mix processing.

---

## 4.5 CHANNEL BUTTON
Displays instrument/sample name.

Left-click:
opens Channel Settings / plugin interface.

Right-click:
channel-management menu and Piano Roll access.

---

## 4.6 CHANNEL SELECTOR
Chooses which Channel is selected and which receives relevant editing/MIDI input.

Multiple selection:
right-click/drag behavior can select multiple channels.

---

## 4.7 STEP SEQUENCER
Each step is commonly a 16th-note position in the default setup.

Left-click:
turn step on.

Right-click:
turn step off.

Use:
drums and simple rhythmic patterns.

Not ideal for:
long expressive notes or complex melodies; use Piano Roll.

---

## 4.8 PIANO ROLL PREVIEW
Shows mini note layout for channels using Piano Roll.

Click:
opens Piano Roll.

---

# 5. PIANO ROLL — TOOL BUTTON ATLAS

Shortcut: F7

## 5.1 DRAW — P
Adds and moves individual notes.

Left-click:
add note.

Right-click:
delete.

Use:
precise melodic editing.

---

## 5.2 PAINT — B
Paints many notes while dragging.

Use:
repeating notes, rapid patterns, chords.

Risk:
easy to create unwanted duplicate content if used carelessly.

---

## 5.3 DRUM PAINT — N
Paint behavior optimized for drum-note sequences.

Useful:
fast rhythmic entry.

---

## 5.4 DELETE — D
Deletes notes.

---

## 5.5 MUTE — T
Mutes notes without deleting them.

Use:
A/B alternatives while preserving data.

---

## 5.6 INTERPOLATE — I
Creates gradients in genuine event automation data.

Not the same as:
ordinary note-property editing.

---

## 5.7 SLICE — C
Cuts notes.

Use:
divide long notes.

Ctrl+G:
can glue touching notes.

---

## 5.8 SELECT — E
Selects groups of notes.

Ctrl:
temporary selection behavior is also common in other tools.

---

## 5.9 ZOOM — Z
Zoom in/out or zoom to selected area.

---

## 5.10 SLIDE NOTE
Shortcut: S in Piano Roll context.

Creates FL Studio slide behavior where supported.

---

## 5.11 PORTAMENTO
Shortcut: O

Used for note transitions/portamento behavior where the instrument supports FL note properties.

---

## 5.12 EVENT / PROPERTY LANE
Edits note-level properties such as:
- velocity
- pan
- pitch-related or plugin-specific properties depending context

Important:
velocity and Channel/Mixer volume are different concepts.

---

## 5.13 SNAP
Controls note alignment.

Musical values include:
- beat fractions
- beats
- bars
- triplet grids

Use:
match rhythmic intent, not always the finest grid.

---

# 6. PLAYLIST — CORE EDITING BUTTONS

Shortcut: F5

Contains:
- Pattern Clips
- Audio Clips
- Automation Clips

## 6.1 DRAW — P
Places selected Clip.

Shift:
can temporarily alter tool behavior.

Right-click:
deletion behavior.

---

## 6.2 PAINT — B
Paints repeated Clips.

Use:
repeating patterns quickly.

---

## 6.3 DELETE — D
Erases Clips.

---

## 6.4 MUTE — T
Mutes individual Clips without muting the whole Playlist track.

Important distinction:
Clip mute != Playlist track mute.

---

## 6.5 SLICE — C
Cuts Clips.

Use:
song edits, vocal chopping, structure changes.

---

## 6.6 SLIP — S
Moves audio/content inside a Clip boundary without moving the Clip itself.

Use:
change what portion of source audio is heard while keeping arrangement timing.

---

## 6.7 SELECT — E
Selects multiple Clips.

---

## 6.8 ZOOM — Z
Zooms timeline area.

---

## 6.9 PLAYBACK — Y
Auditions timeline locations/content according to tool behavior.

---

## 6.10 SNAP
Controls timeline locking.

Alt:
temporarily bypass.

---

## 6.11 STRETCH MODE
Shortcut: Shift+M

When enabled, dragging Audio Clip edges changes duration using the selected stretch method.

Critical:
if stretch method is Resample, pitch can change with duration.
If using Stretch/appropriate algorithm, pitch can remain stable.

---

## 6.12 AUDIO CLIP GAIN
FL Studio 2026 exposes clip-level gain control.

Use:
normalize relative clip loudness before Mixer automation.

Do not confuse with:
Mastering or Mixer fader.

---

## 6.13 FADE HANDLES / CROSSFADE
Clip-level fade handles control transitions at clip edges.

Use:
remove clicks, make natural joins, blend edits.

---

## 6.14 ZERO-CROSS
Moves slice/resize points toward waveform zero crossings.

Benefit:
reduces clicks.

Trade-off:
slice may not happen exactly where the pointer is.

---

## 6.15 MAKE UNIQUE
Creates an independent Clip instance.

Use:
edit one section without changing all copies.

### MAKE UNIQUE AS SAMPLE
Also creates a physically separate sample file.

Use before destructive sample-specific editing.

---

# 7. STEM SEPARATION — NOW VERIFIED AS A REAL FL STUDIO FEATURE

Official FL Studio documentation confirms:
Audio Clip menu can use **Extract stems from sample**.

Components:
- Drums
- Bass
- Instruments
- Vocals

FL Studio 2026 also advertises a **Remix a Song** tool that starts from BPM detection and stem separation.

This resolves the previous project uncertainty that stem separation was only an Owner statement.

Correct status now:
**FEATURE_EXISTS_VERIFIED_BY_OFFICIAL_IMAGE_LINE_DOCUMENTATION**

Still not proven:
- quality on Owner's specific Suno songs
- artifact level
- speed on Owner PC
- best workflow for each song

---

# 8. AUDIO CLIP / SAMPLER TIME-STRETCH CONTROLS

## 8.1 TIME
Controls or derives sample duration.

Right-click options include:
- none
- autodetect
- project tempo
- beat/bar based values

---

## 8.2 MODE / STRETCH METHOD

### Resample
Tape-like behavior.
Changing playback speed changes pitch and duration together.

### Stretch
Keeps rhythmic duration/pitch behavior more stable for tempo changes.

### Stretch Pro
Enhanced stretch with Formant Shift.

### Offline Elastique modes
Higher-quality calculations for non-realtime use.

Reasoning rule:
choose based on source type and whether tempo changes in real time.

---

## 8.3 FIT TO TEMPO
Synchronizes audio clip duration to project tempo.

Useful:
loops and imported full songs.

Risk:
wrong detected BPM can make the result badly stretched.

---

# 9. MIXER — THE MOST IMPORTANT BUTTONS AND SIGNAL LOGIC

Shortcut: F9

## 9.1 TRACK MUTE
Left-click:
mute/unmute.

Right-click / modifier:
solo options.

---

## 9.2 TRACK RECORD ARM
Arms selected Mixer track to record its routed audio.

Color state indicates armed status.

Important:
select the right external input and pickup position.

---

## 9.3 PAN
Positions sound in stereo field.

Use:
separation and spatial placement.

---

## 9.4 LEVEL FADER
Post-effect level control.

Important:
FX are processed before the standard track fader.

This is why:
lowering Mixer fader does not necessarily reduce signal entering plugins earlier in that same track.

---

## 9.5 STEREO SEPARATION
Center:
no change.

Turn right:
moves toward mono.

Turn left:
increases stereo separation.

Risk:
over-widening can harm mono compatibility.

---

## 9.6 PEAK METER
Shows level.

Critical:
Master or hardware output clipping matters.
Insert tracks can use FL Studio's internal floating-point headroom, but this is not a reason to ignore gain structure.

---

## 9.7 INPUT SELECTOR
Chooses audio interface input.

Requires appropriate audio driver, normally ASIO on Windows.

Use:
microphone, line input, instrument recording.

---

## 9.8 OUTPUT SELECTOR
Chooses hardware output.

Master must have a valid output to hear FL Studio.

Use special outputs for:
- headphones
- alternate monitoring
- hardware sends

---

## 9.9 EFFECT SLOTS
10 slots per Mixer track.

Signal flows through the FX chain in slot order.

Actions:
- load effect
- open effect
- reorder effect
- bypass/mute effect
- replace/delete
- move into Patcher

Important:
effect order matters.

Example:
EQ before compressor != compressor before EQ.

---

## 9.10 EFFECT SLOT MIX / ENABLE
Lets an effect be enabled/bypassed and mixed depending control/context.

Use:
A/B processing.

---

## 9.11 SEND SWITCH
Routes selected Mixer track to another track.

After enabling:
send-level knob controls amount.

Use:
- shared reverb
- delay send
- parallel processing

---

## 9.12 SIDECHAIN
Routes control signal to another track/plugin without normal audible send level.

Use:
kick -> compressor on bass, for ducking.

---

## 9.13 ROUTE TO MASTER
Most tracks ultimately route to Master.

If disconnected:
audio may no longer reach main output.

---

## 9.14 INTEGRATED EQ
Mixer track has built-in parametric EQ controls.

Use:
broad corrective shaping.

For surgical work:
a dedicated EQ plugin can provide more detailed control.

---

# 10. EDISON — AUDIO REPAIR/EDIT BUTTONS

Edison is a waveform editor and recorder.

Can be loaded on Mixer tracks or opened from sample contexts.

## 10.1 RECORD
Captures audio at the point Edison exists in the signal chain.

Meaning:
placement matters.

---

## 10.2 SLAVE TRANSPORT
Links Edison playback position to FL Studio transport.

---

## 10.3 SCRUB
Manually plays waveform under cursor movement.

Use:
find exact transients/noises.

---

## 10.4 MUTE INPUT
Stops monitoring Edison input while recording/editing.

---

## 10.5 FREEZE EDITING
Locks editing.

Important:
if nothing seems editable, check this before assuming Edison is broken.

---

## 10.6 UNDO / HISTORY
Reverses destructive edits.

---

## 10.7 NORMALIZE
Raises selected audio so the highest peak reaches maximum available digital level.

Important:
normalization is not compression and does not fix bad dynamics.

---

## 10.8 TRIM SIDE NOISE / GATE
Uses threshold to remove material around/below relevant noise level.

---

## 10.9 FADE IN / FADE OUT
Creates smooth level ramps.

Right-click variants can declick/smooth edges.

---

## 10.10 DENOISE / CLEAN UP
Noise repair tools.

Includes workflows such as:
- noise profile
- clean up
- vocal denoise / isolation
- deverb

Risk:
too much cleanup can create metallic or watery artifacts.

---

## 10.11 TIME STRETCH / PITCH SHIFT
Changes:
- time
- pitch
- formant

independently depending settings.

---

## 10.12 EQUALIZE
Destructive EQ processing of waveform.

Difference from Mixer EQ:
Edison edits sample data; Mixer FX are normally non-destructive during playback.

---

# 11. NEWTONE — VOCAL/PITCH BUTTONS

## 11.1 CENTER
Moves notes toward nearest intended pitch center.

Use carefully:
100% correction can sound unnatural.

---

## 11.2 VARIATION
Reduces pitch drift/vibrato variation.

Risk:
too much can remove human expression.

---

## 11.3 TRANSITION
Controls transition speed between notes.

Use:
natural or stylized legato.

---

## 11.4 SYNC
Aligns NewTone playback/sample timing to FL Studio project tempo.

---

## 11.5 CUT MODE
Slices detected note regions.

---

## 11.6 ADVANCED EDIT
Edits note-specific:
- pitch
- formant
- volume
- vibrato-related parameters

---

## 11.7 SLAVED PLAYBACK
Links NewTone transport to the host/project.

---

## 11.8 AUTO-SCROLL
Keeps playback cursor in view.

---

# 12. AUTOMATION CLIPS — CONTROL MOVEMENT OVER TIME

## 12.1 CREATE AUTOMATION CLIP
For native controls:
Right-click control -> Create automation clip.

For many VST controls:
move parameter -> Tools / Last tweaked -> Create automation clip.

---

## 12.2 CONTROL POINT
Defines a value at a time position.

---

## 12.3 TENSION HANDLE
Changes curve between points.

---

## 12.4 STEP MODE
Draws step-like control changes.

---

## 12.5 SLIDE MODE
Moves a point while preserving relative following structure.

---

## 12.6 INIT SONG WITH THIS POSITION
Sets a starting parameter value.

Critical diagnostic:
if a knob jumps at playback start, inspect Initialized Controls.

---

# 13. AUDIO SETTINGS — CONTROLS THAT AFFECT WHETHER FL STUDIO FEELS "BROKEN"

Open:
Options -> Audio settings / F10 settings navigation.

## 13.1 DEVICE
Choose audio driver/interface.

On Windows:
custom interface ASIO is generally preferred where available; FL Studio ASIO is a broadly compatible option.

---

## 13.2 SAMPLE RATE
Common production default:
44.1 kHz is supported and recommended in Image-Line's general guidance unless project/hardware delivery needs another rate.

---

## 13.3 BUFFER LENGTH
Short buffer:
lower latency, more CPU stress.

Long buffer:
higher latency, more stability.

Use:
- smaller for recording/live performance
- larger for heavy mixing if needed

---

## 13.4 UNDERRUNS
If increasing:
CPU/audio pipeline cannot keep up.

Fixes:
- increase buffer
- reduce heavy processing
- use performance optimization
- use Smart Disable where suitable

---

# 14. EXPORT — WHAT THE IMPORTANT OPTIONS MEAN

## 14.1 MODE
Usually:
Full song for final song render.

---

## 14.2 WAV
Lossless uncompressed.

Use:
- archive
- mastering handoff
- high-quality editing

Bit depth:
- 16-bit for broad final playback compatibility
- 24/32-bit for production/archive workflows as appropriate

---

## 14.3 MP3 / OGG / FLAC / M4A
Compressed or alternative delivery formats.

Use according to distribution requirement.

---

## 14.4 SPLIT MIXER TRACKS
Exports individual Mixer tracks.

Use:
- stems
- external mixing
- archiving

Important:
this is different from AI stem separation.

---

## 14.5 DITHERING
Use only when needed for final reduction to 16-bit.

Do not repeatedly dither intermediate files.

---

## 14.6 ENABLE MASTER EFFECTS
Determines whether Master processing is included in render.

Important:
for stem delivery, decide deliberately whether stems should contain bus/master processing.

---

# 15. FL STUDIO 2026-SPECIFIC FEATURES LEARNED

Official 2026 release features include:

## 15.1 ALL-NEW FLEX
Rebuilt preset instrument workflow with a new browser/library structure and lower CPU goals.

## 15.2 CLOUD PROJECT STORAGE
Project backup to FL Cloud from within FL Studio.

## 15.3 GOPHER
In-app assistant that can:
- organize tracks
- set levels
- route audio
- generate Piano Roll scripts
- generate VFX scripts

Important:
Gopher is an assistant, not a substitute for understanding routing/mix intent.

## 15.4 INSTANT CHORD DETECTION
Chord Panel detects notes/chords directly in Piano Roll.

## 15.5 REMIX A SONG
Workflow built around correct BPM plus stem separation.

## 15.6 AUDIO CLIP GAIN CONTROLS
Direct clip-level level balancing.

## 15.7 AUDIO LOGGER
Keeps the last 60 seconds of Master output recoverable.

---

# 16. POST-SUNO WORKFLOW — WHAT FL STUDIO IS GOOD FOR

For MINH TRÍ's current intended use, FL Studio can be treated as a **music repair and production desk after generation**, not merely a beat maker.

Suggested conceptual workflow:

1. Import Suno WAV.
2. Duplicate / preserve original.
3. Detect or confirm BPM.
4. Fit/lock tempo only if needed.
5. Use stem separation when source quality benefits from it.
6. Route stems to separate Mixer tracks.
7. Check clip gain.
8. Correct timing/edit arrangement in Playlist.
9. Clean problematic audio in Edison.
10. Correct selected vocal pitch/timing in NewTone if needed.
11. Use EQ/compression/reverb/delay on Mixer.
12. Automate levels/effects only where storytelling needs movement.
13. Compare against original.
14. Export production WAV.
15. Only later create distribution format.

---

# 17. BUTTONS THAT ARE EASY TO MISUSE

## PAT/SONG
Symptom:
"song not playing"
Cause:
Pattern mode.

## RECORD AUTOMATION FILTER
Symptom:
knobs move by themselves later.
Cause:
automation accidentally recorded.

## SNAP
Symptom:
clips/notes won't go where intended.
Cause:
grid lock.

## STRETCH + RESAMPLE
Symptom:
audio pitch changes when resizing.
Cause:
wrong stretch method.

## INITIALIZED CONTROLS
Symptom:
parameter jumps when playback starts.
Cause:
stored initial value.

## CHANNEL ROUTING
Symptom:
effect appears to do nothing.
Cause:
sound is routed to a different Mixer track.

## MIXER INPUT
Symptom:
mic not recording.
Cause:
wrong input/driver/arm state.

## MASTER ROUTING
Symptom:
track is silent.
Cause:
routing to Master/output broken.

## EFFECT ORDER
Symptom:
mix behaves very differently than expected.
Cause:
FX chain order.

## EDISON FREEZE
Symptom:
editor seems locked.
Cause:
Freeze editing enabled.

---

# 18. CURRENT UNDERSTANDING LEVEL

### L0 — names only
Passed.

### L1 — explain function
Passed for main FL Studio architecture and major controls.

### L2 — choose the right control for a described task
Passed conceptually for:
- routing
- editing
- time-stretch
- automation
- stem separation
- audio cleanup
- pitch correction
- export

### L3 — diagnose common mistakes from symptoms
Partially achieved from official documentation and scenario reasoning.

Examples understood:
- wrong PAT/SONG state
- accidental automation
- wrong Snap
- wrong stretch mode
- wrong Mixer routing
- unwanted initialized control
- wrong audio input
- clipped/noisy source
- destructive vs non-destructive editing choice

### L4 — hands-on operational mastery
NOT PROVEN.

Still required:
- actual FL Studio 2026 session
- identify buttons visually without manual
- complete a real WAV import -> stem/routing/edit/mix/export workflow
- recover from deliberate mistakes
- demonstrate shortcuts from memory
- verify result by listening and file inspection

Current status:

**FL_STUDIO_2026_UNDERSTANDING = L2_STRONG / L3_PARTIAL / L4_NOT_PROVEN**

---

# 19. NEXT HANDS-ON TEST WHEN OWNER ORDERS PRACTICE

A practical verification session should require:

1. Open FL Studio 2026.
2. Identify Toolbar controls without notes.
3. Open Browser / Channel Rack / Piano Roll / Playlist / Mixer from shortcuts.
4. Import one WAV.
5. Route it correctly.
6. Duplicate safely.
7. Extract stems.
8. Rename and route each stem.
9. Adjust clip gain.
10. Create one fade.
11. Create one slice.
12. Fit one clip to tempo.
13. Use one Edison repair operation.
14. Use one NewTone correction.
15. Add one EQ.
16. Add one compressor.
17. Add one send reverb.
18. Create one automation clip.
19. Export full WAV.
20. Export Split Mixer Tracks.
21. Deliberately create one routing error and diagnose it.
22. Deliberately create an initialized-control jump and diagnose it.

Passing this would move the status toward practical L4.

---

# 20. OFFICIAL SOURCES USED

Image-Line FL Studio 2026 release:
https://www.image-line.com/fl-studio/release/2026

Main workflow:
https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/basics_workflow.htm

Toolbar:
https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/toolbar_panels.htm

Browser:
https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/browser.htm

Channel Rack:
https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/channelrack.htm

Piano Roll:
https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/pianoroll.htm

Playlist:
https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/playlist.htm

Audio Clips:
https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/playlist_audioclip.htm

Mixer:
https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/mixer.htm

Automation Clips:
https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/playlist_automationclip.htm

Sampler / time stretching:
https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/chansettings_sampler.htm

Edison:
https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/plugins/Edison_5.htm

NewTone:
https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/plugins/Newtone.htm

Audio Settings:
https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/envsettings_audio.htm

Export:
https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/fformats_save_export.htm

Shortcuts:
https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/basics_shortcuts.htm

---

# 21. FINAL LEARNING CONCLUSION

The correct model is not "memorize icons."

The correct model is:

**intent -> data/audio location -> right window -> right control -> expected signal change -> verify by listening/meter/timeline -> undo if result differs**

For post-Suno work, the most important chain is:

**Audio Clip -> Playlist edit -> stem/routing -> Mixer processing -> automation -> Master -> export**

And the most important recovery question is:

**Where is the signal right now, and which control is actually acting on it?**

That question prevents most beginner FL Studio confusion.
