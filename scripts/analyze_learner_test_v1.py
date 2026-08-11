"""Validate private session records and write only a de-identified aggregate."""

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from scripts.learner_session_record_rules import semantic_errors
from scripts.learner_test_analysis_core import analyze
from scripts.learner_test_v1_contract import SCHEMA, THRESHOLDS
from scripts.render_learner_test_analysis import render


def _load_records(directory: Path) -> list[dict]:
    paths = sorted(directory.glob("LT1-*.json"))
    if not paths:
        raise ValueError("no LT1-*.json session records found")
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    records = []
    for path in paths:
        record = json.loads(path.read_text(encoding="utf-8"))
        errors = [error.message for error in validator.iter_errors(record)]
        if not errors:
            errors = semantic_errors(record)
        if errors:
            raise ValueError(f"{path.name}: " + "; ".join(errors))
        records.append(record)
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("records", type=Path, help="Restricted directory containing LT1-*.json files")
    parser.add_argument("--evidence-mode", choices=("synthetic_fixtures", "real_consented_sessions"),
                        default="synthetic_fixtures")
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()
    try:
        records = _load_records(args.records)
        thresholds = json.loads(THRESHOLDS.read_text(encoding="utf-8"))
        result = analyze(records, thresholds, args.evidence_mode)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL learner-test analysis: {error}")
        return 1
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.output_md.write_text(render(result), encoding="utf-8")
    print(f"PASS learner-test analysis: {result['gate_effect']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
