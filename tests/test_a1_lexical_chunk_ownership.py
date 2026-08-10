"""Contract tests for exact A1 lexical sets, chunks, and Oxford coverage."""

import json
import unittest

from scripts.a1_lexical_ownership_contract import OUTPUT
from scripts.create_a1_lexical_chunk_ownership import build
from scripts.validate_a1_lexical_chunk_ownership import validate


class A1LexicalChunkOwnershipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(OUTPUT.read_text(encoding="utf-8"))
        cls.items = {row["lexical_item_id"]: row for row in cls.data["course_items"]}

    def test_artifact_is_valid_and_deterministic(self) -> None:
        self.assertEqual([], validate())
        self.assertEqual(self.data, build())

    def test_every_oxford_a1_row_has_one_deliberate_disposition(self) -> None:
        audit = self.data["audit"]
        self.assertEqual(900, audit["oxford_a1_record_count"])
        self.assertEqual(537, audit["selected_oxford_record_count"])
        self.assertEqual(87, audit["grammar_owned_oxford_record_count"])
        self.assertEqual(276, audit["reference_pool_record_count"])
        self.assertEqual(900, sum(audit["oxford_disposition_counts"].values()))

    def test_selected_syllabus_is_exact_but_not_a_word_count_claim(self) -> None:
        audit = self.data["audit"]
        self.assertEqual(104, audit["course_item_count"])
        self.assertEqual(760, audit["distinct_member_count"])
        self.assertIn("not an automatic word-count promise", self.data["policy"]["reference_pool_role"])
        self.assertGreater(audit["reference_pool_record_count"], 0)

    def test_all_legacy_vocabulary_and_phrase_targets_have_owners(self) -> None:
        audit = self.data["audit"]
        self.assertEqual(75, audit["legacy_vocabulary_candidate_count"])
        self.assertEqual(77, audit["legacy_phrase_candidate_count"])
        self.assertEqual([], audit["uncovered_vocabulary_candidate_ids"])
        self.assertEqual([], audit["uncovered_phrase_candidate_ids"])

    def test_every_item_has_evidence_and_a_fresh_recycle(self) -> None:
        audit = self.data["audit"]
        self.assertEqual([], audit["items_without_source_refs"])
        self.assertEqual([], audit["items_without_recycle_locations"])
        for row in self.data["course_items"]:
            self.assertNotIn(row["introduction_location"], row["recycle_locations"])

    def test_personal_open_categories_are_not_arbitrary_lists(self) -> None:
        item = self.items["lexical.own_country_nationality"]
        self.assertEqual("personalized_slot", item["item_type"])
        self.assertIn("learner's country", item["members"][0])
        self.assertEqual(0, self.data["audit"]["final_lesson_decisions_made"])


if __name__ == "__main__":
    unittest.main()
