"""Write reviewed foundational language-target decision partitions."""

from __future__ import annotations

import json

try:
    from scripts.create_identity_lesson_partition import OUTPUT_PATH
    from scripts.lesson_language_target_model import build_map
except ModuleNotFoundError:
    from create_identity_lesson_partition import OUTPUT_PATH
    from lesson_language_target_model import build_map


def main() -> None:
    OUTPUT_PATH.write_text(
        json.dumps(build_map(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"WROTE {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
