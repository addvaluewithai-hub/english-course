# Level Curriculum Design Playbook v1

Status: **AUTHORITATIVE PROCESS HANDOFF**  
Scope: **A2, B1, B2, C1, C2**  
Reference implementation: **A1 on `curriculum/level-source-of-truth-v1`**  
Purpose: allow a new ChatGPT conversation, with no prior chat history, to reproduce the reviewed A1 curriculum-design method safely and consistently for later levels.

---

## 1. Read this first in a new conversation

If there is no chat history, do **not** reconstruct the process from memory and do **not** begin by inventing lessons.

Start by reading:

1. this file;
2. `docs/LEVEL_SOURCE_OF_TRUTH_STATUS_V1.md`;
3. `docs/LEVEL_SOURCE_OF_TRUTH_V1.md`;
4. the target level folder under `curriculum/levels/<level>/`;
5. the target level `exit_contract.json`, `manifest.json`, and `sources.json`;
6. the immediately previous level's locked `exit_contract.json` and `manifest.json`;
7. A1's completed reference artifacts under `curriculum/levels/a1/design-review/` and `curriculum/levels/a1/semantic-lock/` only as **process examples**, not as content/templates to copy blindly.

If an old A1 README or transient note conflicts with this playbook, the current status document, final reviewed artifacts, or machine audits, treat the old note as stale. The playbook plus current locked artifacts are authoritative.

Work on the independent curriculum branch/workstream. Do **not** modify `main`, the existing first-ten pilot, `automation/STATE.json`, or `TEST-002` unless explicitly instructed later.

The core goal is:

> Turn the complete source inventory for a level into a teachable, dependency-aware curriculum in which every required source item has an explicit, role-appropriate learning lifecycle and exit obligation, without confusing source coverage with mastery or forcing every source row to become a separate lesson objective.

---

## 2. What must be copied from A1 — and what must NOT be copied

### Copy the method

Copy these principles and gates:

- source inventory first;
- abilities/learner performance drive the architecture;
- phrases, grammar, words, pronunciation, and previous-level retrieval attach to real learner performances;
- manual semantic review is authoritative where pedagogical meaning is involved;
- automation checks completeness, exact IDs, lifecycle coverage, load, and reproducibility;
- curriculum architecture is allowed to change while evidence is reviewed;
- lesson count emerges from dependencies and load rather than a preset number;
- every required item receives an explicit learning path appropriate to its eventual control role;
- transfer/review lessons cannot hide new required content;
- final productive/receptive/formulaic/support obligations are reconciled after the instructional architecture is understood;
- semantic reconciliation is allowed to reopen earlier design decisions;
- curriculum-design authorization is separate from delivery/media-production authorization;
- CI must reproduce the final reviewed state without silently reverting it.

### Do NOT copy A1's numbers or shape

Do **not** assume later levels should have:

- 10 units;
- 62 lesson slots;
- the same capability count;
- the same proportion of productive vs receptive words/phrases/grammar;
- the same lexical load per lesson;
- the same transfer pattern;
- the same grammar family distribution;
- the same semantic categories or topic sequence;
- the same raw-count load thresholds.

A2–C2 must emerge from their own source evidence, prerequisite structure, cumulative exit contract, semantic/control roles, and instructional load.

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

Therefore, when designing A2, B1, B2, C1, or C2, the target level's new content is not the whole learner state. The previous level's locked exit contract is prerequisite retained knowledge and must be deliberately retrieved/recycled where needed.

### Current inventory-count snapshot

The counts below are a planning snapshot as of **2026-09-24**. The target level's current manifest/status files are authoritative if they ever differ.

| Level | Words / lexical meanings | Phrases / chunks | EGP grammar features | Required granular abilities | Pronunciation strands |
| --- | ---: | ---: | ---: | ---: | ---: |
| A1 | 900 | 199 | 109 | 119 | 10 |
| A2 | 871 | 176 | 291 | 269 | 10 |
| B1 | 809 | 175 | 338 | 249 | 10 |
| B2 | 1,427 | 125 | 243 | 270 | 10 |
| C1 | 1,315 | 75 | 129 | 59 | 10 |
| C2 | 609 | 41 | 112 | 19 | 10 |

These are source-record counts, not teaching-object counts. Multiple rows may describe one teachable system, one row may support several performances, and some source items may be primarily receptive or supporting rather than independent productive targets.

---

## 4. Source hierarchy and evidence rules

