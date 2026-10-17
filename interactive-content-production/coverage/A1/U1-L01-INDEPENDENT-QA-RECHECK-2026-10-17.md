# A1 U1-L01 — Independent adversarial QA recheck (session 2)

**Reviewer date:** 2026-10-17 (Africa/Cairo)  
**Lane:** LEARN; **role:** LESSON_REVIEWER; **step:** OWNER_DECISION_WAIT  
**Disposition:** **BLOCKED_OWNER_DECISION** + concrete **CHANGES_REQUESTED** for the existing product draft.  
**No authorization inferred:** Do not rewrite canonical locked material, take ownership of [product PR #54](https://github.com/addvaluewithai-hub/englishlive/pull/54), run paid `pilot02`, merge, deploy, accept the lesson or begin U1-L02.

## Live-state reconciliation (session 2)

- [English Course PR #13](https://github.com/addvaluewithai-hub/english-course/pull/13) remains **open draft**, with **0 reviewer submissions and 0 owner decision comments** at recheck. Its handoff control state `OWNER_DECISION_WAIT` is **not yet on `main`**.
- [EnglishLive PR #54](https://github.com/addvaluewithai-hub/englishlive/pull/54) remains **open draft** at product head `d9081ddab09d008453fd2e6200381c1a06b836de`; no accepted reviewer submissions or changed product commit found. Authoring is reserved to its existing owner/producer.
- The authoritative [A1 status](https://github.com/addvaluewithai-hub/english-course/blob/main/interactive-content-production/status/A1.md) still reports `U1-L01=in-progress`; `U1-L02=not-started`. No source-role change has been approved.
- Full 12-ID owner decision options and lifecycle consequences remain in [session-1 decision brief](U1-L01-OWNER-DECISION-BRIEF-2026-10-17.md). **This addendum examines the testability and technical/teaching contract; it does not replace that brief.**

## Three source-grounded findings

### P1 — Audio comprehension MC is over-cued **on both sides** of the listening clip

**Evidence:** [`listeningTeacherScript.ts`](https://github.com/addvaluewithai-hub/englishlive/blob/feat/a1-u1-l01-listening-led-otti-pilot/src/lessonScenes/a1/listeningTeacherScript.ts), `first-listen/scene-set`, pre-audio: "هنسمع Maya وLeo بيتقابلوا" and board "Two people meet for the first time." After the full clip, `first-listen/big-picture` says they greeted, exchanged names and asked "How are you?", with a board presenting exactly those three facts. The [definition](https://github.com/addvaluewithai-hub/englishlive/blob/feat/a1-u1-l01-listening-led-otti-pilot/src/lessonScenes/a1/listeningTeacherPilot.ts), `first-listen.activity`, asks *what they were doing*, keyed to "They meet, say their names, and ask how they are." A correct click is therefore compatible with **not understanding or even hearing** the English source.

**Critique of session-1 review:** Earlier reporting highlighted **pre-listening** answer leakage but did not explicitly flag the **post-listening `big-picture` line and board before grading**; fixing pre-audio alone would leave the assessment compromised.

**Producer fix request:** Keep scene set-up neutral (who will speak; why listen), and keep post-listen transition procedural ("Choose what you heard") rather than pre-solving the question. Use a comprehension question with an acoustically discriminating detail from the current six-turn recording, balanced A1 distractors, a replay affordance and feedback tied to the heard detail. Do not make the student guess a fact taught only after the clip.

**Proposed QA checks:**
1. With the **audio muted/omitted** but narration and boards intact, a beginner reviewer should not have the keyed answer revealed; the app must still block completion if recording is unavailable.
2. With **actual audio**, the target detail is audible clearly and still checkable on replay.
3. Correct/wrong feedback justifies the source detail, and no board reveals the answer before selection. Screenshot state alone does not prove 1–2.

### P1 — The named wellbeing excerpt omits the reply that Otti claims to replay

**Evidence:** [`listeningAudioPilot.ts`](https://github.com/addvaluewithai-hub/englishlive/blob/feat/a1-u1-l01-listening-led-otti-pilot/src/lessonScenes/a1/listeningAudioPilot.ts) defines `wellbeing-exchange` as only `how-are-you` (Maya: "How are you, Leo?") and `fine-thanks` (Leo: "Pretty good, thanks. And you?"). Maya's *"Really good, thank you. Bye!"* is the next `okay-bye` turn and **not** in this clip. But in [`listeningTeacherScript.ts`](https://github.com/addvaluewithai-hub/englishlive/blob/feat/a1-u1-l01-listening-led-otti-pilot/src/lessonScenes/a1/listeningTeacherScript.ts) the `ask-how-are-you/listen-wellbeing` beat explicitly replays `wellbeing-exchange`, then `wellbeing-meaning` immediately describes Maya's **"Really good, thank you"** as if demonstrated in the local replay.

**Bounded conclusion:** The full six-turn original dialogue includes that Maya reply, so the line has been heard **once** if first listening played. The **targeted wellbeing replay**, however, does not demonstrate the quoted reply; this risks a learner losing the referent. It is a *script/clip mapping mismatch*, not a claim that English is absent everywhere.

**Producer choices (before any paid recording):** Either (A) restructure the authored source so Maya's final wellbeing reply is a clean separate turn or segment and the reviewed wellbeing clip includes it, preserving natural goodbye separately; **this requires a fresh approved TTS request edition** and re-timed bounds, or (B) stop saying Maya's answer was in that local replay and instead refer unambiguously to the earlier full dialogue and present the phrase as a separately modelled illustration. B avoids creating a 2-speaker audio job solely to fix a script/reference mismatch, but produces less effective focused replay.

**Proposed QA checks:** A learner can point to the exact audible "Really good, thank you" in the reviewed playback being discussed. Inspect actual six turn boundaries and segment trims, verify no goodbye is cut/incorrectly attached, and verify script versus approved WAV/transcript. **Do not insert guessed milliseconds or synthesize without owner approval.**

### P2 — Approved media timing validation currently checks shape but not chronological consistency

**Evidence:** In [`validateLessonAudio`](https://github.com/addvaluewithai-hub/englishlive/blob/feat/a1-u1-l01-listening-led-otti-pilot/src/lessonScenes/a1/listeningAudioPilot.ts) an approved package requires HTTPS URL fields and each turn and clip to have finite `startMs<endMs`; it **does not check** turn order/overlap, clip-to-turn alignment, or invalid gap/clip containment. [`LessonAudioController.ts`](https://github.com/addvaluewithai-hub/englishlive/blob/feat/a1-u1-l01-listening-led-otti-pilot/src/audio/LessonAudioController.ts) stops clips on `timeupdate` at `end - 25ms`, so precision and possible spill into the next turn require real-device confirmation; `timeupdate` alone doesn't establish sample-accurate boundaries.

**Why it matters:** Synthetic test data with each bound individually positive can still represent overlapping turns or a clip that spans the wrong speech. Once owner-approved WAV exists, that can be a **release correctness failure** even with all structural tests green.

**Producer test requests:** Add synthetic negative fixtures for (i) out-of-order turn bounds, (ii) overlapping adjacent turns unless explicitly approved crossfades, (iii) clip bounds failing to contain its declared turns, (iv) wrong clip-to-turn order, (v) missing or extra word-aligned transcript spans, and (vi) actual playback start/end under seek stall and normal/turbo browser timeupdate frequency. Reject inconsistent manifests rather than making them `approved:true`. A fixed 25ms threshold cannot substitute for audible boundary review.

## Adversarial acceptance matrix — runnable by the existing producer after approvals

| Test | Stimulus | Expected pass condition | Type / present status |
| --- | --- | --- | --- |
| LSN-01 | Audio unavailable, learner attempts first MC | No listening completion; readable recoverable retry; teacher does not pretend audio was heard | **Live not tested**; authored fail-closed intent observed |
| LSN-02 | Audio muted, same pre/post Otti prompts and boards | MC answer not already revealed by surrounding Arabic/English text | **Static FAIL** (P1) |
| LSN-03 | Real audio, first listening + replay | Specific audible detail assessed; re-listen available; wrong answer explained | **NOT TESTED**; WAV missing |
| LSN-04 | `wellbeing-exchange` replay | The lines referred to by Otti are actually audible within the named replay, not merely in full audio | **Static FAIL** (P1 mismatch) |
| LSN-05 | Approved manifest with synthetic crossed/overlapping turn offsets | Validation rejects materially inconsistent segment bounds | **Not covered by current validator** |
| LSN-06 | Clip near next turn boundary, Chrome/Safari/Android | No audible next-speaker fragment, lost initial phoneme or premature successful completion | **NOT TESTED** |
| OTI-01 | Otti PCM still audibly speaking before WAV | No overlapping Otti/recorded media and learner mic stays closed through loading/playback | Mock queue tests only; **real provider not tested** |
| OTI-02 | Interruption, permission error, seek stall, WAV decoder failure, reconnect | No success or lesson advance on error; no mic echo, stuck gate or double advance | **NOT TESTED** |
| SPK-01 | Silence, `Okay`, `Bye bye bye` | No fabricated completion; contextual prompt/repair with room to respond | Fixture guidance exists; **Live not tested** |
| SPK-02 | Valid equivalent greeting/name/wellbeing alternatives | Meaningful exchange accepted naturally; no scripted exact-match requirement | **Live not tested** |
| SPK-03 | Five separate productive source phrases; some naturally not spoken in one encounter | Each has actual recorded production evidence or explicit owner-approved retrieval plan; no unsupported "mastered" inference | **Evidence incomplete**, owner decision needed |
| VIS-01 | Re-recorded dialogue/changed teacher beat, 320x640, 400x860, 1280x900 | Rerun current screenshots/contact sheets and inspect originals; no overlapping or revealing board | Prior GitHub frame run claimed green; **new revision not retested** |
| DEP-01 | Cloudflare preview on `d9081dda` | Deploy logs examined independently of GitHub code CI; build outcome explained | Cloudflare bot reported **failed preview**, cause **UNVERIFIED** |

**Differentiation:** Static verdicts come from **authored source/code read**. "Not tested" means no local browser, real WAV, device, or live Gemini run was performed by this reviewer. The current [product QA ledger](https://github.com/addvaluewithai-hub/englishlive/blob/feat/a1-u1-l01-listening-led-otti-pilot/production/a1-u1-l01/QA_STATUS.md) and PR description are evidence pointers, not substitute playback.

## Priorities, ownership, recheck

1. **P1, existing U1-L01 product producer:** eliminate both pre- and post-listening answer leakage. Re-test LSN-02 before viewing LSN-03.
2. **P1, product producer + curriculum reviewer:** settle wellbeing clip/script match; if TTS script changes, seek explicit new-edition signoff and no paid generation of stale `pilot02`.
3. **P2, existing product producer:** strengthen audio-boundary validation and tests before marking a future media manifest approved.
4. **Owner / curriculum authority:** resolve the **12 locked scope escalations** in PR #13 report; especially productive vs receptive distinctions and any Stage-06 lifecycle updates. **No owner decision is presumed** from "next session".
5. **Independent reviewer:** after producer fixes + owner rulings, reread PR diff and real browser/WAV/Live evidence, recheck counterexamples and only then consider `LESSON_REVIEW_PASS`. No self-review PASS for producer.

## Self-critique and limits

**Corrected prior blind spot:** Session 1 noted leakage in the **pre-audio** scene-set but not the **post-audio** big-picture beat; this document addresses both. A learner might also legitimately infer the type of interaction from context even with neutral prompts; the test should distinguish **teaching target before hearing** from mere reasonable prior knowledge, and use audio-specific detail rather than claim all correct guesses are impossible. **Clip mismatch nuance:** Maya's `Really good` IS in the full conversation, just not in the named 2-turn replay; avoid inaccurately claiming it never plays. **Timing risks:** Manifest acceptance weakness is statically visible; a real boundary leak is a *hypothesis* until a real synthesized WAV is played.

**Next permitted action:** owner chooses 12 source scope dispositions and exact paid-media approval; existing producer can address non-semantic P1 code/script fixes on PR #54 within their claim; then reviewer independently rechecks. **Lesson U1-L02 stays not started.**
