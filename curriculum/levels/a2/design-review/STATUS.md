# A2 Design Review Status

Status: **MILESTONE 1 CLOSED — FOUNDATION + EXACT COVERAGE COMPLETE**

This file is the session-independent handoff for A2 curriculum design. It records the current authoritative design state and the next milestone boundary. It does not authorize lesson production.

## Milestone 1 scope completed

A2 source-of-truth inventory reviewed and incorporated:

- abilities: **269 / 269** required rows manually reviewed
- phrases: **176 / 176** manually reviewed
- grammar: **291 / 291** manually reviewed into **46** usable systems/infrastructure families
- words: **871 / 871** manually reviewed into lexical/content homes
- pronunciation: **10 / 10** reviewed
- total exact source records in the provisional lifecycle ledger: **1,617 / 1,617**

Current communicative architecture:

- **26** top-level capability families
- **9** cross-cutting requirements
- **30** lexical/content sets plus an intentional frozen general remainder

Exact A2 word-home expansion:

- source records: **871 / 871**
- exact primary homes: **871**
- explicit headword/exact-ID decisions: **788**
- intentional reviewed `LX-GENERAL` remainder: **83**
- word-home orphans: **0**

## Current course skeleton

Stage-05 baseline currently remains:

- **12 units**
- **83 lesson slots**

The 83-slot count is still a design baseline, not a sacred target. Milestone 2 may split, merge or resequence slots if the human cognitive-load/sequence critic finds a real pedagogical reason.

## Exact coverage ledger result

Stage-06 exact expansion currently passes:

- exact records scheduled: **1,617 / 1,617**
- orphan records: **0**
- missing practice: **0**
- missing fresh retrieval: **0**
- missing recycle: **0**
- missing consolidation: **0**
- missing exit verification: **0**
- mechanical introduction overloads: **0**
- designated transfer/evidence lessons with new introductions: **0**

Current mechanical guardrails remain:

- words introduced per lesson: max **22**
- phrases introduced per lesson: max **10**
- grammar source rows introduced per lesson: max **12**
- ability source rows introduced per lesson: max **9**
- pronunciation source rows introduced per lesson: max **2**
- total source introductions per lesson: max **46**

Current highest total introduction load is **44** source records (`U1-L03`). A source-record count is a mechanical guardrail only; it is not a claim that every row is an independent teaching object.

## Important interpretation

This is still a **pre-semantic-lock provisional lifecycle**.

Milestone 1 proves that every required A2 source record has a deliberate instructional home and complete provisional lifecycle without mechanical overload. It does **not** yet decide final productive/receptive/formulaic/embedded mastery roles for every item.

Do not infer mastery from coverage alone.

## What the rebalancing changed

The first exact ledger exposed heavy concentrations even though the semantic homes were valid. Human scheduling decisions redistributed introduction windows without changing semantic ownership. Examples:

- social-contact, interaction-condition and repair rows were spread across the actual social/repair lessons instead of being concentrated at the start of Unit 1;
- cohesion/discourse phrases were distributed across routine, opinion, direction, narrative, process and writing contexts;
- reference grammar was distributed across profile, description, experience and factual-media tasks rather than making `U3-L06` a 55-row grammar dump;
- broad factual lexis was distributed across practical reading, narrative, inference, local-world and presentation contexts rather than leaving 79 words in `U11-L04` or 76 in `U12-L02`;
- no thresholds were raised merely to obtain a green audit;
- no new lesson slot was added merely to satisfy the validator.

Automation only expanded/counts/validated inside human-approved windows. It did not choose semantic homes.

## CI state at milestone close

- A2 exact coverage-ledger workflow: **SUCCESS**
- global level source-of-truth audit on the milestone-closing design commit: **SUCCESS**

Generated Stage-06 report is authoritative for exact mechanical coverage:

`curriculum/levels/a2/design-review/06-coverage-ledger/generated/coverage-report.md`

## What is NOT closed yet

Do not treat the following as complete:

- final lesson cognitive-load judgment
- final unit/lesson sequence lock
- productive vs receptive vs formulaic vs embedded semantic roles
- role-aware lifecycle reconciliation
- lesson authoring briefs
- lesson/script/media production
- A2 manifest lesson-design authorization

## Next session — Milestone 2

Start with **Milestone 2: Curriculum Load & Sequence Lock**.

Required process:

1. Read this `STATUS.md`.
2. Read `05-curriculum-map/curriculum-map.md`.
3. Read the final Stage-06 `generated/coverage-report.md` and exact ledger as needed.
4. Perform a human lesson-by-lesson cognitive-load and sequence critic across the 83 slots.
5. Treat raw source-row counts as warnings/evidence, not pedagogy by themselves.
6. Check whether each slot contains a coherent primary communicative/evidence outcome, not merely a legal set of source rows.
7. Split, merge, move or resequence only when the human critic finds a real learning reason.
8. Keep unit-end transfer/evidence tasks zero-new unless an explicit redesign decision says otherwise.
9. Re-run exact coverage/lifecycle audit after every structural scheduling change.
10. Close Milestone 2 only when the human critic and the exact ledger agree on a stable unit/lesson architecture.

Do **not** start Stage-08 semantic-lock classification or Stage-07 lesson authoring briefs before Milestone 2 is explicitly closed.

## Boundaries

- Branch: `curriculum/level-source-of-truth-v1`
- `main` remains untouched by this A2 design work.
- A1 remains locked and must not be silently edited to solve an A2 issue.
- `TEST-002` / delivery-production gates remain separate and untouched.
- `lesson_design_authorized` for A2 must remain false until the later authorization gate is legitimately satisfied.
