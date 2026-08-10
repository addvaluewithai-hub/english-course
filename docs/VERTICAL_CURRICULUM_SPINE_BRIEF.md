# Vertical Curriculum Spine Brief

## Decision

Build an A1-C2 curriculum spine before mass-producing the remaining A1 lessons. Treat
Pre-A1 as a diagnostic and remedial on-ramp, not as a promised exit level. Treat A2+,
B1+, and B2+ as internal GSE milestones rather than separate CEFR exit claims.
Use the gold lesson and Unit 1 as authored prototypes to reconcile against the spine,
not as constraints. Revise, replace, or retire their curriculum choices when the
cross-level evidence requires it. A small delivery pilot may proceed in parallel
because it tests a different question.

## Goal

Define what grows, when, and to what degree across every supported English level. The
spine must connect communicative ability with language systems and complexity, rather
than treating CEFR descriptors as a ready-made table of contents.

The supported exit range is locked as A1 through C2.

## Existing assets to reuse

- Full CEFR Companion Volume source snapshots in English and Arabic.
- Full Pearson GSE Adult General English objectives source snapshot.
- English Grammar Profile export with 1,222 records across levels.
- Pearson GSE Grammar Guide.
- Oxford 3000 and Oxford 5000 levelled vocabulary pools.
- Reviewed A1 CEFR/GSE records, 81 source-audited candidate abilities, relationship audits, gold
  lesson, and Unit 1 source packages.

Current extraction and approval code is A1-scoped. Extend it; do not assume it already
proves cross-level coverage.

## Required layers

1. Communicative abilities and functions.
2. Grammar, sentence patterns, and discourse/cohesion.
3. Core vocabulary, chunks, collocations, and domain lexis.
4. Pronunciation, stress, rhythm, connected speech, and intelligibility.
5. Listening and reading input complexity.
6. Speaking and writing output complexity.
7. Mediation, interaction, online communication, and repair strategies.

## Lifecycle model

Every controlled item needs an explicit lifecycle:

`expose -> introduce -> practise -> recycle -> consolidate -> extend`

An item may appear earlier than its independent-control level. Store receptive and
productive expectations separately.

## Minimum spine record

Each record should identify:

- stable id, domain, item type, and canonical item;
- source wording and exact source location;
- first exposure and first controlled-production level;
- recycle and consolidation levels;
- prerequisites and related items;
- receptive/productive status;
- learner-facing examples and Arabic-learner risks;
- decision status, rationale, reviewer, and version.

Do not mix source facts with product decisions in the same field.

## Work packages

### 1. Normalize all-level sources

Create versioned, validated records for all supported levels from CEFR, GSE, EGP, and
Oxford. Preserve raw text, provenance, hashes, exclusions, and ambiguous mappings.

### 2. Define level exit profiles

For each level, state what learners can understand and independently do across skills,
modes, functions, language systems, and input/output complexity.

### 3. Build progression strands

Map abilities and language items vertically. Record introduction, recycling,
consolidation, extension, and deliberate deferral.

### 4. Reconcile A1

Audit the 81 current A1 candidates and eight Unit 1 lessons against the spine. Identify
missing coverage, premature control demands, duplicates, lexical vagueness, and items
that belong to later levels. Keep, revise, split, merge, defer, replace, or retire work
according to evidence; the final count is open.

### 5. Lock A1 scope and sequence v1

Only after reconciliation, finalize A1 units, lesson order, exact language ownership,
recycling points, and exit assessment coverage.

## Acceptance criteria

- Every included source record has a documented disposition.
- Every required language item has a lifecycle owner and no unexplained orphan.
- Level boundaries and cross-level conflicts have explicit rationales.
- Grammar and vocabulary have global coverage audits, not merely per-lesson targets.
- A1 candidates and Unit 1 map to the spine with documented exceptions.
- Sequence and unit boundaries are versioned product decisions, not presented as
  source-proven facts.
- Automated validation checks ids, provenance, lifecycle states, prerequisites,
  coverage, duplicates, and invalid level regressions.
- Independent curriculum review signs off before mass lesson production resumes.

## Pilot boundary

The spine answers whether the right content is taught at the right stage. A learner
pilot answers whether the teaching experience works for people. Continue a small gold
lesson/Unit 1 pilot if useful, but freeze mass production until A1 reconciliation and
scope-and-sequence approval are complete.
