# A1 Manual Ability Review

This folder records the human/manual curriculum-design decisions for the first stage of the new A1 design.

## Rule

No clustering script, heuristic, legacy lesson map, or previous unit sequence is allowed to decide the final capability structure.

The only fixed input is the A1 source inventory in `curriculum/levels/a1/abilities.json` (119 required abilities sourced from CEFR/GSE).

Each ability is read as language/learning evidence and receives an explicit manual disposition:

- `KEEP` — stands as a distinct capability component.
- `MERGE` — same learner performance can be represented under a broader capability without losing an assessment boundary.
- `SPLIT` — source statement contains meaningfully separate learner performances that should not be hidden inside one capability.
- `SUPPORTING` — important evidence/condition, but not a standalone final capability.

## Review safeguards

1. Similar topic does not imply the same capability.
2. Reception, production and interaction boundaries must remain visible even if grouped under one capability family.
3. A final capability is not automatically a lesson.
4. Every source ability must remain traceable to a final capability or an explicit supporting role.
5. Decisions must include a short rationale; no decision is accepted only because an older syllabus did it that way.
6. Later phrase and grammar review may reopen this file if they reveal a missing or overloaded capability.

## Stage outputs

- `manual-review-log.md` — item-by-item decisions and rationale.
- `capability-map-v1.md` — consolidated capability structure after all 119 abilities are reviewed.
- `critic-notes.md` — unresolved questions and issues to challenge before the stage is locked.

Status: **IN PROGRESS**
