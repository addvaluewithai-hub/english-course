# Curriculum Source-Record Contract v1.0.0

## Purpose and boundary

This contract governs machine-extracted and reviewed curriculum evidence. It supports
GSE objectives, CEFR descriptors, English Grammar Profile features, and vocabulary
items without treating later curriculum judgments as source facts.

The schemas are:

- `schemas/curriculum/source-evidence.schema.json` for immutable evidence and location;
- `schemas/curriculum/source-record.schema.json` for one evidence record; and
- `schemas/curriculum/source-record-collection.schema.json` for dataset files.

The Phase 2 skill, mode, and function codes are controlled by
`docs/CURRICULUM_TAG_TAXONOMY.md`. They remain interpretations under this contract and
are not final cluster, unit, lesson, or learner-outcome taxonomies.

Candidate cluster ids are controlled by `docs/CANDIDATE_UNIT_MAP.md` and the schemas.
They remain provisional Phase 2 interpretations; an included CUR-005 record must have
at least one, while a reviewed exclusion remains unmapped.

## Evidence boundary

`source` and `source_facts` contain only material present in the registered source.
`interpretation` contains every normalized tag, inclusion decision, ambiguity, note,
and candidate cluster. Never copy an inference into a source-fact field.

`source.source_text` preserves the published wording, capitalization, and punctuation;
it must not be corrected or paraphrased. If line wraps, footnote markers, or merged
cells require transcription handling, describe that handling in `transcription_notes`.
The SHA-256 is computed from the exact UTF-8 value stored in `source_text`.

All source-provided labels are strings, including numeric-looking GSE values. Use
explicit `null` when a source does not provide a field. Source-specific labels such as
EGP guidewords belong in `source_facts.other_verbatim`.

## Provenance rules

- `source_id` must identify an entry in `sources/registry/SOURCES.md`.
- `source_version` is the publication/export version, not an inferred course version.
- `raw_file` is a forward-slash path below `sources/raw/`; derived mirrors are never
  cited as the authority.
- `source_file_sha256` must match the registered raw-file hash.
- PDF locations use the one-based file page in `page`; `printed_page` is separate and
  nullable. Spreadsheet locations use the worksheet, one-based data row, and columns.
- `page_end` or `row_end` equals the start for a single-location record and must never
  precede it.
- A record spanning non-contiguous evidence must be split rather than given a vague
  range.

## Field mapping

| Audit concept | Contract field |
| --- | --- |
| objective or record id | `record_id`; source id in `source_facts.source_record_id` |
| source and version | `source.source_id`, `source.source_version` |
| exact location | `source.raw_file`, `source.location` |
| verbatim wording | `source.source_text`, `source.source_text_sha256` |
| source CEFR/GSE label | `source_facts.level_text`, `gse_score_or_range` |
| source skill/mode/function | matching `source_facts.*_text` fields |
| normalized CEFR/skill/mode/function | matching `interpretation.*_codes` arrays |
| candidate cluster | `interpretation.candidate_cluster_ids` |
| interpretive notes | `interpretation.notes`, `ambiguities` |
| review state | `review.status`, reviewer, timestamp, and issues |

`record_id` is a stable project identifier and must not encode a judgment likely to
change. For an objective it is the audit's `objective_id`. A source's own identifier,
when present, remains separately verbatim in `source_record_id`.

## Review lifecycle

1. Extraction creates `unreviewed` records with null reviewer and timestamp.
2. Uncertain extraction becomes `needs_review` and records concrete issues or
   ambiguities.
3. A reviewer sets `accepted` only after checking wording, location, hashes, source
   facts, A1 relevance, and interpretations. Accepted records may represent a reviewed
   exclusion, but an exclusion must retain its reason.
4. `rejected` means the record itself is unusable or duplicated, not merely excluded
   from A1. It needs a reviewer, timestamp, and at least one error issue.
5. Files under `data/reviewed/` may contain only `accepted` records.

Reviewer identity is an accountable project identifier, not necessarily a person's
name. Times use ISO 8601 with an offset or `Z`.

## Deterministic validation

Run:

```powershell
python scripts/validate_source_records.py --check-schemas
python scripts/validate_source_records.py path/to/dataset.json
python -m unittest tests.test_source_record_validator
```

The validator checks JSON Schema structure plus rules that JSON Schema alone does not
express cleanly:

- unique `record_id` values;
- raw-file existence and SHA-256 agreement;
- source-text SHA-256 agreement;
- PDF/spreadsheet locator agreement and ordered ranges;
- exclusion/review-state consistency;
- no unresolved error on an accepted record; and
- accepted-only records in `data/reviewed/`.

Schema-clean is not source-reviewed. Human or independent review must still compare
the stored text and location against the raw page or row before acceptance.
