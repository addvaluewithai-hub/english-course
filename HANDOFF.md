# Project Handoff

## What is complete

The project has a reviewed A1 curriculum foundation and one complete content unit.

- 218 reviewed CEFR/GSE source records feed an approved 81-lesson A1 map.
- The gold lesson is `Introduce Yourself` under `gold/introduce-yourself/`.
- The owner tested and accepted the one-teacher Arabic/English presentation style.
- Every English expression in the video scripts has pronunciation guidance for
  mixed-language voice generation.
- Unit 1 contains eight sequenced lessons, lesson-level practice and assessment,
  accessibility requirements, review routing, and a unit mastery experience.
- The static prototype demonstrates the gold lesson without an app or database.

## Important boundary

The authored content package is complete; the product is not production-ready.
There is no rendered media pipeline, learner account system, production database,
analytics layer, or external learner-pilot result yet.

`automation/STATE.json` and `automation/TASKS.json` preserve the original gated
factory history. Later owner-directed work produced Unit 1 before the earlier pilot,
system, and architecture gates were formally closed. Treat this as an explicit
exception, not proof that those gates passed.

## Recommended next work

1. Render and listen-test the eight lesson videos with the chosen voice system.
2. Run a small, consent-based learner pilot of the gold lesson.
3. Record pronunciation, comprehension, completion, and usability findings.
4. Revise the lesson contract only from observed evidence.
5. Lock reusable content schemas and build a thin application slice.
6. Pilot the complete unit before scaling the remaining A1 map.

## Content locations

- Gold lesson: `gold/introduce-yourself/`
- Gold video inputs: `gold/introduce-yourself/video/`
- Unit 1 manifest: `units/unit-01-first-connections/unit-manifest.json`
- Lessons 2-8: `units/unit-01-first-connections/lessons/`
- Unit mastery: `units/unit-01-first-connections/unit-mastery-experience.json`
- A1 lesson map: `data/reviewed/a1-lesson-map.json`
- Prototype: `prototype/gold-lesson/`

Lesson 1 intentionally remains in `gold/introduce-yourself/`; the Unit 1 manifest
references it instead of duplicating it.

## Repository hygiene

This private repository includes verified third-party source files, extracted text
mirrors, and recovered legacy planning inputs. The legacy inputs are historical
context, not approved curriculum evidence. Historic per-agent run logs, caches, and
temporary files remain excluded. Review each publisher's reuse terms before sharing.

For the next curriculum phase, read `docs/VERTICAL_CURRICULUM_SPINE_BRIEF.md` and
`docs/LOCAL_RECOVERY_AUDIT.md` before designing A2 or revising A1.

No repository-wide open-source license has been selected. The new team should choose
one deliberately before accepting outside contributions.

## Working rules

- Read `AGENTS.md` before modifying the project.
- Keep implementation files modular and normally below 200 lines, never above 300.
- Preserve source traceability and distinguish sourced facts from hypotheses.
- Do not treat activity completion as demonstrated mastery.
- Do not introduce infrastructure before a validated product need requires it.
