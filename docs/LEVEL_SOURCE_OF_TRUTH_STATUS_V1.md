# Level Source of Truth v1 — Coverage Status

Status date: 2026-09-23
Branch: `curriculum/level-source-of-truth-v1`

## Purpose

This branch defines the A1-C2 curriculum foundation before future lesson design. It is
independent of the existing first-ten lesson pilot and does not change `TEST-002`.

Each level owns:

- `words.json`
- `phrases.json`
- `grammar.json`
- `abilities.json`
- `pronunciation.json`
- `exit_contract.json`
- `sources.json`
- `manifest.json`

Level inventories contain items newly assigned at that level. Exit contracts are
cumulative through the level.

## Current level counts

| Level | Words / lexical meanings | Phrases / chunks | EGP grammar features | Required granular abilities | Pronunciation strands |
| --- | ---: | ---: | ---: | ---: | ---: |
| A1 | 900 | 199 | 109 | 119 | 10 |
| A2 | 871 | 176 | 291 | 269 | 10 |
| B1 | 809 | 175 | 338 | 249 | 10 |
| B2 | 1,427 | 125 | 243 | 270 | 10 |
| C1 | 1,315 | 75 | 129 | 59 | 10 |
| C2 | 609 | 41 | 112 | 19 | 10 |

The counts above are source-record counts, not a claim that every row is one independent
teaching objective. Grammar-family and communicative-function progression metadata remain
separate from exact feature/source-record counts.

## Coverage audit result

The strict audit `scripts/audit_level_source_of_truth_v3.py` passed in GitHub Actions run
`35884440343`.

Verified coverage:

- Oxford 3000/5000: 5,322 / 5,322 normalized word-entry records represented exactly once
  across A1-C1.
- Current official Oxford Phrase List: 750 / 750 records represented exactly once across
  A1-C1: A1 199, A2 176, B1 175, B2 125, C1 75.
- Pearson GSE Vocabulary C2 General Learner snapshot: 623 / 623 primary source records
  owned exactly once: 609 lexical-meaning items plus 14 direct phrase/phrasal-verb items;
  27 collocations are attached phrase/chunk evidence.
- English Grammar Profile: 1,222 / 1,222 features represented exactly once across A1-C2.
- Pearson GSE Grammar: 456 / 456 reviewed cross-check records represented exactly once
  across A1-C2; they are supporting evidence, not a second grammar target list.
- Reviewed grammar progression: 91 families with 528 explicitly reviewed A1-C2 lifecycle
  stages preserved. Missing early-level family stages are not invented.
- Communicative ability evidence: 2,274 reviewed CEFR/GSE assignments total; 106 Pre-A1
  records remain intentionally outside the six level folders; all 2,168 A1-C2 records
  have an explicit disposition.
- Required granular abilities: 985 total across A1-C2. The remaining A1-C2 records are
  supporting evidence or explicit duplicate/overlap dispositions rather than silently
  becoming extra requirements.
- Communicative function progression: 41 reviewed strands referenced by the granular
  ability layer.
- Pronunciation: 10 reviewed strands x 6 A1-C2 stages = 60 / 60 stages preserved.
- Exit profiles: 102 / 102 reviewed claims preserved, 17 per level.

## Ability disposition totals

| Level | Required | Supporting evidence | Duplicate / overlap disposition | Reviewed total |
| --- | ---: | ---: | ---: | ---: |
| A1 | 119 | 98 | 5 | 222 |
| A2 | 269 | 250 | 10 | 529 |
| B1 | 249 | 277 | 16 | 542 |
| B2 | 270 | 262 | 18 | 550 |
| C1 | 59 | 152 | 6 | 217 |
| C2 | 19 | 89 | 0 | 108 |
| **A1-C2** | **985** | **1,128** | **55** | **2,168** |

Pre-A1 adds 106 reviewed assignments outside these six folders, bringing the reviewed
communicative assignment source total to 2,274.

## Source decisions

### Words

- A1-B2 core: Oxford 3000 by CEFR.
- B2-C1 additions: Oxford 5000 additions by CEFR.
- C2: Pearson GSE Vocabulary General Learner, GSE 85-90 / CEFR C2.

### Phrases

- A1-C1: current official Oxford Phrase List online snapshot, 750 records.
- The legacy Oxford PDF is retained as historical evidence but is not canonical because
  its document styling does not reconcile cleanly to the current online partition.
- C2: Pearson direct `phrase` / `phrasal verb` records plus published collocations tied to
  their lexical owners. Multiword lexical items are not automatically reclassified as
  phrases.

### Grammar

- Canonical exact-feature inventory: English Grammar Profile.
- Cross-check evidence: Pearson GSE Grammar through the reviewed supercategory crosswalk.
- Progression grouping: 91 reviewed grammar families. GSE Grammar evidence does not create
  a second independent target inventory.

### Abilities

- Canonical granular evidence: reviewed CEFR + Pearson GSE communicative assignments.
- Required items are only records with disposition `include_for_spine`.
- `supporting_evidence` remains traceable evidence, not an additional required ability.
- `duplicate_or_overlap` remains explicit and is not silently discarded.
- The 17 reviewed level-exit claims remain the high-level cumulative exit contract and are
  not substituted for the granular ability inventory.

### Pronunciation

- Ten reviewed progression strands are kept as a supporting language-system layer.
- Pronunciation does not independently determine lesson count.

## Gates still open

This is a validated source foundation, not permission to mass-design lessons yet.

- Every manifest still has `lesson_design_authorized: false`.
- The inventories still carry `pending_inventory_review` / equivalent review states where
  semantic curriculum decisions remain to be locked.
- Pearson GSE-derived C2 lexical content carries the production gate
  `commercial_permission_required`. Internal architecture/research can proceed, but this
  branch does not claim commercial licensing clearance.
- Pre-A1 remains an onboarding/support band and is intentionally not one of the six level
  Source-of-Truth folders.
- Existing pilot lessons have not been reconciled against this new foundation yet.

## Next workstream

Before future lesson design:

1. run semantic review of each level inventory, starting with A1;
2. decide any documented exclusions/deferments without losing source provenance;
3. lock the reviewed level exit contract and receptive/productive expectations;
4. set `lesson_design_authorized` only after that level passes the semantic lock;
5. then map existing/new lessons to inventory ownership, recycling, consolidation, and
   exit verification.

No merge to `main` is implied by this status document.
