# Level Curriculum Design Playbook v1

Status: **AUTHORITATIVE PROCESS HANDOFF**  
Scope: **A2, B1, B2, C1, C2**  
Reference implementation: **A1 on `curriculum/level-source-of-truth-v1`**  
Purpose: allow a new ChatGPT conversation, with no prior chat history, to reproduce the A1 curriculum-design process safely and consistently for later levels.

---

## 1. Read this first in a new conversation

If there is no chat history, do **not** reconstruct the process from memory and do **not** begin by inventing lessons.

Start by reading:

1. this file;
2. `docs/LEVEL_SOURCE_OF_TRUTH_STATUS_V1.md`;
3. `docs/LEVEL_SOURCE_OF_TRUTH_V1.md`;
4. the target level folder under `curriculum/levels/<level>/`;
5. the immediately previous level's `exit_contract.json` and `manifest.json`;
6. A1's completed reference artifacts under `curriculum/levels/a1/design-review/` and `curriculum/levels/a1/semantic-lock/` only as **process examples**, not as content/templates to copy blindly.

Work on the independent curriculum branch/workstream. Do **not** modify `main`, the existing first-ten pilot, `automation/STATE.json`, or `TEST-002` unless explicitly instructed later.

The core goal is:

> Turn the complete source inventory for a level into a teachable, dependency-aware curriculum in which every required source item has an explicit learning lifecycle and exit obligation, without confusing source coverage with mastery or forcing every source row to become a separate lesson objective.

---

## 2. What must be copied from A1 — and what must NOT be copied

### Copy the method

Copy these principles and gates:

- source inventory first;
- abilities/learner performance drive the architecture;
- phrases, grammar, words, and pronunciation attach to real learner performances;
- manual semantic review is authoritative where pedagogical meaning is involved;
- automation checks completeness, exact IDs, lifecycle coverage, load, and reproducibility;
- curriculum map is allowed to change while evidence is reviewed;
- lesson count emerges from dependencies and load rather than a preset number;
- every item receives an explicit lifecycle;
- transfer/review lessons cannot hide new required content;
- final productive/receptive/formulaic/support obligations are reconciled after the instructional architecture is understood;
- curriculum-design authorization is separate from delivery/media-production authorization;
- CI must reproduce the final state without silently reverting it.

### Do NOT copy A1's numbers or shape

Do **not** assume later levels should have:

- 10 units;
- 62 lesson slots;
- the same capability count;
- the same proportion of productive vs receptive words/phrases/grammar;
- the same lexical load per lesson;
- the same transfer pattern;
- the same grammar family distribution;
- the same semantic categories or topic sequence.

A2–C2 must emerge from their own source evidence, prerequisite structure, cumulative exit contract, and instructional load.

---

## 3. Fixed source-of-truth inputs

Every level folder contains the standard contract:

- `manifest.json`
- `words.json`
- `phrases.json`
- `grammar.json`
- `abilities.json`
- `pronunciation.json`
- `exit_contract.json`
- `sources.json`

Inventory semantics are:

- level files = **new at level**;
- exit obligation = **cumulative through level**.

Therefore, when designing A2, B1, B2, C1, or C2, the target level's new content is not the whole learner state. The previous level's exit contract is prerequisite retained knowledge and must be deliberately retrieved/recycled where needed.

Current inventory counts are a planning fact, not a teaching-object count:

| Level | Words / lexical meanings | Phrases / chunks | EGP grammar features | Required granular abilities | Pronunciation strands |
| --- | ---: | ---: | ---: | ---: | ---: |
| A1 | 900 | 199 | 109 | 119 | 10 |
| A2 | 871 | 176 | 291 | 269 | 10 |
| B1 | 809 | 175 | 338 | 249 | 10 |
| B2 | 1,427 | 125 | 243 | 270 | 10 |
| C1 | 1,315 | 75 | 129 | 59 | 10 |
| C2 | 609 | 41 | 112 | 19 | 10 |

These counts are source records. Multiple rows may describe one teachable system, one row may support several performances, and some source items may be primarily receptive or supporting rather than independent productive targets.

---

## 4. Source hierarchy and evidence rules

Use the existing reviewed source architecture rather than substituting a new syllabus.

### Words

- A1–C1 lexical source: Oxford 3000/5000 partition already represented in level inventories.
- C2 lexical source: Pearson GSE Vocabulary C2 General Learner snapshot.
- A source word row does not automatically imply unrestricted productive mastery of all senses/collocations.

