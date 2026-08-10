"""Completeness and source-integrity tests for all-level CEFR extraction."""

from __future__ import annotations

import re
import unittest
from collections import Counter
from pathlib import Path

import fitz

from scripts.cefr_a1_parser import extract_descriptors as extract_a1
from scripts.cefr_all_parser import LEVEL_TO_CODE, extract_descriptors
from scripts.cefr_all_records import build_collection
from scripts.validate_source_records import validate_dataset


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "sources/raw/frameworks/cefr-companion-2020-en.pdf"
DATASET = ROOT / "data/derived/cefr-all-descriptors.json"
EXPECTED_LEVEL_COUNTS = {
    "C2": 89,
    "C1": 158,
    "B2+": 11,
    "B2": 267,
    "B1+": 4,
    "B1": 287,
    "A2+": 3,
    "A2": 257,
    "A1": 101,
    "Pre-A1": 47,
}


def _compact(text: str) -> str:
    text = text.replace("\xad", "")
    text = re.sub(r"(?<=\w)([-/])\s+(?=\w)", r"\1", text)
    return re.sub(r"\s+", "", text)


class CefrAllExtractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not PDF.exists():
            raise unittest.SkipTest("CEFR source PDF is unavailable")
        cls.rows = extract_descriptors(PDF)

    def test_all_levels_and_modes_are_present(self) -> None:
        self.assertEqual(set(LEVEL_TO_CODE), {row.level_text for row in self.rows})
        self.assertEqual(7, len({row.mode for row in self.rows}))

    def test_source_table_counts_are_locked(self) -> None:
        self.assertEqual(EXPECTED_LEVEL_COUNTS, dict(Counter(row.level_text for row in self.rows)))
        self.assertEqual(1224, len(self.rows))
        self.assertEqual(85, len({(row.mode, row.skill, row.scale) for row in self.rows}))

    def test_existing_a1_scope_is_preserved_exactly(self) -> None:
        expected, _ = extract_a1(PDF)
        actual = Counter(
            (row.page, row.scale, row.text) for row in self.rows if row.level_text == "A1"
        )
        for row in expected:
            scale = row.scale
            if scale == "Goal-oriented co-operation":
                scale = (
                    "Goal-oriented co-operation (cooking together, discussing a document, "
                    "organising an event, etc.)"
                )
            self.assertGreater(actual[(row.page, scale, row.text)], 0)

    def test_every_descriptor_occurs_on_its_cited_page(self) -> None:
        document = fitz.open(PDF)
        pages = {}
        for row in self.rows:
            pages.setdefault(row.page, _compact(document[row.page - 1].get_text("text")))
            self.assertIn(_compact(row.text), pages[row.page])

    def test_records_are_unique_and_dataset_validates(self) -> None:
        records = build_collection(self.rows)["records"]
        self.assertEqual(len(records), len({row["record_id"] for row in records}))
        self.assertEqual([], validate_dataset(DATASET))


if __name__ == "__main__":
    unittest.main()
