# All-Level Source Coverage Audit v1

Date: 2026-08-10

## Result

The authoritative cross-level source pack is now normalized into deterministic,
validation-clean derived datasets. This closes source normalization, not curriculum
review: every new record remains unreviewed with its curriculum disposition undecided.

## Inventory

| Source | Published range used here | Raw and text present | Structured status |
| --- | --- | --- | --- |
| CEFR Companion Volume 2020 EN | Pre-A1-C2 and plus descriptors | Yes | 1,224 descriptor rows normalized |
| CEFR Companion Volume 2020 AR | Terminology support | Yes | No descriptor mapping; English remains authority |
| Pearson GSE Adult Objectives 2022 | GSE 10-90 / Below A1-C2 | Yes | 1,050 objective rows normalized |
| English Grammar Profile export | A1-C2 | Yes | All 1,222 rows with spreadsheet provenance |
| Pearson GSE Grammar Guide | A1-C1 with plus bands | Yes | 456 productive grammar rows normalized |
| Oxford 3000 | A1-B2 | Yes | 3,307 printed entry lines normalized |
| Oxford 5000 additions | B2-C1 | Yes | 2,015 printed entry lines normalized |

## Normalized dataset counts

| Dataset | Level counts |
| --- | --- |
| GSE objectives | Below A1 59; A1 121; A2 132; A2+ 137; B1 121; B1+ 130; B2 155; B2+ 117; C1 59; C2 19 |
| CEFR descriptors | Pre-A1 47; A1 101; A2 257; A2+ 3; B1 287; B1+ 4; B2 267; B2+ 11; C1 158; C2 89 |
| GSE Grammar | A1 43; A2 50; A2+ 67; B1 133; B1+ 96; B2 46; B2+ 18; C1 3 |
| Oxford 3000 entry lines | A1 900; A2 871; B1 809; B2 727 |
| Oxford 5000 entry lines | B2 700; C1 1,315 |

The Oxford 3000 output contains exactly 3,000 distinct printed headword labels across
3,307 headword-and-part-of-speech lines. The Oxford 5000 additions contain 1,999
distinct printed headword labels across 2,015 lines. Counts describe the PDF layout;
they are not vocabulary targets or lesson counts.

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

## Parse decisions and source exceptions

- All 98 descriptors in the earlier A1 CEFR scope are preserved. Three additional A1
  descriptors come from plurilingual/pluricultural scales omitted from that scope.
- Exact repeated CEFR and GSE wording is retained with warnings rather than silently
  deleted.
- The GSE Grammar guide prints `B2+ (59-66)` although its B2+ rows score 67-75. Both
  facts are preserved and the conflict is flagged on every affected record.
- Oxford extraction uses visual PDF lines, repairing text-mirror breaks such as
  `rifle`, `sanction`, and `settlement` without guessing word content.
- EGP rows now include exact spreadsheet row and raw level text. Three source cells
  with trailing spaces remain documented in the normalization audit.

## Gaps that must remain explicit

- All new records are source evidence with `undecided` inclusion status; lifecycle
  disposition and teaching ownership have not been reviewed.
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

- review source dispositions and the proposed exit profiles;
- build ability, grammar, vocabulary, pronunciation, discourse, and complexity strands;
- continue limited gold-lesson delivery testing.

Not ready yet:

- claim exact A2-C2 lesson maps;
- claim reviewed global grammar or vocabulary ownership;
- mass-produce the remaining A1 lessons;
- use the source lists as a one-item-per-lesson checklist.
