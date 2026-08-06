# A1 Lesson Map Validation Contract v0.1

## Status and boundary

This document records the collection envelope and deterministic acceptance checks for
the in-progress `LESSON-002` map. The topical partitions plus the final
foundation/strategy partition now author reviewed draft candidates and reconcile all
218 included records. This contract still does not approve a lesson or unit count,
impose topical-unit order, or select the gold lesson.

Each candidate continues to use `schemas/curriculum/lesson-candidate.schema.json`. The
map envelope in `schemas/curriculum/lesson-map.schema.json` adds an explicit global
sequence and source-cited cross-cutting support definitions.

The foundation/strategy partition classifies the remaining 42 records as three new
candidates, three source-exact candidate extensions, or scoped cross-cutting support.
The first global audit is recorded in
`data/reviewed/a1-lesson-map-global-audit.json` and its reviewed Markdown companion.
It confirms complete coverage and valid provenance. A reviewed remediation partition
has merged the five same-task overlap groups and resolved both mastery-alignment cases,
reducing 87 provisional drafts to 81 without dropping source evidence. A subsequent
reviewed partition places all 81 candidates once across five pedagogical sequence bands,
records five genuine hard prerequisites with reciprocal successors, and separates 43
helpful-before links from hard gates. Candidate-level language-target and labelled error
decisions are now reviewed for all 81 candidates. The final partition covers six
social-contact and collaboration tasks: agreeing to a request, accepting an offer,
showing sympathy, inviting input and checking understanding, welcoming an idea, and
sharing an idea while asking what others think. All candidate approvals remain open as
a separate review step.

## Deterministic checks

`scripts/validate_lesson_map.py` checks:

- unique candidate and support ids, with the sequence covering every candidate once;
- exact dataset, source, raw-file, location, and source-text-hash provenance;
- candidate interpretation tags supported by the cited reviewed records;
- language-target evidence already declared in the candidate evidence inventory;
- no unknown or excluded records, duplicate full anchors, or unlabelled partial claims;
- valid relationship targets, ordered acyclic hard prerequisites, and reciprocal
  successor links;
- helpful-before links ordered earlier than their targets, without successor or hard-gate
  semantics, and relationship evidence confined to the linked candidate pair;
- symmetric support applicability and cited support-relation evidence;
- basic language-control support on every candidate and interaction-repair support on
  interaction candidates, preserving the passed `CUR-006` dependency audit;
- mastery dimensions using the locked names, always including comprehension and outcome
  performance, with exact level-2 evidence keys; and
- for an `approved` map only: every included source record reconciled, all candidates
  individually approved and accepted, map review accepted, and listening, reading,
  speaking, and writing all represented.

The four-skill check is presence-based. It does not impose equal quotas or invent
objectives to fill the granular gaps documented by `CUR-006`.

## Partial-map behavior

An `in_progress` or `needs_review` map may intentionally leave included records
unassigned while candidates are normalized. All evidence it does contain must already
pass provenance, relationship, support, and mastery checks. Full coverage and approval
checks activate only when the map claims `approved` status.

## Reproduction

When the reviewed map exists, run:

```powershell
python scripts/validate_lesson_map.py
```

Fixture-based contract tests remain in place. The identity, people, routines, home,
travel, service, message, social-contact, and foundation/strategy partitions add
data-level acceptance tests for deterministic reproduction, validation, complete
assignment reconciliation, explicit partial clauses, shared-claim ownership,
cross-cutting support reciprocity, provisional ordering, and skill/mode presence.
The global-audit tests additionally require explicit resolved overlap dispositions,
complete coverage, mastery-alignment decisions, an accepted five-band relationship and
sequence review labelled as a pedagogical hypothesis rather than source-proven order,
visible remaining approval blockers, and a closed Phase 4 gate while `LESSON-002`
remains in progress.
