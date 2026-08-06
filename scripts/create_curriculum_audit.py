"""CLI for deterministic CUR-006 curriculum-audit generation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from scripts.curriculum_audit import build_curriculum_audit
except ModuleNotFoundError:
    from curriculum_audit import build_curriculum_audit


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATHS = (
    Path("data/reviewed/gse-a1-objectives.json"),
    Path("data/reviewed/cefr-a1-descriptors.json"),
)
MAP_PATH = Path("data/reviewed/a1-candidate-unit-map.json")
OUTPUT_PATH = Path("data/reviewed/a1-curriculum-audit.json")


def load(path: Path) -> dict:
    with (PROJECT_ROOT / path).open(encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reviewed-at", required=True, help="ISO 8601 review timestamp")
    parser.add_argument("--check", action="store_true", help="Verify without writing")
    args = parser.parse_args()
    audit = build_curriculum_audit(
        [load(path) for path in SOURCE_PATHS], load(MAP_PATH), args.reviewed_at
    )
    if not args.check:
        path = PROJECT_ROOT / OUTPUT_PATH
        path.write_text(
            json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(json.dumps(audit["verdict"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
