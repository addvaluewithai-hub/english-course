# Gold Lesson Learner-Test Protocol v1

Status: pre-registered TEST-001 protocol. Thresholds are hypotheses, not efficacy
claims. Do not change them after seeing pilot results without versioning the change.

## Test question

Can an Arabic-speaking adult beginner understand and complete the `U1-L03` learning
flow, use correction productively, and give a fresh four-detail spoken
self-introduction without a complete answer model?

Secondary questions are whether the owner-approved Arabic explanation is clear, video
feels useful rather than passive, and a short post-performance teach-back adds useful
understanding without unacceptable fatigue.

## Source-locked test object

- Lesson: `U1-L03`, `lesson_candidate.give_short_self_introduction`.
- Package: `units/a1-v1/unit-01-first-connections/lessons/u1-l03/`.
- Prototype: `prototype/gold-lesson/index.html`.
- Primary mastery: four required detail categories in a changed first-meeting context.
- The text checker is a navigation aid only. A trained evaluator rates the spoken
  fresh task; completion never grants mastery.

## Participants and sample

Target eight completed sessions; six is the minimum for a pilot decision. Recruit
Arabic-speaking adults aged 18+ who self-report as beginners or near-beginners. Record
prior exposure as a coarse category only. A participant who performs clearly above A1
may finish, but exclude that session from the primary beginner denominator and report
the exclusion.

This small convenience sample can expose design failures. It cannot establish broad
learning efficacy or population estimates.

## Conditions and allocation

Alternate valid session numbers between the matched post-performance conditions:

- odd session number: `teachback`;
- even session number: `omit`.

Both conditions receive identical lesson content and fresh mastery first. Teach-back
may never change the mastery rating. Use the approved video when available. The
readable equivalent is an accessibility route and must be recorded as the medium; this
pilot reports video value descriptively and does not claim a causal video advantage.

## Session flow

1. Obtain consent, assign `LT1-NNN`, confirm adult status, and offer fictional details.
2. Record condition, entry band, medium, and requested non-diagnostic support.
3. Let the learner complete explanation, comprehension, application, planning, and
   coached practice. Observe behavior and section time; avoid teaching outside the
   authored supports.
4. Hide full models. Ask the learner to answer the fresh task aloud.
5. Rate comprehension, outcome performance, context transfer, and control or repair
   independently on the lesson rubric. Every required dimension must reach level 2 for
   `demonstrated`; do not average scores.
6. If answer-revealing help was necessary, mark the attempt invalid as mastery. One
   equivalent fresh replacement is allowed after the help becomes practice.
7. Run the allocated post-performance condition, then collect the experience ratings.
8. Record completion outcome separately, de-identify notes, provide the withdrawal
   route, and close. Target duration is 25–45 minutes, but time alone does not pass or
   fail mastery.

## Supports and construct integrity

Permitted support includes extra time, prompt repetition, navigation help, and a plain
restatement that does not shape the English answer. Record each category. A readable
route is equivalent for explanation but cannot prove a listening outcome. A written
mastery response is practice evidence for this speaking lesson, not demonstration.

## Observation codes

Use controlled issue types: `instruction_confusion`, `arabic_clarity`, `level_fit`,
`video_value`, `navigation`, `correction`, `retry`, `mastery_construct`, `teachback`,
`accessibility`, `privacy`, or `safety`. Severity is `info`, `minor`, `major`, or
`severe`. Notes describe the lesson behavior without names, quotations, diagnoses, or
unnecessary biography.

## Reliability

Double-rate at least two completed sessions live without discussing scores until both
records are fixed. Exact demonstrated/not-demonstrated agreement must meet the
pre-registered threshold. If evaluators disagree, preserve both ratings, resolve the
rubric ambiguity for the next version, and do not overwrite the original evidence.

## Analysis and decision

Validate every record against `session-record.schema.json`. Calculate each metric from
the numerator, denominator, minimum denominator, and rule in
`success-thresholds.json`; report counts beside percentages. Missing data never becomes
a pass. Report teach-back and omit results separately but treat the small comparison as
directional only.

- `go_to_system_revision`: every hard safety/privacy gate and every required learning
  or usability gate passes; remaining issues are minor and owned.
- `revise_and_retest`: no stop condition occurs, but one or more required thresholds
  miss or the lesson changes materially during testing.
- `stop_and_redesign`: a severe privacy/accessibility/Arabic/level defect remains, the
  mastery construct is invalid, or the test cannot produce trustworthy evidence.
- `insufficient_evidence`: fewer than six eligible completed sessions or a metric lacks
  its stated minimum denominator.

TEST-002 must publish a de-identified aggregate report, explicit revisions, and one of
these decisions. Individual session files stay outside the public repository.