### Phrases

- A1–C1: current official Oxford Phrase List snapshot.
- C2: Pearson GSE vocabulary phrase/phrasal-verb records plus collocations attached according to source semantics.
- A phrase having a lesson home does not automatically mean it is an independent productive exit requirement.

### Grammar

- Canonical target inventory: English Grammar Profile rows in `grammar.json`.
- Pearson GSE Grammar is supporting/cross-check evidence, not a second canonical target inventory.
- Several EGP rows may jointly describe one usable grammar system; do not create one lesson per row.
- Conversely, do not merge rows if doing so erases a real meaning, form, function, modality, or control boundary.

### Abilities

- Use the granular reviewed CEFR/GSE assignments in `abilities.json`.
- `include_for_spine` items are the required new-at-level ability inventory.
- Keep reception, production, interaction, mediation, and other modality distinctions visible.
- A final capability is not automatically one lesson.

### Pronunciation

- Use the reviewed 10-strand progression at the target level.
- Attach pronunciation to actual communicative use and intelligibility.
- Do not turn pronunciation strands into isolated accent perfection requirements.

### C2 licensing

Pearson GSE-derived C2 lexical content carries `commercial_permission_required`. Curriculum architecture/research may proceed, but do not imply commercial clearance and do not remove the production gate.

---

# PART I — THE DESIGN PIPELINE

## Stage 0 — Preflight and invariants

Before manual curriculum design begins:

1. verify the target level's eight standard files exist;
2. verify manifest counts match inventories;
3. run/inspect the strict source-of-truth audit;
4. confirm there are no source-coverage gaps or duplicated primary IDs;
5. read the previous level exit contract;
6. confirm target-level inventory status and any licensing/production gates;
7. create a target-level `design-review/` workspace without changing existing delivery lessons.

Recommended target structure:

```text
curriculum/levels/<level>/design-review/
  01-abilities/
  02-phrases/
  03-grammar/
  04-words/
  05-curriculum-map/
  06-coverage-ledger/
  07-lesson-briefs/
```

Do not authorize lesson/media production at this stage.

### Stage-0 critic

Fail the stage if:

- source totals do not reconcile;
- target content is mixed with another level without an explicit cumulative/recycle reason;
- source licensing gates are lost;
- an old syllabus/lesson count is being treated as authoritative;
- the process is already assuming a unit count or lesson count.

---

## Stage 1 — Manual ability review and capability architecture

This is the architectural starting point.

A1's strongest rule was:

> No clustering script, heuristic, legacy lesson map, or previous unit sequence decides the final capability structure.

Read **every required ability** at the target level. Give each source ability an explicit manual disposition such as:

- `KEEP` — distinct learner-performance component;
- `MERGE` — represented under a broader capability without losing its assessment boundary;
- `SPLIT` — source statement contains meaningfully distinct learner performances;
- `SUPPORTING` — important condition/evidence, but not a standalone final capability.

Build a final capability architecture that preserves traceability from every source ability.

### Required safeguards

- Similar topic does not imply same capability.
- Listening/reading reception cannot be silently replaced by a speaking task.
- Production cannot be inferred merely because a learner can recognize something.
- Interaction requirements must remain interaction requirements.
- Conditions such as slow/clear speech, familiar context, partner support, repair, or text type must remain visible where source evidence requires them.
- A capability is a learner performance boundary, not automatically a lesson title.
- Later phrase/grammar/word evidence is allowed to reopen the architecture.

### Outputs

At minimum, create equivalents of:

- manual item-by-item review log;
- final capability map;
- critic notes / unresolved questions.

A1 reference: `curriculum/levels/a1/design-review/01-abilities/`.

### Stage-1 critic

Challenge the architecture with these questions:

- Is every source ability traceable?
- Did we collapse different modalities because they share a topic?
- Did we create fake capabilities merely because many vocabulary items share a theme?
- Are assessment boundaries explicit?
- Are any capabilities so broad that later lesson design would hide multiple independent performances?
- Are any capabilities so narrow that they simply mirror individual source rows?

Do not lock the stage while unresolved orphan abilities remain.

---

## Stage 2 — Manual phrase review

Read every target-level phrase/chunk manually against the capability architecture.

For each phrase, record:

- exact source ID;
- primary semantic/capability home;
- useful cross-links;
- communicative function;
- boundary on what the phrase does **not** prove;
- any architecture change it suggests.

