"""Acceptance tests for the LESSON-002 global audit partition."""

from __future__ import annotations

import unittest

from scripts.create_lesson_map_global_audit import JSON_PATH, build_audit
from scripts.lesson_language_target_model import DECISIONS
from scripts.lesson_map_io import DEFAULT_MAP_PATH, load
from scripts.lesson_map_validation import validation_errors


class LessonMapGlobalAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = load(JSON_PATH)

    def test_saved_audit_matches_deterministic_builder(self) -> None:
        self.assertEqual(build_audit(), self.audit)

    def test_source_exact_map_still_validates(self) -> None:
        self.assertEqual([], validation_errors(DEFAULT_MAP_PATH))
        coverage = self.audit["coverage"]
        self.assertEqual(218, coverage["included_records"])
        self.assertEqual(218, coverage["cited_included_records"])
        self.assertEqual([], coverage["orphan_record_ids"])

    def test_overlap_review_has_explicit_dispositions(self) -> None:
        rows = self.audit["overlap_review"]
        self.assertEqual(10, len(rows))
        self.assertEqual(5, sum(row["status"] == "resolved_merge" for row in rows))
        self.assertTrue(all(row["rationale"] for row in rows))

    def test_relationship_and_sequence_review_is_explicit(self) -> None:
        relations = self.audit["relationships_and_sequence"]
        self.assertTrue(relations["sequence_covers_every_candidate_once"])
        self.assertEqual(5, relations["required_before"])
        self.assertEqual(43, relations["helpful_before"])
        self.assertEqual(5, relations["successors"])
        self.assertEqual(5, relations["sequence_bands"])
        self.assertEqual("accepted", relations["status"])
        self.assertFalse(relations["source_proven_strict_order"])

    def test_mastery_and_candidate_approval_are_complete(self) -> None:
        self.assertEqual([], self.audit["mastery"]["alignment_issues"])
        self.assertEqual(2, len(self.audit["mastery"]["alignment_decisions"]))
        approval = self.audit["approval"]
        self.assertEqual({"approved_candidate": 81}, approval["candidate_status_counts"])
        self.assertEqual({"accepted": 81}, approval["candidate_review_counts"])
        self.assertEqual([], approval["empty_language_target_candidate_ids"])
        self.assertEqual([], approval["empty_error_hypothesis_candidate_ids"])

    def test_phase_gate_decision_passes(self) -> None:
        decision = self.audit["decision"]
        self.assertEqual("passed", decision["status"])
        self.assertTrue(decision["lesson_002_may_pass"])
        self.assertEqual(0, decision["open_overlap_groups"])
        self.assertIn("gold lesson", decision["next_partition"])


if __name__ == "__main__":
    unittest.main()
