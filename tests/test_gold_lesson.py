"""Contract tests for the first complete gold lesson."""

from __future__ import annotations

import unittest

from scripts.validate_gold_lesson import JSON_FILES, load, validation_errors


class GoldLessonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.files = {name: load(path) for name, path in JSON_FILES.items()}

    def test_complete_contract_validates(self) -> None:
        self.assertEqual([], validation_errors())

    def test_selected_candidate_and_sources_are_approved(self) -> None:
        manifest = self.files["lesson-manifest.json"]
        packet = self.files["source-packet.json"]
        self.assertEqual(manifest["candidate_id"], packet["selected_candidate_id"])
        self.assertEqual("approved_candidate", packet["candidate"]["status"])
        self.assertEqual(6, len(packet["source_records"]))

    def test_lesson_moves_from_support_to_fresh_performance(self) -> None:
        manifest = self.files["lesson-manifest.json"]
        order = manifest["section_order"]
        self.assertLess(order.index("guided_practice"), order.index("ai_practice"))
        self.assertLess(order.index("ai_practice"), order.index("fresh_mastery"))
        self.assertLess(order.index("fresh_mastery"), order.index("teach_back_variant"))

    def test_mastery_is_not_completion_or_teach_back(self) -> None:
        assessment = self.files["assessment.json"]
        self.assertIn("never grants mastery", assessment["decision"]["completion_rule"])
        self.assertTrue(assessment["teach_back_variant"]["cannot_rescue_failed_mastery"])
        self.assertTrue(assessment["mastery_task"]["safe_identity"])

    def test_ai_is_bounded_and_cannot_assign_mastery(self) -> None:
        contract = self.files["ai-contract.json"]
        self.assertLessEqual(contract["turn_limit"], 6)
        self.assertTrue(any("Never claim mastery" in item for item in contract["behavior"]))


if __name__ == "__main__":
    unittest.main()
