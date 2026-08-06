"""Normalize skills, modes, and functions in the A1 evidence collections."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from scripts.curriculum_tagging import normalize_collection
except ModuleNotFoundError:
    from curriculum_tagging import normalize_collection


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASETS = (
    Path("data/derived/gse-a1-objectives.json"),
    Path("data/derived/cefr-a1-descriptors.json"),
    Path("data/reviewed/gse-a1-objectives.json"),
    Path("data/reviewed/cefr-a1-descriptors.json"),
)


def _load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _write(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reviewer", required=True)
    parser.add_argument("--reviewed-at", required=True)
    args = parser.parse_args()

    for relative_path in DATASETS:
        path = PROJECT_ROOT / relative_path
        collection = _load(path)
        reviewed = "reviewed" in relative_path.parts
        normalized = normalize_collection(
            collection,
            reviewer=args.reviewer if reviewed else None,
            reviewed_at=args.reviewed_at if reviewed else None,
        )
        _write(path, normalized)
        print(f"Tagged {len(normalized['records'])} records in {relative_path.as_posix()}")


if __name__ == "__main__":
    main()
