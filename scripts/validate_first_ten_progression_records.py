from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.first_ten_pilot_record_validation import validate_record


def validate_directory(directory: Path, evidence_mode: str, require_complete: bool) -> list[str]:
    errors = []
    files = sorted(directory.glob("*.json")) if directory.is_dir() else []
    if not files:
        return ["no JSON records found in the private directory"]
    if len(files) > 10:
        errors.append("record count exceeds the pre-registered recruitment maximum of 10")
    codes = set()
    for path in files:
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"{path.name}: unreadable JSON ({error})")
            continue
        code = record.get("participant_code")
        if code in codes:
            errors.append(f"{path.name}: duplicate participant code")
        codes.add(code)
        if record.get("evidence_mode") != evidence_mode:
            errors.append(f"{path.name}: evidence mode differs from requested mode")
        errors += [f"{path.name}: {error}" for error in validate_record(record, require_complete)]
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate private first-ten progression records.")
    parser.add_argument("directory", type=Path)
    parser.add_argument("--evidence-mode", choices=("real_observation", "synthetic_fixture"), required=True)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    errors = validate_directory(args.directory, args.evidence_mode, args.require_complete)
    if errors:
        raise SystemExit("FAIL private progression records\n- " + "\n- ".join(errors))
    print("PASS private progression records (record contents were not printed)")


if __name__ == "__main__":
    main()
