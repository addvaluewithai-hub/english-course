# Gold Lesson Internal QA

Status: revised for the single-teacher video flow; automated revalidation passed before independent expert QA.

## Passed

- The selected candidate is approved and preserves six exact source records.
- The lesson retains one bounded outcome and four small required detail categories.
- The model, explanation, toolkit, six activities, AI contract, fresh mastery task,
  teach-back/omit variants, delayed review, privacy, and accessibility briefs exist.
- Guided support is hidden during the fresh mastery step.
- The text prototype does not claim real speaking mastery or store learner responses.
- `python scripts/validate_gold_lesson.py` passes.
- All 233 project tests pass with third-party pytest plugin autoload disabled.
- Desktop browser QA passed navigation, correct/incorrect feedback, personal planning,
  coached retry, mastery component checks, disabled back navigation, and teach-back.
- The revised content package now starts with one uninterrupted teacher video and moves
  to comprehension, application, planning, coached production, and fresh mastery.
- Scene, sample context, SSML/IPA transcript, pronunciation reference, and post-video
  question placement are explicit in the gold-lesson package.

## Deferred

- Independent Arabic-English pedagogy and level review (`GOLD-003`).
- Real recorded audio/video, image briefs, and real AI integration.
- Mobile visual QA was explicitly deferred while the learner first evaluates content.
- Real learner testing; the current text checker is not a speaking assessment.
