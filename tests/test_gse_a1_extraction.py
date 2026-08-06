"""Completeness and duplicate tests for Pearson GSE A1 extraction."""

from __future__ import annotations

import hashlib
import unittest
from collections import Counter
from pathlib import Path

from scripts.gse_a1_parser import A1_PAGES, extract_objectives
from scripts.gse_a1_records import build_collection


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PDF = PROJECT_ROOT / "sources/raw/frameworks/gse-learning-objectives-adult-general-english-2022.pdf"


class GseA1ExtractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not PDF.exists():
            raise unittest.SkipTest(
                'GSE source PDF is local-only; see sources/registry/SOURCES.md'
            )
        cls.objectives = extract_objectives(PDF)

    def test_expected_counts_and_pages(self) -> None:
        counts = Counter(item.skill for item in self.objectives)
        self.assertEqual(
            {"Reading": 14, "Listening": 34, "Speaking": 54, "Writing": 19},
            dict(counts),
        )
        pages = {skill: sorted({item.page for item in self.objectives if item.skill == skill}) for skill in A1_PAGES}
        self.assertEqual({skill: list(value) for skill, value in A1_PAGES.items()}, pages)

    def test_only_a1_scores_and_complete_objectives(self) -> None:
        for item in self.objectives:
            self.assertIn(int(item.score), range(22, 30))
            self.assertTrue(item.text.startswith("Can "))
            self.assertTrue(item.text.endswith(f"({item.source_code})"))
            self.assertNotRegex(item.text, r"’\s+[,.!?;:]")

    def test_exact_source_duplicate_is_reconciled(self) -> None:
        grouped = Counter((item.skill, item.text) for item in self.objectives)
        duplicates = [key for key, count in grouped.items() if count > 1]
        self.assertEqual(1, len(duplicates))
        skill, text = duplicates[0]
        self.assertEqual("Listening", skill)
        self.assertEqual(
            "Can identify a caller’s name and phone number from a short, simple telephone conversation. (P)",
            text,
        )
        rows = [item for item in self.objectives if (item.skill, item.text) == duplicates[0]]
        self.assertEqual(["23", "26"], [item.score for item in rows])

    def test_records_have_unique_ids_hashes_and_one_exclusion(self) -> None:
        collection = build_collection(self.objectives)
        records = collection["records"]
        self.assertEqual(len(records), len({item["record_id"] for item in records}))
        for record in records:
            text = record["source"]["source_text"]
            self.assertEqual(
                hashlib.sha256(text.encode("utf-8")).hexdigest(),
                record["source"]["source_text_sha256"],
            )
        statuses = Counter(item["interpretation"]["inclusion_status"] for item in records)
        self.assertEqual({"included": 120, "excluded": 1}, dict(statuses))

    def test_review_metadata_is_all_or_nothing(self) -> None:
        with self.assertRaises(ValueError):
            build_collection(self.objectives, reviewer="cur_002_primary")
        collection = build_collection(
            self.objectives,
            reviewer="cur_002_primary",
            reviewed_at="2026-07-15T20:00:00Z",
        )
        self.assertTrue(all(item["review"]["status"] == "accepted" for item in collection["records"]))


if __name__ == "__main__":
    unittest.main()
