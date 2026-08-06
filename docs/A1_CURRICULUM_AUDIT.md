# A1 Curriculum Coverage Audit v0.1

## Status and boundary

`CUR-006` passes the Phase 2 curriculum-audit gate. The reviewed machine result is
`data/reviewed/a1-curriculum-audit.json`; its evidence base is the CUR-005 candidate map
plus the reviewed GSE and CEFR collections.

This result does not finalize eight units, claim objective-to-descriptor equivalence, or
define lessons. The eight topical clusters and two support bands remain provisional
evidence containers. Phase 3 may now define lesson-sized abilities and sequencing.

## Coverage and traceability

- Reviewed source records: 219.
- Included and mapped: 218 (120 GSE objectives and 98 CEFR descriptors).
- Excluded with reason and retained provenance: 1 GSE source row.
- Traceable candidate-map assignments: 219.
- Unmapped inclusions, mapped exclusions, source or assignment orphans: 0.
- Empty clusters: 0.
- Candidate clusters lacking either GSE objectives or CEFR descriptors: 0.

Every audit decision that depends on a specific record cites its record id, raw PDF,
physical page location, and source-text SHA-256. The candidate map remains the complete
record-to-cluster provenance index.

## Duplicate reconciliation

| Published repetition | Source location | Resolution |
| --- | --- | --- |
| Caller name and phone number | Pearson GSE 2022, PDF pages 14 and 15 | Keep page 14 record `gse.adult.2022.p14.005` canonical; retain page 15 evidence row excluded with its exact-duplicate reason. |
| Ask people for things, and give people things | CEFR 2020, PDF pages 77 and 78 | Retain both because the wording is separately published under Goal-oriented co-operation and Obtaining goods and services. |
| Understand questions/instructions and follow directions | CEFR 2020, PDF pages 73, 77, and 79 | Retain all three because the wording is separately published under three interaction scales. |

The two CEFR groups are contextual repetitions, not duplicate curriculum records that
can be silently collapsed. Their distinct scale and page provenance is meaningful.

## Prerequisite and support audit

No strict order among the topical clusters is source-proven. Two cross-cutting support
needs must remain explicit when Phase 3 sequences lesson-sized abilities:

- Basic language control must accompany topical work. Evidence includes CEFR General
  linguistic range (PDF page 131), Grammatical accuracy (132), Overall phonological
  control (135), and Orthographic control (136).
- Repair and clarification must be available before or with interaction tasks. Evidence
  includes CEFR Overall oral interaction (PDF page 72) and Asking for clarification
  (89). Every topical candidate cluster contains interaction evidence, so none should
  assume repair support will appear only in a later standalone unit.

These are source-cited support dependencies, not permission to create a foundation unit,
fix a topical sequence, or treat support descriptors as lesson outcomes.

## Overall evidence balance

| Evidence set | Listening | Reading | Speaking | Writing |
| --- | ---: | ---: | ---: | ---: |
| Included GSE objectives | 33 | 14 | 54 | 19 |
| CEFR supporting descriptors | 45 | 29 | 41 | 19 |

CEFR skill counts can overlap because a descriptor may support more than one channel.
The GSE objective set is speaking-heavy and reading-light; evidence density must not be
mistaken for an equal-skill quota or a final unit-size recommendation.

## Candidate-cluster gaps

Combined GSE and CEFR evidence covers listening, reading, speaking, and writing in every
topical candidate cluster. Granular GSE objectives still have these explicit gaps:

| Candidate cluster | GSE objective skill gap | CEFR support result |
| --- | --- | --- |
| People and relationships | Reading | CEFR supplies reading support. |
| Food, shopping, and services | Reading and writing | CEFR supplies both channels. |
| Messages, signs, and forms | Speaking | CEFR supplies speaking support. |
| Social contact and collaboration | Reading | CEFR supplies reading support. |

Home, objects, and descriptions has no CEFR reading descriptor, but two GSE reading
objectives provide the combined channel. These imbalances are inputs to Phase 3; they
must not be fixed by inventing source objectives.

## Gate verdict

Coverage is complete, the exclusion is justified, repeated wording is reconciled,
support dependencies are source-cited, and skill gaps are documented. Phase 2 passes.
`LESSON-001` may open, but lesson normalization must preserve the candidate status,
source links, and the unresolved question of final unit count and order.

## Reproduction

```powershell
python scripts/create_curriculum_audit.py --reviewed-at <ISO-8601> --check
python scripts/validate_curriculum_audit.py
python scripts/validate_candidate_map.py
python scripts/validate_source_records.py data/reviewed/gse-a1-objectives.json data/reviewed/cefr-a1-descriptors.json
python -m unittest discover -s tests -v
```
