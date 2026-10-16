# AGENTS — إنتاج المحتوى التفاعلي (Interactive Lesson Production)

**This is the short entry point** for an agent who hears: "شوف إحنا واقفين فين في A1 وكمل".

This directory guides production and its QA; the canonical curriculum/semantic locks live elsewhere in **this same repo**. Never pretend that finished lesson briefs or pre-existing scenes mean a released interactive lesson.

## Read these files first, in order

1. `../AGENTS.md`, `../START_HERE.md`, `../CURRENT_STATE.md`
2. `README.md`, `WORKFLOW.md`, `LESSON_CONTRACT.md`, `FRAME_QA.md`
3. `status/A1.md`, `status/A2.md`, `status/B1.md`, `status/B2.md`, `status/C1.md`, `status/C2.md` as relevant.
4. `../.agents/skills/produce-interactive-english-lesson/SKILL.md` (from repo root: `.agents/skills/produce-interactive-english-lesson/SKILL.md`).
5. Exact source lesson brief, level `manifest.json` and semantic/control lock, and any linked in-flight product PRs.

## Just follow this protocol when owner says "كمل A1"

1. Pull `main` of **both repos** and run `python3 interactive-content-production/tools/production_status.py validate`.
2. Run `python3 interactive-content-production/tools/production_status.py next A1`. This returns the **first UNFINISHED lesson in canonical unit/lesson order**, not an arbitrarily later one and source-brief path. For other levels replace A1. If C1/C2 lacks authorized lesson design: STOP, no invented lessons.
3. **Before claiming or resuming**, search open branches/PRs in `english-course` and `englishlive` for the same level/unit/lesson. If command returns `IN_FLIGHT_REVIEW`, the prior lesson is owned or blocked: inspect linked PR and await assignment/explicit owner authorization to resume. **Do not skip to a later unfinished lesson or overwrite another agent's branch.** The Markdown table is a queue, not an atomic distributed lock.
4. Verify that level semantic/lesson-design status allows planning. The manifests currently distinguish approved *design* from **delivery production**, which is still `false` for A1/A2/B1/B2; an explicit owner request authorizes a **scoped draft** but does not alter the delivery gate or authorize bulk publishing. If permission is unclear, ask rather than editing locked files.
5. Create an isolated feature branch and **Draft PR** for the selected lesson in `englishlive`, and a linked status PR/commit in `english-course`. Change the corresponding row to `claimed` with your agent handle, PR URL and a date, then push quickly to minimize race conditions. This row is a shared queue, not a distributed lock; GitHub PR conflicts must be resolved before claiming complete ownership.
6. **Mandatory P0.5 before any script or paid audio:** inspect all source item IDs, semantic role and lifecycle. Run `python3 interactive-content-production/tools/coverage_gate.py check LEVEL Ux-Lyy` for the selected lesson and `python3 interactive-content-production/tools/coverage_gate.py check-all` for every registered lesson. Make a per-lesson JSON map in `coverage/LEVEL/Ux-Lyy.json` and update each item's planned scene/beat/evidence; stop for owner review on conflicts. `ready` must NOT pass with any item escalated, unreviewed or QA/owner gate pending. A checked ledger row is not proof the learner mastered the item.
7. For a listening-led conversational lesson, read `LESSON_CONTRACT.md` (Listening-first section) and use `addvaluewithai-hub/gemini-tts` to plan approved pre-recorded multi-speaker audio + word timestamps; do not use browser TTS as a production recording or dispatch paid jobs without scope approval. Then follow `WORKFLOW.md` P0–P6: curriculum map → coherent authored narration → critique → semantic beats/quiz/feedback and final Speaking → SVG classroom implementation → deterministic Playwright screenshots and opened contact sheets → actual Otti audio test and learner/owner review. Use shared product QA registry/runner; do **not** fork a per-lesson screenshot script.
8. Update row and evidence on each significant gate: `claimed` → `in-progress` → `qa-pending` → `review-needed` → `done` **only after explicit owner acceptance** plus linked product PR, QA artifacts and live audio verdict. Failure stays `review-needed` or `blocked`. Merge/Deploy requires explicit approval and passing checks; don't self-approve.
9. At handoff, report **exact** remaining work, next lesson only after the previous is accepted or explicitly paused. Do not convert all levels in one uncontrolled run.

## Six authoritative production queues

| Level | Status file | Canonical design | Number of approved lesson slots | Initial delivery state |
| --- | --- | --- | ---: | --- |
| A1 | [status/A1.md](status/A1.md) | Stage 07 briefs | 62 | unstarted, manifest delivery gate pending |
| A2 | [status/A2.md](status/A2.md) | Stage 09 briefs | 83 | unstarted, manifest delivery gate pending |
| B1 | [status/B1.md](status/B1.md) | Stage 07 briefs | 85 | B1 U1-L02 has a **partial pilot only** |
| B2 | [status/B2.md](status/B2.md) | Stage 07 briefs | 95 | unstarted, manifest delivery gate pending |
| C1 | [status/C1.md](status/C1.md) | no authorized lesson architecture yet | unknown | BLOCKED |
| C2 | [status/C2.md](status/C2.md) | no authorized lesson architecture yet | unknown | BLOCKED + commercial permission |

## First next lesson: A1

`python3 interactive-content-production/tools/production_status.py next A1` currently points to **IN-FLIGHT U1-L01 — Hello. I'm …**, owned by linked Draft PR #54. Inspect that PR first; do not start U1-L02 just because U1-L01 is already claimed. Read `curriculum/levels/a1/design-review/07-lesson-briefs/lesson-briefs.md` and stage/semantic controls. Existing legacy A1 scenes are examples, not certified deliveries.

## Keep PRs clean

Never modify Practice while implementing Learn. Do not update status to `done` just because CI is green or 78 screenshots exist for *another* lesson. Screenshot automation and real voice QA are two distinct evidence sets. Avoid permanent browser-based test bypasses exposed in production.

**Owner's shorthand:** "بص في [LEVEL] وكمل" = inspect queue, resolve claim, produce next scoped draft in order, QA and hand off. Not permission to silently merge or release an entire level.
