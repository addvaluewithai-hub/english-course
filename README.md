# English Course for Arabic-Speaking Adults

An evidence-led English course for Arabic-speaking adults, beginning at CEFR A1.
The learning loop is: understand, practice, use, explain, review, and retain.

## Current delivery

- The evidence-backed A1-C2 vertical spine is complete: all 9,274 normalized source
  records are dispositioned across 167 reviewed families/strands and 1,015 lifecycle
  stages, with no unexplained orphan or level regression.
- The former 81 A1 source candidates remain traceable inputs. They were reconciled into
  a locked learner-facing A1 v1 syllabus of 45 capabilities in six units.
- All 158 exact A1 grammar, lexical/chunk, and pronunciation items have an ordered
  introduction, fresh recycle, and later consolidation location.
- The owner-approved `Introduce Yourself` gold lesson is migrated and re-QA'd as final
  `U1-L03` under the versioned A1 path; the older gold and Unit 1 packages are preserved
  as prototype lineage, not the final course sequence.
- The owner's next validation release is the actual first ten lessons: all nine lessons
  in Unit 1 plus Unit 2 Lesson 1, not a hand-picked showcase set.
- All ten final-source lesson packages are authored and batch-QA'd: 120 package files,
  49 exact introductions, and 16 fresh recycles. U1-L03 remains the accepted reference.
- A simple continuous learner experience is ready: local video or placeholder, one
  application at a time, a final challenge, controlled feedback, and the next lesson.
  Formal consent and observer tools remain available only on their separate direct route.
- Final Gemini videos are not rendered or listened to, and no real learner journey has
  been collected. TEST-002, reusable system decisions, and later production remain gated.

Read [HANDOFF.md](HANDOFF.md) before continuing the project.

## Try the lesson

From the repository root:

```powershell
python -m http.server 8765 --bind 127.0.0.1
```

Then open <http://127.0.0.1:8765/prototype/first-ten/>. The facilitator route is
<http://127.0.0.1:8765/prototype/first-ten/observer.html>. Use it only for synthetic
rehearsal until the final videos pass listening QA. The Arabic guide is
[`research/first-ten-pilot-v1/START_HERE_AR.md`](research/first-ten-pilot-v1/START_HERE_AR.md).

## Validate the repository

Install the only declared validation dependency, then run the suite:

```powershell
python -m pip install -r automation/requirements-validation.txt
python -m unittest discover -s tests -p "test_*.py"
```

Source-extraction tests are skipped when the external reference files have not been
downloaded. All curriculum, lesson-package, and Unit 1 tests still run.
There is no scheduled task or background curriculum agent.

## Start here

- `HANDOFF.md` - current status, boundaries, and recommended next work
- `docs/MASTER_PLAN.md` - gated roadmap and completion criteria
- `docs/LEARNING_PRINCIPLES.md` - product and pedagogy contract
- `docs/CROSS_LEVEL_CURRICULUM_ARCHITECTURE.md` - approved A1-C2 architecture foundation
- `docs/LEVEL_EXIT_PROFILES_V1.md` - approved human-readable level boundaries
- `docs/SPINE_004_COMPLETION_AUDIT.md` - completed all-level spine gate audit
- `docs/VERTICAL_SPINE_EXECUTION_PLAN.md` - work packages and approval gates
- `docs/A1_SCOPE_AND_SEQUENCE_V1.md` - locked six-unit, 45-capability A1 sequence
- `docs/PILOT_10_PRODUCTION_PLAN_V1.md` - owner-approved first-ten production milestone
- `data/reviewed/a1-first-10-lessons-pilot-v1.json` - machine release contract
- `data/reviewed/a1-first-10-lessons-content-qa-v1.json` - deterministic batch QA
- `units/a1-v1/` - versioned final A1 content packages as they pass their gates
- `prototype/first-ten/` - continuous first-ten learner and observer routes
- `research/first-ten-pilot-v1/` - six-visit progression protocol and record contract
- `units/unit-01-first-connections/` - preserved pre-v1 Unit 1 prototype packages
- `gold/introduce-yourself/` - preserved accepted gold prototype lineage
- `research/learner-test-v1/` - TEST-001 kit and TEST-002 analysis runbook
- `sources/registry/SOURCES.md` - source URLs, roles, and verified hashes
- `automation/AGENT_RUNBOOK.md` - single-primary-agent operating contract

## Repository map

- `automation/` - project checklist, runbook, and state; it does not schedule agents
- `data/derived/` - structured machine-derived curriculum records
- `data/reviewed/` - reviewed curriculum records and audits
- `docs/` - product, pedagogy, policy, and QA decisions
- `gold/` - reference lesson source package
- `prototype/` - dependency-free browser prototype
- `references/legacy/` - recovered historical inputs; never curriculum authority
- `schemas/` - curriculum data contracts
- `scripts/` - small deterministic curriculum utilities
- `sources/raw/` - verified source snapshots used by the extraction pipeline
- `sources/registry/` - source provenance, acquisition details, and hashes
- `tests/` - validation suite
- `units/` - authored unit source packages

Raw source snapshots, extracted text mirrors, and recovered legacy planning inputs
are included for reproducibility. Per-agent run logs and temporary files are excluded.
