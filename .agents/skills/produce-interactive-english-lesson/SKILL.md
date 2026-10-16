---
name: produce-interactive-english-lesson
description: Source-grounded production playbook for turning authorized English Course lesson briefs into authored Otti-led interactive Learn experiences, semantic SVG boards, deterministic MC checks, final Speaking and inspected browser frame sheets. Use when the user asks to build, critique, QA or scale interactive English lessons.
---

# Produce an interactive English lesson

This is an **authoring and QA skill**, NOT permission to edit locked curriculum or publish a student lesson.

Read in order:
1. Root `AGENTS.md`, `START_HERE.md`, `CURRENT_STATE.md` and the current level's manifest, exit contract, lesson brief, semantic/control decisions.
2. [Production factory overview](../../../interactive-content-production/README.md)
3. [Staged gates](../../../interactive-content-production/WORKFLOW.md)
4. [Editorial lesson/board contract](../../../interactive-content-production/LESSON_CONTRACT.md)
5. [Screenshot and visual QA requirements](../../../interactive-content-production/FRAME_QA.md)
6. [Production status](../../../interactive-content-production/templates/PRODUCTION_STATUS.template.md) and [QA report](../../../interactive-content-production/templates/QA_REPORT.template.md).

## Work contract

- Pin canonical repo/path/commit; distinguish new, support, receptive and retrieval material. Don't infer mastery from coverage or promote support language into required Speaking targets.
- Honor the user's explicit stage/scope. Otherwise complete ONE production gate, document it and STOP; revise current gate if corrected. No self-authorized skipping of real browser or learner QA.
- When the canonical brief involves conversational listening, read `interactive-content-production/LISTENING_FIRST.md`; author a dialogue and quality-reviewed recording before teaching beats. Studio WAV/timing approvals are separate from UI screenshot checks and cannot be simulated as mastered listening.
- Write a coherent speakable lesson **before** splitting into small author-owned beats. Each beat has `speech`, purpose, board intent/state and a visual reason. Narration/feedback in the final authored package are canonical.
- Plan genuine subject-specific visuals as bespoke SVG/React states. Show meaning progressively, do not fill a card with text and call it a board. Preserve safe stage/canvas zone for the talking Otti character, on portrait and landscape.
- Add deterministic MC with keyed answer IDs and spoken **why-right / why-wrong**; wrong choice can advance after explanation but must stay recorded as incorrect.
- Keep a genuine final Speaking section when required for EnglishLive Learn: Otti listens/judges with brief repairs rather than accepting random words or goodbye loops. MC isn't evidence of spoken mastery.
- Never build a duplicate player or put product React/Playwright runtime in this `english-course` source repo; implement those in a scoped `englishlive` branch against its actual interfaces and fixtures.
- Use real browser state fixtures to capture **every authored beat**, question-unanswered, right/wrong feedback, hint/error states and final Speaking in 320x640, 400x860, 1280x900. Capture contact sheets and report; open every sheet and correct bugs then rerun. Missing deterministic fixtures or browser access => `not visually verified`.
- Audio tests are separate. Inspect real Otti narration, feedback, interruption/reconnect and final speaking; `SCRIPT` vs `AI` transcripts can assist but cannot alone prove actual audible quality.
- Preserve screenshots and structured QA report as product PR/CI artifacts; link them from the production STATUS. A green CI run is not visual acceptance and does not authorize merge.
- Don't interfere with concurrent Practice PRs. Use a separate feature branch and draft PR. Don't claim files/tests/screenshots made unless they actually exist.

## Before answering

Report the canonical references, branch/PR, which production gate you completed, changed artifacts, tests/screenshots actually run and inspected, unresolved faults and needed human decision. If this is only a playbook documentation task, say so; do not imply a live lesson was produced.