Use the existing reviewed source architecture rather than substituting a new syllabus.

### Words

- A1–C1 lexical source: Oxford 3000/5000 partition already represented in level inventories.
- C2 lexical source: Pearson GSE Vocabulary C2 General Learner snapshot.
- A source word row does not automatically imply unrestricted productive mastery of all senses/collocations.
- Same surface form across levels does not mean duplicate learning. Check sense, part of speech, guideword/function, collocation, and expected control.

### Phrases

- A1–C1: current official Oxford Phrase List snapshot.
- C2: Pearson GSE vocabulary phrase/phrasal-verb records plus attached collocations according to source semantics.
- A phrase having a lesson home does not automatically mean it is an independent productive exit requirement.
- A fixed lower-level phrase does not license a broader higher-level grammar system.

### Grammar

- Canonical target inventory: English Grammar Profile rows in `grammar.json`.
- Pearson GSE Grammar is supporting/cross-check evidence, not a second canonical target inventory.
- Several EGP rows may jointly describe one usable grammar system; do not create one lesson per row.
- Conversely, do not merge rows if doing so erases a real meaning, form, function, modality, discourse, or control boundary.
- A familiar form can still be new at the target level if its function/control requirement is new.

### Abilities

- Use the granular reviewed CEFR/GSE assignments in `abilities.json`.
- `include_for_spine` items are the required new-at-level ability inventory.
- Keep reception, production, interaction, mediation, online interaction, writing/text type, and other modality distinctions visible.
- A final capability is not automatically one lesson.
- If one source ability is design-split into multiple performance components, the source item remains **one source record** with multiple design mappings. Never inflate source counts because a source statement was split pedagogically.

### Pronunciation

- Use the reviewed 10-strand progression at the target level.
- Attach pronunciation to actual communicative use and intelligibility.
- Do not turn pronunciation strands into isolated accent-perfection requirements.

### C2 licensing and owner-inherited evidence

Pearson GSE-derived C2 lexical content carries `commercial_permission_required`. Curriculum architecture/research may proceed, but do not imply commercial clearance and do not remove the production gate.

For C2 attached/owner-inherited collocations, distinguish **primary required inventory items** from supporting evidence inherited from an owner record. Do not automatically create a new independent semantic obligation for every attached collocation. Promote attached evidence to an independent obligation only by explicit human review.

---

## 5. Automation boundary — strict rule

Automation may:

- expand explicit human mappings to exact source IDs;
- count and reconcile records;
- detect missing/duplicate/orphan records;
- generate compact review aids;
- calculate lesson load and lifecycle coverage;
- enforce invariants;
- reproduce reviewed decisions deterministically.

Automation may **not** claim final human review merely because it:

- clustered by similarity;
- matched strings;
- inherited a role from a lexical set;
- inferred a semantic home from tags;
- inferred productive/receptive status from a rule;
- copied a previous level's structure.

Any such output is a **candidate/review aid** until a human/manual curriculum decision accepts or changes it.

---

# PART I — THE DESIGN PIPELINE

## Stage 0 — Preflight and invariants

Before manual curriculum design begins:

1. verify the target level's eight standard files exist;
2. verify manifest counts match inventories;
3. run/inspect the strict source-of-truth audit;
4. confirm there are no source-coverage gaps or duplicated primary IDs;
5. read the target level exit contract and its current status;
6. read the previous level locked exit contract and manifest;
7. confirm target-level licensing/production gates;
8. create a target-level `design-review/` workspace without changing existing delivery lessons.

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

`lesson_design_authorized: false` at this point does **not** forbid curriculum research/design review. It means the target level is still a candidate design and must not yet be treated as the authoritative controlled-authoring contract.

Do not authorize delivery/media production at this stage.

### Stage-0 critic

Fail the stage if:

- source totals do not reconcile;
- target content is mixed with another level without an explicit cumulative/recycle reason;
- source licensing gates are lost;
- an old syllabus/lesson count is being treated as authoritative;
- the process is already assuming a unit count or lesson count;
- the previous level is being silently edited to make the target level easier.

### Previous-level immutability rule

A previously locked level is immutable by default. If target-level work exposes a real contradiction or missing prerequisite in the previous level:

1. record the cross-level issue explicitly;
2. do not silently patch the previous level;
3. reopen the previous semantic/design lock only by an explicit decision;
4. re-run all affected audits and downstream reconciliation after the fix.

---

## Stage 1 — Manual ability review: capabilities + cross-cutting requirements

