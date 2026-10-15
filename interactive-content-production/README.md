# إنتاج المحتوى التفاعلي — Interactive English Lesson Production

**Status:** reusable authoring/QA factory contract, not a published lesson or authorization to modify locked curriculum, run paid media, merge, or deploy. Source of truth remains `main` and the applicable level semantic/control locks.

## Why this exists

An agent should deliver a **teachable, inspected lesson** rather than a stack of word cards, a nice screenshot, or a passing build. The methodology adapts the proven authoring and **frame-sheet QA** from [learn-curriculums](https://github.com/addvaluewithai-hub/learn-curriculums), especially its [agent skill](https://github.com/addvaluewithai-hub/learn-curriculums/blob/main/.agents/skills/produce-learn-lesson/SKILL.md), [stage gates](https://github.com/addvaluewithai-hub/learn-curriculums/blob/main/instructions/stage-gates.md), [visual craft](https://github.com/addvaluewithai-hub/learn-curriculums/blob/main/instructions/visual-craft.md), and [Playwright frame generator](https://github.com/addvaluewithai-hub/learn-curriculums/blob/main/preview-sdk/tools/frames.mjs).

**Do not literally copy its preview player:** that project currently ships *reading-first* material and defers audio by owner policy. EnglishLive uses a separate Otti Live renderer, speech and interaction runtime. We adapt the process and its evidence bar, not its technical player, physics notation, or audio policy.

## Repo ownership / boundaries

| Repo | Owns | Must not own |
| --- | --- | --- |
| `english-course` | level inventories, locked semantic roles, authoritative lesson briefs, production specification/templates, traceable decisions | React lesson UI, second player, deployed screenshots as curriculum claims |
| `englishlive` | application, Otti playback/live tools, lesson renderer, Playwright fixture routes, captured frames/QA artifacts, runtime and integration tests | silently rewritten curriculum inventories/semantic locks |
| `learn-curriculums` | reference workflow/techniques for this factory | EnglishLive feature requirements or its final learning design |
| `new-learn` | reference teacher-led and authored reading playback behavior | shared production authority across repos |

`english-course/AGENTS.md`, `START_HERE.md`, `CURRENT_STATE.md`, levels' manifest, exit contract, `design-review`, semantic locks and authorization remain authoritative. A source row ≠ a mandatory separate flashcard, and a transfer slot cannot introduce new required material.

## Start any lesson production request

For automatic next-lesson selection, the short entry point is [AGENTS.md](AGENTS.md); the six status queues are under [status/](status/), and the inspector is `python3 interactive-content-production/tools/production_status.py next A1`. No agent should guess which lesson has already shipped.


1. Identify **exact** `level/unit/lesson` by the canonical lesson brief/semantic ledger (not a stale prototype ID). Record repo/ref/commit, source path and approved semantic roles.
2. Read [WORKFLOW.md](WORKFLOW.md), [LESSON_CONTRACT.md](LESSON_CONTRACT.md), and [FRAME_QA.md](FRAME_QA.md) *before* authoring.
3. Copy [templates/PRODUCTION_STATUS.template.md](templates/PRODUCTION_STATUS.template.md) and [templates/QA_REPORT.template.md](templates/QA_REPORT.template.md) into the scoped lesson production branch/artifact directory. **Never mark review passed without actual evidence**.
4. See the [example fixture matrix](templates/fixture-cases.example.json) and [portable Playwright frame harness](templates/playwright-frame-harness.example.mjs): they define the *future EnglishLive product-side fixture contract*, not screenshots that exist already.
5. For a scoped requested gate only, author/critique and stop. A comment from the owner revises that gate. If the owner requests a complete multi-stage run explicitly, work within that scope but still report the quality gates and unresolved real-browser/human steps.
6. Keep **all changes on a scoped branch/draft PR**, with separate lesson IDs and fixtures. No writes to other agents' Practice PRs.
7. Store final render/interaction tests and screenshots with the **product PR or its CI artifacts**, linked from the production status. Do not check binary screenshot dumps into this curriculum source of truth.

## Required delivery inventory (for each interactive lesson)

- Canonical source/role mapping and prerequisites; what is **new**, **recycled**, **receptive**, or **deferred**.
- One coherent story/learning journey with a written **teacher script**, beat order and explanatory feedback. Author the teaching first, then divide into scenes. No prompt-only lectures.
- Beat-by-beat board plan: semantic unit ID, narration, *what changes visually and why*, pre-reveal content and accessibility text; portrait **re-layout**.
- Questions: answer keys; attractive plausible distractors; correct and incorrect **reasoning**, not empty praise; not showing answers beforehand.
- Correct handling of MC vs speaking evidence: MC is receptive recognition, **not** productive speaking mastery. Retain the required final **live speaking** assessment for appropriate EnglishLive lesson flows; Otti judges conversation sufficiency, with logs and failure cases for human review.
- Deterministic product fixtures for each state and both success/failure branches; Playwright frame sheets and defect reinspection.
- Honest delivery record: structural tests, screenshot files actually opened, bugs fixed, audio/live QA separately, human acceptance/release separately.

## Release language

- `draft`: material still being written; never described as ready.
- `script-reviewed`: spoken/teaching text critiqued with source mapping.
- `visual-review-pending`: implemented preview, **no inspected frames**.
- `visual-reviewed (AI)`: named real frames actually inspected, defects documented and repaired.
- `live-audio-pending`: UI may look good, but no verified live Otti behavior yet.
- `learner-trial-pending`: needs owner/real learner to report comprehension problems.
- `accepted-for-product-review`: owner has explicitly accepted authoring/visual proposal; not deployed or certified.
- `released`: only after product owner deploy approval and confirmed release, never inferred from CI.

Reference example: `B1 U1-L02` is about **sustaining a conversation**. It must not be flattened into mandatory exact production of every support phrase just because the prototype happens to quiz those phrases. Formal speaking transfer must change the situation and withhold answer-bearing help.

## Agent handoff checklist

Before stopping, report: exact repo/branch/PR; requested gate; canonical source refs; files changed; tests run with actual results; screenshots captured **and viewed**, viewports and states; open defects; runtime/speech trials; human decision requested. Never say "verified" if you only wrote documentation or ran a typechecker.
