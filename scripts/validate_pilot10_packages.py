from __future__ import annotations

import argparse

from scripts.pilot10_common_validation import validate_package
from scripts.pilot10_package_contract import ROOT, release


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate authored first-ten packages.")
    parser.add_argument("--require-all", action="store_true")
    args = parser.parse_args()
    completed = []
    errors = []
    lessons = release()["lessons"]
    for lesson in lessons:
        lesson_id = lesson["lesson_id"]
        path = ROOT / lesson["content_path"]
        if not (path / "lesson-manifest.json").is_file():
            if args.require_all:
                errors.append(f"{lesson_id}: package is missing")
            continue
        completed.append(lesson_id)
        errors.extend(f"{lesson_id}: {error}" for error in validate_package(lesson_id))
    if errors:
        raise SystemExit("FAIL first-ten packages\n- " + "\n- ".join(errors))
    print(f"PASS first-ten packages ({len(completed)}/10 authored: {', '.join(completed)})")


if __name__ == "__main__":
    main()
