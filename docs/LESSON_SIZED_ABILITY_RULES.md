# Lesson-Sized Ability Rules v1

Status: approved contract for `LESSON-002`. It defines candidates and review rules; it
does not create a final lesson map, unit count, or sequence.

## Boundary and unit of design

A lesson-sized ability is one coherent, measurable real-life performance that an A1
learner can demonstrate in a fresh task. Topic, grammar point, source sentence, screen
sequence, and estimated duration are not lesson boundaries by themselves.

Use this outcome form:

> In **[fresh situation]**, the learner can **[observable communicative action]** with
> **[essential content or response]** in English, independently enough to **[clear A1
> success condition]**.

The statement must name what the learner does, not what they know, understand in the
abstract, watch, complete, or practise. Reception may be the primary performance when
the learner must select, locate, follow, or act on meaning rather than merely report
exposure.

## Required coherence tests

A candidate passes only when every answer is yes:

1. **One-purpose test:** all parts serve the same real-life purpose in one plausible
   situation or tightly related situation family.
2. **Same-task test:** one fresh task can elicit enough evidence for every claimed part
   without stitching together unrelated mini-tests.
3. **Single-judgment test:** a reviewer can make one defensible demonstrated/not-yet
   judgment using the mastery policy; required dimensions are observable together.
4. **A1-load test:** the task limits content, turns, text length, choices, and language
   demands so success does not depend on above-A1 complexity.
5. **Source-fidelity test:** every coverage claim links to reviewed evidence without
   rewriting source text or asserting objective-to-descriptor equivalence.
6. **Independence test:** the fresh performance can hide the complete model and avoid
   answer-revealing support.

Failure of any test requires revision or a recorded split. A `complex` scope candidate
also needs an explicit explanation of why splitting would destroy one coherent
performance.

## Merge rules

Merge source objectives or draft fragments only when all of these conditions hold:

- they contribute necessary or naturally co-occurring moves to the same purpose;
- the same fresh task can validly demonstrate them together;
- their prerequisites and expected independence level are compatible;
- the combined receptive, productive, interaction, and language load remains A1; and
- the mapping records whether each source record is fully covered, partly covered, or
  supporting only.

Shared topic, vocabulary, grammar, candidate cluster, or convenient duration is not a
merge reason. A supporting CEFR descriptor may strengthen a candidate without being
declared equivalent to a granular GSE objective. Contextual duplicate descriptors keep
their distinct scale and physical-page provenance.

## Split rules

Split a draft when any of these conditions applies:

- its parts have different real-life purposes or require unrelated situations;
- one valid fresh task cannot expose all required evidence;
- a learner could independently master one part while consistently failing another;
- receptive input and productive response are merely co-located, not one necessary
  communicative sequence;
- one part requires materially different prerequisite support or task conditions;
- the combined language, turn, text, or choice load makes the task above A1; or
- a compound source record contains separable actions that need different mastery
  judgments.

Splitting curriculum coverage never edits or duplicates the source record. Each child
links to the same immutable record, states `partial` coverage, and names the covered
clause or action in an interpretation field. All children together must account for
the intended included coverage; overlap must be purposeful and labelled.

## Relationships and support

Record prerequisites and successors as typed candidate-to-candidate links, and record
cross-cutting support as a named support reference:

- `required_before`: absence would make the target performance invalid or above level;
- `helpful_before`: improves efficiency but is not necessary for a valid attempt;
- `successor`: a later candidate reuses or extends this ability; and
- `concurrent_support`: a support reference for language control, pronunciation,
  spelling, clarification, or
  repair needed within relevant topical work rather than as a forced standalone unit.

Every link needs a short rationale and supporting record ids. Do not infer a strict
topical-cluster order from source order. A circular `required_before` relation is
invalid; `helpful_before` and `concurrent_support` must not masquerade as hard gates.

## Scope bands

Scope is based on performance load, not minutes:

- `focused`: one short move, interpretation, or response with limited variation;
- `standard`: a short connected sequence or bounded exchange serving one purpose; or
- `complex`: several necessary moves that still pass every coherence test and have a
  recorded no-split justification.

Record an estimated time range only as a planning hypothesis. It cannot make an
incoherent draft acceptable or force a coherent ability to fill a fixed lesson length.

## Approved candidate template

Each candidate must contain the fields enforced by
`schemas/curriculum/lesson-candidate.schema.json`:

- stable candidate id, version, draft/review status, and provisional cluster links;
- structured measurable outcome: situation, action, essential content, independence,
  success condition, and complete statement;
- exact evidence references with record/dataset/source ids, raw file, location,
  source-text hash, role, coverage claim, and interpretation note;
- normalized skill, mode, and function codes as interpretations;
- merge/split decision, contributing records or drafts, test results, and rationale;
- typed prerequisites, successors, and concurrent support;
- grammar, vocabulary, phrases, and pronunciation targets with evidence references;
- Arabic-speaker error hypotheses kept separate from source facts and marked for
  expert or learner-test validation;
- fresh task family, required rubric dimensions, concrete level-2 evidence, critical
  failures, non-blocking errors, permitted support, and delayed probe brief;
- scope band, load rationale, time-range hypothesis, risks, and review record.

An empty slot is not silent approval. If a field is not applicable, record the schema's
explicit empty value plus a rationale where required. Grammar, vocabulary,
pronunciation, and learner-error decisions cannot be invented to fill a quota.

## Acceptance checklist for `LESSON-002`

A candidate may be approved for the final-map audit only when:

- all six coherence tests pass and `complex` candidates justify no split;
- its outcome is observable, fresh-task assessable, A1-bounded, and non-duplicative;
- every included source-coverage claim is traceable and all partial coverage is named;
- required-before links are acyclic and cross-cutting support is present where needed;
- target-language decisions are cited and hypotheses are labelled;
- the mastery specification conforms to `docs/MASTERY_PROGRESS_POLICY.md`; and
- an independent coverage pass finds no orphan, accidental duplicate, or unassessed
  source claim across the complete map.

Approval of one candidate does not approve a unit boundary or ordering. Final counts,
balance, sequencing, and gold-lesson selection remain later decisions.
