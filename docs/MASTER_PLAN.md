# Master Plan v0.1

## Outcome

Build an evidence-based English course for Arabic-speaking adults. Start with A1, prove
the learning experience with one gold lesson, then build and pilot Unit 1 before
scaling. The database and media factory must follow the validated experience.

## Why the order matters

The earlier conversation contains a strong product vision but also several untested
assumptions: seven exact units, a rigid lesson flow, fixed duration, and teach-back in
every lesson. Building the full app around those assumptions would create expensive
rework. The project therefore uses gated phases.

## Phase 0 - Source and workspace foundation

Status: complete for the initial source pack.

Deliverables:

- authoritative raw sources, provenance URLs, hashes, and readable-page checks;
- plain-text mirrors of PDF sources for deterministic agent use;
- complete English Grammar Profile export and A1 subset;
- modular project folders, runbook, queue, state, and run logs.

Exit gate: every required file is present, readable, hashed, and registered.

## Phase 1 - Lock the learning model

Produce a concise product learning contract covering:

- learner profile and serious-learning promise;
- role of English, Modern Standard Arabic, video, AI, and teach-back;
- definition of a lesson-sized ability;
- mastery rubric and progress states;
- accessibility, privacy, and safe AI limits;
- hypotheses that must be tested rather than treated as facts.

Exit gate: no unresolved contradiction can change the shape of the gold lesson.

## Phase 2 - Complete the A1 curriculum audit

1. Extract all A1-relevant GSE adult objectives with exact source location.
2. Extract supporting A1 CEFR descriptors across reception, production, interaction,
   mediation, online interaction, and communicative competence.
3. Normalize skills and functions without rewriting source text.
4. Create a candidate objective-to-unit clustering from the evidence.
5. Audit coverage, duplicates, prerequisites, four-skill balance, and orphan items.
6. Treat the seven earlier units as candidates, not constraints.

Core data fields:

`objective_id`, `source`, `source_version`, `source_location`, `source_text`, `cefr`,
`gse_score_or_range`, `skill`, `mode`, `function`, `candidate_cluster`, `notes`.

Exit gate: 100% of included objectives are traceable and mapped; exclusions have
reasons; no final unit count is announced before the coverage audit.

## Phase 3 - Normalize lesson-sized abilities

Turn related source objectives into coherent learner outcomes. Merge outcomes that are
too small, split outcomes that are too large, and make prerequisites explicit.

Each lesson candidate needs:

- one measurable real-life outcome;
- source objective and descriptor links;
- prerequisite and successor relationships;
- target grammar, vocabulary, phrases, pronunciation, and common learner errors;
- a mastery rubric that can be observed in a fresh task;
- an estimated scope band, not an arbitrary fixed duration.

Exit gate: the final A1 lesson map has no tiny fragments, overloaded lessons, missing
skills, or untraceable outcomes.

## Phase 4 - Design one gold lesson

Default candidate: `Introduce Yourself`, subject to the curriculum audit.

Build the complete content specification:

- warm-up/situation, Arabic explanation or video script, toolkit, examples;
- vocabulary, phrases, grammar, pronunciation, and Arabic-speaker errors;
- varied guided practice moving toward speaking and writing;
- personal use, bounded AI conversation, retry-aware correction;
- fresh transfer challenge and mastery rubric, then matched include/omit variants for
  a short post-performance teach-back, plus review items;
- asset briefs for images, audio, video, captions, and accessibility.

Do not build production infrastructure. Use placeholders where they test the experience.

Exit gate: source traceability and expert QA pass with no major language-level,
pedagogy, Arabic, or exercise defect.

## Phase 5 - Prototype and learner test

Create a clickable prototype with fake AI where practical. Test with a small set of
Arabic-speaking adult beginners and observe behavior, not only opinions.

Measure:

- comprehension of the goal and instructions;
- time and drop-off by section;
- independent final-task performance;
- correction usefulness and retry success;
- value of Arabic explanation, video, and teach-back;
- boredom, confusion, difficulty, and perceived lesson value.

Initial pilot thresholds are hypotheses: most learners should complete the final task
without a full model, major instruction confusion should be rare, and no severe level or
Arabic clarity issue may remain. Record exact thresholds before testing.

Exit gate: evidence supports a revised lesson flow and mastery rule.

## Phase 6 - Lock the lesson system

Turn gold-lesson evidence into versioned contracts:

- lesson content schema and screen/scene types;
- exercise, answer, feedback, and retry schemas;
- AI challenge and teach-back state machines;
- mastery scoring, review scheduling, and completion rules;
- media, captions, localization, and accessibility requirements;
- automated validation plus human review workflow.

Exit gate: the same schema can express the gold lesson without one-off exceptions.

## Phase 7 - Technical architecture

Only now choose the app stack and data model. PostgreSQL is allowed and likely useful,
but it should implement the validated contracts. Design for curriculum versions,
source traceability, lesson items, attempts, AI interactions, mastery evidence, review
scheduling, media, and audit history.

Exit gate: architecture review, migration plan, threat/privacy review, and a thin
end-to-end technical spike pass.

## Phase 8 - Build and pilot Unit 1

Build the smallest complete multi-lesson journey: progression, cross-lesson review,
unit mastery, AI context limits, error recovery, and accessible media. Pilot for one to
two weeks and revise duration, Arabic amount, media style, difficulty, teach-back, and
review timing.

Exit gate: agreed retention, usability, reliability, and content-quality criteria pass.

## Phase 9 - Scale to full A1

Create a controlled content factory only after Unit 1 works. Each run produces one
bounded lesson or asset package, passes automated validators and independent review,
and preserves source links. Image, audio, and video generation begin here under quotas,
licensing, voice, and consistency rules.

Exit gate: full A1 coverage, native-Arabic review, CEFR/GSE/grammar/vocabulary audit,
technical QA, and release readiness.

## Current critical path

Learning contract -> A1 source extraction -> objective coverage map -> normalized
lesson map -> gold lesson -> learner test -> lesson contracts -> architecture -> Unit 1
-> full A1.

## Things agents must not do yet

- finalize seven units without the coverage audit;
- generate all lessons, videos, images, or audio;
- create a production PostgreSQL schema;
- equate watching, exercise completion, or a multiple-choice score with mastery;
- silently rewrite source descriptors or lose page/row provenance;
- make the lesson flow rigid before gold-lesson evidence.
