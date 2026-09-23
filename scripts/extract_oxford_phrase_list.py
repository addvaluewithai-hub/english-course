#!/usr/bin/env python3
"""Extract levelled Oxford Phrase List entries from the official PDF styling."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "sources/raw/vocabulary/oxford-phrase-list.pdf"
OUT = ROOT / "data/derived/oxford-phrase-list-all.json"
LEVELS = {"A1", "A2", "B1", "B2", "C1"}
ENTRY_FONT = "MyriadPro-Regular"


def normalize_phrase(text: str) -> str:
    return " ".join(text.casefold().replace("…", "...").split())


def main() -> None:
    doc = fitz.open(PDF)
    current_level: str | None = None
    records: list[dict] = []
    font_counts: Counter[str] = Counter()

    for page_index, page in enumerate(doc):
        rows = []
        width = page.rect.width
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                spans = [s for s in line.get("spans", []) if s.get("text", "").strip()]
                if not spans:
                    continue
                for span in spans:
                    font_counts[span.get("font", "unknown")] += 1
                text = "".join(s["text"] for s in spans).strip()
                x0 = min(s["bbox"][0] for s in spans)
                y0 = min(s["bbox"][1] for s in spans)
                col = min(3, max(0, int(x0 / (width / 4))))
                fonts = {s.get("font", "") for s in spans}
                is_entry = ENTRY_FONT in fonts
                rows.append((col, y0, x0, text, is_entry, fonts))

        for col, y0, x0, text, is_entry, fonts in sorted(rows, key=lambda x: (x[0], x[1], x[2])):
            if text in LEVELS:
                current_level = text
                continue
            if not current_level or not is_entry:
                continue
            if "Oxford Phrase List" in text or "Oxford University Press" in text:
                continue
            records.append({
                "record_id": f"oxford.phrase.p{page_index + 1:02d}.{len(records) + 1:03d}",
                "level": current_level,
                "phrase": text,
                "source_page": page_index + 1,
                "source_x": round(x0, 2),
                "source_y": round(y0, 2),
            })

    counts = Counter(r["level"] for r in records)
    phrase_counts = Counter(normalize_phrase(r["phrase"]) for r in records)
    duplicate_keys = {phrase for phrase, count in phrase_counts.items() if count > 1}
    duplicates = [
        (r["level"], r["phrase"], r["source_page"], r["source_x"], r["source_y"])
        for r in records if normalize_phrase(r["phrase"]) in duplicate_keys
    ]
    print("fonts:", dict(font_counts))
    print("level counts:", dict(counts), "total:", len(records))
    print("unique normalized phrases:", len(phrase_counts))
    print("duplicate phrase records:", duplicates)
    if len(records) != 750:
        raise SystemExit(
            f"Expected 750 phrase entries, extracted {len(records)}; "
            f"unique={len(phrase_counts)}; duplicates={duplicates}"
        )
    if set(counts) != LEVELS:
        raise SystemExit(f"Missing expected levels: {LEVELS - set(counts)}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "schema_version": 1,
        "dataset_id": "oxford_phrase_list_all",
        "source_file": str(PDF.relative_to(ROOT)).replace("\\", "/"),
        "published_count": 750,
        "record_count": len(records),
        "level_counts": dict(counts),
        "records": records,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
