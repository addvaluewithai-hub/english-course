# Listening-first production pattern — context before isolated phrases

**Recommended when the canonical lesson skill is spoken interaction or receptive listening.** Not a mandate for every reading, writing or grammar lesson. Source of truth remains the applicable level/lesson brief, semantic locks, prerequisite roles and human review decisions.

## Pedagogical sequence

1. **Short situational orientation (Arabic A1-friendly if needed):** identify who/where, the global listening task, never read the entire conversation or reveal quiz answers beforehand.
2. **One complete listening:** two distinct natural speakers, meaningful situation and enough time to hear without Otti talking over it. First check is comprehension of the *situation* rather than exact recall of one unfamiliar word.
3. **Teach by revisiting authored recordings:** Otti reads a short approved explanatory line, invokes or schedules `play_lesson_audio({clipId})` for a stable reviewable segment, highlights that part of the board and teaches a useful phrase/grammar chunk in its communicative purpose. Add non-scripted clarification only if learner needs it.
4. **Active recognition via MC** when appropriate: distractors should be plausible, objectively keyed and teachably explained whether selected right or wrong. Wrong MC can continue after explanation but is not proof of spoken mastery.
5. **Separate final Speaking** if this lesson's performance requires productive transfer. New person/context, no full transcript or model answers visible, Otti handles learner's actual reply and decides when the main outcome is demonstrated.

**A1 example:** canonical `U1-L01 — Hello. I'm …`: two people meet, exchange names, ask about wellbeing, close politely. Do not mix later age, origin, occupations or broader news reactions into U1-L01 just because a dialogue could contain them.

## Audio content package (canonical source, independent from speech renderer)

- Every dialogue has an **immutable script**, actor/speaker IDs, level/lesson version, simple recording instructions, and one playable master recording with approved pronunciation/pace.
- The delivered master must include an auditable transcript, per-word/per-turn timecodes derived from the **rendered audio** (not scripts or character lengths), and stable authored clip IDs such as `full-conversation`, `name-exchange`, `wellbeing-exchange`.
- For each clip define `clipId`, `startMs`, `endMs`, `turnIds`, learner-visible transcript access rules, and scene/beat that can request it. Ensure boundaries contain complete words.
- Studio generation, transcription, timestamps, media hosting and accessibility files belong in a separate bounded **content-production job**, not inside an always-on Gemini Live session or a paid request for each student's replay.
- Asset status lifecycle: `script-approved` → `studio-request-prepared` → `audio-generated` → `timings-audited` → `audio-approved`. Missing/failed audio must not count as completed listening. Never silently substitute another voice or assume fake playback succeeded.
- Record edition and immutable asset identity. Regeneration requires a new edition and review; don't overwrite the previous clip that students may already cache.

## Runtime responsibilities (in EnglishLive product repo)

```text
Otti reads authored setup line
→ application waits for Otti PCM to drain
→ play approved asset clip (master URL + reviewed range)
→ highlight speaker/current phrase using rendered-audio timecodes
→ audio actually ends
→ notify the teaching director (not before)
→ next authored line / keyed MC / repeat segment
→ final speaking with Otti Live
```

- Application owns actual audio playback, clip lookup and timing. The Gemini client tool `play_lesson_audio({clipId})` may ask only for registered clip IDs; arbitrary URLs and arbitrary start/end times are forbidden.
- Only one audio source at a time: suspend learner mic and Live Otti playback while the recorded lesson clip plays; resume coherently on completion, interruption or media error.
- **Blocking tool completion means the physical audio ended,** not a tool call was acknowledged, queued or a timer elapsed. On failure return a truthful error; don't advance the authored narration.
- Playback can be learner-initiated (Replay button) as well as Otti-initiated. Let students repeat useful segments and expose current speaker/line only after appropriate first-listening rules.
- Long asset loads must time out and permit retry; avoid zombie pending Gemini tool calls or opening the mic in an incorrect state.
- If the recording is *not* accessible to Gemini as an actual input source, give Otti the script and timing metadata and say clearly he knows the authored recording **from metadata**, not from having literally heard its audio.

## Required QA states and release evidence

In addition to every teaching beat and MC branch, capture: `listening-before`, `audio-playing` for each clip beat, `replay-available`, `transcript-revealed`, `audio-error/retry`, `speaking-without-model`. Test at 320x640, 400x860, 1280x900 with real shared product components.

Browser-frame QA is not audio QA. Actually listen to the produced asset at a real playback speed and test: exact speakers, clear English, first-listen answer not leaked, clip boundary not slicing words, timecode/text synchronization, no Otti overlap, mic gating, unsupported autoplay, interruption/reconnect, malformed input, final live speaking under weak/incoherent responses.

An explicit **approved recording** and separate live-Otti/device QA are release gates; a nice contact sheet or a correct JSON manifest does not imply real recording exists.

## Pilot references (not completed releases)

- EnglishLive [Draft PR #54](https://github.com/addvaluewithai-hub/englishlive/pull/54): A1 U1-L01 authors a first-contact listening lesson, multi-choice comprehension and final Speaking.
- Audio recording is produced through a **separate Gemini TTS Factory request**. The pilot's recording-production handoff is `englishlive/production/a1-u1-l01/README.md`. The request being prepared is not evidence of generated or approved audio.
- Status remains `in-progress` in A1 until owner review and production evidence are complete.
