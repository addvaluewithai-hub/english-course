"""Coverage and evidence-boundary tests for CUR-005 candidate clustering."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.candidate_clustering import cluster_collection
from scripts.candidate_map import build_candidate_map
from scripts.cluster_model import CLUSTER_IDS


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REVIEWED = (
    PROJECT_ROOT / "data/reviewed/gse-a1-objectives.json",
    PROJECT_ROOT / "data/reviewed/cefr-a1-descriptors.json",
)


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class CandidateClusteringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.originals = [load(path) for path in REVIEWED]
        cls.clustered = [cluster_collection(item) for item in cls.originals]
        cls.records = [record for data in cls.clustered for record in data["records"]]
        cls.candidate_map = build_candidate_map(cls.clustered, "2026-07-16T05:05:00+03:00")

    def test_all_included_records_are_mapped_and_exclusion_is_unmapped(self) -> None:
        included = [r for r in self.records if r["interpretation"]["inclusion_status"] == "included"]
        excluded = [r for r in self.records if r["interpretation"]["inclusion_status"] == "excluded"]
        self.assertEqual(218, len(included))
        self.assertEqual(1, len(excluded))
        self.assertTrue(all(r["interpretation"]["candidate_cluster_ids"] for r in included))
        self.assertTrue(all(not r["interpretation"]["candidate_cluster_ids"] for r in excluded))

    def test_cluster_ids_are_controlled(self) -> None:
        allowed = set(CLUSTER_IDS)
        for record in self.records:
            self.assertLessEqual(
                set(record["interpretation"]["candidate_cluster_ids"]), allowed
            )

    def test_source_evidence_source_facts_and_tags_are_unchanged(self) -> None:
        for original, clustered in zip(self.originals, self.clustered, strict=True):
            for before, after in zip(original["records"], clustered["records"], strict=True):
                self.assertEqual(before["source"], after["source"])
                self.assertEqual(before["source_facts"], after["source_facts"])
                for field in ("cefr_codes", "skill_codes", "mode_codes", "function_codes"):
                    self.assertEqual(
                        before["interpretation"][field], after["interpretation"][field]
                    )

    def test_clustering_is_idempotent(self) -> None:
        for clustered in self.clustered:
            self.assertEqual(clustered, cluster_collection(clustered))

    def test_representative_semantic_mappings(self) -> None:
        records = {record["record_id"]: record for record in self.records}
        expected = {
            "gse.adult.2022.p22.009": "identity_personal_information",
            "gse.adult.2022.p24.005": "places_directions_travel",
            "gse.adult.2022.p37.016": "messages_signs_forms",
            "cefr.cv2020.p089.asking_for_clarification.02": "communication_strategies",
            "cefr.cv2020.p132.grammatical_accuracy.01": "language_foundations",
        }
        for record_id, cluster_id in expected.items():
            self.assertIn(cluster_id, records[record_id]["interpretation"]["candidate_cluster_ids"])

    def test_prior_seven_unit_proposal_is_not_forced(self) -> None:
        proposal = self.candidate_map["prior_proposal_test"]
        self.assertEqual("not_supported_as_an_exact_final_map", proposal["verdict"])
        self.assertGreater(proposal["fit_counts"]["forced"], 0)
        self.assertGreater(proposal["fit_counts"]["overlap"], 0)
        objective_fits = proposal["objective_fit_counts"]
        self.assertEqual(
            120, sum(objective_fits[key] for key in ("natural", "overlap", "forced"))
        )

    def test_map_is_traceable_and_complete(self) -> None:
        candidate_map = self.candidate_map
        self.assertEqual(219, candidate_map["coverage"]["record_count"])
        self.assertEqual(10, len(candidate_map["clusters"]))
        source_ids = {record["record_id"] for record in self.records}
        map_ids = {item["record_id"] for item in candidate_map["assignments"]}
        self.assertEqual(source_ids, map_ids)
        for item in candidate_map["assignments"]:
            self.assertTrue(item["raw_file"].startswith("sources/raw/"))
            self.assertEqual(64, len(item["source_text_sha256"]))


if __name__ == "__main__":
    unittest.main()
