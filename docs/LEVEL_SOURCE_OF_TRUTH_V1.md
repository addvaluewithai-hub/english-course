# Level Source of Truth v1

Owner decision: define the complete A1-C2 language foundation before new lesson design.

Each level has:
`manifest.json`, `words.json`, `phrases.json`, `grammar.json`, `abilities.json`,
`pronunciation.json`, `exit_contract.json`, and `sources.json`.

The level inventory is a reviewed curriculum decision layer. Publisher/framework files
remain evidence sources under `sources/`; normalized machine extraction belongs under
`data/derived/`; reviewed reconciliations belong under `data/reviewed/`.

No existing pilot lesson is changed by this branch. A later audit will map lessons to the
locked inventories only after the inventories pass coverage and provenance checks.