Primary home is not exclusive use. Recycling is expected.

Do not make automated string matching authoritative. Exact matching can be a review aid only.

### Important lesson from A1

Phrase evidence can legitimately alter the ability architecture. In A1, phrase review exposed missing/under-specified communicative functions and caused capability changes. The later levels must allow the same feedback loop.

### Phrase critic

For every phrase set, ask:

- Does this phrase naturally serve the assigned learner performance?
- Is it productive, receptive, formulaic, or contextual support — and are we prematurely assuming one?
- Are we accidentally treating a fixed phrase as evidence for a broad grammar system?
- Are time/past/future/comparison/etc. phrases creating an unjustified grammar claim?
- Are receptive signs/notices/instructions being converted into productive memorization tasks?
- Are there orphan phrases or phrases placed only because of superficial topic similarity?

Stage output should report zero silent exclusions and zero unexplained orphans.

A1 reference: `02-phrases/phrase-review.md`.

---

## Stage 3 — Manual grammar review

Read every canonical EGP row for the target level. Use reviewed grammar-family progression and GSE Grammar only as supporting evidence/cross-check.

For each grammar row/system, determine:

- usable learner meaning/function;
- capability homes;
- prerequisite grammar from earlier levels;
- whether multiple rows belong to one teachable system;
- whether the expected control is productive, formulaic, receptive, or embedded/supporting;
- explicit boundary preventing overgeneralization.

Do not build the curriculum as a grammar table-of-contents.

### Grammar critic

Reject any design that:

- makes one lesson per EGP row;
- assumes a phrase licenses a full productive system;
- teaches a higher-level grammar family early merely because one fixed lower-level chunk contains its form;
- merges grammar functions that differ communicatively;
- hides required grammar inside transfer/review lessons;
- moves grammar later than a capability that depends on it;
- expands source evidence into unrestricted tense/modal/comparison/narrative mastery.

A1 reference: `03-grammar/grammar-review.md`.

---

## Stage 4 — Manual word / lexical-content review

Read the target-level lexical inventory as content evidence, not as a giant flashcard syllabus.

For each lexical item or semantic batch, establish:

- natural capability/content homes;
- likely active/productive core vs recognition/receptive role;
- bounded sense/function relevant at this level;
- grammar-owned/system-owned treatment where appropriate;
- cross-unit reuse opportunities;
- whether the item lacks a natural communicative home and needs a lexical/reference/review treatment.

### Critical distinction

**Coverage home != productive mastery.**

A word can have a clear lesson home because the learner must encounter and understand it, while independent production may not be an exit requirement.

Likewise, `source row = one teaching object` is false. Broad lexical sets should use:

- active core;
- supported recognition;
- repeated contextual exposure;
- later fresh retrieval;
- cumulative exit evidence appropriate to the semantic role.

### Word critic

Ask:

- Would a real learner naturally need this word in the assigned task?
- Is the lesson becoming a vocabulary dump?
- Are multiple meanings being conflated?
- Are we promoting a word to productive control only because it exists in a published level list?
- Are abstract/meta/genre terms better treated as support/recognition?
- Does the lexical load exceed what a lesson can actually make learnable?

A1 reference: `04-words/word-review.md`.

---

## Stage 5 — Curriculum map: units and lesson slots

Only after abilities, phrases, grammar, and words have been semantically reviewed should the level be organized into a lesson sequence.

### Primary organizing rule

Organize primarily around **learner performances / communicative functions**, then attach the necessary:

- words;
- phrases;
- grammar;
- pronunciation;
- previous-level retrieval.

Do not organize the entire level primarily as vocabulary themes or grammar chapters.

### Let the number of lessons emerge

Do not start with a target like 45, 62, or any other fixed number.

The final number of units/lessons must emerge from:

- capability boundaries;
- prerequisites;
- introduction load;
- need for practice and fresh retrieval;
- transfer/consolidation opportunities;
- cumulative assessment coverage.

A level with more source rows does not necessarily need proportionally more lessons if those rows cluster naturally into usable systems. Conversely, a smaller source inventory can still need several lessons if performances are meaningfully distinct.

### Dependency ordering

Order lessons so prerequisites precede dependent performance. Consider:

- previous-level retained systems;
- new grammar dependencies;
- lexical prerequisites;
- discourse/repair resources;
- modality progression;
- increasing independence and reduced support.

### Curriculum-map critic

