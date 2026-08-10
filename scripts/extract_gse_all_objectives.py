"""Write all-level Pearson GSE Adult objective records."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

try:
    from scripts.gse_all_parser import extract_objectives
    from scripts.gse_all_records import build_collection
except ModuleNotFoundError:
    from gse_all_parser import extract_objectives
    from gse_all_records import build_collection


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PDF = PROJECT_ROOT / "sources/raw/frameworks/gse-learning-objectives-adult-general-english-2022.pdf"
DEFAULT_OUTPUT = PROJECT_ROOT / "data/derived/gse-all-objectives.json"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    objectives = extract_objectives(args.pdf)
    data = build_collection(objectives)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    by_band = Counter(row.band.key for row in objectives)
    by_skill = Counter(row.skill for row in objectives)
    print(f"Extracted {len(objectives)} source evidence rows.")
    print("Bands: " + "; ".join(f"{key}={value}" for key, value in by_band.items()))
    print("Skills: " + "; ".join(f"{key}={value}" for key, value in by_skill.items()))


if __name__ == "__main__":
    main()