This is the architectural starting point.

A1's strongest rule was:

> No clustering script, heuristic, legacy lesson map, or previous unit sequence decides the final capability structure.

Read **every required ability** at the target level. Give each source ability an explicit manual disposition such as:

- `KEEP` — distinct learner-performance component;
- `MERGE` — represented under a broader capability without losing its assessment boundary;
- `SPLIT` — source statement contains meaningfully distinct learner performances;
- `SUPPORTING` — important condition/evidence, but not a standalone final capability.

Produce **two outputs**, not one:

1. **Capability Architecture** — top-level learner-performance families.
2. **Cross-cutting Requirements** — requirements that matter across capabilities but should not become fake standalone lessons/capabilities.

Typical cross-cutting examples include:

- repair strategies;
- spelling/written-form support;
- punctuation/capitalization where required;
- discourse expansion/linking;
- intelligibility/pronunciation conditions;
- input-speed/familiar-context conditions;
- interaction support conditions;
- text-type/register conditions.

### Required safeguards

- Similar topic does not imply same capability.
- Listening/reading reception cannot be silently replaced by a speaking task.
- Production cannot be inferred merely because a learner can recognize something.
- Interaction requirements must remain interaction requirements.
- Conditions such as slow/clear speech, familiar context, partner support, repair, or text type must remain visible where source evidence requires them.
- A capability is a learner-performance boundary, not automatically a lesson title.
- Later phrase/grammar/word/pronunciation evidence may reopen the architecture.
- A `SPLIT` creates design components, not duplicate source records.

### File hygiene

Prefer one working/final authoritative file per stage where practical. Critic findings should normally be folded into the authoritative stage file once resolved. Delete superseded candidate/v1/v2/critic artifacts when they no longer serve an audit purpose. Do not create file-version sprawl as a substitute for making a decision.

### Stage-1 critic

Challenge the architecture with these questions:

- Is every source ability traceable?
- Did we collapse different modalities because they share a topic?
- Did we create fake capabilities because vocabulary shares a theme?
- Did a cross-cutting requirement accidentally become a fake top-level capability?
- Are assessment boundaries explicit?
- Are any capabilities so broad that later lesson design would hide multiple independent performances?
- Are any capabilities so narrow that they simply mirror individual source rows?

Do not lock the stage while unresolved orphan abilities remain.

A1 reference: `curriculum/levels/a1/design-review/01-abilities/`.

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

Phrase evidence can legitimately alter the ability architecture. In A1, phrase review exposed missing/under-specified communicative functions and caused capability changes. Later levels must allow the same feedback loop.

### Phrase critic

For every phrase set, ask:

- Does this phrase naturally serve the assigned learner performance?
- Is it likely productive, receptive, formulaic, or contextual support — and are we prematurely assuming one?
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
- likely control type without prematurely finalizing it;
- explicit boundary preventing overgeneralization.

Do not build the curriculum as a grammar table of contents.

### Grammar critic

Reject any design that:

- makes one lesson per EGP row;
- assumes a phrase licenses a full productive system;
- teaches a higher-level grammar family early merely because one fixed lower-level chunk contains its form;
- merges grammar functions that differ communicatively;
- hides required grammar inside transfer/review lessons;
- moves grammar later than a capability that depends on it;
- expands source evidence into unrestricted tense/modal/comparison/narrative mastery;
- marks a familiar surface form as duplicate without checking whether the target-level function/control is new.

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
- whether the item lacks a natural communicative home and needs lexical/reference/review treatment.

### Critical distinction

**Coverage home != productive mastery.**

A word can have a clear lesson home because the learner must encounter and understand it, while independent production may not be an exit requirement.

Likewise, `source row = one teaching object` is false. Broad lexical sets should use:

- active core;
- supported recognition;
- repeated contextual exposure;
- later fresh retrieval;
- cumulative exit evidence appropriate to the final semantic role.

### Same-form / new-function rule

Do not dismiss an item because its headword/string appeared at an earlier level. Check:

- source record/sense;
- part of speech;
- guideword/meaning;
- collocation/frame;
- learner function;
- expected control.

The same surface form may represent a genuinely new target-level obligation.

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

## Stage 4.5 — Pronunciation, target-exit constraints, and previous-level carry-forward

Before building units/lessons, explicitly reconcile three constraints that should not be left implicit.

### A. Pronunciation review

Read all target-level pronunciation stages and determine:

