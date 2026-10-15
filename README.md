# English Course — Curriculum Source of Truth

This repository is the canonical workspace for the A1–C2 general-English curriculum.

## Start here

Read in this order:

1. `START_HERE.md`
2. `CURRENT_STATE.md`
3. `docs/LEVEL_CURRICULUM_DESIGN_PLAYBOOK_V1.md`
4. `curriculum/levels/<current-level>/manifest.json`
5. The current level's `design-review/` workspace and the immediately previous locked level when prerequisite evidence is needed.

## Canonical structure

- `curriculum/levels/` — level inventories, exit contracts, design reviews, lifecycle ledgers, semantic locks and authorization evidence.
- `sources/` — pinned raw/reference sources and source registry.
- `data/` — reviewed and derived evidence used by the curriculum pipeline.
- `docs/` — curriculum architecture, progression and design rules.
- `scripts/` — deterministic builders, audits and review aids.
- `tests/` — curriculum validation tests.
- `schemas/` — machine contracts used by the pipeline.
- `.github/workflows/` — reproducible audits/builds.

## Authority

`main` is the only active curriculum source of truth.

The complete pre-cleanup snapshot is preserved on:
`archive/level-source-of-truth-v1-2026-09-27`

Use the archive only to trace historical decisions. Do not continue active curriculum design there.

## Interactive lesson production (optional authoring workstream)

For authorized conversion of **existing, approved** English lesson briefs into Otti-led interactive lessons, start at [Interactive content production — إنتاج المحتوى التفاعلي](interactive-content-production/README.md). It contains a reusable agent skill, authored lesson/board contract, real-browser frame-sheet QA procedure, production status and defect templates. The runtime and screenshot runner are implemented against the actual **EnglishLive product** in a separate PR; this repository still owns only canonical curriculum and authoring guidance.

## Scope boundary

This workspace is for curriculum design and its evidence. Old delivery pilots, prototype lesson packages, gold-lesson experiments, learner-research kits and legacy conversations are intentionally not part of the active tree. They remain recoverable from the archive branch.
