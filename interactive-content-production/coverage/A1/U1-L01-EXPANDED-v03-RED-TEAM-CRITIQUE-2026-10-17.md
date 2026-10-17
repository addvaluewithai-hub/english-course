# A1 U1-L01 v03 — RED-TEAM editorial + product readiness critique

**Reviewer:** the author of the v03 candidate, performing a **self-critique** rather than falsely claiming independent approval.  
**Source:** [18-turn v03 dialogue](U1-L01-EXPANDED-DIALOGUE-v03.CANDIDATE.json), [7-scene editorial plan](U1-L01-EXPANDED-FULL-LESSON-DESIGN-v03.md), [36-ID manifest](U1-L01-EXPANDED-EDITORIAL-MANIFEST-v03.CANDIDATE.json), current [A1 Stage-07 brief](https://github.com/addvaluewithai-hub/english-course/blob/main/curriculum/levels/a1/design-review/07-lesson-briefs/lesson-briefs.md), [lesson contract](../../LESSON_CONTRACT.md).  
**Disposition:** **CHANGES_REQUESTED / EDITORIAL FAIL for v03 as a build-ready package**. Not a judgment that an expanded listening-first approach is wrong. Owner requested exploring a fuller, natural dialogue; that **does not mean this particular edition is accepted or licensed for paid TTS**. 

## Exact factual audit

- Draft dialogue has **18 two-speaker turns / 140 whitespace-counted English words**.
- Editorial manifest has **7 scenes, 20 beats, 6 MC questions + 1 final Speaking, 6 clip IDs**, one separate reading card.
- **All six MC answer IDs occupy option index 0** (the first answer) in the manifest. The user-facing board has no specified seeded shuffle/position balancing. Even without leaking actual answer text, this introduces a **position bias**.
- Playback of mandatory `full-conversation` + `first-contact` + `wellbeing-contrast` + `class-photograph` + `advice-and-close` means **41 rendered dialogue-turn playbacks**, versus 18 distinct turns. That is **2.28× the original source-turn count**, *before* 20 Otti narration beats, 6 question/feedback cycles, a reading task and live Speaking. The separate `leave-taking` is an optional extra 3 turns.
- Exact 36 source IDs are retained in the candidate source map, with **12 still marked owner ruling required**, **7 explicit productive items** (5 phrases + `excited`, `feeling`). Everything is marked `actualStudentEvidence: NOT_COLLECTED`.
- The previous "16/16 PASS" was an **ad hoc editor consistency assertion** (IDs, files, null timestamps, clips, etc.), **NOT** a saved automated lesson test, app build, source-coverage `ready` gate, real waveform review, browser screenshot QA, or evidence that learning succeeds.

## P0 / must resolve before declaring editorial script final

### CRT-01 — Correct answer is ALWAYS first (six of six)

The correct option has index **0** for `q01`, `q02`, `q03`, `q04`, `q05`, `q06`. A pattern-aware student, test fixture, or buggy QA path can pass by clicking the first option without understanding. **Fix:** create balanced positions in authored choices **or** deterministic seeded shuffling with answer ID semantics preserved. Test real rendered order, answer alignment and wrong-choice feedback after permutation. Do not shuffle on re-render, or the selected answer could change underneath the learner.

### CRT-02 — Scene S01 calls a photo-detail question "gist-first"

`s01-set` says "ركز ... Leo ورّى Maya إيه؟"; `q01-cat` asks whether Leo shows a cat photograph, a friend's photograph or a book. The item is introduced at **turn 10 of 18**. That checks delayed detection/recall of a **specific mid-dialogue prop**, not the gist of why Maya and Leo are interacting. It potentially pushes an absolute A1 beginner to listen anxiously through many unknown words searching for the prop, rather than understanding the first contact.

**Fix:** decide an **authentic non-spoiler listening goal**. Option A: first-listen assess broad social situation with plausible alternatives **only after** neutral setup/boards (do not repeat old answer leakage). Then quiz cat/photo *after targeted Act B replay*. Option B: retain an audio-dependent detail question but honestly rename the skill and place it in an appropriate detail-listening segment. Real audio-muted test is mandatory: no setup/board may disclose the keyed answer. Do not use an obvious "two people meeting" board before a "meeting" gist MC.

### CRT-03 — The story bends around ledger words, causing a causal/communicative break

After both speakers have already exchanged names (T01–T02), Leo asks at T08 "The teacher says, 'Introduce yourself.' What can I say?" then Maya instructs him to start with his name (T09). Leo abruptly produces a photograph of his cat (T10), followed by an argument about whether the cat is sad or tired (T11–12). Maya's "Is everything okay?" (T13) ambiguously refers to Coco rather than Leo's class anxiety; Leo replies "Nothing is wrong. But can I ask for advice?" (T14), as if the previous exchange had not addressed his nerves. This *can* be made coherent, but v03 currently sounds **vocabulary-serving rather than naturally happening**.

**Fix:** write one clearly motivated *first-day class* arc: greeting → first-day nerves → practical self-introduction task/photo as optional personal prompt → small correction → practical tip → confident goodbye. E.g. make clear the teacher asked each student to introduce themselves **to the class with one thing they like** (different from privately exchanging names). Connect T13 and the tip to Leo's known nerves; otherwise trim/move the photo/advice subplot after explicit source-owner review. Do **not** use "the ledger has this word" as a reason to keep unnatural dialogue.

### CRT-04 — v03 called a "full authored lesson", but executable content is NOT complete

The manifest `scenes[].beats[]` contains **IDs, boardState IDs and clip IDs**, not the exact authored Otti `speech`, `readText`, accessibility `altText`, per-beat state or transition rules required by [LESSON_CONTRACT](../../LESSON_CONTRACT.md). Those are scattered in Markdown. Manifest `assessment.feedback` is literally `"full exact Arabic authoring in linked editorial script"` for **every** MC, while detailed right/wrong feedback is actually authored only for S01; S02–S06 feedback is described generically ("Wrong explanation...", "record receptive", "feedback quotes ...") rather than present as immutable utterances per outcome.

**Fix:** before producer integration, create **one machine-readable authoritative lesson authoring package** with `sceneId/beatId`, exact Egyptian Arabic `teacherSpeech` and accessible `readText`, `boardStateId`, reveal phase, clip ID, full question/options, independent right/wrong *spoken* explanation, misconceptions per option, alt text, expected learner evidence and progression. Then write a repeatable schema/coverage QA that checks no missing branches or orphan IDs. Markdown can be editorial guidance, but should not be the only source of exact runtime speech.

## P1 / substantial pedagogical and assessment changes

### CRT-05 — A1 cognitive and audio burden is unvalidated

18 turns/140 source words is plausible **for an upper A1 or carefully scaffolded learner**, but absolute first-lesson beginners may struggle, especially with contractions, `afraid`, `feeling`, `it's/its`, `isn't`, `nothing`, `advice`, `photograph`, a quoted imperative and 6 MC stops. The mandatory replay plan totals 41 dialogue turns and adds 20 Otti teaching lines. An attractive storyboard does not prove tolerable seat time.

**Fix:** separately time each segment and narration after real synthesis; run a first-time A1 comprehension pilot, assess frustration/time-on-task, expose short chapters and pause/replay, and consider **a short 8–12 turn core** with a coherent extended source if owner approvals require it. Never silently drop required items; source scope decides what must be first-introduced versus encountered elsewhere. No invented minutes until measured.

### CRT-06 — Several receptive mappings are only mentions, not diagnostic evidence

The manifest maps `advice`, `nothing`, `its`, `photograph`, `sad`, `tired`, `afraid` to a beat labelled `receptive-question`; nevertheless the actual Q03 tests **both** emotional states with stark "only tired/only sad" distractors, Q04 tests the obvious correction for a *new tired dog* while its prompt already states "not sad, tired", and Q05 asks which friendly recommendation fits an anxious classmate—not whether the learner understood the **word advice** as heard in the audio. `nothing` and `its` have no independent keyed recognition probe tied to their meaning.

**Fix:** provide a source-ID × actual *question/prompt/accepted evidence* matrix. Use plausible changed-context distractors: e.g. `nothing is wrong` vs `something is wrong`; `its name` vs `it is` **in text**, recognizing the forms are **homophones in sound**; ensure audio-only tests do not claim spelling/ownership recognition from /ɪts/. Keep MC receptive, not productive.

### CRT-07 — Productive evidence is not an assessment instrument yet

Five phrases `Good morning`, `How are you?`, `pretty good`, `really good`, `Thank you`, plus `excited` and `feeling` are linked **all to the single `s07-new-person` beat**. There is a proposed status list (`observed_independent/supported/not_evidenced`), but no prompt sequence, turn-linked provenance, delayed/retrieval contract or implementation schema. A strong natural social encounter may use just `really good` and another valid synonym, and should not be penalized because a learner doesn't unnaturally produce all seven strings in one conversation.

**Fix:** differentiate **successful meaningful first contact** from per-item productive proof; define separate, natural prompt opportunities across changed contexts (morning greeting, two different wellbeing moments, after-class feelings), preserve actual audio/transcript and evidence strength, and seek owner-approved retrieval timing for genuinely unelicited exact target phrases. Otti completion should not falsely set seven independent mastery flags.

### CRT-08 — The reading check is useful but unproven as independent evidence

S06 introduces a genuinely unseen `WELCOME TO ENGLISH CLASS` note, better than treating audio as reading. But the selected right answer almost **copies the printed instruction**, and the question has two obviously irrelevant distractors; `yourself` is not necessarily independently understood merely because the learner matches the whole chunk.

**Fix:** assess one small meaning-bearing change such as the action or addressee using natural distractors, do not have Otti read the answer to the learner before the attempt, retain accessibility read-aloud as **supported** evidence, test at narrow phone widths, and flag that one card is **bounded** reading evidence rather than proof of general transferable text comprehension.

### CRT-09 — Visual reveal and sync claims exceed the executable contract

The B-states are thoughtful specifications but **there is no v03 React/SVG implementation, alt text asset, viewport sheet or runtime event map**. Teacher speech from Gemini Live is not presently supplied with audited per-word audio timestamps. A reliable board change can be **beat-aligned after audible start/finish**, but the draft's “exact when spoken” implication would be overstated unless an explicit speech-cue alignment implementation and real provider evidence exist. WAV transcript word timing is a *different* problem from Otti's live narrated audio.

**Fix:** author an event table for each beat `BEFORE_TTS` / `PCM_STARTED` / `PCM_DRAINED` / `SOURCE_AUDIO_STARTED` / `SOURCE_AUDIO_TURN` / `QUESTION` / `FEEDBACK`. Freeze and capture all states with actual `A1FirstMeetingVisual.tsx`. Call source audio **word-synced only when true timestamped data exists**; label Otti board as **beat-synced** until better evidence.

### CRT-10 — Source arc lacks an early choice/attention check before a long play

All 18 turns play before the first comprehension choice. This may be acceptable for an immersion segment but is a risk for zero-start A1, because a student may disengage before the photo twist at turn 10. The draft doesn't say how Otti gives the learner explicit replay/stop/pause permission, or how the full-listen scene deals with partially understood outcomes. **Fix:** first-load permission/fail-closed test, visible short listening goal, optionally two-stage gist then detail and rewind, automatic replay on request, and a learner-tolerant retry without losing evidence of first incorrect attempt.

## P2 / quality and QA discipline

### CRT-11 — Distractors are too easy or artificial

Examples: choosing "I'm Omar" against "Goodbye Nora" for a name question, or giving the worried classmate "Tell everyone to go home" as a competing piece of advice. These detect some basic recognition but can be answered by social common sense or removing ludicrous choices. **Fix:** plausible same-domain distractors without trickery; authored per-distractor misconceptions and targeted spoken wrong feedback.

### CRT-12 — Production handoff is not producer completion

The 16 assertions checked candidate shape only and were **not checked into a runnable test suite**. New content has not been implemented against the product React/QA registry, and the old screenshot run on EnglishLive #54 cannot demonstrate new v03 board states. **Fix:** save executable assertions as CI tests, integrate into existing producer branch **without competing claimed PR**, run typecheck/tests, capture all screenshots and examine contact sheets, test real WAV/PCM/Live Speaking; separate actual results from plans.

### CRT-13 — Two-voice candidate is a valid-looking paid factory JSON with only textual guard

The draft JSON follows most of the real paid request shape (including `routing`, voices, transcript and metadata), with `purpose: EDITORIAL-DRAFT-DO-NOT-DISPATCH`. This is useful for authoring but a future user could still paste and run it if the factory ignores metadata. **Fix:** keep it explicitly out of the executable request path, require exact version/hash/job ID/cost cap and approval before copying to a dispatchable production request. Do not reuse or overwrite `pilot02`; do not mark released because JSON parses.

## Suggested sequence, not a silent redesign

1. **Rewrite story logic and simplify target density**. Make name exchange → first-class nerves → class task/photo → advice → goodbye causally connected. Preserve the owner's preferred **test expansion first** direction while critically checking whether all 12 source items fit *naturally*.
2. **Correct the first-listen task and all six MC positions**, then create meaningful, non-answer-leaking prompts/distractors and exact right/wrong explanation script.
3. **Create one production-ready teacher + board + clip package** with exact speech/alt/state/quiz/evidence fields, based on the source-approved dialogue, so the existing producer doesn't hand-copy Markdown.
4. **Close source evidence gaps**: every item mapped to an actual specific check or clearly bounded role; productive phrase/word evidence must not be automatically awarded. Seek the owner's 12 exact semantic/lifecycle judgments **against the revised story**, not against an obsolete 6-turn source.
5. Existing EnglishLive producer builds the 7-scene app and SVG visual variants, adds Playwright and live/audio tests, and supplies before/after QA proof.
6. Only after exact source edition and price cap approval: commissioned Gemini WAV + reviewed transcript + clip offsets + time-sync QA. Independent editor/learner re-review and owner release follow.

## Test expectations for v04

| Audit | Pass criterion | v03 verdict |
| --- | --- | --- |
| Choice positional bias | Correct IDs balanced/seeded across answer positions, order stable | **FAIL: all first** |
| First listen skill | Gist genuinely assessed or renamed to detail; no answer leak | **FAIL: mislabeled detail** |
| Narrative causality | Actions and help requests follow a believable class situation | **Needs rewrite** |
| Authoritative executable teacher/quiz text | Each beat and both MC outcomes have immutable exact speech | **FAIL: placeholders** |
| Locked 36 source IDs | Still exact with roles and 12 explicit owner decisions | **Structural only** |
| Per-word evidence | Not inferred from authoring mention; accepted proof matrix | **Missing** |
| SVG/app UI | Actual visuals, 3 viewport screenshots inspected | **Not implemented/tested** |
| Audio and Otti live | Final WAV, audited times, real device/teacher QA | **Not commissioned/tested** |
| Approval | Owner signed scope, spend and release separately | **Outstanding** |

**Final editorial verdict:** This v03 is a useful **concept and coverage exploration**, but **NOT an implementation-ready source of truth, NOT an audio approval and NOT `LESSON_REVIEW_PASS`**. The author cannot independently approve their own rewritten lesson; a second reviewer/owner must critique v04 once it becomes executable and testable.
