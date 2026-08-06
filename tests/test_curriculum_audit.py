"""Acceptance tests for the CUR-006 curriculum audit."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.curriculum_audit import build_curriculum_audit
from scripts.validate_curriculum_audit import validation_errors


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATHS = (
    PROJECT_ROOT / "data/reviewed/gse-a1-objectives.json",
    PROJECT_ROOT / "data/reviewed/cefr-a1-descriptors.json",
)
MAP_PATH = PROJECT_ROOT / "data/reviewed/a1-candidate-unit-map.json"
AUDIT_PATH = PROJECT_ROOT / "data/reviewed/a1-curriculum-audit.json"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class CurriculumAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.collections = [load(path) for path in SOURCE_PATHS]
        cls.candidate_map = load(MAP_PATH)
        cls.audit = load(AUDIT_PATH)

    def test_audit_is_deterministic_and_schema_valid(self) -> None:
        expected = build_curriculum_audit(
            self.collections, self.candidate_map, self.audit["reviewed_at"]
        )
        self.assertEqual(expected, self.audit)
        self.assertEqual([], validation_errors(AUDIT_PATH))

    def test_coverage_has_no_orphans_or_unmapped_inclusions(self) -> None:
        coverage = self.audit["coverage"]
        self.assertEqual(219, coverage["reviewed_record_count"])
        self.assertEqual(218, coverage["included_count"])
        self.assertEqual(218, coverage["mapped_included_count"])
        for field in (
            "unmapped_included_ids", "mapped_excluded_ids",
            "assignment_orphan_ids", "source_orphan_ids", "empty_cluster_ids",
            "candidate_clusters_without_objectives",
            "candidate_clusters_without_descriptors",
        ):
            self.assertEqual([], coverage[field])

    def test_all_repeated_wording_is_reconciled(self) -> None:
        groups = self.audit["duplicate_groups"]
        self.assertEqual(3, len(groups))
        self.assertEqual(
            {"exclude_repeated_source_row": 1, "retain_distinct_scale_placements": 2},
            {
                resolution: sum(g["resolution"] == resolution for g in groups)
                for resolution in {
                    "exclude_repeated_source_row",
                    "retain_distinct_scale_placements",
                }
            },
        )
        excluded = next(
            group for group in groups
            if group["resolution"] == "exclude_repeated_source_row"
        )
        self.assertEqual("gse.adult.2022.p14.005", excluded["canonical_record_id"])

    def test_support_dependencies_are_cited_without_inventing_order(self) -> None:
        prerequisite = self.audit["prerequisite_audit"]
        self.assertEqual([], prerequisite["strict_cluster_prerequisites"])
        self.assertEqual(2, len(prerequisite["support_needs"]))
        for need in prerequisite["support_needs"]:
            self.assertEqual(8, len(need["target_cluster_ids"]))
            self.assertTrue(need["evidence_refs"])
            for evidence in need["evidence_refs"]:
                self.assertTrue(evidence["raw_file"].startswith("sources/raw/"))
                self.assertIn("page", evidence["location"])

    def test_skill_gaps_are_explicit_and_not_filled_by_invention(self) -> None:
        rows = {
            row["cluster_id"]: row for row in self.audit["balance"]["clusters"]
            if row["role"] == "candidate_unit"
        }
        expected_gaps = {
            "people_relationships": ["reading"],
            "food_shopping_services": ["reading", "writing"],
            "messages_signs_forms": ["speaking"],
            "social_contact_collaboration": ["reading"],
        }
        self.assertEqual(
            expected_gaps,
            {
                key: row["objective_skill_gaps"]
                for key, row in rows.items() if row["objective_skill_gaps"]
            },
        )
        self.assertTrue(all(not row["combined_skill_gaps"] for row in rows.values()))

    def test_builder_does_not_mutate_source_evidence(self) -> None:
        before = copy.deepcopy((self.collections, self.candidate_map))
        build_curriculum_audit(
            self.collections, self.candidate_map, "2026-07-16T23:10:21+03:00"
        )
        self.assertEqual(before, (self.collections, self.candidate_map))


if __name__ == "__main__":
    unittest.main()
