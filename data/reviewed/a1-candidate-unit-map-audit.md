# CUR-005 Candidate Unit Map Audit

## Evidence coverage

- Reviewed records evaluated: 219.
- Included and mapped: 218 (120 GSE objectives and 98 CEFR descriptors).
- Reviewed exclusion left unmapped: 1 duplicated GSE evidence row.
- Natural topical mappings: 151 records.
- Natural topical mappings with cross-cutting support: 21 records.
- Cross-cutting-only mappings: 46 records.
- Explicit exclusions: 1 record.

Every assignment in `a1-candidate-unit-map.json` carries the source dataset, raw file,
exact PDF location, and source-text SHA-256. Candidate cluster ids were also written to
the corresponding reviewed and derived source records. Source text, source facts,
inclusion decisions, normalized tags, and prior ambiguities were not changed.

## Earlier seven-unit test

The old proposal was tested rather than used as a fixed target. For the 120 included
GSE objectives, the result is 58 natural, 35 overlapping, and 27 forced mappings. For
the 98 CEFR descriptors, it is 33 natural, 25 overlapping, and 40 forced mappings.
Therefore the exact seven-unit claim is rejected at candidate-map stage.

Eight candidate-unit clusters preserve the useful topical and functional evidence. Two
cross-cutting support bands prevent generic language-control, repair, mediation, and
facilitation evidence from being mislabeled as standalone topical units.

## Review notes and deferred risks

- Compound records may legitimately appear in multiple clusters; their source wording
  was not split or rewritten.
- Assignment counts are evidence density, not a unit-size recommendation.
- Some generic objectives are cross-cutting because their source gives no topic. This
  is an explicit mapping result, not invented topical specificity.
- Candidate unit order, prerequisite relationships, duplicate reconciliation beyond the
  retained source duplicate, and skill balance remain deferred to `CUR-006`.
- Objective-to-descriptor equivalence and lesson-sized outcomes remain unclaimed.

## Reproduction and validation

```powershell
python scripts/create_candidate_unit_map.py --reviewed-at <ISO-8601> --check
python scripts/validate_candidate_map.py
python scripts/validate_source_records.py data/reviewed/gse-a1-objectives.json data/reviewed/cefr-a1-descriptors.json
python -m unittest discover -s tests -v
```