For each proposed lesson slot:

- What is the single primary learner performance?
- Why does this lesson need to exist separately?
- What new required content is introduced here?
- What earlier knowledge is prerequisite?
- What will be retrieved later in a changed context?
- Could this be merged without losing a meaningful assessment boundary?
- Should it be split because it hides two independent performances?
- Is a transfer/review lesson secretly introducing new required content?

A1 reference: `05-curriculum-map/curriculum-map.md`.

---

## Stage 6 — Exact coverage ledger and learning lifecycle

This stage converts the curriculum map into a machine-checkable exact source-record contract.

Every required primary item must appear in the ledger exactly and retain its source ID.

Use the lifecycle:

> **introduce → practice → fresh retrieval → recycle → consolidate → exit verify**

Not every item needs identical frequency or treatment, but no item may disappear after introduction.

### Required ledger properties

For each source item record:

- category;
- exact item/source ID;
- semantic/capability home(s);
- introduction lesson;
- practice evidence;
- later fresh retrieval;
- recycle/consolidation placement as appropriate;
- exit-verification path;
- semantic/control role where already known;
- notes/overrides when algorithmic assignment is not pedagogically correct.

Keep manual overrides explicit rather than hiding exceptions in code.

A1 reference structure:

```text
06-coverage-ledger/
  lifecycle-plan.json
  manual-source-overrides.json
  generated/
    coverage-ledger.json
    coverage-report.md
    load-attribution.md
```

### Coverage invariants

The audit should fail when any of these occurs:

- inventory item missing from ledger;
- duplicate/ambiguous primary ownership that violates the contract;
- orphan item with no introduction/home;
- item introduced but never retrieved later;
- item lacking exit verification where required;
- transfer lesson introducing hidden required records;
- lesson introduction load exceeds the agreed threshold without explicit review;
- ledger count does not equal target inventory total.

### Completion is not mastery

A ledger saying an item was introduced does **not** prove mastery. Exit evidence must be fresh enough to distinguish retained control from copying/recent rehearsal.

A1's coverage ledger ultimately represented all **1,337/1,337** A1 primary records with zero orphans and later retrieval/exit paths. Later levels must achieve their own exact totals.

---

## Stage 7 — Lesson authoring briefs and adversarial critic

Create one concise instructional brief per lesson slot. This is an authoring contract, not a finished lesson script.

Each brief should specify:

- primary learner performance;
- essential language/content core;
- semantic/grammar boundary;
- prerequisite/recycled resources;
- fresh evidence/retrieval design;
- exact introduction load by category;
- explicit note when the lesson must introduce zero new records.

### Global authoring rules carried from A1

1. Source record != separate teaching object.
2. One primary learner performance per instructional lesson.
3. Foreground only what the performance requires; assigned items may include supported exposure.
4. Broad lexical sets use active core + supported recognition + later retrieval.
5. Multiple EGP rows may describe one system; no one-rule-one-slide syllabus.
6. Use chunks before unnecessary grammar explanation.
7. Pronunciation attaches to use and intelligibility.
8. Transfer lessons introduce no hidden required content/system.
9. Fresh retrieval changes the prompt/context; it is not model repetition.
10. Mastery evidence cannot be copied from a complete model.
11. Receptive capabilities remain genuinely receptive where sources require reception.
12. If real authoring cannot fit naturally, reopen the architecture instead of hiding/rushing content.

### The critic pass is not optional

After all briefs exist, run an adversarial manual critic across the whole level.

Look specifically for:

- static vs movement language mixed incorrectly;
- time/date/frequency/duration overloaded into one fake lesson;
- lexical sets placed by topic rather than function;
- grammar introduced after it is already required;
- hidden new grammar/content inside transfer lessons;
- receptive targets replaced by productive tasks;
- future/past/comparison/modal boundaries expanded beyond evidence;
- lesson load spikes;
- missing spaced retrieval;
- units that are coherent as themes but incoherent as learner-performance progressions.

When the critic finds a problem, move the source records and re-run the ledger/load audit. Do not patch the prose only.

A1 reference: `07-lesson-briefs/lesson-briefs.md`.

---

# PART II — FORMAL SEMANTIC RECONCILIATION

## Stage 8 — Reconcile the finished design into a formal semantic lock

This is where A1 taught the most important process lesson.

### Do not start here too early

An early semantic-lock attempt created unnecessary ambiguity because an item can have a curriculum home before its final productive/receptive obligation is clear.

