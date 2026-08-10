"""Completeness and PDF-layout tests for Oxford vocabulary extraction."""

from __future__ import annotations

import unittest
from collections import Counter
from pathlib import Path

import fitz

from scripts.oxford_wordlist_parser import extract_wordlist
from scripts.oxford_wordlist_records import build_collection
from scripts.validate_source_records import validate_dataset


ROOT = Path(__file__).resolve().parents[1]
SPECS = {
    "oxford_3000": (
        ROOT / "sources/raw/vocabulary/oxford-3000-by-cefr-level.pdf",
        ROOT / "data/derived/oxford-3000-all.json",
    ),
    "oxford_5000": (
        ROOT / "sources/raw/vocabulary/oxford-5000-by-cefr-level.pdf",
        ROOT / "data/derived/oxford-5000-all.json",
    ),
}
EXPECTED_COUNTS = {
    "oxford_3000": {"A1": 900, "A2": 871, "B1": 809, "B2": 727},
    "oxford_5000": {"B2": 700, "C1": 1315},
}


class OxfordWordlistExtractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if any(not pdf.exists() for pdf, _ in SPECS.values()):
            raise unittest.SkipTest("Oxford source PDFs are unavailable")
        cls.rows = {key: extract_wordlist(pdf, key) for key, (pdf, _) in SPECS.items()}

    def test_published_levels_are_present(self) -> None:
        self.assertEqual({"A1", "A2", "B1", "B2"}, {x.level_text for x in self.rows["oxford_3000"]})
        self.assertEqual({"B2", "C1"}, {x.level_text for x in self.rows["oxford_5000"]})

    def test_source_entry_counts_are_locked(self) -> None:
        for key, expected in EXPECTED_COUNTS.items():
            self.assertEqual(expected, dict(Counter(row.level_text for row in self.rows[key])))
        self.assertEqual(3307, len(self.rows["oxford_3000"]))
        self.assertEqual(2015, len(self.rows["oxford_5000"]))
        self.assertEqual(3000, len({row.headword_source for row in self.rows["oxford_3000"]}))
        self.assertEqual(1999, len({row.headword_source for row in self.rows["oxford_5000"]}))

    def test_visual_line_parser_repairs_known_text_mirror_breaks(self) -> None:
        entries = {row.source_text for row in self.rows["oxford_5000"]}
        self.assertIn("rifle n.", entries)
        self.assertIn("sanction n.", entries)
        self.assertIn("settlement n.", entries)

    def test_each_entry_occurs_on_its_cited_page(self) -> None:
        for key, (pdf, _) in SPECS.items():
            document = fitz.open(pdf)
            for row in self.rows[key]:
                page_text = "".join(document[row.page - 1].get_text("text").split())
                self.assertIn("".join(row.source_text.split()), page_text)

    def test_records_are_unique_and_datasets_validate(self) -> None:
        for key, rows in self.rows.items():
            records = build_collection(rows)["records"]
            self.assertEqual(len(records), len({row["record_id"] for row in records}))
            self.assertEqual([], validate_dataset(SPECS[key][1]))


if __name__ == "__main__":
    unittest.main()
