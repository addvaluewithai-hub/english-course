"""Write the reviewed LESSON-002 relationship and sequence partition."""

from __future__ import annotations

import json
from pathlib import Path

try:
    from scripts.create_identity_lesson_partition import OUTPUT_PATH
    from scripts.lesson_relationship_model import build_map, build_review
except ModuleNotFoundError:
    from create_identity_lesson_partition import OUTPUT_PATH
    from lesson_relationship_model import build_map, build_review


ROOT = Path(__file__).resolve().parents[1]
REVIEW_PATH = ROOT / "data/reviewed/a1-lesson-relationship-review.json"


def main() -> None:
    lesson_map = build_map()
    review = build_review(lesson_map)
    OUTPUT_PATH.write_text(
        json.dumps(lesson_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    REVIEW_PATH.write_text(
        json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"WROTE {OUTPUT_PATH}")
    print(f"WROTE {REVIEW_PATH}")


if __name__ == "__main__":
    main()
