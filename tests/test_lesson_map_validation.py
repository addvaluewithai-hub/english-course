"""Acceptance tests for the LESSON-002 lesson-map validation partition."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.lesson_map_validation import validation_errors
from tests.lesson_map_fixtures import source_record, valid_fixture


class LessonMapValidationTests(unittest.TestCase):
    def errors(self, lesson_map: dict, collections: list[dict]) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            map_path = root / "map.json"
            map_path.write_text(json.dumps(lesson_map), encoding="utf-8")
            source_paths = []
            for index, collection in enumerate(collections):
                path = root / f"source-{index}.json"
                path.write_text(json.dumps(collection), encoding="utf-8")
                source_paths.append(path)
            return validation_errors(map_path, tuple(source_paths))

    def test_complete_approved_fixture_passes(self) -> None:
        lesson_map, collections = valid_fixture()
        self.assertEqual([], self.errors(lesson_map, collections))

    def test_exact_provenance_is_required(self) -> None:
        lesson_map, collections = valid_fixture()
        lesson_map["candidates"][0]["evidence_refs"][0]["location"]["page"] = 99
        errors = self.errors(lesson_map, collections)
        self.assertTrue(any("location does not match" in error for error in errors))

    def test_approved_map_reconciles_every_included_record(self) -> None:
        lesson_map, collections = valid_fixture()
        collections[0]["records"].append(source_record(
            "fixture.uncovered", "fixture_one", 4, "D",
            skills=["reading"], modes=["reception"],
            functions=["comprehend_information"],
        ))
        errors = self.errors(lesson_map, collections)
        self.assertTrue(any("uncovered" in error for error in errors))

    def test_context_only_citation_does_not_satisfy_coverage(self) -> None:
        lesson_map, collections = valid_fixture()
        lesson_map["candidates"][0]["evidence_refs"][0]["coverage"] = "context_only"
        errors = self.errors(lesson_map, collections)
        self.assertTrue(any("uncovered" in error for error in errors))

    def test_in_progress_map_may_be_incomplete(self) -> None:
        lesson_map, collections = valid_fixture()
        collections[0]["records"].append(source_record(
            "fixture.pending", "fixture_one", 5, "E",
            skills=["reading"], modes=["reception"],
            functions=["locate_information"],
        ))
        lesson_map["status"] = "in_progress"
        lesson_map["review"] = {
            "status": "unreviewed", "reviewer": None, "reviewed_at": None, "issues": [],
        }
        lesson_map["candidates"][0]["status"] = "draft"
        lesson_map["candidates"][0]["review"] = {
            "status": "unreviewed", "reviewer": None, "reviewed_at": None, "issues": [],
        }
        self.assertEqual([], self.errors(lesson_map, collections))

    def test_full_anchor_cannot_be_duplicated(self) -> None:
        lesson_map, collections = valid_fixture()
        duplicate = copy.deepcopy(lesson_map["candidates"][0])
        duplicate["candidate_id"] = "lesson_candidate.fixture_duplicate"
        lesson_map["candidates"].append(duplicate)
        lesson_map["sequence"].append(duplicate["candidate_id"])
        for support in lesson_map["support_definitions"]:
            support["applies_to_candidate_ids"].append(duplicate["candidate_id"])
        errors = self.errors(lesson_map, collections)
        self.assertTrue(any("full anchor is duplicated" in error for error in errors))

    def test_hard_prerequisite_cycle_is_rejected(self) -> None:
        lesson_map, collections = valid_fixture()
        second = copy.deepcopy(lesson_map["candidates"][0])
        first = lesson_map["candidates"][0]
        second["candidate_id"] = "lesson_candidate.fixture_second"
        first["relationships"]["required_before"] = [self.relation(second["candidate_id"])]
        first["relationships"]["successors"] = [self.relation(second["candidate_id"])]
        second["relationships"]["required_before"] = [self.relation(first["candidate_id"])]
        second["relationships"]["successors"] = [self.relation(first["candidate_id"])]
        lesson_map["candidates"].append(second)
        lesson_map["sequence"].append(second["candidate_id"])
        for support in lesson_map["support_definitions"]:
            support["applies_to_candidate_ids"].append(second["candidate_id"])
        errors = self.errors(lesson_map, collections)
        self.assertTrue(any("contain a cycle" in error for error in errors))

    def test_interaction_candidate_requires_repair_support(self) -> None:
        lesson_map, collections = valid_fixture()
        candidate = lesson_map["candidates"][0]
        candidate["relationships"]["concurrent_support"].pop()
        lesson_map["support_definitions"].pop()
        errors = self.errors(lesson_map, collections)
        self.assertTrue(any("interaction_repair" in error for error in errors))

    def test_mastery_dimension_keys_must_match(self) -> None:
        lesson_map, collections = valid_fixture()
        del lesson_map["candidates"][0]["mastery"]["level_2_evidence"]["control_or_repair"]
        errors = self.errors(lesson_map, collections)
        self.assertTrue(any("level_2_evidence keys" in error for error in errors))

    @staticmethod
    def relation(candidate_id: str) -> dict:
        return {
            "candidate_id": candidate_id,
            "rationale": "Synthetic dependency for cycle testing.",
            "evidence_record_ids": ["fixture.anchor"],
        }


if __name__ == "__main__":
    unittest.main()