- natural capability/lesson homes;
- progression across the level;
- intelligibility goal;
- where fresh pronunciation retrieval should occur;
- what must not be turned into accent perfection.

### B. Target exit-contract constraints

Read the target level exit contract as a design constraint. Identify:

- mandatory cumulative performance claims;
- modality requirements;
- freshness/independence conditions;
- any claim that requires more than one lesson/evidence event.

Do not wait until the end to discover that the lesson map cannot support the exit contract.

### C. Previous-level carry-forward map

Create an explicit prerequisite/retrieval map showing which locked previous-level capabilities/systems are:

- assumed retained;
- deliberately refreshed;
- prerequisites for new target-level content;
- scheduled for fresh retrieval without being reclassified as new target-level inventory.

This is what makes the course genuinely cumulative rather than a sequence of isolated levels.

### Stage-4.5 critic

Fail/reopen earlier stages if:

- a pronunciation target has no natural use context;
- a target exit claim has no plausible evidence path;
- a previous-level prerequisite is silently being retaught as new content;
- a new target-level system depends on an unstated prerequisite;
- carry-forward material is absent long enough that later performance assumes unverified retention.

---

## Stage 5 — Curriculum map: units and lesson slots

Only after abilities, phrases, grammar, words, pronunciation, target-exit constraints, and carry-forward dependencies have been reviewed should the level be organized into a lesson sequence.

### Primary organizing rule

Organize primarily around **learner performances / communicative functions**, then attach the necessary:

- words;
- phrases;
- grammar;
- pronunciation;
- cross-cutting requirements;
- previous-level retrieval.

Do not organize the entire level primarily as vocabulary themes or grammar chapters.

### Lesson-performance rule

Each instructional lesson should have **one primary communicative/evidence outcome**. At higher levels, that outcome may legitimately integrate skills (for example: read evidence → evaluate → discuss) if the sequence forms one coherent performance. Do not interpret this rule as “one micro-skill only.”

### Let the number of lessons emerge

Do not start with a target like 45, 62, or any other fixed number.

The final number of units/lessons must emerge from:

- capability boundaries;
- prerequisites;
- introduction load;
- need for practice and fresh retrieval;
- transfer/consolidation opportunities;
- cumulative assessment coverage;
- expected learner independence.

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

- What is the single primary communicative/evidence outcome?
- Why does this lesson need to exist separately?
- What new required content is introduced here?
- What earlier knowledge is prerequisite?
- What will be retrieved later in a changed context?
- Could this be merged without losing a meaningful assessment boundary?
- Should it be split because it hides independent performances?
- Is a transfer/review lesson secretly introducing new required content?

A1 reference: `05-curriculum-map/curriculum-map.md`.

---

## Stage 6 — Provisional exact coverage ledger and learning lifecycle

This stage converts the curriculum map into a machine-checkable exact source-record contract **before final semantic/control roles are locked**.

Every required primary item must appear in the ledger exactly and retain its source ID.

Use the provisional lifecycle:

> **introduce/use → practice/contextual use → later fresh retrieval → recycle/consolidate → provisional exit path**

The purpose is to prove that every required source item has a real instructional home and later contact. It is **not yet** a claim that every item needs the same type of exit test.

### Required ledger properties

For each source item record:

- category;
- exact item/source ID;
- semantic/capability home(s);
- introduction/use lesson;
- practice/contextual evidence;
- later fresh retrieval;
- recycle/consolidation placement as appropriate;
- provisional exit-verification path;
- semantic/control role where already strongly evidenced, otherwise `pending reconciliation`;
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
- item introduced but never encountered/retrieved later;
- no plausible provisional exit path;
- transfer lesson introducing hidden required records;
- ledger count does not equal target primary inventory total.

### Load guardrails

Raw source-count thresholds are **mechanical warning/guardrail signals**, not proof that a lesson is pedagogically light or heavy.

Human load review must also consider:

- number of independent systems/functions;
- active lexical core vs supported recognition;
- task complexity;
- modality demands;
- processing/production burden;
- learner independence expected at the level.

Do not copy A1 load thresholds blindly into later levels.

### Completion is not mastery

A ledger saying an item was introduced does **not** prove mastery. Final semantic roles and role-appropriate exit evidence are reconciled later in Stage 8/8.5.

---

## Stage 7 — Lesson authoring briefs + rolling adversarial critic

Create one concise instructional brief per lesson slot. This is an authoring contract candidate, not a finished lesson script.

