# Project Handoff

Authoritative machine state: `automation/STATE.json` and `automation/TASKS.json`.
These are project memory and a gated checklist. They do not schedule agents.

## Current checkpoint

The curriculum architecture and A1 syllabus are locked. Production and internal QA of
the actual first ten lessons are complete, together with the continuous progression
prototype and ethical six-visit instrument.

- Last completed task: `PILOT10-003`.
- Active task: `TEST-002`.
- Real learner sessions collected: 0.
- The release is U1-L01 through U1-L09 followed by U2-L01; it is not a showcase set.
- All ten packages and the continuous instrument are ready. Real collection cannot
  begin until the ten final videos are rendered, transcript-matched, and listened to.
- Reusable system decisions remain locked until TEST-002 has real progression evidence.
- The current workflow uses one continuing primary agent; no scheduled or hourly agent
  team exists.

## Completed curriculum work

- All 9,274 normalized CEFR, GSE, EGP, GSE Grammar, Oxford 3000, and Oxford 5000
  records have a reviewed disposition and retained source provenance.
- The A1-C2 spine contains 41 communicative-function strands, 91 grammar families, 10
  lexical-resource strands, 10 pronunciation strands, and 15 performance dimensions:
  167 families/strands and 1,015 lifecycle stages in total.
- All 1,222 EGP features and 456 GSE Grammar records are crosswalked. Oxford entries
  remain level-aware resources, not an arbitrary word-count promise.
- No unexplained source orphan or invalid level regression remains in SPINE-004.
- All 81 historical A1 source candidates were reviewed: 23 keep, 22 revise, 21 merge,
  14 support-only, and 1 split decision.
- The final learner-facing A1 v1 has 45 capabilities in six units with lesson counts
  `[9, 9, 7, 7, 5, 8]`.
- All 158 exact grammar, lexical/chunk, and pronunciation items have a final
  introduction, fresh recycle, and later consolidation placement.
- All 24 mapped prerequisite edges are aligned. Nineteen unit mastery stations cover
  all 45 capabilities, and seven exit stations cover all seven A1 exit dimensions.

The locked human and machine sources are:

- `docs/SPINE_004_COMPLETION_AUDIT.md`;
- `data/reviewed/a1-final-candidate-decisions-v1.json`;
- `docs/A1_FINAL_CANDIDATE_DECISIONS_V1.md`;
- `data/reviewed/a1-scope-and-sequence-v1.json`; and
- `docs/A1_SCOPE_AND_SEQUENCE_V1.md`.

## Completed gold-lesson work

The owner-approved one-teacher Egyptian-Arabic/English lesson is final `U1-L03`, after
a social opening and a listening-input lesson.

- Final package: `units/a1-v1/unit-01-first-connections/lessons/u1-l03/`.
- Seven exact items are introduced and three are freshly recycled with source hashes.
- Every spoken English span in the transcript uses the required English-language and
  phoneme markup for mixed-language voice generation.
- The explanation video contains one teacher and no applied interaction; questions
  start after the video.
- Conversational Arabic avoids artificial tanween forms while retaining natural
  `مثلًا`.
- Fresh mastery has one equivalent replacement task and at most two fresh attempts.
- `gold/introduce-yourself/` is preserved as accepted prototype lineage, not the final
  sequence location.

QA evidence is in `data/reviewed/gold-lesson-v1-qa.json` and
`docs/GOLD_LESSON_V1_QA.md`.

## Learner-test readiness

TEST-001 is complete:

- learner route: `prototype/gold-lesson/index.html`;
- observer route: `prototype/gold-lesson/observer.html`;
- Arabic start guide: `research/learner-test-v1/START_HERE_AR.md`;
- consent, facilitator, privacy, and accessibility controls;
- target eight and minimum six eligible completed real sessions;
- odd/even `teachback` and `omit` allocation;
- nine pre-registered gating metrics;
- two or more live double-rated sessions;
- versioned JSON Schema and semantic validation for private records; and
- a guarded aggregate pipeline that forces synthetic fixtures to
  `simulation_only_no_gate_effect`.

Browser verification passed consent, all nine learner steps, the omit route, no-answer
timing, observer consent enforcement, and zero console errors after the discovered
planning-index defect was fixed.

This kit is retained as the method prototype. It does not approve the first-ten
progression release on its own.

## First-ten release

`PILOT10-001` is complete. The machine contract at
`data/reviewed/a1-first-10-lessons-pilot-v1.json` contains the exact A1 positions 1–10:
nine Unit 1 lessons and Unit 2 Lesson 1. It assigns 49 introductions and 16 fresh
recycles without duplicate capability ownership.

The human plan is `docs/PILOT_10_PRODUCTION_PLAN_V1.md`. Every package must use the
accepted one-teacher bilingual presentation style, SSML plus IPA for spoken English,
post-video application, fresh mastery, safe fictional identities, and source hashes.

`PILOT10-002` and `PILOT10-003` are also complete:

- all ten packages pass the shared contract and contain 120 source files;
- the batch owns all 65 exact introduction and fresh-recycle roles;
- the learner route is `prototype/first-ten/index.html`;
- the facilitator route is `prototype/first-ten/observer.html`;
- the six-visit protocol and consent kit are in `research/first-ten-pilot-v1/`;
- private longitudinal records have schema and semantic validation; and
- synthetic fixtures are explicitly unable to satisfy TEST-002.

The content QA names U1-L08 as the primary load/split candidate and U1-L05 as the
secondary. This is an observation priority, not a pre-decided split.

## Exact next work

1. Generate one-teacher Gemini media from each approved `video/scene.txt`,
   `video/sample-context.txt`, and `video/transcript.txt` source.
2. Listen to every rendered lesson and verify speaker count, transcript match, English
   pronunciation, Arabic naturalness, pacing, and absence of in-video applied questions.
3. Rehearse the six-visit route with a `synthetic_fixture`; it remains non-evidence.
4. Run consented real-learner journeys, publish only de-identified aggregates and named
   revisions, and record the go/revise/stop/insufficient decision.
5. If that gate passes, complete `SYSTEM-001`, then `ARCH-001`, then controlled
   production of the remaining A1 lessons.

Synthetic, agent-generated, owner, or previously exposed records cannot replace the
required beginner observations. Do not unlock later gates merely because tooling or
fixtures pass.

## Preserved historical work

- `units/unit-01-first-connections/` contains eight pre-v1 source packages. They are
  useful lineage only; the nine final Unit 1 packages now exist in `units/a1-v1/`.
- `data/reviewed/a1-lesson-map.json` contains the 81-candidate source audit. It remains
  traceable input, not the final learner syllabus.
- `references/legacy/` contains recovered planning conversations. They establish
  historical product intent, never curriculum authority.

## Repository and publication boundaries

- The repository contains publisher source snapshots and has no selected open-source
  license. Review reuse rights before public redistribution.
- Never commit private participant records, contacts, raw answers, audio, video, or
  screen recordings.
- No production app, account system, database, or media factory has been authorized.
- Direct push to `main` remains the owner's standing publication instruction.

## Working rules

- Read `AGENTS.md` and `automation/AGENT_RUNBOOK.md` before modifying the project.
- Keep implementation files modular and normally below 200 lines, never above 300.
- Preserve source traceability and separate sourced facts from course policy.
- Never equate viewing, section completion, recognition questions, or coached practice
  with demonstrated mastery.
- Continue the active gate; do not work around missing human evidence by silently
  changing the definition of completion.
