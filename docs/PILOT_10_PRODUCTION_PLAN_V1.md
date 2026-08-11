# First Ten Lessons: Production and Pilot Plan v1

## Decision

The next validation release is the actual first ten lessons in locked A1 sequence,
not ten showcase lessons and not one isolated gold lesson. It contains all nine lessons
in Unit 1 followed by Unit 2 Lesson 1.

The A1-C2 spine and the exact A1 scope and sequence are sufficiently complete for
content production. This decision expands the delivery test; it does not reopen the
high-level curriculum or change the 45-capability A1 v1 syllabus.

Current status (2026-08-11): gates 1–3 are complete. All ten packages and the
continuous local instrument pass repository validation. Gate 4 waits on rendered,
transcript-matched, listened-to media and real consented learner journeys.

## Why ten lessons

One gold lesson can validate voice, tone, explanation, and the shape of practice. It
cannot validate progression, cognitive load across days, recycling, delayed review,
unit mastery, or the transition between units. The first ten lessons expose all of
those questions while ensuring every produced package belongs to the final course.

## Locked release

| Position | Lesson | Learner-facing outcome |
|---:|---|---|
| 1 | U1-L01 — Start and End a Conversation | Open, sustain briefly, and close a basic social exchange. |
| 2 | U1-L02 — Understand an Introduction | Identify the main details in a fresh spoken introduction. |
| 3 | U1-L03 — Introduce Yourself | Give a short, relevant self-introduction. |
| 4 | U1-L04 — Ask and Answer Personal Questions | Exchange direct personal details orally. |
| 5 | U1-L05 — Hear Names and Phone Numbers | Recover names and contact details from speech. |
| 6 | U1-L06 — Find Personal Details | Locate required details in short written profiles. |
| 7 | U1-L07 — Complete a Simple Form | Transfer personal details accurately into a form. |
| 8 | U1-L08 — Write a Short Profile | Write a bounded connected personal profile. |
| 9 | U1-L09 — Exchange Details in Writing | Ask for and reply with personal details in writing. |
| 10 | U2-L01 — Understand Talk about Family | Identify basic facts about a person or family. |

The machine-readable authority is
`data/reviewed/a1-first-10-lessons-pilot-v1.json`. It is generated directly from the
locked scope, exact item lifecycles, and reviewed ownership sources.

## Production contract

Every lesson must:

1. use the exact outcome and sequence owner from A1 v1;
2. teach only its assigned introductions and make assigned recycles genuinely fresh;
3. use one teacher in the explanation video, with application after the video;
4. wrap every spoken English span with `en-US` language and IPA pronunciation markup;
5. provide a readable equivalent and explicit Arabic/English text direction;
6. move from comprehension to bounded application to independent fresh performance;
7. permit a safe fictional identity and avoid unnecessary personal-data capture;
8. distinguish coached practice, lesson completion, fresh mastery, and delayed retention;
9. include an equivalent replacement mastery task after answer-revealing help; and
10. retain source hashes and exact item IDs in its source packet.

U1-L03 remains the accepted quality reference. Its content is preserved unless batch
QA exposes a progression conflict.

## Gates

1. Lock the ten-lesson release contract.
2. Author all ten final packages and pass source, sequence, Arabic, SSML, pedagogy,
   accessibility, privacy, and mastery QA.
3. Build one continuous learner prototype with delayed-review routing and Unit 1
   mastery.
4. Run consented progression pilots. A learner need not complete all ten in one sitting;
   the protocol must observe attrition and return behavior instead of hiding them.
5. Revise the packages and record a go, revise, stop, or insufficient-evidence decision.
6. Only then freeze reusable system contracts and technical architecture.

The former single-lesson test kit is retained as the method prototype. It cannot by
itself approve this ten-lesson release.
