# A1 Lesson Map: Places, Directions, and Travel Partition Audit

Status: reviewed draft partition; `LESSON-002` remains in progress.

## Boundary

This partition reconciles all 31 assignments containing
`places_directions_travel`. It adds 12 lesson-sized draft candidates, extends one
existing home-location candidate with directly overlapping evidence, and treats one
copying objective as cross-cutting form support. It does not approve a final lesson
count, unit boundary, global order, language target, or gold lesson.

## Candidate decisions

- Reading separates following written wayfinding directions from locating explicit
  facts in a short place or hotel information text.
- Listening separates route following, concrete place-and-time extraction, referent
  identification, guided-tour outline comprehension, and station-announcement figures.
- Live direction following remains distinct from a map information gap because the
  first assesses acting on an interlocutor's instructions and the second assesses
  asking for and giving wayfinding information.
- Public-transport ticket purchase and hotel check-in remain separate transactions;
  either can be assessed independently and each uses different essential fields.
- Travel-form completion remains a written production task. Real passport, booking,
  immigration, and travel data are explicitly unnecessary.

## Shared evidence reconciliation

- Existing full owners retain the meeting arrangement, people's stated locations,
  hotel-registration personal fields, and time-or-place mediation records.
- `gse.adult.2022.p14.007` adds only the place-name clause beside its prior people-name
  claim.
- `cefr.cv2020.p048.overall_oral_comprehension.02` adds concrete place information
  beside the prior concrete-time claim.
- `cefr.cv2020.p077.goal_oriented_co_operation.02` adds location instructions beside
  the prior time-and-number claim.
- `cefr.cv2020.p084.notes_messages_and_forms.01` contributes only its arrival and hotel
  context; its full personal-form owner is unchanged.
- The travel example in the broad illustrated personal-interest reading descriptor and
  the station example in the figures/prices/times descriptor are named partial claims.
- The three identical short-direction wordings on CEFR pages 73, 77, and 79 remain
  distinct cited scale evidence. They are not collapsed or treated as duplicate rows.
- Immediate-environment object location strengthens the existing
  `understand_where_things_or_people_are` candidate instead of creating an overlapping
  travel lesson.
- Copying a direction sentence is cross-cutting basic-language support rather than a
  standalone learner ability.

## Counts and balance

- Assignments reconciled: 31 of 31.
- New candidates: 12; new candidate evidence references: 25.
- One evidence reference was added to the existing home-location candidate, and one
  evidence record was added to cross-cutting support.
- Expanded map: 53 candidates, 124 candidate evidence references to 114 unique reviewed
  records, nine support records, and 123 unique cited included records overall.
- New candidates represent listening, reading, speaking, and writing plus reception,
  production, and interaction. The cluster's mediation assignment retains its prior
  source-exact owner.

## Critique and unresolved work

Every assignment has a non-context citation or support owner. No source record becomes
a duplicate full anchor, and every partial claim names the covered clause. Candidate
tags are supported by cited reviewed records, all tasks use fresh variants, and all
mastery evidence remains observable. No MSA text is introduced in this data partition.

All candidates and the map remain `needs_review`. Grammar, vocabulary, phrases,
pronunciation, Arabic-speaker error hypotheses, time estimates, hard prerequisites,
successors, and final sequence remain empty or provisional until reviewed evidence and
later partitions justify them.

## Validation

- Lesson-map schema and semantic validation: pass.
- Travel partition acceptance tests: 8 pass.
- Full project suite: 86 tests pass.
- Reviewed source collections, candidate map, curriculum audit, and lesson map: pass.
- Deterministic rebuild SHA-256:
  `6B6D285C65D0BB0DFDA0ECAC4C7F1C88BAC797BB49311F1FBBC9856DFC0902DD`.
- Python compilation, six authoritative raw-source hashes, and modular line limits:
  pass.

## Next bounded partition

Normalize the 30 `food_shopping_services` assignments. Reconcile the 26 records not
yet cited with existing price, quantity, request, transaction, and form owners without
duplicating full claims or fixing the global lesson sequence.
