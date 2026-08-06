# Project Agent Rules

Read these before changing anything:

1. `docs/MASTER_PLAN.md`
2. `docs/LEARNING_PRINCIPLES.md`
3. `automation/AGENT_RUNBOOK.md`
4. `automation/STATE.json`
5. `automation/TASKS.json`

## Non-negotiable engineering rule

Keep the project modular. Prefer multiple focused files and folders over large files.
Keep source files below 200 lines when practical and never exceed 300 lines without an
explicit exception recorded in `docs/DECISIONS.md`. Do not compress code merely to meet
the limit. Raw references, extracted text, and generated datasets are exempt; split
their processing logic, not the evidence itself.

## Product guardrails

- This is a serious English course for Arabic-speaking adults.
- Source evidence comes before invented curriculum structure.
- Do not design the production database before the gold lesson is tested.
- Do not mass-generate lessons, images, audio, or video before the gold-lesson gate.
- Keep raw sources immutable. Derived data belongs in `data/derived/`.
- Every lesson objective must retain traceability to its sources.
- Modern Standard Arabic is the current explanation baseline; see the decision log.
