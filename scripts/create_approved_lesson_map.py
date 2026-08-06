"""Write the consolidated approved A1 lesson map."""

from __future__ import annotations

import json

try:
    from scripts.lesson_approval_model import build_approved_map
    from scripts.lesson_map_io import DEFAULT_MAP_PATH
except ModuleNotFoundError:
    from lesson_approval_model import build_approved_map
    from lesson_map_io import DEFAULT_MAP_PATH


def main() -> None:
    lesson_map = build_approved_map()
    DEFAULT_MAP_PATH.write_text(
        json.dumps(lesson_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"WROTE {DEFAULT_MAP_PATH}")


if __name__ == "__main__":
    main()
