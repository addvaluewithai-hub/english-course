"""Write the reviewed LESSON-002 overlap and mastery remediation partition."""

from __future__ import annotations

import json

try:
    from scripts.create_foundation_lesson_partition import build_map as build_foundation_map
    from scripts.create_identity_lesson_partition import OUTPUT_PATH
    from scripts.lesson_map_overlap_reconciliation import reconcile_overlaps
except ModuleNotFoundError:
    from create_foundation_lesson_partition import build_map as build_foundation_map
    from create_identity_lesson_partition import OUTPUT_PATH
    from lesson_map_overlap_reconciliation import reconcile_overlaps


def build_map():
    return reconcile_overlaps(build_foundation_map())


def main() -> None:
    OUTPUT_PATH.write_text(
        json.dumps(build_map(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"WROTE {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
