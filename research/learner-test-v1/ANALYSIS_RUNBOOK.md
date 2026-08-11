# TEST-002 Analysis Runbook

This runbook turns validated private session records into a de-identified aggregate.
It cannot recruit participants, substitute synthetic records for people, or decide that
the lesson works before the pre-registered evidence exists.

## Private input location

Create a restricted directory outside this repository. Store only records downloaded
from `prototype/gold-lesson/observer.html`, named `LT1-001.json`, `LT1-002.json`, and
so on. Do not place individual session files in Git, the public repository, a shared
chat, or a general project folder.

Validate one record:

```powershell
python -m scripts.validate_learner_session_record C:\private-pilot\LT1-001.json
```

The validator rejects missing consent, wrong odd/even allocation, answer-bearing
mastery evidence, inconsistent double ratings, raw-data flags, and invalid fields.

## Dry-run mode

Synthetic fixtures may test the calculator, but their report is forced to
`simulation_only_no_gate_effect`:

```powershell
python -m scripts.analyze_learner_test_v1 C:\fixture-records `
  --evidence-mode synthetic_fixtures `
  --output-json C:\temp\fixture-analysis.json `
  --output-md C:\temp\fixture-analysis.md
```

## Real evidence mode

Use this mode only after the consented sessions actually happened and every record was
checked by the facilitator:

```powershell
python -m scripts.analyze_learner_test_v1 C:\private-pilot `
  --evidence-mode real_consented_sessions `
  --output-json data\reviewed\learner-test-v1-aggregate.json `
  --output-md docs\LEARNER_TEST_V1_RESULTS.md
```

The aggregate contains counts, ratios, condition summaries, timing, ratings, issue
counts, and the pre-registered decision. It intentionally drops individual notes and
never copies a raw learner answer or direct identifier.

## Required review before committing results

- Confirm at least six eligible completed sessions and report the target of eight.
- Confirm at least two live double-rated sessions.
- Compare every metric with `success-thresholds.json`; do not move thresholds.
- Read unresolved major/severe issues in the restricted records and assign revisions.
- Keep completion, demonstration, and retention claims separate.
- Treat teach-back/omit differences as directional because this pilot is small.
- Commit only the aggregate JSON, aggregate report, named lesson revisions, and the
  resulting go/revise/stop/insufficient decision.
- Delete individual records 90 days after TEST-002 synthesis and keep a deletion log
  outside the public repository.