The stronger process is:

> **manual design evidence first → formal semantic role reconciliation second**

Once the capability map, phrase review, grammar review, word review, curriculum map, ledger, and lesson briefs exist, resolve item-level exit/control roles using that evidence.

### Typical semantic roles

Use level-appropriate roles. A1 used categories such as:

#### Words

- `productive_required`
- `receptive_required`
- `grammar_owned_required`

#### Phrases

- `productive_required`
- `formulaic_productive_required`
- `receptive_required`

#### Grammar

- `productive_control_required`
- `formulaic_productive_control_required`
- `receptive_control_required`
- `embedded_support_required`

#### Abilities

- productive performance;
- receptive performance;
- interactive performance;
- other explicit modality roles as the level requires.

#### Pronunciation

- intelligibility/support role appropriate to the reviewed strand progression.

Later levels may require additional distinctions. Do not force the A1 label set if the target source evidence needs a clearer category; add a well-defined role rather than mislabeling evidence.

### Semantic-lock safeguards

- Every item receives exactly one final primary semantic/control role.
- A lesson home does not determine productive control automatically.
- Fixed/formulaic language does not imply a broad grammar system.
- Published level membership does not prove unrestricted productive mastery.
- Use exact item IDs.
- Automatic matching is review assistance only, not final semantic judgment.
- If reviewing a frozen pending set, store an exact count/digest so future source drift cannot be silently accepted.
- Human-review queue must reach zero before curriculum-design authorization.

A1 reference: `curriculum/levels/a1/semantic-lock/`.

---

## Stage 9 — Authorization gate and deterministic finalization

When semantic review is complete:

- semantic report status should be locked/reviewed;
- human review queue = 0;
- `manifest.json` may set `lesson_design_authorized: true`;
- `exit_contract.json` should reflect the locked semantic inventory;
- **delivery/media production must remain a separate gate** unless explicitly authorized.

A1 intentionally distinguishes:

- curriculum lesson design / controlled authoring planning: authorized;
- mass lesson-package/audio/image/video production: not automatically authorized;
- existing `TEST-002`: untouched.

### Prevent rebuild drift

A major A1 engineering lesson: a base inventory builder can silently overwrite a manually authorized manifest/exit contract back to draft values.

Therefore pipeline order must end by restoring/finalizing the reviewed semantic state, e.g. conceptually:

> base inventories → grammar enrichment → granular abilities → semantic finalizer → tests/audits

A rebuild must reproduce the same authorized state. If it does not, the process is not done.

---

## Stage 10 — CI and final validation

Before declaring a level complete, validate the state in CI, not only by reading files.

At minimum verify:

1. full source-of-truth rebuild succeeds;
2. strict A1–C2 source coverage audit still passes;
3. target-level coverage-ledger audit passes;
4. unit tests for manifests/contracts pass;
5. semantic human-review queue is zero;
6. no generated rebuild changes the reviewed architecture unexpectedly;
7. previous level and other level folders remain intact;
8. delivery gates/licenses remain intact.

### GitHub Actions caveat learned in A1

Commits pushed by `github-actions[bot]` may not recursively trigger downstream workflows. Do not mistake “no downstream run” for success. When validating a newly changed audit/build dependency, trigger or run the relevant audit explicitly and inspect its result.

---

# PART III — THE CRITIC METHOD

## 11. What "critic-reviewed" means

Critic review is not proofreading. It is an adversarial attempt to prove the architecture wrong before lesson production.

Run the critic at the end of each stage and again across the complete level.

Use this checklist.

### A. Completeness

- Every source item accounted for?
- Any silent exclusion?
- Any orphan?
- Any duplicate ownership that creates contradictory obligations?
- All previous-level prerequisite assumptions explicit?

### B. Modality and performance integrity

- Reception still assessed as reception?
- Production still independent production where required?
- Interaction actually requires exchange, not solo sentence production?
- Mediation/repair/online/writing/text-type conditions preserved?

### C. Semantic/control boundaries

- Fixed phrase being mistaken for grammar mastery?
- One word sense being expanded to all senses?
- Receptive exposure promoted to productive mastery without evidence?
- Comparison/past/future/modal language overgeneralized?
- Supporting evidence incorrectly made a canonical target?

### D. Dependency correctness

- Prerequisite taught before dependent performance?
- Previous-level material retrieved rather than unnecessarily retaught?
- New system introduced early enough for later spaced retrieval?
- Higher-level system imported too early?

