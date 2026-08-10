# Project Handoff

## What is complete

The project has a reviewed A1 curriculum foundation and one complete content unit.

- 218 reviewed CEFR/GSE source records feed 81 source-audited A1 candidates. They are
  evidence-backed working material, not an owner-approved lesson count or syllabus.
- The gold lesson is `Introduce Yourself` under `gold/introduce-yourself/`.
- The owner tested and accepted the one-teacher Arabic/English presentation style.
- Every English expression in the video scripts has pronunciation guidance for
  mixed-language voice generation.
- Unit 1 contains eight sequenced lessons, lesson-level practice and assessment,
  accessibility requirements, review routing, and a unit mastery experience.
- The static prototype demonstrates the gold lesson without an app or database.
- The owner has directed the team to build an A1-C2 vertical curriculum before mass
  production. The proposal, exit profiles, source audit, and execution plan are in
  `docs/CROSS_LEVEL_CURRICULUM_ARCHITECTURE.md`,
  `docs/LEVEL_EXIT_PROFILES_V0.md`, and `docs/VERTICAL_SPINE_EXECUTION_PLAN.md`.
- All cross-level source inventories are normalized under `data/derived/`: 1,050 GSE
  objectives, 1,224 CEFR descriptors, 1,222 EGP features, 456 GSE Grammar entries,
  3,307 Oxford 3000 entry lines, and 2,015 Oxford 5000 entry lines. They are derived
  evidence, not approved syllabuses.

## Important boundary

The authored content package is complete; the product is not production-ready.
There is no rendered media pipeline, learner account system, production database,
analytics layer, or external learner-pilot result yet.

`automation/STATE.json` and `automation/TASKS.json` preserve the gated factory history
and now act only as project memory and a checklist. They do not create scheduled tasks.
Later owner-directed work produced Unit 1 before the earlier pilot,
system, and architecture gates were formally closed. Treat this as an explicit
exception, not proof that those gates passed.

## Recommended next work

1. Review every normalized source record's curriculum disposition and revise the A1-C2
   exit-profile proposal against that evidence.
2. Build reviewed progression strands and lifecycle ownership across all levels.
3. Reconcile, replace, or retire the 81 A1 candidates and Unit 1 as needed, then lock
   A1 scope and sequence v1 without preserving the current lesson count by default.
4. In parallel, run a small consent-based gold-lesson pilot and record delivery evidence.
5. Resume mass A1 production only after the vertical-spine and delivery gates pass.

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
`docs/CROSS_LEVEL_CURRICULUM_ARCHITECTURE.md` before designing A2 or revising A1.

No repository-wide open-source license has been selected. The new team should choose
one deliberately before accepting outside contributions.

## Working rules

- Read `AGENTS.md` before modifying the project.
- Keep implementation files modular and normally below 200 lines, never above 300.
- Preserve source traceability and distinguish sourced facts from hypotheses.
- Do not treat activity completion as demonstrated mastery.
- Do not introduce infrastructure before a validated product need requires it.
