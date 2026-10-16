# Agent Rules — Curriculum Workspace

## Shared execution control (start here for production / review)

For requests such as "افتح وكمل", "شوف إحنا واقفين فين", producing a Learn lesson, reviewing one lesson, reviewing each five-lesson batch, or coordinating Practice missions, **first open [`ENGLOTTI_MASTER_WORKFLOW.md`](ENGLOTTI_MASTER_WORKFLOW.md)** on the latest `main`. Verify the live status queues and open PRs; its cached control panel is a snapshot, not permission to override curriculum locks or ownership. Follow its `STEP 0 → STEP 1 → STEP 2`, then use the domain-specific instructions below. Keep the master workflow and status/PR evidence aligned in each handoff. Never silently merge/deploy, pay for media, or mark a lesson `done` without the required acceptance.

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

## Interactive content production and autonomous next-lesson queue

For any request such as **"شوف A1 واقف فين وكمل"** or a user asking to produce the next lesson, follow [interactive-content-production/AGENTS.md](interactive-content-production/AGENTS.md). It defines six reviewed production status tables, sequential `next LEVEL` lookup that stops on earlier in-flight work, scoped PR claims, source-lock checks, screenshot QA and owner acceptance. Do **not** silently treat curricular briefs or previous pilots as completed interactive lessons. Lesson production is a **separate delivery workstream** and cannot by itself bypass curriculum authorization or commercial gates.