Each brief should specify:

- primary communicative/evidence outcome;
- essential foreground language/content core;
- embedded/support content;
- semantic/grammar boundary;
- prerequisite/recycled resources;
- pronunciation/cross-cutting integration;
- fresh evidence/retrieval design;
- exact introduction load by category;
- explicit note when the lesson must introduce zero new required records.

### Global authoring rules carried from A1

1. Source record != separate teaching object.
2. One primary communicative/evidence outcome per instructional lesson; coherent integrated-skill performance is allowed.
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

### Rolling critic is mandatory

Do **not** wait until all lesson briefs are written.

Run a human adversarial critic:

- after each unit or sensible batch;
- whenever load/semantic placement feels unnatural;
- again across the complete level after all briefs exist.

Look specifically for:

- static vs movement language mixed incorrectly;
- time/date/frequency/duration or other related systems overloaded into one fake lesson;
- lexical sets placed by topic rather than function;
- grammar introduced after it is already required;
- hidden new grammar/content inside transfer lessons;
- receptive targets replaced by productive tasks;
- future/past/comparison/modal/discourse boundaries expanded beyond evidence;
- lesson load spikes hidden by acceptable raw counts;
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

> **manual design evidence first → formal semantic-role reconciliation second**

Once the capability map, phrase review, grammar review, word review, pronunciation/exit/carry-forward review, curriculum map, provisional ledger, and lesson briefs exist, resolve item-level exit/control roles using that evidence.

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

- Every **primary required inventory item** receives exactly one final primary semantic/control role.
- Attached/owner-inherited supporting evidence is not automatically promoted to a new independent obligation.
- A lesson home does not determine productive control automatically.
- Fixed/formulaic language does not imply a broad grammar system.
- Published level membership does not prove unrestricted productive mastery.
- Same surface form across levels must be checked for sense/function/control progression.
- Use exact item IDs.
- Automatic matching is review assistance only, not final semantic judgment.
- If reviewing a frozen pending set, store an exact count/digest so future source drift cannot be silently accepted.
- Human-review queue must reach zero before curriculum-design authorization.

A1 reference: `curriculum/levels/a1/semantic-lock/`.

---

## Stage 8.5 — Role-aware lifecycle and brief reconciliation

Stage 8 can invalidate assumptions made in the provisional Stage-6 ledger or Stage-7 briefs. This reconciliation is mandatory.

For every final semantic/control role, verify that the learning path matches the obligation.

Examples:

- **productive item** → must receive opportunities for independent/controlled production plus later fresh production evidence appropriate to the level;
- **receptive item** → comprehension/recognition evidence may be appropriate; do not invent an independent production requirement;
- **formulaic productive item** → require bounded chunk/frame use, not unrestricted grammar generalization;
- **embedded/support item** → may be evidenced inside a larger performance rather than by a standalone exit item;
- **grammar-owned lexical item** → do not double-assess it as a separate lexical mastery target unless explicitly justified;
- **pronunciation support** → verify intelligibility within real performance rather than isolated accent scoring unless the strand specifically requires otherwise.

### Required feedback loop

If Stage 8 changes an assumption that appears in the map, ledger, or briefs:

1. update the underlying human design artifact;
2. update lifecycle/lesson ownership as needed;
3. update the brief if foreground/embedded treatment changed;
4. re-run load and coverage audits;
5. re-check transfer lessons for hidden new content;
6. re-check exit evidence for role appropriateness.

Do not allow the semantic report and lesson briefs to tell different stories.

### Final lifecycle after reconciliation

The final role-aware lifecycle is conceptually:

> **introduce/use → practice → fresh retrieval → recycle → consolidate → role-appropriate exit verify**

Not every role uses identical evidence, frequency, or assessment form.

---

## Stage 9 — Authorization gate and deterministic finalization

When semantic review **and Stage-8.5 reconciliation** are complete:

- semantic report status should be locked/reviewed;
- human review queue = 0;
- coverage/lifecycle audits pass after reconciliation;
- briefs and ledger agree with final semantic roles;
- `manifest.json` may set `lesson_design_authorized: true`;
- `exit_contract.json` should reflect the locked semantic inventory;
- **delivery/media production must remain a separate gate** unless explicitly authorized.

A1 intentionally distinguishes:

- curriculum lesson design / controlled authoring planning: authorized;
- mass lesson-package/audio/image/video production: not automatically authorized;
- existing `TEST-002`: untouched.

