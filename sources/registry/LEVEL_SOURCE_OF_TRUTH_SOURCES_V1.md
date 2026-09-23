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

## Newly verified remote sources

### Oxford Phrase List

Official PDF:
https://www.oxfordlearnersdictionaries.com/external/pdf/wordlists/oxford-phrase-list/Oxford%20Phrase%20List.pdf

Published scope: 750 common phrases, A1-C1. Oxford states that the list includes idioms,
phrasal verbs, compounds, collocations, prepositional phrases, and other common fixed phrases.
The official source is verified and readable, but a local raw snapshot is still pending because
the source host currently blocks direct binary acquisition from the execution environment.
Do not substitute an unofficial mirror as authority.

### Pearson GSE Vocabulary

Official framework/toolkit information:
https://www.pearson.com/languages/why-pearson/the-global-scale-of-english.html
https://www.pearson.com/languages/why-pearson/the-global-scale-of-english/resources.html

Published scope reaches GSE 10-90 / CEFR through C2. Pearson describes a searchable vocabulary
database with tens of thousands of vocabulary items plus collocations and phrases. This is the
planned lexical completion source where Oxford word/phrase lists stop at C1. A reproducible
structured C2 extract is still pending; until then C2 words and phrases remain explicitly open.

## Authority rule

Publisher/framework sources are evidence. The reviewed files under `curriculum/levels/` become
the course source of truth only after extraction, reconciliation, provenance validation, and
coverage review pass. Unofficial mirrors and scraped datasets may be used for research comparison
only; they cannot silently become curriculum authority.
