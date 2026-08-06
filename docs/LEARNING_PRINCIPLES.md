# Learning Principles v0.1

Status: working contract to validate before engineering.

The detailed learner scope and language boundaries are locked in
`docs/LEARNER_LANGUAGE_POLICY.md` for the current phase.

## Learner and promise

The primary learner is an Arabic-speaking adult beginner who wants practical command
of English, not a casual streak game. The promise is not exposure or random
memorization. It is usable ability with understanding and retention.

## Core learning loop

1. Understand the real-life ability and why it matters.
2. Notice useful language in context.
3. Practice from recognition toward production.
4. Personalize the language.
5. Demonstrate the ability in a fresh situation.
6. When the test variant includes teach-back, explain one key idea after the fresh
   performance.
7. Revisit weak items in later review and delayed retention probes.

## Language policy

- English: situations, examples, questions, listening, speaking, and production.
- Modern Standard Arabic: concise explanations and important corrections.
- Avoid word-for-word translation and long grammar lectures.
- Egyptian Arabic was proposed earlier, but the current live-teacher brief explicitly
  requires Modern Standard Arabic. MSA is the baseline until learner testing says
  otherwise.

## Lesson definition

One lesson has one coherent, measurable real-life outcome. It may map to several
closely related GSE objectives, CEFR descriptors, grammar points, and lexical items.
The product's word "ability" is not required to equal one source sentence.

The approved merge, split, relationship, scope, and candidate-template rules are in
`docs/LESSON_SIZED_ABILITY_RULES.md`. They govern Phase 3 normalization without fixing
the final lesson or unit count.

Lesson duration is adaptive, initially expected to fall around 20-45 minutes. Duration
is not a success criterion; demonstrated ability is.

## Version-one lesson hypothesis

Warm-up or situation -> explanation or optional video -> toolkit -> guided practice ->
personal use -> bounded AI practice -> fresh mastery performance -> optional short
teach-back variant -> close and review pack.

This sequence is testable, not permanent architecture. The gold lesson may change it.

## Video hypothesis

Video is an optional input or explanation medium, not a required lesson stage and not
mastery evidence. The gold lesson must keep its learning content separable from the
medium, provide captions and an equivalent readable route, and make video's added value
testable rather than assuming that watching improves performance.

## AI teacher behavior

The bounded behavior contract, retry limits, safety boundaries, and acceptance
scenarios are locked in `docs/AI_TEACHER_TEACHBACK_POLICY.md` for the current phase.

- Ask one question at a time and react to the learner's real answer.
- Keep conversations bounded by a lesson goal.
- Correct one important issue at a time.
- Show the important error, one natural correction, a short Arabic explanation, and a
  retry.
- Ignore harmless hesitation when meaning is clear.
- Require a fresh final performance rather than ending after one correct answer.

## Teach-back hypothesis

Initially test one brief, focused teach-back after the fresh lesson performance and a
deeper synthesis at the end of a unit. Test value, fatigue, repetition, language choice,
and whether some lessons should omit it before making the pattern permanent.

For the gold-lesson comparison, keep the included variant after fresh performance and
author a matched omit variant. Teach-back evidence is reported separately and cannot
turn a failed performance into a demonstrated result.

## Privacy and accessibility

The minimum prototype boundaries for data collection, accessible media, permitted
support, and construct-preserving mastery evidence are locked in
`docs/PRIVACY_ACCESSIBILITY_POLICY.md`. They are learning-model constraints, not a
production storage or architecture design.

## Mastery

The reusable rubric and state transitions are locked in
`docs/MASTERY_PROGRESS_POLICY.md` for the current phase.

Completion and mastery are different. A lesson is demonstrated in a valid fresh task
when the learner can:

- understand the target prompt or situation;
- produce the needed language without copying a full model;
- interact or respond appropriately in a fresh scenario;
- repair or explain an important pattern only when control or repair is applicable; and
- meet level 2 on every lesson-required rubric dimension, with interaction or transfer
  and control or repair marked not applicable when the outcome does not expose them.

Suggested states: not started, learning, practiced, demonstrated, needs review,
retained. Retention requires a later fresh demonstration; completion never advances a
mastery state automatically.
