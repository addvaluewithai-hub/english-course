"""Coverage and evidence-boundary tests for CUR-004 normalization."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.curriculum_tagging import normalize_collection
from scripts.tag_model import FUNCTION_CODES, MODE_CODES, SKILL_CODES


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REVIEWED = (
    PROJECT_ROOT / "data/reviewed/gse-a1-objectives.json",
    PROJECT_ROOT / "data/reviewed/cefr-a1-descriptors.json",
)


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class CurriculumTaggingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.originals = [load(path) for path in REVIEWED]
        cls.normalized = [normalize_collection(item) for item in cls.originals]

    def test_all_219_records_receive_controlled_tags(self) -> None:
        records = [record for data in self.normalized for record in data["records"]]
        self.assertEqual(219, len(records))
        for record in records:
            interpretation = record["interpretation"]
            self.assertTrue(interpretation["skill_codes"])
            self.assertTrue(interpretation["mode_codes"])
            self.assertTrue(interpretation["function_codes"])
            self.assertLessEqual(set(interpretation["skill_codes"]), SKILL_CODES)
            self.assertLessEqual(set(interpretation["mode_codes"]), MODE_CODES)
            self.assertLessEqual(set(interpretation["function_codes"]), FUNCTION_CODES)

    def test_source_evidence_and_source_facts_are_unchanged(self) -> None:
        for original, normalized in zip(self.originals, self.normalized, strict=True):
            for before, after in zip(original["records"], normalized["records"], strict=True):
                self.assertEqual(before["record_id"], after["record_id"])
                self.assertEqual(before["source"], after["source"])
                self.assertEqual(before["source_facts"], after["source_facts"])
                self.assertEqual(
                    before["interpretation"]["inclusion_status"],
                    after["interpretation"]["inclusion_status"],
                )
                self.assertEqual(
                    before["interpretation"]["candidate_cluster_ids"],
                    after["interpretation"]["candidate_cluster_ids"],
                )

    def test_tagging_is_idempotent(self) -> None:
        for normalized in self.normalized:
            self.assertEqual(normalized, normalize_collection(normalized))

    def test_source_labels_map_to_expected_primary_channels(self) -> None:
        gse = self.normalized[0]["records"]
        expected = {
            "Reading": "reading", "Listening": "listening",
            "Speaking": "speaking", "Writing": "writing",
        }
        for record in gse:
            source_skill = record["source_facts"]["skill_text"]
            self.assertIn(expected[source_skill], record["interpretation"]["skill_codes"])

    def test_genuine_channel_ambiguity_is_flagged(self) -> None:
        cefr = {record["record_id"]: record for record in self.normalized[1]["records"]}
        record = cefr["cefr.cv2020.p107.expressing_a_personal_response_to_creative_texts.01"]
        self.assertEqual(["speaking", "writing"], record["interpretation"]["skill_codes"])
        self.assertTrue(any("does not fix" in item for item in record["interpretation"]["ambiguities"]))

    def test_record_actions_override_broad_source_labels(self) -> None:
        gse = {record["record_id"]: record for record in self.normalized[0]["records"]}
        cefr = {record["record_id"]: record for record in self.normalized[1]["records"]}
        self.assertEqual(["interaction"], gse["gse.adult.2022.p22.004"]["interpretation"]["mode_codes"])
        self.assertEqual(["production"], gse["gse.adult.2022.p22.007"]["interpretation"]["mode_codes"])
        self.assertEqual(["locate_information"], cefr["cefr.cv2020.p051.understanding_announcements_and_instructions.03"]["interpretation"]["function_codes"])
        self.assertEqual(["follow_instructions"], cefr["cefr.cv2020.p073.understanding_an_interlocutor.02"]["interpretation"]["function_codes"])
        self.assertEqual(["reading", "speaking"], cefr["cefr.cv2020.p104.translating_a_written_text_in_speech_or.01"]["interpretation"]["skill_codes"])

    def test_review_metadata_must_be_paired(self) -> None:
        with self.assertRaises(ValueError):
            normalize_collection(self.originals[0], reviewer="cur_004_primary")


if __name__ == "__main__":
    unittest.main()
