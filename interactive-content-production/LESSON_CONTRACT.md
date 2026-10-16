# LESSON CONTRACT — content, states, progression and proof

This is a **portable authoring shape**, not a drop-in React/EnglishLive schema. A product adapter converts the editorial package into the actual live lesson runtime. See [template](templates/lesson-package.example.json).

## Canonical identity

Each package references:
- `courseRepo` / `courseCommit` / `levelId` / `unitId` / `lessonId` / `lessonBriefPath` / `semanticLockPaths`.
- `unitOutcome` and `foregroundItems` vs `supportItems` vs `retrievalItems`; exact targets may not be silently promoted.
- `contentRevision` and `ownerStatus`, with explicit scope: sample chapter, full authored lesson, or deployed product.
- Stable scene/beat IDs; any reordering/replacement is recorded in a content change note.

## Listening-led branch (when appropriate)

For real spoken or receptive conversation lessons, follow [LISTENING_FIRST.md](LISTENING_FIRST.md): author a two-speaker dialogue and its educational purpose, generate/review the recording separately, attach trusted rendered-audio timestamps and named replay clips, then tie actual clip playback to authored explanation beats. Do **not** treat missing prerecorded audio or synthetic preview as successful listening.

## Teaching unit fields

Every `scene` must declare:
- `purpose` = concrete learner understanding/action, not only topic.
- `beats`: `beatId`, `speech` (wording Otti will be asked to read), `readText` (if standalone readable mode), `visualIntent` (what *meaning* gets revealed, why now), `boardStateId`, `boardSummary`, `altText`.
- `visual`: descriptive diagram specification with explicit `portrait` and `landscape` arrangements; point to custom SVG/React code in the **product** when implemented, not an invented file in the curriculum repo.
- `assessment` (optional): question, prompt context, options with stable IDs, correct ID, per-choice misconception, and distinct `correctFeedback` / `wrongFeedback`. Correct answer must not be accidentally displayed on `question` state.
- `hint`: trigger and escalating support if the scene requires help. Hints must be clearly clickable and not clutter the base lesson surface.
- `progression`: what constitutes a teacher question, answer click, completed feedback, next authored line, or final live Speaking decision.

## Canonical classroom state flow

```text
TEACH_BEAT -> (audio actually ended) -> next TEACH_BEAT
last beat -> QUIZ_READY
QUIZ_READY -> click(choiceId) -> (grade deterministically)
-> ANSWER_RECORDED(correct|wrong)
-> authored VOICE_FEEDBACK -> (audio actually ended)
-> TEACHER_NEXT_TOOL_REQUEST -> next scene
...
FINAL_SPEAKING -> Otti listens/responds/repairs -> Otti decides completion
```

- Otti chooses when a meaningful *spoken* conversation is sufficient, not the app's keyword regex. Preserve evidence summary and ungraded status limitations.
- Deterministic MC key is owned by content/runtime, **not invented or judged** by Otti.
- `attempt.answered=true` is not the same as `attempt.correct=true`.
- Wrong MC answers can advance after **reasoning**; preserve a pending review item. No fake "mastered".
- One audio completion can advance at most one beat; interruptions/reconnections must not skip unread lines.
- Silence, arbitrary words, generic acknowledgements or goodbyes must not be considered B1 Speaking mastery.
- Real voice feedback must not overlap the next narration line.
- Phone-sized board has no **internal** scroll. Fit one idea in the stage or split into multiple beats. The page as a whole may scroll when required for accessibility; never clip content or hide touch targets to satisfy an artificial no-scroll rule.

## Board design: top-quality pedagogical SVGs

1. Visualize a *meaningful relationship* (timeline, conversation move, cause/effect, distance/contact, choice/contrast), not a row of generic emojis.
2. Draw **state progression**: what changes from Beat 1 to Beat 2. Don't repeat the same board throughout the scene.
3. Keep labels short and readable at narrow-phone sizes; reserve layout so reveals don't move the whole page.
4. Treat Arabic/English bidi deliberately, with isolated English runs and tested punctuation.
5. Otti can stand at lower-right of the board if not covering learning content. Provide a dedicated safe zone in both desktop/mobile layouts; reposition for very short viewports.
6. Keep contrast and visual meaning independent of color; use accessible labels/icons and reduced-motion fallback.
7. Screenshots *prove rendering*, not that the diagram teaches correctly. Inspect semantic alignment with script separately.

## Question construction

- Ask about what **was just taught**, but with changed details; don't let one distractor be obviously ridiculous while others are plausible.
- Right and wrong feedback must explain why, with the correct example. No response should congratulate an incorrect choice.
- MC checks receptive understanding, but the lesson's independent speaking objective survives. Do not turn the whole course into multiple-choice tests.
- For grammar/phrases, include a context rationale, not mechanical literal translations. Correct student alternatives during final Speaking fairly when meaning is conveyed in natural English.

## Example mapping for B1 U1-L02

The authoritative brief: `curriculum/levels/b1/design-review/07-lesson-briefs/lesson-briefs.md#u1-l02--keep-a-familiar-conversation-going`. **Main goal:** sustain several turns, acknowledge, relevant follow-up and simple turn management. Formulaic phrases and integrated grammar support that goal; the selected prototype's 4 MC steps are not a full lesson nor sufficient evidence of conversational independence.

A staged chapter can teach `react -> pick detail -> ask follow-up`, `get to know` and `keep in touch`, then MC recognition and finally spoken new-context transfer. Later production extends the approved full B1 content without changing the locked authoring roles.
