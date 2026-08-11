"""Tests for TEST-002 aggregation without claiming synthetic evidence."""

import json
import unittest

from scripts.learner_test_analysis_core import analyze
from scripts.learner_test_v1_contract import THRESHOLDS
from scripts.render_learner_test_analysis import render
from tests.learner_test_fixtures import synthetic_record


class LearnerTestAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.thresholds = json.loads(THRESHOLDS.read_text(encoding="utf-8"))

    def test_passing_fixture_only_has_hypothetical_go(self) -> None:
        result = analyze(
            [synthetic_record(index) for index in range(1, 9)],
            self.thresholds, "synthetic_fixtures",
        )
        self.assertEqual("go_to_system_revision", result["hypothetical_decision"])
        self.assertEqual("simulation_only_no_gate_effect", result["gate_effect"])
        self.assertIn("cannot\ncomplete TEST-002", render(result))

    def test_same_counts_from_real_mode_can_open_next_gate(self) -> None:
        result = analyze(
            [synthetic_record(index) for index in range(1, 9)],
            self.thresholds, "real_consented_sessions",
        )
        self.assertEqual("go_to_system_revision", result["gate_effect"])
        self.assertEqual(8, result["sample"]["eligible_completed_sessions"])
        self.assertEqual(2, result["sample"]["double_rated_sessions"])

    def test_privacy_incident_forces_stop(self) -> None:
        records = [synthetic_record(index) for index in range(1, 9)]
        records[0]["issues"] = [{
            "type": "privacy", "severity": "major", "resolved": True,
            "note": "Preventable privacy event, described without learner identity.",
        }]
        result = analyze(records, self.thresholds, "real_consented_sessions")
        self.assertEqual("stop_and_redesign", result["gate_effect"])

    def test_too_few_sessions_is_insufficient(self) -> None:
        result = analyze(
            [synthetic_record(index) for index in range(1, 5)],
            self.thresholds, "real_consented_sessions",
        )
        self.assertEqual("insufficient_evidence", result["gate_effect"])

    def test_low_demonstration_rate_requires_revision(self) -> None:
        records = [synthetic_record(index, demonstrated=index <= 3) for index in range(1, 9)]
        result = analyze(records, self.thresholds, "real_consented_sessions")
        self.assertEqual("revise_and_retest", result["gate_effect"])

    def test_aggregate_drops_individual_issue_notes(self) -> None:
        records = [synthetic_record(index) for index in range(1, 9)]
        secret_note = "unique private observation text"
        records[0]["issues"] = [{
            "type": "navigation", "severity": "minor", "resolved": True,
            "note": secret_note,
        }]
        result = analyze(records, self.thresholds, "synthetic_fixtures")
        self.assertNotIn(secret_note, json.dumps(result))
        self.assertEqual(1, result["descriptive"]["issues"]["by_type"]["navigation"])

    def test_duplicate_session_id_is_rejected(self) -> None:
        record = synthetic_record(1)
        with self.assertRaisesRegex(ValueError, "duplicate session_id"):
            analyze([record, record], self.thresholds, "synthetic_fixtures")


if __name__ == "__main__":
    unittest.main()
