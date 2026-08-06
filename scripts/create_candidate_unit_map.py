"""CLI for CUR-005 candidate clustering and unit-map generation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from scripts.candidate_clustering import cluster_collection
    from scripts.candidate_map import build_candidate_map
except ModuleNotFoundError:
    from candidate_clustering import cluster_collection
    from candidate_map import build_candidate_map


PROJECT_ROOT = Path(__file__).resolve().parents[1]
COLLECTION_PATHS = (
    Path("data/derived/gse-a1-objectives.json"),
    Path("data/derived/cefr-a1-descriptors.json"),
    Path("data/reviewed/gse-a1-objectives.json"),
    Path("data/reviewed/cefr-a1-descriptors.json"),
)
MAP_PATH = Path("data/reviewed/a1-candidate-unit-map.json")


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def generate(reviewed_at: str) -> tuple[list[tuple[Path, dict]], dict]:
    outputs = []
    for relative_path in COLLECTION_PATHS:
        path = PROJECT_ROOT / relative_path
        outputs.append((
            path,
            cluster_collection(
                load_json(path), reviewer="cur_005_primary", reviewed_at=reviewed_at
            ),
        ))
    reviewed = [value for path, value in outputs if "reviewed" in path.parts]
    return outputs, build_candidate_map(reviewed, reviewed_at)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reviewed-at", required=True, help="ISO 8601 review timestamp")
    parser.add_argument("--check", action="store_true", help="Verify without writing")
    args = parser.parse_args()
    outputs, candidate_map = generate(args.reviewed_at)
    if not args.check:
        for path, value in outputs:
            write_json(path, value)
        write_json(PROJECT_ROOT / MAP_PATH, candidate_map)
    print(json.dumps(candidate_map["coverage"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
