"""Validate the reviewed A1 lesson map against its source evidence and contracts."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from scripts.lesson_map_io import DEFAULT_MAP_PATH
    from scripts.lesson_map_validation import validation_errors
except ModuleNotFoundError:
    from lesson_map_io import DEFAULT_MAP_PATH
    from lesson_map_validation import validation_errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_MAP_PATH)
    args = parser.parse_args()
    errors = validation_errors(args.path)
    if errors:
        print(f"FAIL {args.path}")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"PASS {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
