# Pearson GSE A1 Objective Extraction Audit

## Scope and authority

- Dataset: `data/reviewed/gse-a1-objectives.json`
- Raw authority: `sources/raw/frameworks/gse-learning-objectives-adult-general-english-2022.pdf`
- Source version: September 2022
- Source SHA-256: `CE5713618E4583F416C02276F7EC7FEBA7EBDD2CA4E55EC2BB0FAFC29DD8604D`
- Included band: the source-labelled `GSE 22–29/A1` tables only
- Review identity and time: `cur_002_primary`, `2026-07-15T22:52:59+03:00`

## Counts

| Skill | PDF pages | Evidence rows | Canonical included objectives |
| --- | ---: | ---: | ---: |
| Reading | 9 | 14 | 14 |
| Listening | 14–15 | 34 | 33 |
| Speaking | 22–24 | 54 | 54 |
| Writing | 37 | 19 | 19 |
| **Total** | 7 pages | **121** | **120** |

Score counts by skill:

- Reading — 22: 1; 23: 1; 25: 1; 26: 1; 27: 3; 28: 3; 29: 4.
- Listening — 22: 1; 23: 6; 24: 4; 25: 4; 26: 7; 27: 5; 28: 4; 29: 3.
- Speaking — 22: 6; 23: 3; 24: 7; 25: 4; 26: 9; 27: 7; 28: 11; 29: 7.
- Writing — 23: 1; 24: 3; 25: 1; 26: 2; 27: 4; 28: 5; 29: 3.

All 121 evidence rows are accepted source transcriptions. Of these, 120 are included in
the canonical A1 objective count and one is a reviewed duplicate exclusion.

## Duplicate reconciliation

Pearson prints the exact Listening objective “Can identify a caller’s name and phone
number from a short, simple telephone conversation. (P)” twice:

- `gse.adult.2022.p14.005` at GSE 23 is the first occurrence and is included;
- `gse.adult.2022.p15.002` at GSE 26 is retained as accepted evidence but excluded from
  the canonical objective count as a duplicate.

Both records carry a `source_duplicate` warning and cross-location ambiguity text. The
choice of the first occurrence is a deterministic deduplication rule, not a claim that
Pearson intended GSE 23 rather than GSE 26.

## Review performed

- Rendered and visually checked PDF pages 9, 14, 15, 22, 23, 24, and 37 against every
  extracted A1 table; page 38 was checked to confirm the Writing A2 boundary.
- Confirmed all records begin with source wording, retain the printed origin code, cite
  one exact PDF page, and carry a GSE value from 22 through 29.
- Confirmed page/skill coverage, score inheritance within table groups, unique project
  record IDs, source-text hashes, and the single exact duplicate group.
- Twenty-four records carry explicit transcription notes for joined PDF line wraps or
  removal of extraction-only spacing before punctuation after closing quotation marks.
- `CUR-004` subsequently applied the controlled skill, mode, and function tags documented
  in `docs/CURRICULUM_TAG_TAXONOMY.md`. `CUR-005` subsequently applied the candidate
  clusters documented in `docs/CANDIDATE_UNIT_MAP.md`. Source facts and the A1 inclusion
  decisions from this extraction are unchanged.

## Validation result

- Both derived and reviewed JSON collections pass the source-record validator.
- All three JSON Schemas pass Draft 2020-12 checking.
- Eleven extraction and source-record validator tests pass.
- Python byte-compilation passes for all new extraction modules and tests.
