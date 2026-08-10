# English Course for Arabic-Speaking Adults

An evidence-led English course for Arabic-speaking adults, beginning at CEFR A1.
The learning loop is: understand, practice, use, explain, review, and retain.

## Current delivery

- The A1 curriculum map contains 81 source-audited lesson candidates. They passed an
  internal contract, but the owner has not approved them as the final A1 syllabus.
- The gold lesson, `Introduce Yourself`, is complete and owner-approved.
- Unit 1, `First Connections`, has eight complete lesson source packages.
- A browser prototype is available for the gold lesson.
- An A1-C2 vertical-curriculum proposal and validated level exit profiles are ready
  for evidence review.
- All-level CEFR, GSE objectives, EGP, GSE Grammar, Oxford 3000, and Oxford 5000
  source records are normalized with page or row provenance. Curriculum dispositions
  and lifecycle ownership remain pending.
- Rendered voice/video assets and external learner-pilot evidence are still pending.

Read [HANDOFF.md](HANDOFF.md) before continuing the project.

## Try the lesson

From the repository root:

```powershell
python -m http.server 8765 --directory prototype/gold-lesson
```

Then open <http://127.0.0.1:8765>.

## Validate the repository

Install the only declared validation dependency, then run the suite:

```powershell
python -m pip install -r automation/requirements-validation.txt
python -m unittest discover -s tests -p "test_*.py"
```

Source-extraction tests are skipped when the external reference files have not been
downloaded. All curriculum, lesson-package, and Unit 1 tests still run.

## Start here

- `HANDOFF.md` - current status, boundaries, and recommended next work
- `docs/MASTER_PLAN.md` - gated roadmap and completion criteria
- `docs/LEARNING_PRINCIPLES.md` - product and pedagogy contract
- `docs/CROSS_LEVEL_CURRICULUM_ARCHITECTURE.md` - proposed A1-C2 vertical contract
- `docs/VERTICAL_SPINE_EXECUTION_PLAN.md` - work packages and approval gates
- `units/unit-01-first-connections/` - complete first-unit source package
- `gold/introduce-yourself/` - accepted reference lesson and video script
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
