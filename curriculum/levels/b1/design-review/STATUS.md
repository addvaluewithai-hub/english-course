# B1 Curriculum Design Status

Status: **STAGE 9 CLOSED — LESSON DESIGN AUTHORIZED; DELIVERY / MEDIA PRODUCTION STILL NOT AUTHORIZED**  
Branch: `curriculum/level-source-of-truth-v1`  
Architecture: **12 units / 85 lesson slots**  
Exact B1 new-at-level inventory: **1,581 records**

This is the authoritative handoff/resume point for B1 curriculum design.

## Current gate state

- `lesson_design_authorized = true`
- `delivery_content_production_authorized = false`
- human semantic review queue = **0**
- `TEST-002` is untouched and not bypassed
- A2 remains the locked prerequisite/retrieval level and is unedited by B1 design
- B2–C2 remain lesson-design locked

## Closed milestones

### Foundation / Stages 0–4.5

- exact B1 source inventory reviewed: **1,581** records
- abilities: **249** required rows → **20 capability families + 8 cross-cutting requirements** after grammar feedback
- phrases: **175 / 175** manually reviewed
- grammar: **338 / 338** canonical EGP rows → **59** reviewed systems/infrastructure families
- words: **809 / 809** exact lexical records home-mapped; intentional general remainder is not treated as orphaning
- pronunciation: **10** reviewed strands; intelligibility-first
- B1 exit constraints and A2 carry-forward are explicit

### Stage 5 / curriculum architecture

- final architecture: **12 units / 85 lesson slots**
- lesson count emerged from B1 performance/dependency evidence; it was not copied from A2
- **16** designated zero-new transfer/final-integration slots

### Stage 6 / exact lifecycle + Milestone 2 load/sequence lock

- exact coverage ledger: **1,581 / 1,581**
- orphans: **0**
- practice gaps: **0**
- fresh-retrieval gaps: **0**
- recycle gaps: **0**
- consolidation gaps: **0**
- exit-verify gaps: **0**
- zero-new transfer/integration violations: **0 / 16**
- the remaining **15** raw source-count warnings are human-reviewed diagnostics, not teaching-object counts
- thresholds were not raised to force a pass
- Stage-08.5 routing feedback was re-audited and re-pinned with the raw warning set unchanged
- architecture retained: **12 / 85**

### Stage 7 / lesson authoring briefs

- lesson briefs: **85 / 85**
- rolling unit critics: **12 / 12**
- whole-level adversarial critic: complete
- Stage-08.5 feedback is folded back into the brief file
- exact brief introduction counts match the reconciled Stage-06 ledger
- all **16 / 16** zero-new slots remain protected

### Stage 8 / formal semantic lock

Final exact semantic accounting after the Stage-08.5 critic:

- exact source roles: **1,581 / 1,581**
- semantic orphans: **0**
- automation-inferred semantic roles: **0**
- human review queue: **0**

Mastery modes:

- productive: **597**
- interactive: **57**
- receptive: **611**
- integrated support: **316**

By category:

- abilities — **249**: 101 productive · 57 interactive · 66 receptive · 25 support
- phrases — **175**: 128 productive/formulaic · 6 receptive · 41 support
- grammar — **338**: 128 productive rows · 2 receptive rows · 208 support rows
- words — **809**: 240 productive/contextual · 536 receptive/contextual · 33 support
- pronunciation — **10**: 1 receptive · 9 support

B1 `mediation` remains preserved as an explicit source mode. It is not silently relabelled generic production.

### Stage 8.5 / role-aware feedback

Exact human semantic corrections:

- **67 words** productive → receptive
- **17 grammar rows** productive → integrated support
- **1 phrase** productive → receptive
- total exact semantic overrides: **85**

Exact lifecycle-routing corrections:

- ability review row **6** → `U9-L05` (health/medication instruction reception)
- ability review row **151** → `U9-L06` (symptom production)
- phrase review row **174** → `U9-L06` (`wrong with sb/sth` with symptom communication)

