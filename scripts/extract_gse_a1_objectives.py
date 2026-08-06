"""Write derived and optionally reviewed Pearson GSE A1 objective records."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

try:
    from scripts.gse_a1_parser import extract_objectives
    from scripts.gse_a1_records import build_collection
except ModuleNotFoundError:  # Direct invocation places scripts/ on sys.path.
    from gse_a1_parser import extract_objectives
    from gse_a1_records import build_collection


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PDF = PROJECT_ROOT / "sources/raw/frameworks/gse-learning-objectives-adult-general-english-2022.pdf"
DEFAULT_DERIVED = PROJECT_ROOT / "data/derived/gse-a1-objectives.json"
DEFAULT_REVIEWED = PROJECT_ROOT / "data/reviewed/gse-a1-objectives.json"


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--derived-output", type=Path, default=DEFAULT_DERIVED)
    parser.add_argument("--reviewed-output", type=Path, default=DEFAULT_REVIEWED)
    parser.add_argument("--reviewer")
    parser.add_argument("--reviewed-at")
    args = parser.parse_args()

    objectives = extract_objectives(args.pdf)
    _write(args.derived_output, build_collection(objectives))
    if args.reviewer or args.reviewed_at:
        reviewed = build_collection(
            objectives, reviewer=args.reviewer, reviewed_at=args.reviewed_at
        )
        _write(args.reviewed_output, reviewed)

    counts = Counter(item.skill for item in objectives)
    unique = len({(item.skill, item.text) for item in objectives})
    print(f"Extracted {len(objectives)} evidence rows; {unique} canonical objectives.")
    print("; ".join(f"{skill}: {counts[skill]}" for skill in counts))


if __name__ == "__main__":
    main()