### Meaning of `lesson_design_authorized`

- `false` → design research/review may continue, but the level remains a candidate and should not be treated as the final controlled-authoring contract.
- `true` → semantic/design reconciliation is locked enough to serve as the authoritative curriculum authoring contract, subject to separate delivery/media gates.

### Prevent rebuild drift

A major A1 engineering lesson: a base inventory builder can silently overwrite a manually authorized manifest/exit contract back to draft values.

Therefore pipeline order must end by restoring/finalizing the reviewed semantic state, e.g. conceptually:

> base inventories → grammar enrichment → granular abilities → reviewed semantic finalizer → tests/audits

A rebuild must reproduce the same authorized state. If it does not, the process is not done.

---

## Stage 10 — CI and final validation

Before declaring a level complete, validate the state in CI, not only by reading files.

At minimum verify:

1. full source-of-truth rebuild succeeds;
2. strict A1–C2 source coverage audit still passes;
3. target-level coverage/lifecycle audit passes after Stage 8.5;
4. unit tests for manifests/contracts pass;
5. semantic human-review queue is zero;
6. no generated rebuild changes the reviewed architecture unexpectedly;
7. previous level and other level folders remain intact;
8. delivery gates/licenses remain intact;
9. role-aware lifecycle and exit evidence remain consistent after regeneration.

### GitHub Actions caveat learned in A1

Commits pushed by `github-actions[bot]` may not recursively trigger downstream workflows. Do not mistake “no downstream run” for success. When validating a newly changed audit/build dependency, trigger or run the relevant audit explicitly and inspect its result.

---

# PART III — THE CRITIC METHOD

## 11. What "critic-reviewed" means

Critic review is not proofreading. It is an adversarial attempt to prove the architecture wrong before authoring/production.

Run the critic at the end of each stage, during lesson-brief batches, after semantic reconciliation, and again across the complete level.

### A. Completeness

- Every primary source item accounted for?
- Any silent exclusion?
- Any orphan?
- Any duplicate ownership that creates contradictory obligations?
- Are owner-inherited/supporting records being mistaken for extra primary obligations?
- All previous-level prerequisite assumptions explicit?

### B. Modality and performance integrity

- Reception still assessed as reception?
- Production still independent production where required?
- Interaction actually requires exchange, not solo sentence production?
- Mediation/repair/online/writing/text-type conditions preserved?
- Cross-cutting requirements preserved without fake capabilities?

### C. Semantic/control boundaries

- Fixed phrase being mistaken for grammar mastery?
- One word sense being expanded to all senses?
- Receptive exposure promoted to productive mastery without evidence?
- Comparison/past/future/modal/discourse language overgeneralized?
- Supporting evidence incorrectly made a canonical target?
- Same surface form wrongly dismissed as duplicate despite new meaning/function/control?

### D. Dependency correctness

- Prerequisite taught/retrieved before dependent performance?
- Previous-level material retrieved rather than unnecessarily reclassified/re-taught?
- New system introduced early enough for later spaced retrieval?
- Higher-level system imported too early?
- Was a previous locked level silently changed rather than explicitly reopened?

### E. Instructional load

- Too many raw source introductions in one lesson?
- More importantly, too many independent systems/functions in one lesson?
- Vocabulary dump disguised as a communicative lesson?
- Grammar chapter disguised as a capability lesson?
- Active lexical core too large despite a reasonable total record count?
- Task/modality complexity too high for the target learner?
- A split/merge needed?

### F. Retrieval and mastery

- Fresh retrieval actually changes context/prompt?
- Any item appears only once?
- Transfer lesson zero-new where claimed?
- Exit task fresh enough to test retained control?
- Does exit evidence match the final semantic role?
- Completion/exposure being mistaken for mastery?

### G. Architectural honesty

- Are we preserving a lesson/unit merely because it existed before?
- Are we forcing a predetermined lesson count?
- Are we hiding awkward items instead of giving them an explicit home?
- Are prose docs, semantic roles, and machine ledger telling the same story?
- Are we creating version-file sprawl instead of folding resolved critic decisions into authoritative files?

A critic finding that changes ownership, semantic role, lifecycle, or load must be implemented in the underlying map/ledger/briefs and re-audited — not just mentioned in notes.

---

# PART IV — LESSONS LEARNED FROM A1

## 12. Mistakes to avoid repeating

### 12.1 Do not over-engineer semantic classification before the instructional map exists

