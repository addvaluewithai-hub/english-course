"""Write Oxford 3000 and Oxford 5000 provenance-complete source records."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

try:
    from scripts.oxford_wordlist_parser import extract_wordlist
    from scripts.oxford_wordlist_records import build_collection
except ModuleNotFoundError:
    from oxford_wordlist_parser import extract_wordlist
    from oxford_wordlist_records import build_collection


ROOT = Path(__file__).resolve().parents[1]
SPECS = (
    ("oxford_3000", ROOT / "sources/raw/vocabulary/oxford-3000-by-cefr-level.pdf", ROOT / "data/derived/oxford-3000-all.json"),
    ("oxford_5000", ROOT / "sources/raw/vocabulary/oxford-5000-by-cefr-level.pdf", ROOT / "data/derived/oxford-5000-all.json"),
)


def main() -> None:
    for list_id, pdf, output in SPECS:
        rows = extract_wordlist(pdf, list_id)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(build_collection(rows), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        counts = Counter(row.level_text for row in rows)
        print(f"{list_id}: {len(rows)} rows; " + "; ".join(f"{k}={v}" for k, v in counts.items()))


if __name__ == "__main__":
    main()
