# Lesson Package Authoring Contract v2

This is the bounded authoring contract for the first-ten pilot. It is derived from the
accepted U1-L03 package and applies before the later production-system freeze.

## Package files

Each final lesson directory contains exactly these twelve files:

- `lesson-manifest.json`
- `source-packet.json`
- `content.json`
- `activities.json`
- `assessment.json`
- `ai-contract.json`
- `ASSET_BRIEFS.md`
- `video/scene.txt`
- `video/sample-context.txt`
- `video/transcript.txt`
- `video/pronunciation-map.json`
- `video/README.md`

The package is editable source material for content, voice, visuals, practice, and a
later application. It is not evidence that final media has been rendered.

## Sequence and curriculum

- Identity, position, outcome, source candidates, and exact item roles must match
  `data/reviewed/a1-first-10-lessons-pilot-v1.json` exactly.
- Every introduced item is bounded to the forms and use needed in this lesson.
- A fresh recycle changes speaker, details, channel, or purpose. Repeating an
  answer-bearing model is exposure, not recycle evidence.
- Content may incidentally contain later language for natural input only when the task
  does not require learner control of it. It must not become an unrecorded target.
- Source packets retain hashes for the release, scope, final decisions, and grammar,
  lexical, and pronunciation ownership datasets.

## Teaching video

- One teacher only.
- Natural Egyptian Arabic explanation suitable for adults; avoid artificial case
  endings in conversation while retaining natural forms such as `مثلًا`.
- Every spoken English span uses the exact wrapper
  `<lang xml:lang="en-US"><phoneme alphabet="ipa" ph="…">…</phoneme></lang>`.
- IPA follows the General American teaching reference. Natural variants remain valid
  when meaning is intelligible.
- The video models and explains. Applied learner questions start after the video.
- The transcript is a readable equivalent; captions, pause, replay, and reduced motion
  remain required for the rendered route.

## Learning loop

1. Establish a believable adult situation and a reason to understand.
2. Model the target in context.
3. Notice meaning and the smallest useful form or sound distinction.
4. Check comprehension after the video.
5. Move through bounded application and coached use.
6. Use a fresh independent task for mastery.
7. If answer-revealing help occurs, use one equivalent replacement task.
8. Schedule next-day, three-day, and seven-day review with changed content.

The assessment distinguishes comprehension, outcome performance, context transfer,
and control or repair. Completing sections, recognition items, or coached AI practice
never grants mastery.

## AI coach and privacy

- Ask one thing at a time and correct at most one important issue per turn.
- Prefer clarification before correction and ask for one retry after correction.
- Respect the lesson boundary; do not teach later grammar opportunistically.
- Never claim mastery from the coached attempt.
- Permit fictional identities, families, addresses, and contact details.
- Do not require microphone access or retain raw answers by default.

## QA gate

A lesson is batch-ready only when the common validator passes and a human content pass
finds no major or medium issue in outcome alignment, Arabic clarity, level load,
progression, answer leakage, pronunciation markup, accessibility, privacy, or source
traceability.