Early A1 work spent too much effort trying to decide productive/receptive roles before enough lesson/capability context existed. The better order is design review first, formal semantic reconciliation later.

### 12.2 Do not confuse automation with manual review

Rule-based mapping built on reviewed data is useful, but it is not the same thing as reading an item and making a curriculum decision. Label outputs accurately.

### 12.3 Do not infer "productive word" from "member of a productive lexical set"

That is a candidate inference, not proof. The actual target must be supported by level evidence and learner-performance needs.

### 12.4 Do not infer productivity from a phrase having a primary home

A phrase can be important for comprehension/context and still not be an independent productive exit requirement.

### 12.5 Exact matching is safer than fuzzy matching — but still not semantic judgment

A1 used exact normalized matching as a conservative aid. It intentionally undercounted rather than making fuzzy false-positive semantic claims. Human review supplied the final meaning.

### 12.6 Do not force legacy lesson counts

A1's old 45-lesson architecture was not treated as a constraint. The reviewed design became 62 slots because that is what the evidence/load/dependencies required. A2–C2 must also be allowed to land elsewhere.

### 12.7 Transfer must not become a hiding place

A1 critic passes found hidden new material in transfer slots and moved it into real instructional lessons. Later levels should enforce the same rule mechanically where possible.

### 12.8 Source-record coverage is necessary but insufficient

100% coverage can coexist with poor learning design. Coverage must be paired with lifecycle, fresh retrieval, role-aware evidence, load control, and exit verification.

### 12.9 Builder order matters

Generated base files can overwrite reviewed status. Final semantic state must be restored deterministically after base generation/enrichment.

### 12.10 Curriculum authorization is not delivery authorization

Do not let `lesson_design_authorized: true` bypass a live delivery experiment, licensing gate, or media-production gate.

### 12.11 Provisional lifecycle is not final assessment policy

Before semantic roles are locked, the ledger proves that content has a learning path. It does not prove that every item deserves the same type of exit test. Stage 8.5 must reconcile the lifecycle to the final role.

### 12.12 Previous locked levels are not silently editable dependencies

If a later level exposes a genuine earlier-level defect, reopen the earlier level explicitly and re-audit. Do not patch history invisibly.

### 12.13 File proliferation can hide indecision

Prefer a small set of authoritative stage files. Once a critic decision is resolved, fold it into the final stage artifact and remove superseded candidate copies unless audit/history value justifies keeping them.

---

# PART V — LEVEL-SPECIFIC RISK PROMPTS

The sections below are **risk prompts to investigate from the target inventory**, not assumptions that override source evidence.

## 13. A2 risk prompts

Because A2 is cumulative from locked A1, investigate whether:

- A1 exit capabilities are being used as prerequisites/retrieval rather than reclassified as new A2 content;
- A2's larger grammar/ability inventory creates dependency clusters that need careful sequencing;
- raw A1 lesson-load thresholds are inappropriate for A2;
- familiar A1 forms acquire genuinely new A2 functions/control requirements.

Do not assume these patterns; verify them from A2 evidence.

## 14. B1 risk prompts

Investigate whether B1 evidence requires:

- more learner independence;
- broader discourse/integrated performance;
- larger systems needing multiple spaced evidence events;
- capability labels that are broad enough to require several lessons rather than one oversized lesson.

Do not convert “greater range” into unlimited productive scope.

## 15. B2 risk prompts

The current B2 files contain the largest word inventory among A1–C2, so explicitly investigate:

- active core vs receptive range;
- whether lexical items form coherent functional/domain/text-type networks;
- whether lesson count is being inflated by treating lexical rows independently;
- whether capability/discourse progression remains central despite lexical volume.

## 16. C1 risk prompts

The current C1 inventory has fewer required granular abilities than B2 but a large lexical inventory. Investigate:

- discourse precision;
- register/text-type boundaries;
- productive range vs recognition;
- integrated skills;
- whether one broad capability needs multiple lessons/evidence events.

Do not infer “simpler course” from fewer ability rows.

## 17. C2 risk prompts

C2 differs materially from A1–C1. Verify:

- lexical inventory comes from the Pearson GSE C2 General Learner snapshot;
- current primary inventory counts remain consistent with manifest/status files;
- owner-inherited collocations are not silently promoted to independent obligations;
- `commercial_permission_required` remains visible;
- architecture/research does not pretend the licensing gate is cleared;
- A1–C1 Oxford-specific handling code is not reused without adapting to the C2 source schema.

---

