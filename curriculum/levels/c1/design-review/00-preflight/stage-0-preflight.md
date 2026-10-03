# C1 Stage 0 — Preflight and Invariants

Status: **PREFLIGHT CANDIDATE PASS — CI CONFIRMATION PENDING**  
Date: 2026-10-03  
Branch: `curriculum/c1-stage-0-1`

## Purpose

Confirm that C1 curriculum design can begin from the canonical source inventory without reopening locked B2, inventing curriculum structure, or weakening source/licensing boundaries.

## Inputs reviewed

- `AGENTS.md`
- `START_HERE.md`
- `CURRENT_STATE.md`
- `docs/LEVEL_CURRICULUM_DESIGN_PLAYBOOK_V1.md`
- `curriculum/levels/c1/manifest.json`
- `curriculum/levels/c1/exit_contract.json`
- `curriculum/levels/c1/sources.json`
- C1 `words.json`, `phrases.json`, `grammar.json`, `abilities.json`, `pronunciation.json`
- locked B2 `manifest.json` and `exit_contract.json`

## Standard-file existence

The C1 level directory contains all eight standard source-of-truth files:

1. `manifest.json`
2. `words.json`
3. `phrases.json`
4. `grammar.json`
5. `abilities.json`
6. `pronunciation.json`
7. `exit_contract.json`
8. `sources.json`

Existing design-review directories for abilities, phrases, grammar, and words are workspace only; they do not constitute reviewed curriculum decisions.

## Canonical inventory snapshot

| Category | Manifest count | Current source status |
| --- | ---: | --- |
| Words | 1,315 | `extracted_pending_inventory_review` |
| Phrases | 75 | `extracted_from_current_official_oxford_pending_inventory_review` |
| Grammar | 129 | `canonical_egp_with_reviewed_gse_crosscheck_pending_inventory_lock` |
| Required abilities | 59 | `reviewed_granular_source_assignments_v1` |
| Pronunciation | 10 | `reviewed_progression_v1` |
| **Total primary records** | **1,588** | planning total only; not teaching-object count |

Ability evidence additionally records 152 supporting items, 6 excluded duplicate/overlap items, and 217 reviewed C1 source records in total. Supporting/excluded evidence does not inflate the 59-item primary ability inventory.

## Target gate state

- C1 manifest status: `generated_pending_inventory_review`.
- `lesson_design_authorized:false`.
- `blocking_categories:[]`.
- `production_gates:[]`.
- C1 exit contract status: `draft_pending_full_inventory_lock`.
- C1 inventory semantics remain `new_at_level`; exit obligation is cumulative through C1.
- No C1 unit count or lesson count is authorized or inferred at Stage 0.

## Source and licensing check

C1 sources remain the existing verified source architecture:

- CEFR Companion Volume 2020 — abilities / exit / pronunciation boundary;
- Pearson GSE Adult General English 2022 — abilities / exit boundary;
- English Grammar Profile — canonical grammar;
- GSE Grammar — grammar cross-check;
- Oxford 5000 additions — words;
- Oxford Phrase List snapshot — phrases.

The source registry reports verified local acquisition/structured extraction states. The C1 word and phrase inventories have no active license gate. The special Pearson commercial-permission gate documented for C2 is not a C1 gate and is not imported into C1.

## Locked B2 prerequisite

B2 is the immediately previous level and is treated as immutable prerequisite state:

- manifest status: `semantic_design_lock_reviewed_lesson_design_authorized`;
- `lesson_design_authorized:true`;
- semantic human-review queue: 0;
- locked architecture: 13 units / 95 lesson slots;
- exact primary inventory: 2,075 records;
- exit contract status: `semantic_inventory_locked_v1`;
- completion is not mastery and later fresh evidence remains required;
- delivery/media production remains separately unauthorized.

C1 work may deliberately retrieve B2 abilities/language, but must not relabel B2 records as new C1 content or silently edit locked B2 artifacts.

## C1 exit constraints visible before architecture

The current C1 exit contract requires later curriculum evidence for at least:

1. synthesis of demanding input;
2. a complex position across multiple domains;
3. audience/register adaptation without rehearsed wording;
4. extended/implicit complex reception;
5. complex speaking with integrated sub-themes and developed points;
6. well-structured complex writing appropriate to the reader;
7. precise, flexible oral interaction and register adaptation;
8. complex written/online interaction;
9. mediation across long complex sources and multiple perspectives;
10. broad complex range, consistently high grammatical accuracy, idiomatic lexical command, intelligibility, discourse control, and high fluency.

These are constraints on later architecture and assessment. They do **not** determine a Stage-0 unit/lesson count.

## Stage-0 critic

- Source totals: **candidate PASS**, subject to strict CI audit on this branch/PR.
- Eight standard files: **PASS**.
- Target/previous-level boundary: **PASS**; no B2 change made.
- Licensing/production gates preserved: **PASS**.
- Existing/legacy lesson count treated as authoritative: **NO**.
- Unit or lesson count assumed: **NO**.
- Coverage treated as mastery: **NO**.
- Delivery/media production authorized: **NO**.

## Decision

C1 curriculum research/design review may proceed to Stage 1 while `lesson_design_authorized` remains false. Stage 0 is not a semantic lock or authoring authorization. Strict source-of-truth CI must confirm the candidate preflight after the branch is opened as a PR.
