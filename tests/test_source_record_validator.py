"""Contract tests for the curriculum source-record validator."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from scripts.validate_source_records import validate_dataset


class SourceRecordValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        raw_path = self.root / "sources" / "raw" / "frameworks" / "fixture.pdf"
        raw_path.parent.mkdir(parents=True)
        raw_path.write_bytes(b"schema fixture only")
        self.raw_hash = hashlib.sha256(raw_path.read_bytes()).hexdigest()
        self.text = "Fixture source wording."
        self.dataset = {
            "schema_version": "1.0.0",
            "dataset_id": "source_record_fixture",
            "records": [self._record("fixture.objective.001")],
        }

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _record(self, record_id: str) -> dict:
        return {
            "record_id": record_id,
            "record_kind": "objective",
            "source": {
                "source_id": "fixture_source",
                "source_version": "test-only",
                "raw_file": "sources/raw/frameworks/fixture.pdf",
                "source_file_sha256": self.raw_hash,
                "location": {
                    "kind": "pdf_page",
                    "page": 1,
                    "page_end": 1,
                    "printed_page": None,
                    "section": "Fixture",
                },
                "source_text": self.text,
                "source_text_sha256": hashlib.sha256(self.text.encode()).hexdigest(),
                "transcription_notes": [],
            },
            "source_facts": {
                "source_record_id": None,
                "level_text": "A1",
                "gse_score_or_range": None,
                "skill_text": "Fixture skill",
                "mode_text": None,
                "function_text": None,
                "scale_text": None,
                "other_verbatim": {},
            },
            "interpretation": {
                "inclusion_status": "undecided",
                "exclusion_reason": None,
                "cefr_codes": ["a1"],
                "skill_codes": [],
                "mode_codes": [],
                "function_codes": [],
                "candidate_cluster_ids": [],
                "notes": [],
                "ambiguities": [],
            },
            "review": {
                "status": "unreviewed",
                "reviewer": None,
                "reviewed_at": None,
                "issues": [],
            },
        }

    def _validate(self, dataset: dict, reviewed: bool = False) -> list[str]:
        folder = self.root / "data" / ("reviewed" if reviewed else "derived")
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / "fixture.json"
        path.write_text(json.dumps(dataset), encoding="utf-8")
        return validate_dataset(path, self.root)

    def test_valid_unreviewed_record_passes(self) -> None:
        self.assertEqual([], self._validate(self.dataset))

    def test_duplicate_and_text_hash_are_rejected(self) -> None:
        dataset = deepcopy(self.dataset)
        duplicate = deepcopy(dataset["records"][0])
        duplicate["source"]["source_text_sha256"] = "0" * 64
        dataset["records"].append(duplicate)
        errors = self._validate(dataset)
        self.assertTrue(any("duplicate" in error for error in errors))
        self.assertTrue(any("source_text_sha256" in error for error in errors))

    def test_exclusion_requires_reason(self) -> None:
        dataset = deepcopy(self.dataset)
        dataset["records"][0]["interpretation"]["inclusion_status"] = "excluded"
        errors = self._validate(dataset)
        self.assertTrue(any("exclusion needs a reason" in error for error in errors))

    def test_reviewed_dataset_requires_accepted_record(self) -> None:
        errors = self._validate(self.dataset, reviewed=True)
        self.assertTrue(any("reviewed datasets" in error for error in errors))

    def test_reviewed_dataset_accepts_final_record(self) -> None:
        dataset = deepcopy(self.dataset)
        review = dataset["records"][0]["review"]
        review.update(
            status="accepted",
            reviewer="curriculum_reviewer",
            reviewed_at="2026-07-15T18:00:00Z",
        )
        self.assertEqual([], self._validate(dataset, reviewed=True))

    def test_accepted_record_needs_identity_and_no_error(self) -> None:
        dataset = deepcopy(self.dataset)
        review = dataset["records"][0]["review"]
        review["status"] = "accepted"
        review["issues"] = [{"code": "bad_text", "severity": "error", "message": "Mismatch"}]
        errors = self._validate(dataset)
        self.assertTrue(any("reviewer and time" in error for error in errors))
        self.assertTrue(any("accepted record has an error" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