Role-aware load findings confirmed no split/merge need. Representative active teaching-object estimates after reconciliation:

- `U3-L02`: ~**16**
- `U3-L03`: ~**16**
- `U3-L04`: ~**15**
- `U4-L01`: reception-led / **0 planned active semantic objects**
- `U9-L05`: reception-only
- `U9-L06`: ~**14**
- `U10-L02`: ~**16** despite 56 raw source rows
- `U11-L02`: ~**12**
- `U11-L04`: ~**14**

Final Stage-08.5 decision: **retain 12 units / 85 lessons; no structural reopening remains.**

## Stage 9 authorization

Human declaration:

`curriculum/levels/b1/design-review/09-authorization-gate/authorization.json`

The declaration pins the exact reviewed evidence blobs and explicitly states:

- lesson design / controlled authoring contract: **authorized**
- delivery/media production: **not authorized**
- human review queue: **0**
- architecture: **12 / 85**
- `TEST-002`: untouched

Deterministic finalizer:

`scripts/finalize_b1_authorization.py`

The finalizer validates the pinned evidence, exact counts, Stage-08.5 override counts, lifecycle completeness, zero-new protection, critic markers and reconciled 85-brief architecture before it can restore the authorized manifest/exit-contract state after a clean rebuild.

## Deterministic rebuild proof

Authorization declaration / pin close:

- `cf234c9dc3acf7ab6090170baff0400b5df23868` — `curriculum: pin reconciled B1 lesson briefs in authorization gate`

Finalizer:

- `ed59830ceef4024a59c55b5f35a3c5bbbbf640c4` — `curriculum: add deterministic B1 lesson-design authorization finalizer`

Build pipeline integration:

- `3a86d9a970cc8fb842caef71a03de0ae5c61f53c` — `ci: restore reviewed B1 authorization after clean rebuild`
- GitHub Actions run `36292574208`: **SUCCESS**
- deterministic generated commit: `e7cf2bcc4c3405d3a440e943a1dbd353d1c8da70` — `curriculum: generate level inventory candidates`

That rebuild successfully executed:

base inventories → grammar enrichment → granular abilities → review aids → A1 finalization → A2 finalization → **B1 Stage-9 finalization** → unit tests.

## Cross-level validation

Cross-level source/authorization audit recognizes A1, A2 and B1 as independently reviewed lesson-design locks while keeping B2–C2 locked.

- audit guardrail commit: `69b7eb5f25993028ee9e8d07aeaaf62e3a63a462`
- GitHub Actions run `36292602529`: **SUCCESS**

Target-level validation already closed green after reconciliation:

- B1 Stage-06 coverage/lifecycle audit: **SUCCESS**
- B1 Stage-07/08.5 brief audit: **SUCCESS**
- B1 Stage-08/08.5 semantic audit: **SUCCESS**
- clean source-of-truth rebuild + unit tests: **SUCCESS**
- cross-level source/authorization audit: **SUCCESS**

## What is authorized now

Controlled B1 lesson design / authoring implementation may now use the **85 locked briefs** as the authoritative curriculum contract, while preserving:

- one coherent learner-performance outcome per lesson
- final productive / interactive / receptive / support roles
- formulaic vs generative boundaries
- mediation as source transformation
- role-appropriate lifecycle and fresh evidence
- all 16 zero-new transfer/integration slots
- A2 as prerequisite/retrieval rather than new B1 inventory
- pronunciation as intelligibility/processing/interaction support
- explicit reopening + re-audit if real authoring exposes a contradiction

## What is still not authorized

Do **not** start:

- mass lesson-package production
- audio production
- image production
- video production
- mass delivery-artifact generation
- any change, bypass or weakening of `TEST-002`

## Next session boundary

Begin **Controlled B1 Lesson Authoring** from `U1-L01`.

First establish one stable lesson-authoring contract/template on `U1-L01`, run a human critic against the locked brief + semantic ledger, then scale only in bounded batches. Do not start media/delivery production as part of that step.
