"""Completeness tests for the Pearson GSE Grammar extraction."""

from __future__ import annotations

import unittest
from collections import Counter
from pathlib import Path

import fitz

from scripts.gse_grammar_parser import EXPECTED_RANGES, extract_entries
from scripts.gse_grammar_records import build_collection
from scripts.validate_source_records import validate_dataset


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "sources/raw/grammar/gse-grammar-guide-adult-framework.pdf"
DATASET = ROOT / "data/derived/gse-grammar-all.json"
EXPECTED_COUNTS = {
    "A1": 43, "A2": 50, "A2+": 67, "B1": 133,
    "B1+": 96, "B2": 46, "B2+": 18, "C1": 3,
}


class GseGrammarExtractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not PDF.exists():
            raise unittest.SkipTest("GSE Grammar source PDF is unavailable")
        cls.rows = extract_entries(PDF)

    def test_all_published_bands_are_present(self) -> None:
        self.assertEqual(set(EXPECTED_RANGES), {row.level_text for row in self.rows})
        for row in self.rows:
            minimum, maximum = EXPECTED_RANGES[row.level_text]
            self.assertIn(row.score, range(minimum, maximum + 1))

    def test_source_table_counts_are_locked(self) -> None:
        self.assertEqual(EXPECTED_COUNTS, dict(Counter(row.level_text for row in self.rows)))
        self.assertEqual(456, len(self.rows))

    def test_required_source_fields_are_not_blank(self) -> None:
        for row in self.rows:
            self.assertTrue(row.objective.startswith("Can "))
            self.assertTrue(row.structure)
            self.assertTrue(row.categories)

    def test_b2_plus_printed_range_conflict_is_preserved(self) -> None:
        rows = [row for row in self.rows if row.level_text == "B2+"]
        self.assertTrue(rows)
        self.assertTrue(all(row.printed_level_heading == "B2+ (59-66)" for row in rows))
        self.assertTrue(all(any("conflicts" in note for note in row.transcription_notes) for row in rows))

    def test_objectives_occur_on_cited_pages(self) -> None:
        document = fitz.open(PDF)
        for row in self.rows:
            page_text = "".join(document[row.page - 1].get_text("text").split())
            self.assertIn("".join(row.objective.split()), page_text)

    def test_records_are_unique_and_dataset_validates(self) -> None:
        records = build_collection(self.rows)["records"]
        self.assertEqual(len(records), len({row["record_id"] for row in records}))
        self.assertEqual([], validate_dataset(DATASET))


if __name__ == "__main__":
    unittest.main()
