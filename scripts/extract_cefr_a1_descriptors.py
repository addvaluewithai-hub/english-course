"""Write derived and reviewed CEFR Companion Volume A1 descriptor records."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

try:
    from scripts.cefr_a1_parser import extract_descriptors
    from scripts.cefr_a1_records import build_collection
except ModuleNotFoundError:
    from cefr_a1_parser import extract_descriptors
    from cefr_a1_records import build_collection


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "sources/raw/frameworks/cefr-companion-2020-en.pdf"
DERIVED = ROOT / "data/derived/cefr-a1-descriptors.json"
REVIEWED = ROOT / "data/reviewed/cefr-a1-descriptors.json"


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, default=PDF)
    parser.add_argument("--derived-output", type=Path, default=DERIVED)
    parser.add_argument("--reviewed-output", type=Path, default=REVIEWED)
    parser.add_argument("--reviewer")
    parser.add_argument("--reviewed-at")
    args = parser.parse_args()
    descriptors, inventory = extract_descriptors(args.pdf)
    _write(args.derived_output, build_collection(descriptors))
    if args.reviewer or args.reviewed_at:
        _write(args.reviewed_output, build_collection(descriptors, args.reviewer, args.reviewed_at))
    modes = Counter(item.mode for item in descriptors)
    print(f"Extracted {len(descriptors)} A1 descriptors from {len(inventory)} scales.")
    print("; ".join(f"{mode}: {count}" for mode, count in modes.items()))


if __name__ == "__main__":
    main()
