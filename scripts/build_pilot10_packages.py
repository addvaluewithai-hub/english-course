from __future__ import annotations

import argparse

from scripts.pilot10_package_builder import write_package
from scripts.pilot10_specs.registry import SPECS


def main() -> None:
    parser = argparse.ArgumentParser(description="Build authored first-ten lesson packages.")
    parser.add_argument("--lesson", choices=sorted(SPECS))
    args = parser.parse_args()
    selected = [args.lesson] if args.lesson else sorted(SPECS)
    for lesson_id in selected:
        output = write_package(SPECS[lesson_id])
        print(f"WROTE {lesson_id} -> {output}")


if __name__ == "__main__":
    main()
