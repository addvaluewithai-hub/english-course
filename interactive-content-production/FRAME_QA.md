# FRAME QA — screenshot/inspection/repair loop

Based on actual `learn-curriculums/preview-sdk/tools/frames.mjs`. That runner uses Vite + Playwright Chromium, navigates **every reading beat**, takes scene contact sheets in portrait/landscape, writes `REPORT.md`, and checks for overflow, missing captions, visually unchanged frames, sideways scroll and browser errors. It also tests hidden answers on the attempt state. This factory adopts those checks; **EnglishLive needs its own deterministic fixture route**, not a copied `.rl-board` selector.

## In the product repo, provide a deterministic preview

A fixture MUST:
- Render the **actual** lesson components/board using authored package and app styling; mocks may replace Gemini/network/audio transport but not the UI renderer.
- Set `lessonId`, `sceneId`, `beatId`, `mode`, `selectedOptionId` deterministically by an explicit test API or test-only route.
- Support at least `teaching`, `question` (no answer selected), `correct-feedback`, `wrong-feedback`, `final-speaking-listening`, `final-speaking-otti`, `complete`. Additional hint and error states if supported.
- Freeze nondeterministic animation for screenshots, wait for fonts/assets and stable layout before capture. Use an ordinary-motion test separately to catch reveal glitches; don't call frozen screenshots motion QA.
- Run without microphone access, API keys or TTS charges; QA sample learner data must be fictional.
- Expose a board root and semantic ID/phase selectors (`data-lesson-id`, `data-scene-id`, `data-beat-id`, `data-lesson-state`) so a runner doesn't guess from text or timers. Example selectors are **requirements to implement**, not claims the current app provides them.

## Required capture matrix

| Context | Viewport (px) | Goal |
| --- | --- | --- |
| Narrow phone portrait | `320 × 640` | clipping, footer, tap target, short-height flow |
| Typical phone portrait | `400 × 860` | primary authored reading/interaction experience |
| Desktop landscape | `1280 × 900` | full classroom proportions and placement |

For each **scene** capture every authored **beat**, not just first/last. Include one unanswered MC screenshot, *correct and wrong* answer+feedback, hints open/closed, chapter transition, error/interruption where applicable, and the final **unprompted Speaking** states. Build a `<scene>-<layout>.png` contact sheet plus `REPORT.md`, link individual screenshots when needed. In CI use a 30-day retained `actions/upload-artifact` set; avoid checking generated PNGs into the curriculum repo.

## Browser probe checklist (automatable hints only)

- JS page errors / 4xx+ network responses, missing font/asset loads.
- Horizontal page overflow.
- Board root and visible children: text/image bounds outside its safe area; `scrollHeight > clientHeight` where board overflow is forbidden.
- Tiny text and hit targets smaller than approx. 44 CSS px (exceptions documented, not silently green).
- Captions absent during teaching, scene/beat ID mismatch, missing canvas/alt description.
- Unanswered quiz visibly contains correct answer/reasoning before submission.
- Rapid Next/Back/interruption restoring future state, duplicate scene completion, wrong/correct branch not distinguishable.
- Characters/canvas masking questions or buttons. Verify Otti never covers the actual learning focus.
- Source/wording mismatch: transcript/narration says one thing but board contradicts it (manual review).

**Important:** The probe can flag suspicious bounds, but cannot decide that a diagram has pedagogical value, that Arabic is readable, or that Otti speech is accurate. Never equate no automated warnings with acceptance.

## Human/agent visual inspection checklist

Actually **open every generated sheet**. On each beat ask:
1. Do the visual and narration teach the same idea *at the same time*?
2. Does an element appear too soon (answer leakage) or too late (narration outruns it)?
3. Could a first-time English learner parse the diagram with no prior explanation?
4. Are Arabic/English lines ordered correctly; are line breaks legible?
5. Does the correct and incorrect branch show useful feedback, not only green/red?
6. Is one board state overloaded or oddly empty? Is the main concept visible at the chosen viewport?
7. When hints/objectives open, do they obscure voice controls or change the layout unpredictably?
8. Is the final Speaking genuinely separate from MC and can learners recover from a weak answer?

## Repair protocol

For each issue record:
- `id`, `severity`, viewport, exact scene/beat/state, before screenshot, what was **observed** (not only "looks bad"), cause hypothesis, changed file/ref, after screenshot, actual recheck result.
- Fix in product branch, rerun **same** state and affected neighboring beats in every impacted viewport, inspect images again.
- Never erase failed attempts in a way that makes the PR look pristine. Link CI artifact and defect ledger.
- New script/board/layout/app build invalidates the old frame review. Record updated commit/build SHA and rerun.

## CI recipe for product agent

Playwright runner belongs next to the real product tests, for example `englishlive/scripts/test-lesson-frame-sheets.mjs` (this is a **proposed location**, not an existing file). In its workflow:
1. `npm ci`; `npx playwright install --with-deps chromium`.
2. Build/start app or deterministic fixture host; wait for health and version.
3. Drive explicit scene/beat/state selectors using fixture API and take PNGs for all viewports.
4. Generate a per-scene contact sheet with captions from canonical beat IDs; write JSON+Markdown reports.
5. Run automatic browser checks; fail for browser errors/missing states/true overflow. Keep visual critique independent.
6. Upload PNG contact sheets and report even on failure (`if: always()`, retention ~30 days).
7. Reviewer opens and critiques all sheets; fixes and reruns. Only after actual human/agent inspection update `QA_REPORT` to `visual-reviewed`.

For an **illustrative** harness starter (not hooked to EnglishLive yet) see [templates/playwright-frame-harness.example.mjs](templates/playwright-frame-harness.example.mjs). Do not paste its placeholder fixtures into production and claim coverage.

## Live-only gates

A deterministic fixture cannot establish: Otti's real pronunciation, script fidelity, interruption races with Gemini, provider latency, mic permissions or educational quality of AI's Speaking judgment. Test real voice with (a) correct quiz, (b) wrong quiz, (c) weak/no-sense speaking, (d) adequate speaking, (e) interrupted narration and reconnection. Compare authored `SCRIPT` against `AI` transcript and audio, using synthetic test learners only.

**Proof levels:** `built` ≠ `browser-captured` ≠ `images-opened-and-critiqued` ≠ `live-audio-tested` ≠ `owner-accepted` ≠ `released`.