### E. Instructional load

- Too many source introductions in one lesson?
- Too many independent learner performances in one lesson?
- Vocabulary dump disguised as a communicative lesson?
- Grammar chapter disguised as a capability lesson?
- A split/merge needed?

### F. Retrieval and mastery

- Fresh retrieval actually changes context/prompt?
- Any item appears only once?
- Transfer lesson zero-new where claimed?
- Exit task fresh enough to test retained control?
- Completion/exposure being mistaken for mastery?

### G. Architectural honesty

- Are we preserving a lesson/unit merely because it existed before?
- Are we forcing a predetermined lesson count?
- Are we hiding awkward items instead of giving them an explicit home?
- Are prose docs and machine ledger telling the same story?

A critic finding that changes ownership, lifecycle, or load must be implemented in the underlying map/ledger and re-audited — not just mentioned in notes.

---

# PART IV — LESSONS LEARNED FROM A1

## 12. Mistakes to avoid repeating

### 12.1 Do not over-engineer semantic classification before the instructional map exists

Early A1 work spent too much effort trying to decide productive/receptive roles before enough lesson/capability context existed. The better order is design review first, formal semantic reconciliation later.

### 12.2 Do not confuse automation with manual review

Rule-based mapping built on reviewed data is useful, but it is not the same thing as reading an item and making a curriculum decision. Label outputs accurately.

### 12.3 Do not infer "productive word" from "member of a productive lexical set"

That is a candidate inference, not proof. The actual target must be supported by level evidence and learner performance needs.

### 12.4 Do not infer productivity from a phrase having a primary home

A phrase can be important for comprehension/context and still not be an independent productive exit requirement.

### 12.5 Exact matching is safer than fuzzy matching — but still not semantic judgment

A1 used exact normalized matching as a conservative aid. It intentionally undercounted rather than making fuzzy false-positive semantic claims. Human review supplied the final meaning.

### 12.6 Do not force legacy lesson counts

A1's old 45-lesson architecture was not treated as a constraint. The reviewed design became 62 slots because that is what the evidence/load/dependencies required. A2–C2 must also be allowed to land elsewhere.

### 12.7 Transfer must not become a hiding place

A1 critic passes found hidden new material in transfer slots and moved it into real instructional lessons. Later levels should enforce the same rule mechanically where possible.

### 12.8 Source-record coverage is necessary but insufficient

100% coverage can coexist with poor learning design. Coverage must be paired with lifecycle, fresh retrieval, load control, and exit evidence.

### 12.9 Builder order matters

Generated base files can overwrite reviewed status. Final semantic state must be restored deterministically after base generation/enrichment.

### 12.10 Curriculum authorization is not delivery authorization

Do not let `lesson_design_authorized: true` bypass a live delivery experiment, licensing gate, or media-production gate.

---

# PART V — LEVEL-SPECIFIC ADAPTATION

## 13. A2

Design A2 as cumulative from locked A1.

Important implications:

- do not reclassify A1 content as new A2 inventory;
- use A1 exit capabilities as prerequisites/retrieval material;
- A2 has substantially more new grammar and abilities than A1, so capability grouping and dependency analysis are likely to matter more than simple lexical theming;
- do not assume A1's lesson load thresholds transfer unchanged without checking actual A2 systems and expected learner independence.

## 14. B1

B1 typically introduces greater independence, broader discourse, and more integrated performance. Critic review must guard against:

- turning broad ability statements into oversized lessons;
- under-allocating fresh retrieval for larger grammar/discourse systems;
- treating increased range as permission for unlimited productive scope.

## 15. B2

B2 has the largest word inventory among A1–C2 in the current files. This makes lexical architecture especially important:

- active core vs receptive range must be deliberate;
- do not inflate lesson count by treating every lexical row independently;
- use domains/functions/text types to create coherent retrieval networks;
- keep capability and discourse progression central.

## 16. C1

C1 has fewer required granular abilities than B2 but still a large lexical inventory. Do not interpret fewer ability rows as a simpler course. Higher-level performances may be broader and more demanding.

Critic should focus on:

- discourse precision;
- register/text-type boundaries;
- productive range vs recognition;
- integrated skills;
- whether broad capabilities need multiple lessons/evidence events despite one top-level capability label.

## 17. C2

C2 differs materially from A1–C1:

