# Vertical Spine Execution Plan

Status: active critical path. Work packages 1-5 are complete; A1 reconciliation is
next.

## Work package 1 - Scope and governance

Lock A1-C2 as exit levels, Pre-A1 as an onboarding support band, and A2+/B1+/B2+ as
internal GSE milestones. Keep a small delivery pilot independent from curriculum
approval and record the mass-production freeze.

Acceptance:

- supported levels and milestone semantics are explicit;
- source facts and product decisions have separate fields;
- the lifecycle vocabulary is fixed and validated.

## Work package 2 - Normalize all-level sources

Create deterministic, versioned records for:

- CEFR descriptors across Pre-A1 to C2;
- GSE Adult objectives across scores 10-90;
- all 1,222 EGP grammar features;
- Pearson GSE Grammar entries;
- Oxford 3000 and Oxford 5000 entries by published level.

Acceptance:

- every record retains raw file, hash, page or row, exact source text, level, and review
  state;
- counts reconcile to the registered source and duplicate/parse issues are explicit;
- extraction code is modular and deterministic.

Current result: this work package is complete. The all-level datasets are
`cefr-all-descriptors.json`, `gse-all-objectives.json`, `egp-all-levels.json`,
`gse-grammar-all.json`, `oxford-3000-all.json`, and `oxford-5000-all.json` under
`data/derived/`. Counts and parse exceptions are documented in
`docs/SOURCE_COVERAGE_AUDIT_ALL_LEVELS.md`.

## Work package 3 - Build source dispositions

Give every relevant record a reviewed disposition without forcing it into a lesson.
The reviewed contract separates three different questions:

- `source_role`: what kind of evidence the record supplies;
- `control_expectation`: receptive, productive, both, or not applicable;
- `disposition`: include for spine, supporting evidence, reference pool,
  duplicate/overlap, or excluded with reason.

Acceptance:

- no unexplained orphan records;
- cross-source overlap does not imply equivalence;
- gaps and conflicts are reported by level and strand.

Current result: complete. All 9,274 records have a disposition in
`data/reviewed/source-dispositions-v1.json`; the audit reports 27 exact-text overlap
groups, no cross-level exact-text conflict, no unclassified record, and no unexplained
orphan.

## Work package 4 - Review level exit profiles

Review `data/reviewed/level-exit-profiles-v0.json` against the normalized records and
approve or revise each level's reception, production, interaction, mediation, language
control, pronunciation, discourse, and assessment boundary.

Acceptance:

- every exit claim has source references;
- receptive and productive expectations are distinct;
- adjacent levels show a clear increase in independence, complexity, or precision;
- C2 is not described as native-speaker imitation.

Current result: complete. The approved contract contains 102 reviewed claims in
`data/reviewed/level-exit-profiles-v1.json`; every source-boundary claim points to a
validated bundle in `data/reviewed/level-exit-evidence-v1.json`. The combined gate
audit is `docs/SPINE_003_REVIEW_AUDIT.md`.

## Work package 5 - Build progression strands

Create record-level strands for:

- communicative functions and real-life abilities;
- grammar and sentence patterns;
- vocabulary, chunks, collocations, and register;
- pronunciation and intelligibility;
- discourse, cohesion, fluency, and repair;
- receptive and productive text complexity;
- oral, written, online, and mediated interaction.

Each controlled item receives lifecycle levels, prerequisites, examples, Arabic-learner
risks, rationale, and review metadata.

Acceptance:

- no invalid level regressions;
- every consolidated item was introduced and practised earlier or has an explicit
  rationale;
- every level has purposeful recycling and exit-assessment ownership.

Current result: complete. The reviewed spine contains 41 communicative-function
strands, 91 grammar families, 10 lexical-resource strands, 10 English-specific
pronunciation strands, and 15 performance/complexity dimensions. All 9,274 normalized
source records have one primary evidence treatment. The 167 families/strands contain
1,015 lifecycle stages with no unexplained orphan or invalid level regression. The
completion gate is `docs/SPINE_004_COMPLETION_AUDIT.md`.

## Work package 6 - Reconcile current A1

Audit all 81 current A1 candidates, the gold lesson, and eight Unit 1 source packages
against the reviewed spine. They are working evidence, not fixed syllabus decisions.
Identify gaps, premature demands, duplicates, vague lexical targets, missing recycling,
and later-level leakage.

Acceptance:

- every candidate has a keep/revise/split/merge/defer/support-only/replace/retire decision;
- the final lesson count follows the evidence rather than preserving 81 by default;
- grammar, vocabulary, phrases, and pronunciation have exact ownership and lifecycle
  states;
- every change retains original source evidence and rationale.

## Work package 7 - Lock A1 scope and sequence v1

Only after reconciliation, define final learner-facing units, lesson order, review
points, unit synthesis, and exit assessment coverage.

Acceptance:

- unit boundaries are versioned product decisions;
- prerequisites are acyclic and review spacing is visible;
- all A1 exit-profile dimensions are assessed in fresh tasks;
- independent curriculum review accepts the map.

## Parallel delivery rule

Gold-lesson QA and a small learner pilot may continue because they test comprehension,
pacing, Arabic, video, interaction, and mastery experience. Do not use pilot progress
as permission to mass-produce A1 before work packages 2-7 pass.

## Recommended review roles

- curriculum architect: owns vertical coherence and final disposition;
- CEFR/GSE evidence reviewer: checks source fidelity and level interpretation;
- English grammar reviewer: resolves EGP/GSE Grammar ownership and prerequisites;
- lexical syllabus reviewer: owns word, chunk, collocation, and register decisions;
- pronunciation specialist: creates the English-specific intelligibility progression;
- Arabic-English specialist: reviews learner risks without treating hypotheses as facts;
- assessment reviewer: checks that exit claims have valid fresh performance evidence.
