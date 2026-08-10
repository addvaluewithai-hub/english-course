# All-Level Source Coverage Audit v0

Date: 2026-08-10

## Result

The private repository contains the authoritative raw material needed to propose an
A1-C2 vertical curriculum. It does not yet contain normalized and reviewed all-level
communicative, grammar, vocabulary, or pronunciation mappings.

## Inventory

| Source | Published range used here | Raw and text present | Structured status |
| --- | --- | --- | --- |
| CEFR Companion Volume 2020 EN | Pre-A1-C2 | Yes | Reviewed A1 subset only |
| CEFR Companion Volume 2020 AR | Terminology support | Yes | No descriptor mapping; English remains authority |
| Pearson GSE Adult Objectives 2022 | GSE 10-90 / Below A1-C2 | Yes | Reviewed A1 subset only |
| English Grammar Profile export | A1-C2 | Yes | All 1,222 rows derived; reviewed use remains A1-only |
| Pearson GSE Grammar Guide | A1-C1 with plus bands | Yes | Searchable text only |
| Oxford 3000 | A1-B2 | Yes | Searchable text only |
| Oxford 5000 additions | B2-C1 | Yes | Searchable text only |

## English Grammar Profile counts

| Level | Feature rows |
| --- | ---: |
| A1 | 109 |
| A2 | 291 |
| B1 | 338 |
| B2 | 243 |
| C1 | 129 |
| C2 | 112 |
| Total | 1,222 |

The all-level derived snapshot is `data/derived/egp-all-levels.json`. These counts show
source inventory, not the number of grammar lessons or mandatory productive targets.

## Reliable level anchors

- CEFR page 175 gives the global A1-C2 scale.
- CEFR pages 177-181 compare reception, production, interaction, online interaction,
  and mediation across all six levels.
- CEFR pages 131-142 define linguistic and pragmatic range, grammatical accuracy,
  vocabulary, phonology, orthography, cohesion, precision, and fluency.
- GSE pages 7-8 map GSE bands to CEFR global levels: A1 22-29, A2 30-42, B1 43-58,
  B2 59-75, C1 76-84, and C2 85-90.

## Gaps that must remain explicit

- CEFR and GSE communicative records above A1 are not normalized into source-record
  JSON, so record-level coverage cannot yet be claimed.
- EGP features are extracted at all levels but have no reviewed lifecycle disposition.
- Oxford files are lexical pools, not a syllabus, and the current text mirrors contain
  layout-related line breaks that require PDF-aware normalization.
- Oxford provides no C2-specific levelled list; C2 lexical selection needs an explicit
  corpus/domain method.
- CEFR gives pronunciation level boundaries but not an English-specific sound and
  prosody teaching sequence for Arabic-speaking adults.
- Arabic-speaker error predictions in current A1 work are hypotheses, not conclusions
  supplied by CEFR, GSE, EGP, or Oxford.
- No all-level source proves final units, lesson counts, lesson order, or lifecycle
  ownership. Those remain reviewed product decisions.

## Readiness judgment

Ready now:

- approve the supported levels and lifecycle contract;
- review the proposed exit profiles;
- begin all-level deterministic extraction and disposition work;
- continue limited gold-lesson delivery testing.

Not ready yet:

- claim exact A2-C2 lesson maps;
- claim complete global grammar or vocabulary coverage;
- mass-produce the remaining A1 lessons;
- use the source lists as a one-item-per-lesson checklist.
