# B2 Stage 0 — Preflight and Invariants

Status: **PASS**
Reviewed against `main` at commit `13a2f3eab0268ffcca5268779311f2363027a7cc` and recorded on branch `curriculum/b2-stage-0-1`.

## Standard files

All eight required level files are present:

- `manifest.json`
- `words.json`
- `phrases.json`
- `grammar.json`
- `abilities.json`
- `pronunciation.json`
- `exit_contract.json`
- `sources.json`

## Inventory reconciliation

B2 manifest counts:

- words: 1,427
- phrases: 125
- grammar: 243
- abilities: 270
- pronunciation: 10

Total primary candidate records: 2,075.

The canonical `CURRENT_STATE.md` reports the same B2 counts and status `generated_pending_inventory_review`.

## Integrity validation

The latest Curriculum integrity workflow for canonical `main` at commit `13a2f3eab0268ffcca5268779311f2363027a7cc` completed successfully on 2026-09-29.

Both required validation steps passed:

1. `python scripts/audit_level_source_of_truth_v4.py`
2. `python -m unittest tests.test_level_source_of_truth`

This satisfies the Stage-0 strict source-of-truth integrity check for the current canonical snapshot.

## Exit and prerequisite state

B2:

- `lesson_design_authorized: false`
- exit-contract status: `draft_pending_full_inventory_lock`
- inventory semantics: new-at-level with cumulative exit obligation
- no B2 production gates are currently declared

B1 prerequisite:

- status: `semantic_design_lock_reviewed_lesson_design_authorized`
- `lesson_design_authorized: true`
- semantic human-review queue: 0
- architecture: 12 units / 85 lesson slots

B1 is therefore treated as an immutable prerequisite unless explicitly reopened by the owner.

## Source and licensing check

B2 source roles are assigned and all listed source snapshots are recorded as locally verified. The level currently declares no production gates. No source/licensing blocker is present for curriculum research/design review.

## Stage-0 invariants

- No unit count assumed.
- No lesson count assumed.
- No semantic/productive-control roles inferred from raw source rows.
- No locked lower-level content changed.
- No target-level content mixed with another level except future explicit carry-forward/retrieval work.
- Delivery/media production is not authorized by this preflight.

## Decision

**Stage 0 passes.**

Proceed to Stage 1: manual review of all 270 required B2 abilities into capability architecture and cross-cutting requirements, preserving exact source traceability and modality/performance boundaries.
