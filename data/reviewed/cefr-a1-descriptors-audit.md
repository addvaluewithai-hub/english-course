# CEFR A1 Descriptor Extraction Audit

## Scope and authority

- Task: `CUR-003`.
- Authority: Council of Europe, *CEFR Companion Volume* (2020), English edition.
- Raw file: `sources/raw/frameworks/cefr-companion-2020-en.pdf`.
- Verified SHA-256: `BFBD8C74090419AC4B9B352D6BA26E180713B31F45265D7D775B7C36DD7AD1B1`.
- Included source sections: reception, production, interaction, online interaction,
  mediation, and communicative language competences.
- Excluded from this bounded task: the plurilingual/pluricultural competence scales,
  signing-competence chapter, appendices, self-assessment grids, and example-domain
  expansions. They are not among the Phase 2 descriptor modes named in the master plan.
- The Arabic edition remains a terminology reference; the registered English edition is
  the descriptor authority.

## Results

- Reviewed 82 scale placements with A1 rows across 64 physical PDF pages. `Turntaking`
  appears in two source sections, so these are 81 distinct scale titles.
- Accepted 98 A1 descriptor records from 59 scale placements on 48 pages.
- Recorded 23 scale placements whose published A1 row says `No descriptors available`;
  these produce no evidence record but remain asserted in the extraction specification.
- Mode totals: Reception 24; Production 11; Interaction 30; Online interaction 3;
  Mediation 15; Communicative language competences 15.
- Every record retains the physical PDF page, printed page, exact scale title, source
  hierarchy labels, verbatim descriptor text, source-file hash, and text hash.
- Sixty-five records join visual line wraps. Two also remove extraction-only whitespace
  after a line-final slash or hyphen. Each affected record declares the handling in
  `transcription_notes`.

## Duplicate and boundary review

- The exact descriptor `Can understand questions and instructions addressed carefully
  and slowly to them and follow short, simple directions.` appears in three different
  source scales on pages 73, 77, and 79. All three are retained because each is distinct
  scale evidence, not a duplicated extraction row.
- No duplicate record identifiers, missing texts, reversed locators, orphan page
  references, A2/Pre-A1 row leakage, or blank descriptor records were found.
- Multi-column mediation and phonological-control tables were checked against rendered
  pages so each descriptor remains attached to its correct column scale.

## Review and validation

- Rendered and visually reviewed all 64 in-scope table pages, including pages whose A1
  rows contain no descriptor.
- Confirmed every stored descriptor occurs on its cited raw PDF page after only the
  declared line-wrap normalization.
- Both derived and reviewed collections pass the Draft 2020-12 source-record schemas and
  semantic provenance validation.
- The reviewed collection contains 98 accepted records and no unresolved review issue.
- `CUR-004` subsequently applied the controlled skill, mode, and function tags documented
  in `docs/CURRICULUM_TAG_TAXONOMY.md`. `CUR-005` subsequently applied the candidate
  clusters documented in `docs/CANDIDATE_UNIT_MAP.md`. Source hierarchy wording remains
  separately retained as source fact.

## Remaining boundary

This extraction supplies supporting CEFR evidence only. Later tasks normalize and
cluster the evidence, but objective-to-descriptor equivalence, final units, lessons, and
the Phase 2 exit gate remain unresolved.
