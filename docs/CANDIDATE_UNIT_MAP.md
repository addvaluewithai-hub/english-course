# A1 Candidate Unit Map v0.1

## Status and boundary

This is the `CUR-005` evidence organization, not a final unit sequence. It maps every
included reviewed GSE objective and CEFR descriptor to one or more candidate clusters.
`CUR-006` subsequently passed the coverage, duplicate, prerequisite-support, and
skill-balance audit documented in `docs/A1_CURRICULUM_AUDIT.md`. No cluster is a
lesson-sized ability.

The machine-readable map is `data/reviewed/a1-candidate-unit-map.json`. Each assignment
retains its source dataset, raw file, exact PDF location, and source-text SHA-256. The
full verbatim wording remains in the referenced reviewed source collection.

## Candidate organization

| Candidate cluster | Role | GSE objectives | CEFR descriptors |
| --- | --- | ---: | ---: |
| Identity and personal information | candidate unit | 14 | 10 |
| People and relationships | candidate unit | 14 | 7 |
| Routines, time, and leisure | candidate unit | 26 | 12 |
| Home, objects, and descriptions | candidate unit | 20 | 9 |
| Places, directions, and travel | candidate unit | 14 | 17 |
| Food, shopping, and services | candidate unit | 14 | 16 |
| Messages, signs, and forms | candidate unit | 6 | 16 |
| Social contact and collaboration | candidate unit | 10 | 12 |
| Communication strategies | cross-cutting support | 3 | 18 |
| Language foundations | cross-cutting support | 24 | 23 |

Counts overlap because a compound source statement can support more than one cluster.
The two support bands are deliberately not proposed as topical units. They carry
generic comprehension, language control, pronunciation, spelling, repair, mediation,
translation, and facilitation evidence across the candidate units.

## Test of the earlier seven units

The earlier proposal was Identity; People & Relationships; Everyday Life; Places &
Movement; Needs & Transactions; Simple Communication; and Reading, Signs & Forms.
It is not supported as an exact final map.

Of the 120 included GSE objectives, 58 fit naturally, 35 overlap earlier boundaries,
and 27 would need to be forced. The retained duplicate exclusion is not applicable.
Across the 98 supporting CEFR descriptors, 33 fit naturally, 25 overlap, and 40 would
be forced.

The main problems are structural:

- Home, objects, and descriptions has enough distinct evidence to expose overlaps
  between People & Relationships, Everyday Life, and Places & Movement.
- Reading, Signs & Forms mixes a delivery channel with unrelated communicative goals;
  reading evidence also belongs throughout the other clusters.
- Simple Communication is too broad: social contact, collaboration, repair, mediation,
  translation, and language control behave differently.
- Generic language foundations and communication strategies should support many units,
  not be forced into one topical container.

## Interpretation rules

Cluster ids are controlled in the source-record and candidate-map schemas. Deterministic
rules use verbatim wording plus the reviewed function and mode tags. Multiple mappings
are retained only when the source itself contains compound topics or purposes. An
included record with no mapping is invalid; an excluded record with a mapping is also
invalid.

This candidate organization does not claim objective-to-descriptor equivalence, decide
unit order, define prerequisites, or announce a final unit count. The audit found no source-proven strict cluster order; lesson-sized sequencing remains
Phase 3 work.
