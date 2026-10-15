# Agent Rules — Curriculum Workspace

Before changing curriculum, read:

1. `START_HERE.md`
2. `CURRENT_STATE.md`
3. `docs/LEVEL_CURRICULUM_DESIGN_PLAYBOOK_V1.md`
4. The current level manifest, exit contract and design-review stages.

## Authority

- `main` is the active source of truth.
- Locked lower levels are immutable prerequisites unless explicitly reopened.
- The archive branch is provenance/history only, not an active workspace.

## Curriculum rules

- Source evidence comes before invented curriculum structure.
- Do not assume unit or lesson counts before Stage 5 architecture.
- One source row is not automatically one teaching object or one productive requirement.
- Human semantic/control decisions are authoritative.
- Automation may build review aids, expand explicit decisions, count, reconcile and validate; it may not invent final pedagogy or claim human review.
- Preserve exact provenance and lifecycle ownership.
- Coverage is not mastery. Fresh retrieval, recycle, consolidation and exit evidence must remain explicit.
- Transfer/retrieval slots must not hide new required content.

## Scope

This branch contains active curriculum design, evidence and validation tooling. Do not restore removed pilot/prototype/gold/research/legacy delivery material into `main` unless the owner explicitly reopens that workstream.

## Interactive lesson production (separate workstream)

For a user-authorized task turning an existing lesson brief into an interactive Otti Learn experience, read [interactive-content-production/README.md](interactive-content-production/README.md) and the discoverable [production skill](.agents/skills/produce-interactive-english-lesson/SKILL.md). These are **process guidance only**; product rendering, Playwright screenshots and actual voice QA belong in the product repo. Preserve canonical source/semantic locks, keep feature work on a scoped draft PR, and do not restore old delivery prototypes into this curriculum source tree.
