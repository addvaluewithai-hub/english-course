# Level Source of Truth v1 — Coverage and Design Status

Status date: 2026-09-24  
Branch: `curriculum/level-source-of-truth-v1`

## Purpose

This branch defines the A1-C2 curriculum foundation independently of the existing first-ten lesson pilot. It does **not** change `TEST-002`, `automation/STATE.json`, or the current pilot gate.

Each level owns:

- `words.json`
- `phrases.json`
- `grammar.json`
- `abilities.json`
- `pronunciation.json`
- `exit_contract.json`
- `sources.json`
- `manifest.json`

Level inventories contain items newly assigned at that level. Exit contracts are cumulative through the level.

## Current level counts

| Level | Words / lexical meanings | Phrases / chunks | EGP grammar features | Required granular abilities | Pronunciation strands |
| --- | ---: | ---: | ---: | ---: | ---: |
| A1 | 900 | 199 | 109 | 119 | 10 |
| A2 | 871 | 176 | 291 | 269 | 10 |
| B1 | 809 | 175 | 338 | 249 | 10 |
| B2 | 1,427 | 125 | 243 | 270 | 10 |
| C1 | 1,315 | 75 | 129 | 59 | 10 |
| C2 | 609 | 41 | 112 | 19 | 10 |

These are source-record counts, not a claim that every row is one independent teaching objective.

## Source coverage audit

The strict source audit has passed and continues to pass in CI.

Verified coverage includes:

- Oxford 3000/5000: 5,322 / 5,322 normalized word-entry records represented across A1-C1.
- Current official Oxford Phrase List: 750 / 750 records represented across A1-C1: A1 199, A2 176, B1 175, B2 125, C1 75.
- Pearson GSE Vocabulary C2 General Learner snapshot: 623 / 623 source records owned: 609 lexical-meaning items plus 14 direct phrase/phrasal-verb items; 27 collocations remain attached evidence.
- English Grammar Profile: 1,222 / 1,222 features represented across A1-C2.
- Pearson GSE Grammar: 456 / 456 reviewed cross-check records represented; supporting evidence, not a second canonical grammar target inventory.
- Reviewed grammar progression: 91 families with 528 explicitly reviewed A1-C2 lifecycle stages.
- Communicative ability evidence: 2,274 reviewed CEFR/GSE assignments total; 106 Pre-A1 records intentionally outside the six level folders; all 2,168 A1-C2 assignments have a disposition.
- Required granular abilities: 985 total across A1-C2.
- Pronunciation: 10 reviewed strands x 6 A1-C2 stages = 60 / 60 stages.
- Exit profiles: 102 / 102 reviewed claims, 17 per level.

## A1 manual design-review status

A1 now has a substantial **reviewed design candidate** built from the source inventories. This work is useful evidence for semantic-lock reconciliation, but it does not override the formal semantic gate.

Completed A1 design-review stages:

1. `01-abilities` — 119/119 required abilities manually read and consolidated into a reviewed capability architecture.
2. `02-phrases` — 199/199 Oxford A1 phrases manually reviewed with explicit semantic homes and boundaries.
3. `03-grammar` — 109/109 canonical A1 EGP features manually reviewed, with GSE Grammar used only as supporting cross-check evidence.
4. `04-words` — 900/900 Oxford A1 word records manually reviewed into required lexical/content homes with explicit system boundaries.
5. `05-curriculum-map` — evidence-led 10-unit / 62-slot candidate skeleton.
6. `06-coverage-ledger` — exact 1,337-record lifecycle ledger covering 119 abilities + 199 phrases + 109 grammar + 900 words + 10 pronunciation strands.
7. `07-lesson-briefs` — all 62 slots manually briefed and critic-reviewed as an instructional design candidate.

The latest A1 coverage-ledger audit passes with:

- source records expanded: **1,337 / 1,337**;
- orphan records: **0**;
- records without later fresh retrieval: **0**;
- records without exit verification: **0**;
- introduction-load threshold violations: **0**.

Manual Stage-07 corrections included static-vs-movement language, time/date placement, large-number context, cohesion-grammar placement, weather/possibility placement, and lexical load rebalancing. Transfer slots U7-L05 and U8-L06 now introduce zero new source records.

## Formal A1 semantic-lock gate — still open

The formal artifact `curriculum/levels/a1/semantic-lock/semantic-lock-report.json` still has status `semantic_lock_candidate_pending_review`.

Its current unresolved item-level control queue is **487**:

- grammar: **30**;
- phrases: **181**;
- words: **276**.

The manual design-review work above gives much stronger evidence than existed when that candidate was generated, but it has **not yet been reconciled back into the semantic-lock artifact at item level**. In particular, a semantic teaching home is not automatically the same thing as a final productive/receptive control decision.

Therefore:

- `curriculum/levels/a1/manifest.json` correctly remains `lesson_design_authorized: false`;
- Stage 07 is complete **as a reviewed design candidate**, not as production authorization;
- lesson/script mass production is not unlocked by Stage 07;
- the existing first-ten pilot and `TEST-002` remain untouched and continue under their own project gate.

## A1 next workstream

Reconcile the completed manual reviews back into the semantic-lock candidate, category by category:

1. **Grammar first (30):** use the 109/109 manual grammar review to resolve productive, receptive/formulaic, embedded-support, or bounded-system treatment without inventing control beyond canonical EGP evidence.
2. **Phrases next (181):** use the 199/199 phrase review and capability homes to decide required productive vs receptive/formulaic control; do not infer productive mastery merely from a phrase having a lesson home.
3. **Words last (276):** use the 900/900 word review and lexical/content homes to resolve minimum exit control and bounded sense/function. Preserve receptive-only/basic/fixed treatment where broader productive control is not justified.
4. Regenerate the semantic-lock report; require the human-review queue to reach zero with no silent exclusion.
5. Only then change `lesson_design_authorized` and treat the 62-slot design as authorized for controlled lesson production.

## Other gates

- Pearson GSE-derived C2 lexical content still carries `commercial_permission_required`; internal architecture/research may proceed, but this branch does not claim commercial licensing clearance.
- Pre-A1 remains an onboarding/support band rather than a seventh Source-of-Truth level folder.
- No merge to `main` is implied by this status document.
