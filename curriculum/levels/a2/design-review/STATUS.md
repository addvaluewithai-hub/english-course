# A2 Design Review Status

Status: **A2 CURRICULUM DESIGN COMPLETE — A1-PARITY FINAL AUDIT CLOSED**

This is the session-independent A2 handoff. A2 is complete at the same curriculum-design boundary used to close A1: the full level inventory has been turned into a locked unit/lesson architecture, every required source item has a role-appropriate lifecycle, every lesson slot has an authoring brief, the whole level has been critic-reviewed, and the reviewed state is reproducible by CI.

## Final A2 shape

- **12 units**
- **83 lesson slots**
- **26 capability families**
- **9 cross-cutting requirements**
- **30 lexical/content sets plus frozen intentional general remainder**

A1 remains locked and is used only as cumulative prerequisite/retrieval evidence. It was not silently edited.

## Source inventory — COMPLETE

- abilities: **269 / 269**
- phrases: **176 / 176**
- grammar: **291 / 291** across **46** reviewed systems/infrastructure families
- words: **871 / 871**
- pronunciation: **10 / 10**
- exact A2 source records: **1,617 / 1,617**

## Exact lifecycle coverage — COMPLETE

Stage-06 exact ledger result:

- source records scheduled: **1,617 / 1,617**
- orphans: **0**
- missing practice: **0**
- missing fresh retrieval: **0**
- missing recycle: **0**
- missing consolidation: **0**
- missing exit verification: **0**
- mechanical introduction overloads: **0**
- designated transfer/evidence lessons introducing new required records: **0**

Exact raw introduction load by lesson remains authoritative in `06-coverage-ledger/generated/coverage-report.md`. A2 additionally keeps role-aware active-load views after semantic reconciliation so raw source-row density is not mistaken for the number of teaching objects.

## Load and sequence — COMPLETE

The human load/sequence critic retained **12 units / 83 lesson slots** after exact source routing and dependency review.

Important performance distinctions remain explicit, including:

- phone call vs phone message vs repair;
- request vs permission vs opinion vs suggestion vs advice;
- location/directions vs travel information vs ticket/tourist exchange vs accommodation/reservation;
- invitation/arrangement vs intention vs scheduled event vs prediction/possibility;
- factual past/experience vs narrative background/sequence;
- practical procedure/safety vs survival-level health communication;
- personal correspondence vs factual-media reception/inference vs survey/interview work.

Authoritative record: `06.5-load-sequence-lock/load-sequence-lock.md`.

## Semantic / mastery lock — COMPLETE

Every exact source record has one explicit human-authored semantic/control role.

Final role counts:

- abilities: **133 productive / 46 interactive / 74 receptive / 16 support**
- phrases: **118 productive-formulaic / 28 receptive / 30 support**
- grammar rows: **184 productive / 9 receptive / 98 support** across **30 productive / 14 support / 2 receptive systems**
- words: **500 productive / 317 receptive / 54 support**
- pronunciation: **1 receptive / 9 integrated support**

Semantic orphans: **0**. Automation-inferred semantic roles: **0**.

Stage 08.5 manually reviewed the role-aware hotspot queue, retained the 83-slot architecture, and found no remaining reason to split/merge a lesson or reopen the semantic architecture.

Authoritative records:

- `08-semantic-lock/`
- `08.5-role-aware-critic/`

## Lesson-by-lesson curriculum contract — COMPLETE

Authoritative file: `09-lesson-briefs/lesson-briefs.md`

- units complete: **12 / 12**
- lesson briefs complete: **83 / 83**
- rolling unit critics complete: **12 / 12**
- whole-level critic complete: **1 / 1**
- structural changes required after all briefs: **0**
- semantic reopenings required after all briefs: **0**
- lesson splits/merges required: **0**
- designated transfer/evidence slots remain **zero-new semantic teaching**

Each brief defines the lesson's primary learner outcome, foreground productive/formulaic language, receptive/support input, learning shape, evidence/transfer task, and explicit boundaries against likely over-teaching.

## A1-parity final audit — CLOSED

A1 reference completion boundary was checked against A2 functionally, not by copying A1's numbers or legacy file layout.

A1 had:

- standard level source files;
- a manually locked curriculum map;
- exact source coverage/lifecycle mapping;
- one authoring brief for every lesson slot;
- critic review;
- semantic lock with human queue zero;
- authorized/reproducible manifest and exit contract.

A2 now satisfies all of those same completion obligations and adds the later-level safeguards required by the current playbook:

- explicit pronunciation / target-exit / A1 carry-forward review;
- dedicated load-sequence lock;
- formal post-design semantic reconciliation;
- mandatory role-aware Stage-08.5 critic;
- deterministic Stage-9 authorization pinned to reviewed evidence.

No A1 legacy candidate artifacts such as the old `curriculum-map/*-v0.json` files were copied into A2 because they are not part of the authoritative A1 completion method.

## Authorization state

Human declaration: `10-authorization-gate/authorization.json`

- `lesson_design_authorized = true`
- human review queue = **0**
- architecture = **12 units / 83 lesson slots**
- `manifest.json` status = `semantic_design_lock_reviewed_lesson_design_authorized`
- `exit_contract.json` status = `semantic_inventory_locked_v1`

The authorization is pinned to the reviewed coverage ledger, semantic decisions/ledger, Stage-08.5 decisions and completed lesson briefs. Evidence drift causes finalization to fail instead of silently keeping A2 authorized.

## CI / deterministic validation

The Stage-9 authorization decision already completed **4 / 4 SUCCESS**:

- Build level source of truth
- Audit level source of truth
- Audit A2 coverage ledger
- Audit A2 semantic lock

The build includes `tests.test_level_source_of_truth` and restores A2's reviewed authorization only after validating the pinned human decision. The final A1-parity close is required to preserve the same invariants.

## Definition of DONE for A2

For this curriculum workstream, A2 is now **DONE**.

That means we have finished deciding:

- how many units A2 has;
- how many lessons each unit contains;
- what each lesson is for;
- where all A2 words, phrases, grammar, abilities and pronunciation requirements live across the level;
- which items are productive, interactive, receptive or support;
- where practice, fresh retrieval, recycle, consolidation and exit evidence occur;
- and whether the complete 83-lesson architecture remains coherent after adversarial review.

Future work that writes or renders the actual learner-facing lesson is a different downstream workstream and is not part of declaring the A2 curriculum map complete.

## Next curriculum target

**B1** is the next level for this curriculum-design process. Start from the authoritative playbook and the locked A2 exit contract as the previous-level prerequisite. Do not copy A2's 12-unit / 83-lesson shape into B1; B1's architecture must emerge from B1 evidence.

## Boundaries

- Branch: `curriculum/level-source-of-truth-v1`
- `main` untouched.
- A1 remains locked.
- A2 curriculum-design state is **complete and locked**.
- A2 `lesson_design_authorized` is **true**.
- Separate downstream delivery/production gates remain unchanged.
