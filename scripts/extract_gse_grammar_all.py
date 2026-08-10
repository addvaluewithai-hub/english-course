"""Write all Pearson GSE Grammar records from the registered guide."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

try:
    from scripts.gse_grammar_parser import extract_entries
    from scripts.gse_grammar_records import build_collection
except ModuleNotFoundError:
    from gse_grammar_parser import extract_entries
    from gse_grammar_records import build_collection


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "sources/raw/grammar/gse-grammar-guide-adult-framework.pdf"
OUTPUT = ROOT / "data/derived/gse-grammar-all.json"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, default=PDF)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    rows = extract_entries(args.pdf)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(build_collection(rows), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Extracted {len(rows)} GSE Grammar rows.")
    print("; ".join(f"{key}={value}" for key, value in Counter(x.level_text for x in rows).items()))


if __name__ == "__main__":
    main()