- lexical inventory comes from Pearson GSE C2 General Learner snapshot;
- 609 lexical meanings + 41 phrase/chunk entries in current level files;
- phrase records include direct source phrases/phrasal verbs and collocations with owner-record inheritance semantics;
- `commercial_permission_required` must remain visible;
- architecture/research may continue without pretending the licensing gate is cleared.

Do not force the Oxford A1–C1 phrase/word handling code onto C2 without adapting to the C2 source schema.

---

# PART VI — DEFINITION OF DONE

## 18. A level is not complete until all of these are true

### Source/inventory

- target inventories reconcile exactly to reviewed sources;
- no duplicated primary IDs;
- source/licensing metadata preserved.

### Manual design review

- every required ability manually dispositioned and traceable;
- every phrase reviewed and homed/bounded;
- every grammar row reviewed and mapped to usable systems/performances;
- every word/lexical item reviewed into a semantic/content home with appropriate control boundary;
- no silent exclusions or unexplained orphans.

### Curriculum architecture

- dependency-aware unit/lesson map exists;
- lesson count is evidence-led, not predetermined;
- each instructional lesson has one primary performance;
- review/transfer/consolidation slots are explicit;
- previous-level cumulative knowledge has planned retrieval.

### Coverage/lifecycle

- every target primary item present in exact ledger;
- introduction exists;
- later fresh retrieval exists;
- recycle/consolidation exists where appropriate;
- exit verification exists;
- no hidden new records in transfer slots;
- load audit passes.

### Lesson briefs / critic

- every slot has an authoring brief;
- full-stage critic complete;
- critic corrections propagated into map + ledger;
- audits re-run after corrections.

### Semantic lock

- final item-level control role reconciled;
- human-review queue = 0;
- semantic report locked;
- manifest/exit contract agree with the report.

### Engineering

- full rebuild is deterministic;
- source-of-truth audit passes;
- target coverage audit passes;
- tests pass;
- reviewed state survives regeneration;
- delivery/media gates remain separate and unchanged unless explicitly authorized.

Only then may `lesson_design_authorized` be true for that level.

---

# PART VII — NEW-CHAT EXECUTION INSTRUCTIONS

## 19. Minimal handoff prompt for a future conversation

A user can say:

> Work on the next English-course level using `docs/LEVEL_CURRICULUM_DESIGN_PLAYBOOK_V1.md` as the authoritative process. Read the current status and target level inventories first. Reproduce the A1 method, not the A1 numbers. Keep main/TEST-002 untouched. Continue until the current stage is fully reviewed/audited, and use adversarial critic passes rather than accepting automatic mappings as semantic truth.

The assistant should then:

1. inspect the current branch head and status;
2. read this playbook;
3. read target level `manifest`, inventories, `exit_contract`, and sources;
4. read previous-level exit contract;
5. run/inspect source audit;
6. create/continue the target level `design-review/` stages in order;
7. report concrete stage counts, unresolved items, and critic findings;
8. commit changes only on the independent curriculum branch/workstream;
9. validate with CI before declaring a stage locked;
10. never assume prior chat history is required.

---

## 20. Reference A1 artifacts

A1 is the completed process example. Use it to understand file shapes and review depth:

```text
curriculum/levels/a1/design-review/
  01-abilities/
    README.md
    manual-review-log.md
    final-capability-map.md
  02-phrases/
    phrase-review.md
  03-grammar/
    grammar-review.md
  04-words/
    word-review.md
  05-curriculum-map/
    curriculum-map.md
  06-coverage-ledger/
    lifecycle-plan.json
    manual-source-overrides.json
    generated/
      coverage-ledger.json
      coverage-report.md
      load-attribution.md
  07-lesson-briefs/
    lesson-briefs.md

curriculum/levels/a1/semantic-lock/
  ... reviewed decision maps and generated semantic-lock reports ...
```

The exact A1 filenames/scripts may evolve. The **process invariants in this playbook** are the authoritative reusable method.

---

## 21. Final operating principle

The process can be summarized as:

> **Inventory → manual capability architecture → phrase/grammar/word semantic review → dependency-aware curriculum map → exact lifecycle ledger → lesson briefs → adversarial critic → formal semantic lock → deterministic authorization → CI.**

Or, in practical terms:

> We already know what the learner needs to know. The job is to build the best sequence that makes them actually learn it, retrieve it later, and prove it at exit — with nothing silently missing and nothing falsely claimed as mastery.
