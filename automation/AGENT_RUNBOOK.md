# Primary Curriculum Agent Runbook

The owner has chosen one continuing primary Codex task, not scheduled or hourly
execution. `automation/TASKS.json` is a durable checklist and `automation/STATE.json`
is project memory; neither file creates an automation or a background agent.

The primary agent may complete as many coherent partitions as are safe in one turn.
Quality, source traceability, and honest status matter more than file count or speed.

## 1. Orient before a work session

Read completely, in this order:

1. `AGENTS.md`
2. `docs/MASTER_PLAN.md`
3. `docs/LEARNING_PRINCIPLES.md`
4. `docs/DECISIONS.md`
5. `sources/registry/SOURCES.md`
6. `automation/STATE.json`
7. `automation/TASKS.json`

Inspect historical reports in `logs/runs/` only when needed for the current task.

## 2. Respect the phase gate

Continue the task whose status is `in_progress`; otherwise work on the first `ready`
task whose dependencies are complete.
Do not work ahead of the active phase. If no task is ready, diagnose and correct the
dependency state or explain the genuine owner decision that is required.

Do not build the app, database, or mass content while discovery tasks remain.

## 3. Ownership

One primary agent owns implementation, integration, validation, and status. Do not
create scheduled tasks or delegate to sub-agents unless the owner explicitly changes
this decision. No `RUNNING.json` lock is required for this single-agent workflow.

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

If a task is large, finish and validate coherent partitions while keeping the parent
task `in_progress`. Continue in later turns without pretending the task is complete.

## 5. Critique before acceptance

For curriculum work, check at minimum:

- source fidelity and page/row provenance;
- duplicate, missing, and orphan records;
- CEFR/GSE level consistency;
- balance across listening, reading, speaking, writing, interaction, and mediation;
- whether interpretations have been mislabeled as source facts;
- clear Modern Standard Arabic where Arabic is present.

Run separate deterministic checks and structured self-review for high-impact mappings.
External specialist or learner review remains a named gate where evidence requires it.

## 6. Verify and record

For a completed milestone or material partition, create a focused report under
`logs/runs/` when the evidence would otherwise be hard to reconstruct. Include:

- task and outcome;
- files created or changed;
- source evidence and counts;
- validation performed and results;
- assumptions, risks, and unresolved questions;
- exact recommended next task.

Then update `automation/TASKS.json` and `automation/STATE.json`. Mark a task complete
only when its acceptance criteria pass.

Use intentional commits for verified milestones. Push only when the owner has
authorized publishing; the current private repository may be pushed directly to its
main branch under the owner's standing instruction.

## 7. Completion and pause conditions

Continue while safe work remains. If all tasks are genuinely complete, set project
status to `complete` and report the final evidence. If an owner decision is genuinely
required, record the precise question and continue any safe independent work.

Never communicate externally, spend money, deploy publicly, publish content, or upload
private files. Do not expose credentials. Image/audio/video generation is prohibited
until its phase is explicitly active.
