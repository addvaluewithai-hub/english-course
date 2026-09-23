# Level Source of Truth source matrix v1

This file records the evidence sources used by the independent A1-C2 inventory workstream.
Existing pilot lessons are not modified by this source matrix.

## Local verified sources already in the repository

- CEFR Companion Volume 2020 (English): abilities, level boundaries, pronunciation/intelligibility evidence.
- Pearson GSE Adult General English Objectives 2022: granular abilities and level progression.
- English Grammar Profile Online export: canonical grammar evidence across A1-C2.
- Pearson GSE Grammar Guide: grammar cross-check.
- Oxford 3000 by CEFR level: word inventory evidence for A1-B2.
- Oxford 5000 additions by CEFR level: additional word inventory evidence for B2-C1.

## Oxford Phrase List: canonical A1-C1 phrase evidence

Canonical source for this workstream: the current official Oxford Phrase List web page.

- URL: `https://www.oxfordlearnersdictionaries.com/wordlists/oxford-phrase-list`
- Raw snapshot: `sources/raw/vocabulary/oxford-phrase-list-online.html`
- Structured extraction: `data/derived/oxford-phrase-list-online.json`
- Snapshot SHA-256: `20C59670CDA661B48B8B88205A19C77FAD5ACCB252D164DAAE939DAF4BE893C1`
- Extracted rows: 750
- Level counts: A1 199; A2 176; B1 175; B2 125; C1 75.

The official legacy PDF is retained at `sources/raw/vocabulary/oxford-phrase-list.pdf`
with SHA-256 `35DA430C8C0353D4A44C6293CA0D05AE00787488562BEAED1FF2835C6E37E118`.
It is evidence/history, not the canonical structured phrase input: its document styling produces
a different main-entry partition from the current online list. No rows are silently deleted to
force the legacy PDF to match the current source.

## Pearson GSE Vocabulary: C2 lexical completion evidence

Oxford 3000/5000 and the Oxford Phrase List stop before C2. The C2 lexical layer therefore uses
the official Pearson GSE Teacher Toolkit General Learner vocabulary search for GSE 85-90 / C2.

- Toolkit: `https://www.english.com/gse/teacher-toolkit/user/vocabulary`
- API endpoint used by the Toolkit: `https://www.english.com/gse/teacher-toolkit/user/api/v1/vocabulary/search`
- Structured snapshot: `data/derived/gse-vocabulary-c2-gl.json`
- Audit: `data/derived/gse-vocabulary-c2-gl-audit.json`
- Query: audience `GL`, GSE `85-90`, wildcard vocabulary search.
- Records: 623 unique source records.
- Normalized records SHA-256: `65DF05986C56F4AF17D058DF73C6D8AF1C12AD21BD767E0888A38425AFEBC1B7`.

The curriculum partition is deliberately conservative:

- 609 records remain lexical word/meaning items because Pearson does not classify them as
  `phrase` or `phrasal verb`, even when the expression itself contains spaces.
- 14 records explicitly classified by Pearson as `phrase` or `phrasal verb` become direct phrase
  inventory items with their own GSE scores.
- 27 published collocation rows become phrase/chunk items linked to their lexical owner. Their C2
  placement is inherited from the owner record and is not represented as an independent GSE score.
- Multiword variants remain attached to their lexical owner and are not silently promoted into
  separate required phrase items.

Pearson usage is also a production gate: internal curriculum research and architecture may use the
verified snapshot, but commercial/product use of GSE components requires the applicable Pearson
permission/license. `lesson_design_authorized` remains false while the inventory review is open.

## Authority rule

Publisher/framework sources are evidence. The reviewed files under `curriculum/levels/` become
the course source of truth only after extraction, reconciliation, provenance validation, and
coverage review pass. Unofficial mirrors and scraped datasets may be used for research comparison
only; they cannot silently become curriculum authority.
