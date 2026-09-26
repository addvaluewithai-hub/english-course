# A2 Stage 08.5 — Role-Aware Lifecycle / Load Critic

Status: **HUMAN CRITIC COMPLETE — ROLE-AWARE RECONCILIATION LOCKED**  
Level: **A2**  
Architecture retained: **12 units / 83 lesson slots**

This stage reconciles the Stage-08 mastery roles with the exact Stage-06 lifecycle and lesson scheduling. It does **not** create lesson briefs, authorize delivery production, or use a numeric lesson-load target as a curriculum objective.

## Critic principles

1. Raw source-row count is not the number of teaching objects.
2. Semantic demotion is allowed only when independent A2 production is not required by the reviewed task contract.
3. A productive item may move to a later or more natural first-introduction lesson without changing its mastery role.
4. Receptive/contextual and integrated-support records remain taught/retrieved evidence; they are not deleted.
5. Grammar rows remain inside their reviewed Stage-03 system identity.
6. Automation may resolve review rows to exact source IDs, apply explicit human decisions, count and validate only.

## Final semantic result after critic

All **1,617 / 1,617** required A2 source records retain exactly one explicit human-authored semantic role.

### Words — 871

- productive/contextual: **500**
- integrated support: **54**
- receptive/contextual: **317**

The first Stage-08 pass intentionally over-included productive vocabulary at 591 words. Stage 08.5 demoted **91 exact reviewed word rows** after role-aware lesson review showed that they were optional topic breadth, meta-language, low-necessity synonyms, or primarily receptive factual content in this A2 architecture.

The exact final row overrides are authoritative in `overrides.json`; automation is not allowed to infer additional demotions or promotions.

Representative demotion reasons include:

- optional hobby/content breadth that is useful in input but not universally required for learner output;
- optional clothing/object/detail labels where a smaller productive repertoire already supports the capability;
- course/meta-language such as labels for communication processes that the learner need not independently produce;
- abstract/general nouns whose principal role is carrying factual input rather than enabling a required A2 performance;
- overlapping evaluative/personality breadth where core productive alternatives already satisfy the mapped task.

### Phrases — 176

- productive/formulaic: **118**
- receptive/contextual: **28**
- integrated discourse/writing support: **30**

### Grammar — 46 reviewed systems / 291 source rows

- productive bounded systems: **30**
- integrated-support systems: **14**
- receptive bounded systems: **2**

Expanded source-row roles after system ownership:

- productive grammar rows: **184**
- integrated-support rows: **98**
- receptive rows: **9**

### Abilities — 269

- productive: **133**
- interactive: **46**
- receptive: **74**
- integrated support: **16**

### Pronunciation — 10

- receptive sound-perception requirement: **1**
- distributed integrated-support/intelligibility requirements: **9**

## Applied scheduling decisions

### U1-L03 — background questions

The lesson keeps reliable core question formation needed to ask about another person's background, while expanded question functions are introduced later in contexts that actually need them.

Examples of explicit moves:

- negative/pragmatic question rows → `U4-L06`;
- indirect and alternative questions → `U11-L06` survey/interview work;
- negative-question suggestion use → `U7-L01` invitation/arrangement work;
- modal yes/no questions → `U4-L02` permission/obligation/action language.

Final active-load aid: approximately **13 teaching objects**, with **2 productive grammar systems**, 1 active phrase and 8 active words.

### U4-L04 — suggestions

The original role-aware pass exposed a real mixed-load problem. Opinion/evaluation chunks, broad vocabulary and grammar functions were redistributed to their natural lessons.

The final lesson is deliberately narrow:

- capability: making/responding to suggestions;
- productive grammar systems: **2**;
- active phrases: `if you want to`, `Why not…?`;
- active word: `suggest`.

Final active-load aid: approximately **6 teaching objects**.

### Other exact moves

The critic also moved productive language to the task that requires it, including invitation language, requests/offers, opinion/evaluation, advice/problem solving, future arrangements/predictions, correspondence, comparison/product choice, social-contact language, safety language and process/equipment language.

The exact row-level scheduling decisions are persisted in `overrides.json`.

## Final hotspot review

After the final Stage-08.5 pass, the remaining highest approximate teaching-object loads are not accidental mixed systems:

- `U2-L02` — approx **19**: people/personality description within one coherent descriptive field plus one grammar system;
- `U3-L03` — approx **19**: comparison/physical-property language with two related comparison systems;
- `U10-L01` — approx **19**: practical rules/instructions/conditions in one procedural performance;
- `U6-L03` — approx **18**: route/direction production with spatial language and two related systems;
- `U10-L02` — approx **18**: process/instruction language in one procedural outcome;
- `U4-L03` — approx **17**: opinion/evaluation with reason framing;
- `U2-L03` — approx **16**: routine/activity description;
- `U3-L02` — approx **19**: home/object material/ownership description.

These lessons were reviewed as **coherent performance systems**, not accepted merely because they are below a threshold. No remaining hotspot provides evidence for a new lesson split.

Important contrast: raw-row-heavy `U11-L04` now contains approximately **10 active teaching objects** and no new active grammar/ability system, confirming that its earlier raw count was primarily receptive/support density rather than active teaching overload.

## Architecture decision

**Retain 12 units / 83 lesson slots.**

No lesson is added, removed, merged or split in Stage 08.5. The identified problems were solved through semantic correction and natural first-introduction placement rather than by protecting or chasing a lesson-count target.

## Lock conditions — satisfied

- exact semantic roles: **1,617 / 1,617**;
- semantic orphans: **0**;
- automation-inferred semantic roles: **0**;
- Stage-06 exact lifecycle remains complete;
- mechanical coverage overloads remain **0**;
- designated transfer/evidence lessons remain zero-new;
- role-aware hotspot queue manually reviewed;
- remaining high-load lessons explicitly justified by one coherent communicative/system outcome.

## Validation

The human Stage-08.5 commit `1dbcbf636a8db9d659b4705592bbb6abeb5e2c0b` completed with **4 / 4 GitHub checks successful**, including the A2 semantic audit and repository build/audit checks.

Generated evidence:

- `../08-semantic-lock/generated/semantic-role-ledger.json`
- `../08-semantic-lock/generated/semantic-role-report.md`
- `../08-semantic-lock/generated/lesson-semantic-attribution.md`
- `../08-semantic-lock/generated/active-load-aid.md`

## Verdict

**Stage 08 + Stage 08.5 are closed. Milestone 3 may close.**

This authorizes the next curriculum-design milestone only. It does **not** authorize lesson/script/media production and does not change the A2 manifest production gate.