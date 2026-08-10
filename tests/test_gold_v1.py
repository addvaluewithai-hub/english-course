"""Contract tests for the A1 v1 position of the accepted gold lesson."""

import json
import unittest

from scripts.gold_v1_contract import OUTPUT, REQUIRED_INTRODUCTIONS, REQUIRED_RECYCLES
from scripts.gold_v1_validation_core import validate
from scripts.migrate_gold_to_a1_v1 import build_outputs


class GoldLessonV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads((OUTPUT / "lesson-manifest.json").read_text(encoding="utf-8"))
        cls.packet = json.loads((OUTPUT / "source-packet.json").read_text(encoding="utf-8"))
        cls.content = json.loads((OUTPUT / "content.json").read_text(encoding="utf-8"))
        cls.activities = json.loads((OUTPUT / "activities.json").read_text(encoding="utf-8"))
        cls.assessment = json.loads((OUTPUT / "assessment.json").read_text(encoding="utf-8"))

    def test_complete_package_is_valid_and_deterministic(self) -> None:
        self.assertEqual([], validate())
        self.assertEqual(12, len(build_outputs()))

    def test_gold_is_final_u1_l03_after_two_prerequisites(self) -> None:
        self.assertEqual("U1-L03", self.manifest["lesson_id"])
        self.assertEqual(3, self.manifest["global_sequence_position"])
        self.assertEqual(["U1-L01", "U1-L02"], self.manifest["prerequisites"])

    def test_exact_curriculum_ownership_is_locked(self) -> None:
        introductions = {row["item_id"] for row in self.packet["exact_introductions"]}
        recycles = {row["item_id"] for row in self.packet["exact_recycles"]}
        self.assertEqual(REQUIRED_INTRODUCTIONS, introductions)
        self.assertEqual(REQUIRED_RECYCLES, recycles)

    def test_video_is_one_teacher_and_interaction_free(self) -> None:
        self.assertEqual(1, self.manifest["video"]["speaker_count"])
        self.assertFalse(self.manifest["video"]["interaction_during_video"])
        self.assertTrue(self.content["delivery"]["interaction_starts_after_video"])

    def test_bounded_new_forms_have_application(self) -> None:
        activity_ids = {row["id"] for row in self.activities["activities"]}
        self.assertIn("my_and_job_articles", activity_ids)
        self.assertIn("My name is ...", self.content["curriculum_alignment"]["bounded_new_forms"])

    def test_mastery_is_fresh_and_non_answer_bearing(self) -> None:
        task = self.assessment["mastery_task"]
        self.assertIn("no sentence frames or model", task["support"])
        self.assertIn("no complete introduction", task["prior_lesson_support"])
        self.assertTrue(task["safe_identity"])


if __name__ == "__main__":
    unittest.main()
