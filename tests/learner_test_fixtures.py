"""Synthetic TEST-002 records; never usable as learner evidence."""

import copy
import json

from scripts.learner_test_v1_contract import TEMPLATE


def synthetic_record(index: int, demonstrated: bool | None = None) -> dict:
    record = copy.deepcopy(json.loads(TEMPLATE.read_text(encoding="utf-8")))
    record["session_id"] = f"LT1-{index:03d}"
    record["condition"]["post_performance"] = "teachback" if index % 2 else "omit"
    record["participant"].update({
        "adult_confirmed": True, "arabic_speaking": True,
        "entry_band": "a1", "eligible_primary_sample": True,
    })
    record["consent"].update({
        "voluntary_confirmed": True, "data_boundary_confirmed": True,
        "participation_agreed": True,
    })
    record["completion"].update({
        "outcome": "completed", "last_step": 9, "fresh_task_attempted": True,
    })
    passed = index <= 6 if demonstrated is None else demonstrated
    score = 2 if passed else 1
    record["mastery"].update({
        "evidence_valid": True, "full_model_visible": False,
        "ratings": {
            "comprehension": score, "outcome_performance": score,
            "context_transfer": score, "control_or_repair": score,
        },
        "decision": "demonstrated" if passed else "practiced",
    })
    record["correction"] = {
        "important_corrections": int(index <= 3),
        "successful_immediate_retries": int(index <= 3),
    }
    if index <= 2:
        record["reliability"] = {
            "double_rated": True,
            "secondary_ratings": dict(record["mastery"]["ratings"]),
            "secondary_decision": record["mastery"]["decision"],
            "exact_decision_agreement": True,
        }
    record["timing"] = {
        "total_seconds": 1800 + index * 30,
        "section_seconds": [{"step": step, "seconds": 180 + step} for step in range(1, 10)],
    }
    record["experience"] = {
        "arabic_clarity": 4, "difficulty": 3, "boredom": 2,
        "perceived_value": 4, "video_helpfulness": 4,
        "teachback_helpfulness": 4 if index % 2 else None,
        "teachback_fatigue": 2 if index % 2 else None,
    }
    record["data_controls"]["withdrawal_route_given"] = True
    return record
