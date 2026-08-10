"""Write all-level CEFR Companion Volume illustrative descriptor records."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

try:
    from scripts.cefr_all_parser import extract_descriptors
    from scripts.cefr_all_records import build_collection
except ModuleNotFoundError:
    from cefr_all_parser import extract_descriptors
    from cefr_all_records import build_collection


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "sources/raw/frameworks/cefr-companion-2020-en.pdf"
OUTPUT = ROOT / "data/derived/cefr-all-descriptors.json"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, default=PDF)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    rows = extract_descriptors(args.pdf)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(build_collection(rows), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Extracted {len(rows)} source evidence rows.")
    print("Levels: " + "; ".join(f"{k}={v}" for k, v in Counter(x.level_text for x in rows).items()))
    print("Modes: " + "; ".join(f"{k}={v}" for k, v in Counter(x.mode for x in rows).items()))


if __name__ == "__main__":
    main()
