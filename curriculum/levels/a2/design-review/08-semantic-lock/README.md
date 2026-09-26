# A2 Stage 08 — Semantic / Mastery Lock

Status: **IN PROGRESS — HUMAN SEMANTIC REVIEW**  
Level: **A2**  
Structural prerequisite: Milestone 2 closed at **12 units / 83 lesson slots**.

This stage decides what level of learner control is actually claimed for every required A2 source record. It exists to prevent a coverage ledger from silently becoming an all-active mastery contract.

## Non-negotiable rule

**Automation may expand, join, count and validate human decisions. It may not choose a semantic role.**

A word is not productive because it appears in a lesson. A phrase is not generative because it contains grammar. An EGP row is not an independent teaching objective. A receptive ability is not converted into productive mastery. Cross-cutting support is not promoted into a fake standalone exit target.

## Inputs

Authoritative human-reviewed inputs:

- `../01-abilities/final-capability-map.md`
- `../02-phrases/phrase-review.md`
- `../03-grammar/grammar-review.md`
- `../04-words/word-review.md`
- `../04-words/generated/word-home-map.json`
- `../04.5-pronunciation-exit-carry-forward/constraints.md`
- `../05-curriculum-map/curriculum-map.md`
- `../06-coverage-ledger/generated/coverage-ledger.json`
- `../06.5-load-sequence-lock/load-sequence-lock.md`

Canonical source inventories remain `curriculum/levels/a2/{abilities,phrases,grammar,words,pronunciation}.json`.

## Semantic contract

Every exact source record receives three independent fields.

### 1. `mastery_mode`

- **productive** — learner must independently produce the language/performance when the communicative task calls for it.
- **receptive** — learner must recognise, understand, locate or interpret it in source-bounded A2 input; independent production is not claimed.
- **interactive** — successful control is defined through initiating/responding/repairing in an exchange, not through decontextualised production.
- **integrated_support** — the record supports another learner performance and must be taught/reused, but is not an independent exit target.

### 2. `control_scope`

- **generative** — learner can make new source-bounded combinations, not merely replay one model.
- **bounded_pattern** — learner controls a limited A2 pattern/system in its reviewed functions; broader later-level meanings are excluded.
- **formulaic** — learner can deploy/recognise a fixed or semi-fixed chunk as a unit; this is explicitly not evidence of unrestricted grammar.
- **contextual** — control is tied to familiar lexical/content contexts or supported input rather than unrestricted topic mastery.
- **quality_constraint** — the record changes intelligibility, cohesion, reference, writing quality or interaction conditions inside other performances.

### 3. `exit_evidence`

- **independent_possible** — the item/system may legitimately be sampled as an explicit task requirement at A2 exit.
- **integrated_required** — exit evidence should occur inside a larger communicative/receptive task; a separate item test is unnecessary.
- **support_condition** — the record is a condition/quality constraint on other exit evidence, not a standalone target.

These dimensions are deliberately separate. For example:

- a request ability may be `interactive + bounded_pattern + independent_possible`;
- `Why not…?` may be `productive + formulaic + integrated_required`;
- comparative grammar may be `productive + bounded_pattern + integrated_required`;
- a broad factual word such as `government` may be `receptive + contextual + integrated_required`;
- reference tracking may be `integrated_support + quality_constraint + support_condition`.

## Category decision principles

### Abilities

Source mode/task semantics are authoritative. Reception stays receptive; interaction stays interaction when success requires exchange; production stays productive unless the source itself is only a support/quality condition. Fixed-expression wording narrows `control_scope` to formulaic/bounded rather than inventing generative control.

### Phrases

Oxford Phrase List inclusion establishes useful A2 phrase evidence, not universal active mastery. Transactional/social/repair chunks may receive formulaic productive control when they directly enable a required capability. Informational/content/discourse phrases may remain receptive or integrated support. Polysemy is always sense-bounded to the reviewed home.

### Grammar

The 291 EGP rows are interpreted through the 46 manually reviewed systems. A system may be generative/productive, receptive-supporting or embedded infrastructure. Raw row count never decides mastery. Fixed phrase evidence never expands grammar beyond canonical EGP support.

### Words

The 871 Oxford word records are not all active vocabulary. Productive control is reserved for lexis required to complete core A2 communicative tasks and linked descriptions. Broad environment/science/crime/media/society/culture vocabulary can be receptive/contextual when its main function is to carry factual input. Grammar-owned function words are integrated support under Stage-03 systems. Homographs/senses remain exact-record-specific.

### Pronunciation

Pronunciation is a distributed performance-quality contract. It is not an accent target and not a standalone capability. A2 requires generally understandable familiar-situation speech, with repetition/listener effort still possible. New A2 prominence/rhythm, connected speech and interactional intonation remain bounded and integrated.

## Required outputs

1. `ability-roles.md` — human role decisions for all 269 required ability rows.
2. `phrase-roles.md` — human role decisions for all 176 phrases.
3. `grammar-roles.md` — human role decisions for all 46 systems / 291 rows, including row exceptions where needed.
4. `word-roles.md` — human role decisions for the 30 lexical sets + `LX-GENERAL`, with exact item overrides where needed.
5. `pronunciation-roles.md` — human role decisions for all 10 strands.
6. `semantic-decisions.json` — machine-readable human-authored family/set/row decisions; no inferred roles.
7. `generated/semantic-role-ledger.json` — exact 1,617-record expansion.
8. `generated/semantic-role-report.md` — counts/orphans/decision provenance and lesson-level active-load view.
9. Stage 08.5 reconciliation after Stage 08 roles are locked.

## Lock criteria

Stage 08 may close only when:

- all **1,617 / 1,617** exact records receive an explicit semantic role;
- no role is inferred merely from lesson presence, frequency or source order;
- productive/formulaic/receptive/support distinctions are visible and auditable;
- every productive claim stays inside A2 source boundaries;
- `LX-GENERAL` is not silently made active;
- high-load lessons are re-counted by mastery role, not raw rows;
- Stage 08.5 confirms the lifecycle can support the semantic claims without inventing extra mastery evidence;
- any lesson reopening is based on a real role-aware learning/evidence problem.

Do not start lesson briefs or production before Stage 08 + 08.5 are closed.
