# Hourly Curriculum Agent Runbook

Each scheduled run completes exactly one bounded task from `automation/TASKS.json`,
verifies it, records the result, and stops. Quality and traceability matter more than
the number of files produced.

## 1. Orient every run

Read completely, in this order:

1. `AGENTS.md`
2. `docs/MASTER_PLAN.md`
3. `docs/LEARNING_PRINCIPLES.md`
4. `docs/DECISIONS.md`
5. `sources/registry/SOURCES.md`
6. `automation/STATE.json`
7. `automation/TASKS.json`

Inspect recent reports in `logs/runs/` only when needed for the selected task.

## 2. Respect the phase gate

Select the first task whose status is `ready` and whose dependencies are complete.
Never work ahead of the active phase. If no task is ready, diagnose dependency state,
record a short no-op report, and stop.

Do not build the app, database, or mass content while discovery tasks remain.

## 3. Concurrency and ownership

Create `automation/RUNNING.json` with the run id, task id, and start time before edits.
If it already exists and is newer than three hours, stop without editing. If older than
three hours, treat it as stale, mention recovery in the report, and replace it.

The primary scheduled agent is the only writer. It may use up to three sub-agents for
independent read-only extraction, source checking, or critique. Sub-agents must not edit
shared files. The primary agent integrates and verifies their findings.

## 4. Execute one bounded task

- Preserve raw sources exactly.
- Put machine extraction in `data/derived/` and reviewed results in `data/reviewed/`.
- Preserve source text verbatim in dedicated fields; put interpretations in separate
  fields.
- Record exact source file and page or row for every objective, descriptor, grammar
  feature, and vocabulary decision.
- Prefer deterministic scripts for repeated transformations.
- Keep files focused and under the project line limits.
- Use authoritative sources for any web research and record URLs.

If a task is too large for one run, finish one coherent partition, validate it, record
the partition in the task notes, leave the task `in_progress`, and stop.

## 5. Critique before acceptance

For curriculum work, check at minimum:

- source fidelity and page/row provenance;
- duplicate, missing, and orphan records;
- CEFR/GSE level consistency;
- balance across listening, reading, speaking, writing, interaction, and mediation;
- whether interpretations have been mislabeled as source facts;
- clear Modern Standard Arabic where Arabic is present.

Use an independent read-only reviewer for high-impact mappings when practical.

## 6. Verify and record

Create `logs/runs/YYYY-MM-DDTHH-mm-ss_TASK-ID.md` with:

- task and outcome;
- files created or changed;
- source evidence and counts;
- validation performed and results;
- assumptions, risks, and unresolved questions;
- exact recommended next task.

Then update `automation/TASKS.json` and `automation/STATE.json`. Mark a task complete
only when its acceptance criteria pass. Remove `automation/RUNNING.json` last.

If the project is a Git repository, create one local commit for the verified task using
`task: TASK-ID - short outcome`. Never push from the scheduled run.

## 7. Stop conditions

Stop after one task or one coherent task partition. Do not begin the next task.

If all tasks are complete, set project status to `complete`, report that the plan has
finished, and do no further work. If a product decision is genuinely required, set the
task to `needs_user` with a concrete question and continue any other safe independent
task on later runs.

Never communicate externally, spend money, deploy publicly, publish content, or upload
private files. Do not expose credentials. Image/audio/video generation is prohibited
until its phase is explicitly active.