# PART VI — DEFINITION OF DONE

## 18. A level is not complete until all of these are true

### Source/inventory

- target inventories reconcile exactly to reviewed sources;
- no duplicated primary IDs;
- source/licensing metadata preserved.

### Manual design review

- every required ability manually dispositioned and traceable;
- capability architecture and cross-cutting requirements explicitly separated;
- every phrase reviewed and homed/bounded;
- every grammar row reviewed and mapped to usable systems/performances;
- every word/lexical item reviewed into a semantic/content home with a bounded meaning/control hypothesis;
- pronunciation stages reviewed and naturally placed;
- target exit constraints explicitly checked;
- previous-level carry-forward/prerequisite map exists;
- no silent exclusions or unexplained orphans.

### Curriculum architecture

- dependency-aware unit/lesson map exists;
- lesson count is evidence-led, not predetermined;
- each instructional lesson has one primary communicative/evidence outcome;
- coherent integrated-skill performance is allowed where appropriate;
- review/transfer/consolidation slots are explicit;
- previous-level cumulative knowledge has planned retrieval.

### Provisional coverage/lifecycle

- every target primary item present in exact ledger;
- introduction/use exists;
- later fresh retrieval exists;
- recycle/consolidation exists where appropriate;
- provisional exit path exists;
- no hidden new records in transfer slots;
- raw-load audit and human-load critic pass.

### Lesson briefs / rolling critic

- every slot has an authoring brief;
- critic performed during units/batches and again across the whole level;
- critic corrections propagated into map + ledger;
- audits re-run after corrections.

### Semantic lock

- final item-level control role reconciled;
- human-review queue = 0;
- semantic report locked;
- owner-inherited/supporting evidence treated correctly;
- manifest/exit contract agree with the report.

### Role-aware reconciliation

- Stage-8.5 reconciliation complete;
- lifecycle evidence matches final semantic roles;
- briefs agree with final foreground/receptive/formulaic/support treatment;
- no double assessment of grammar-owned/support items without justification;
- coverage/load audits pass again after reconciliation.

### Engineering

- full rebuild is deterministic;
- source-of-truth audit passes;
- target coverage/lifecycle audit passes;
- tests pass;
- reviewed state survives regeneration;
- previous locked levels remain unchanged unless explicitly reopened;
- delivery/media gates remain separate and unchanged unless explicitly authorized.

Only then may `lesson_design_authorized` be true for that level.

---

# PART VII — NEW-CHAT EXECUTION INSTRUCTIONS

## 19. Minimal handoff prompt for a future conversation

A user can say:

> Work on the next English-course level using `docs/LEVEL_CURRICULUM_DESIGN_PLAYBOOK_V1.md` as the authoritative process. Read the current status and target/previous-level contracts first. Reproduce the A1 method, not the A1 numbers. Keep main/TEST-002 untouched. Continue until the current stage is fully reviewed/audited, use adversarial critic passes rather than accepting automatic mappings as semantic truth, and do not silently change a previously locked level.

The assistant should then:

1. inspect the current branch head and status;
2. read this playbook;
3. read target level manifest, inventories, pronunciation, exit contract, and sources;
4. read previous-level manifest and locked exit contract;
5. run/inspect source audit;
6. create/continue the target level `design-review/` stages in order;
7. maintain capability + cross-cutting separation and a previous-level carry-forward map;
8. report concrete stage counts, unresolved items, and critic findings;
9. commit changes only on the independent curriculum branch/workstream;
10. validate with CI before declaring a stage locked;
11. run Stage 8.5 after semantic roles are finalized;
12. never assume prior chat history is required.

---

## 20. Reference A1 artifacts

A1 is the completed process example. Use it to understand file shapes and review depth, not to copy counts or curriculum shape:

```text
curriculum/levels/a1/design-review/
  01-abilities/
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

> **Inventory → manual capability architecture + cross-cutting requirements → phrase/grammar/word review → pronunciation + exit + carry-forward constraints → dependency-aware curriculum map → provisional exact lifecycle ledger → lesson briefs + rolling critic → formal semantic lock → role-aware lifecycle/brief reconciliation → deterministic authorization → CI.**

Or, in practical terms:

> We already know what the learner needs to know. The job is to build the best sequence that makes them actually learn it, retrieve it later, and prove the correct kind of mastery at exit — with nothing silently missing, nothing falsely claimed as productive mastery, and no locked earlier level silently rewritten to make the next level easier.
