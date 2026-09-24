# Level Source of Truth v1 — Coverage and Design Status

Status date: 2026-09-24  
Branch: `curriculum/level-source-of-truth-v1`

## Purpose

This branch defines the A1-C2 curriculum foundation independently of the existing first-ten lesson pilot. It does **not** change `TEST-002`, `automation/STATE.json`, or the current pilot gate.

Level inventories contain items newly assigned at that level; exit contracts are cumulative through the level.

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

## Source coverage status

The strict source audit covers the full registered source baseline:

- Oxford 3000/5000: 5,322 / 5,322 normalized word-entry records across A1-C1.
- Current Oxford Phrase List: 750 / 750 records across A1-C1.
- Pearson GSE Vocabulary C2 General Learner: 623 / 623 primary records owned; 609 lexical items, 14 direct phrase/phrasal-verb items, plus 27 attached collocations.
- English Grammar Profile: 1,222 / 1,222 features across A1-C2.
- Pearson GSE Grammar: 456 / 456 reviewed cross-check records.
- Reviewed grammar progression: 91 families and 528 A1-C2 lifecycle stages.
- Communicative evidence: 2,274 reviewed CEFR/GSE assignments; 106 Pre-A1 records intentionally outside the six level folders and 2,168 A1-C2 assignments explicitly dispositioned.
- Required granular abilities: 985 total across A1-C2.
- Pronunciation: 10 strands x 6 levels = 60 stages.
- Exit profiles: 102 reviewed claims, 17 per level.

## A1 semantic lock — reviewed and locked

A1 semantic review is complete. The authoritative artifact is:

`curriculum/levels/a1/semantic-lock/semantic-lock-report.json`

Current state:

- status: `semantic_lock_reviewed_locked_v1`;
- primary items reviewed: **1,337**;
- human review queue: **0**;
- `lesson_design_authorized: true`;
- source items silently excluded: **0**.

Final A1 control roles:

| Category | Final reviewed obligation |
| --- | --- |
| Words — 900 | **627 productive**, **185 receptive**, **88 grammar-owned** |
| Phrases — 199 | **114 productive**, **40 formulaic productive**, **45 receptive** |
| Grammar — 109 | **92 productive control**, **3 formulaic productive control**, **12 embedded support**, **2 receptive control** |
| Abilities — 119 | **50 productive performance**, **46 receptive performance**, **23 interactive performance** |
| Pronunciation — 10 | **10 supporting intelligibility required** |

The former 276-word reference-pool review set is frozen by exact item-ID SHA-256:
`6e746736bfabcdb2f460423f3c2f95d6f43f23443c541fb5437b3a89e3eeb0d2`.
Its reviewed treatment is conservative: productive control is promoted only where the A1 performance architecture gives positive evidence; otherwise the published A1 item remains a receptive exit requirement. Productive control never implies all dictionary senses.

The 199 Oxford A1 phrases are also reviewed independently of exact-string matching: a phrase home does not automatically imply productive control. Grammar-owned words are not double-assessed as independent lexical targets.

## A1 design-review and lifecycle plan

The completed manual design-review remains the reviewed instructional plan built against the semantic inventory:

1. `01-abilities` — 119/119 required abilities reviewed.
2. `02-phrases` — 199/199 phrases reviewed.
3. `03-grammar` — 109/109 EGP A1 features reviewed.
4. `04-words` — 900/900 Oxford A1 word records reviewed.
5. `05-curriculum-map` — evidence-led **10-unit / 62-slot** A1 candidate structure.
6. `06-coverage-ledger` — exact lifecycle ledger for all **1,337** A1 primary items.
7. `07-lesson-briefs` — all **62/62** slots manually briefed and critic-reviewed.

The coverage ledger requires introduce/use, later fresh retrieval, recycling/consolidation, and exit verification rather than treating one appearance as mastery. Its latest reviewed structure has zero source orphans and zero hidden-new-content transfer violations after the manual fixes to past cohesion, weather/possibility, time/date placement, static-vs-movement language, and lexical load balancing.

## Authorization boundary

A1 curriculum **lesson design and controlled authoring planning are authorized** on this branch because the semantic queue is zero and the exit contract is locked.

This does **not** authorize mass delivery-content production. `curriculum/levels/a1/manifest.json` explicitly keeps:

`delivery_content_production_authorized: false`

The separate first-ten delivery workstream remains at `TEST-002`; real learner evidence, lesson-system and architecture gates continue to govern lesson-package/media production. This branch does not modify or bypass those gates.

A2-C2 remain `lesson_design_authorized: false` until each level receives its own semantic lock. Pearson GSE-derived C2 lexical content also retains `commercial_permission_required`.

## Deterministic rebuild protection

The A1 authorization is now part of the build/audit contract rather than a manual flag:

- the semantic-lock workflow rebuilds the conservative candidate, preserves the frozen word-review context, applies reviewed grammar/phrase/word decisions, then finalizes A1 manifest and exit contract;
- the full level-inventory workflow runs A1 semantic finalization after base inventory, grammar and granular-ability generation so a rebuild cannot silently reset A1 to pending;
- the strict v4 audit requires A1 semantic lock status, queue zero, manifest/exit-contract authorization consistency, delivery production still false, and A2-C2 still locked.

Pre-A1 remains an onboarding/support band rather than a seventh Source-of-Truth level folder. No merge to `main` is implied by this status document.
