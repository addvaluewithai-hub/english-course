"""Validate one private learner-session record before TEST-002 analysis."""

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from scripts.learner_session_record_rules import semantic_errors
from scripts.learner_test_v1_contract import SCHEMA


def record_errors(path: Path) -> list[str]:
    record = json.loads(path.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = [error.message for error in Draft202012Validator(schema).iter_errors(record)]
    return errors + ([] if errors else semantic_errors(record))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    errors = record_errors(args.record)
    if errors:
        print("FAIL learner-session record")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("PASS learner-session record")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
