import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.first_ten_pilot_contract import STATION_IDS, VISIT_PLAN
from scripts.first_ten_pilot_record_validation import validate_record
from scripts.validate_first_ten_progression_records import validate_directory
from scripts.validate_first_ten_pilot import validate


def attempt(decision="demonstrated"):
    rated = decision != "not_rated"
    score = 2 if rated else None
    return {
        "attempted": rated,
        "answer_model_visible": False,
        "ratings": {
            "comprehension": score,
            "outcome": score,
            "transfer": score,
            "control_or_repair": score,
        },
        "decision": decision,
        "secondary_decision": None,
        "exact_agreement": None,
    }


def lesson(lesson_id):
    return {
        "lesson_id": lesson_id,
        "completed": True,
        "duration_seconds": 600,
        "help": {"non_answer_revealing_count": 0, "answer_revealing_count": 0},
        "primary": attempt(),
        "replacement": attempt("not_rated"),
        "experience": {"difficulty": 2, "fatigue": 2, "boredom": 1, "perceived_value": 5},
        "issue_codes": ["none"],
    }


def complete_record(evidence_mode="synthetic_fixture"):
    visits = []
    for number, lesson_ids in VISIT_PLAN.items():
        visits.append({
            "visit_number": number,
            "day_number": number * 2 - 1,
            "consent_reaffirmed": True,
            "completion": "completed",
            "duration_seconds": 1800,
            "lesson_records": [lesson(lesson_id) for lesson_id in lesson_ids],
            "unit1_stations": ([
                {"station_id": station_id, "decision": "demonstrated"}
                for station_id in sorted(STATION_IDS)
            ] if number == 6 else []),
            "delayed_probes": ([{
                "probe_id": "P10-PROBE-06",
                "source_lesson_id": "U1-L05",
                "days_since_lesson": 6,
                "decision": "demonstrated",
            }] if number == 6 else []),
        })
    return {
        "schema_version": 1,
        "study_id": "a1_first_10_progression_pilot_v1",
        "participant_code": "P10-A7K2",
        "evidence_mode": evidence_mode,
        "eligibility": {
            "adult": True,
            "arabic_dominant": True,
            "beginner_boundary": True,
            "no_answer_material_exposure": True,
            "not_owner_or_author": True,
        },
        "initial_consent": {
            "voluntary": True,
            "data_boundary_understood": True,
            "withdrawal_route_understood": True,
            "agreed": True,
        },
        "media": {
            "release_id": "a1_first_10_lessons_pilot_v1",
            "render_batch_id": "P10-MEDIA-V01",
            "all_transcript_matched": True,
            "all_listened": True,
        },
        "visits": visits,
        "withdrawal": {"status": "completed", "after_visit": 6, "reason_code": None},
        "privacy": {
            "contains_direct_identifier": False,
            "contains_raw_answer": False,
            "contains_audio": False,
            "contains_video": False,
            "stored_outside_repository": True,
        },
    }


class FirstTenPilotContractTests(unittest.TestCase):
    def test_repository_instrument_is_ready(self):
        self.assertEqual([], validate())

    def test_complete_synthetic_fixture_passes_but_has_no_gate_effect(self):
        record = complete_record()
        self.assertEqual("synthetic_fixture", record["evidence_mode"])
        self.assertEqual([], validate_record(record, require_complete=True))

    def test_real_record_rejects_unreviewed_media(self):
        record = complete_record("real_observation")
        record["media"]["all_listened"] = False
        self.assertIn("real observation uses unapproved or unreviewed media",
                      validate_record(record, require_complete=True))

    def test_demonstrated_rejects_visible_answer_model(self):
        record = complete_record()
        record["visits"][0]["lesson_records"][0]["primary"]["answer_model_visible"] = True
        errors = validate_record(record, require_complete=True)
        self.assertTrue(any("requires four independent level-2 ratings" in error for error in errors))

    def test_completed_visit_rejects_wrong_lesson_order(self):
        record = complete_record()
        record["visits"][0]["lesson_records"].reverse()
        errors = validate_record(record, require_complete=True)
        self.assertIn("visit 1: completed lesson set differs from protocol", errors)

    def test_schema_rejects_added_identifier(self):
        record = copy.deepcopy(complete_record())
        record["participant_name"] = "prohibited"
        self.assertTrue(any("Additional properties" in error for error in validate_record(record)))

    def test_private_directory_validator_does_not_need_repository_storage(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "P10-A7K2.json"
            path.write_text(json.dumps(complete_record()), encoding="utf-8")
            self.assertEqual([], validate_directory(Path(directory), "synthetic_fixture", True))


if __name__ == "__main__":
    unittest.main()
