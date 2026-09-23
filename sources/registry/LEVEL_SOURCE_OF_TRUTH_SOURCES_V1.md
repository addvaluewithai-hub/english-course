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

## C2 lexical completion source: open

Oxford 3000/5000 and the Oxford Phrase List stop before C2. Pearson GSE Vocabulary is the
preferred completion candidate because the official Toolkit reaches C2 and supplies levelled word
meanings, functional phrases and collocations. Pearson documents a searchable vocabulary database
with tens of thousands of word meanings plus collocations and phrases.

- Framework: `https://www.pearson.com/languages/why-pearson/the-global-scale-of-english.html`
- Toolkit: `https://www.english.com/gse/teacher-toolkit/user/vocabulary`

A reproducible structured C2 extract has not yet been locked. The Toolkit supports result downloads,
but large downloads are limited, so C2 words and phrases stay explicitly blocked until acquisition
and licensing/provenance checks pass. CEFR-J/Octanove C1-C2 data may be evaluated as an open
cross-check, not silently substituted as authority.

## Authority rule

Publisher/framework sources are evidence. The reviewed files under `curriculum/levels/` become
the course source of truth only after extraction, reconciliation, provenance validation, and
coverage review pass. Unofficial mirrors and scraped datasets may be used for research comparison
only; they cannot silently become curriculum authority.
