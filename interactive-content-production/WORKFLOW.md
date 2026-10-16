# WORKFLOW — staged production with actual evidence

Adapted from `learn-curriculums/instructions/stage-gates.md`, but adapted to **already-designed English curricula**, not book/PDF intake and not automatic publication. A normal `next` advances one requested gate and stops; the owner may explicitly authorize a larger scope. STATUS must record incomplete work and never silently advance.

| Gate | Deliverable and stop condition |
| --- | --- |
| **P0 — Curriculum mapping** | Verify current branch, exact canonical lesson brief, semantic/control ledger, lifecycle and prior-level prerequisites; capture source ref/SHA and affected target IDs. Stop if no authorized semantic role/lesson brief. |
| **P1 — Connected instruction** | Author a single coherent Egyptian-Arabic/English teacher script with transitions, examples, learner confusion paths, planned final speaking transfer; sketch visuals **before** formal scene split. Preserve lexical roles and B1 skill focus. Stop for critique. |
| **P2 — Teaching critique** | Critique step-by-step from a real learner's point of view: first-use vocabulary, unmotivated examples, grammatical correctness, too-early question, repetitive praise, mistranslation, false mastery, cognitive load, *independent final speaking*. Rewrite and log concrete changes. |
| **P3 — Canonical beat + assessment package** | Cut accepted narration into beat IDs, exactly one semantic reveal per beat; define board before/during/after, stable question IDs, choices/distractors, keyed answer and per-outcome spoken reasoning; final Otti Speaking rubric. **The authored beat package becomes the canonical speech source.** |
| **P4 — Product renderer (external repo)** | Implement a scoped feature branch in `englishlive`, using existing Otti/lesson APIs rather than building another player. A test-only/fixture path must let Playwright jump deterministically to each beat/interaction state without a paid live provider. |
| **P5 — Screenshot audit + repair** | Run real browser capture for every semantic beat and interactive state in `400x860` portrait and `1280x900` landscape (also `320x640` compact phone). Generate one contact sheet per scene, warnings and a report. **Open every sheet**; fix specific faults; re-run and inspect before/after. CI or screenshot existence is NOT inspection. |
| **P6 — Live voice / learner trial / handoff** | Try actual Otti audio, correct and wrong choices, pronunciation/mixed language, interruptions, final Speaking with weak answers. Compare `SCRIPT` vs actual model speech. Record learner findings and owner decisions; release remains an independent product approval. |

## Listening-first extension

For conversational/receptive lessons with a suitable scenario, first author a listening source dialogue and review the **actual recording** separately. Refer to [LISTENING_FIRST.md](LISTENING_FIRST.md) for stable clip IDs, Gemini tool playback, audio synchronization and evidence gates. Do not interpret the P5 visual pass as a P6 audio pass.

## Parallel agent roles

- **Curriculum mapper:** accepts only authorized semantic/control decisions; maps learning goals and evidence; never silently reopens locked levels.
- **Writer/educator:** script and Arabic/English examples, learner attempt, likely misconceptions, right/wrong explanation, quiz distractors.
- **Visual director:** plans causal or communicative diagrams and progressive reveals for each beat. A polished generic icon isn't automatically useful pedagogy.
- **Frontend implementer:** accessible responsive renderer and deterministic state fixture in product repo; no parallel lesson engine.
- **Screenshot critic:** independently walks each state and both question branches; records screenshot filenames, actual visible bugs and proposed repairs.
- **Live QA reviewer:** verifies actual teaching audio and learner interaction; not inferred from mocked screenshots.

One agent may cover multiple roles but must preserve their *independent checklists* and not claim human approval.

## Dependency and content rules

- One source row is not one scene. Integrate vocabulary, chunks and grammar in **meaningful use**, not isolated card factories.
- A B1 communicative objective should lead the lesson. Recognizing a phrase in MC is **practice evidence**; success in final Speaking is a different, human/teacher-judged performance condition.
- Use one connected social situation for supported instruction and a **different** situation for final transfer.
- During lesson authoring, scripted Otti teaching lines are exact; spontaneous Otti speech is reserved for necessary clarification and final live practice.
- If the design uses auto progression after MC: correct OR wrong → authored explanatory voice feedback → completion signal → next beat. Preserve `wrong` in evidence; don't claim mastery.
- Questions do not show the answer before a click. Click should not be possible while teacher audio is speaking. Incorrect choices should never result in false praise.
- Maintain semantic state IDs in data/DOM. Never infer lesson state by timeouts, image similarity or what a model might be saying.
- The final live Speaking stage must remain authentic: no MC substitutes, no automatic pass on "Okay", "Bye" or silence; Otti may request a follow-up or explanation. This is still model judgment and requires testing with counterexamples.

## PR quality gate

The product PR should provide:

1. Deterministic preview route + fixture metadata; readiness selector; runtime SHA.
2. Evidence artifacts: contact sheets per scene and view, individual states as required, automated warnings, console/network errors.
3. Defect ledger: `OPEN/REPAIRED/RECHECKED/ACCEPTED_RISK`, impact, source state, before/after file, reviewer/date.
4. Test results: schema checks, browser interaction checks, responsive screenshots, live voice test, no regressions in Practice.
5. Clear **not tested** declarations for anything skipped.

A new scene or changed script/visual invalidates affected screenshots. New runtime CSS/layout dependencies require refreshed viewport captures. Human acceptance is not inherited from an earlier SHA.

## Scope caution

The analogous `learn-curriculums` project currently forbids new audio production until its own owner explicitly reopens it. That policy is **not** a restriction on EnglishLive's already authorized live Otti experiment; it simply means their audio/timing pipeline is not the reusable screenshot source. The product must supply its own preview routes and Playwright harness. This folder does not install one or imply a live browser has been tested here.
