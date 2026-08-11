# First-Ten Progression Analysis Runbook

Individual records stay in a restricted directory outside this repository. Never copy
that directory into the project, attach it to an issue, or push it to GitHub.

## Validate records

From the repository root, validate a real completed collection with:

```powershell
python -m scripts.validate_first_ten_progression_records `
  "D:\restricted\english-pilot-10" `
  --evidence-mode real_observation `
  --require-complete
```

Use `synthetic_fixture` only while rehearsing the instrument. Synthetic records can
test code but always have `simulation_only_no_gate_effect`; they never support a go,
revise, or stop decision.

## What to give Codex

Give Codex only the local restricted-directory path. Do not paste participant records
into chat. Codex should validate first, calculate the pre-registered metrics, inspect
the U1-L05 and U1-L08 split triggers, and write only a de-identified aggregate report
to the repository.

The aggregate report may include denominators, ratios, medians, lesson-level controlled
issue counts, revisions, and the decision. It must not include participant codes,
verbatim answers, free-text observations, contact details, audio, video, or screenshots.
