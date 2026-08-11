"""Aggregate de-identified pilot records without retaining learner notes."""

from collections import Counter
from statistics import mean, median

from scripts.learner_test_metric_rules import evaluate_metric


EXPERIENCE_KEYS = (
    "arabic_clarity", "difficulty", "boredom", "perceived_value",
    "video_helpfulness", "teachback_helpfulness", "teachback_fatigue",
)


def _experience(records: list[dict]) -> dict:
    result = {}
    for key in EXPERIENCE_KEYS:
        values = [row["experience"][key] for row in records if row["experience"][key] is not None]
        result[key] = {"responses": len(values), "mean": None if not values else round(mean(values), 2)}
    return result


def _issue_counts(records: list[dict]) -> dict:
    types = Counter(issue["type"] for row in records for issue in row["issues"])
    severities = Counter(issue["severity"] for row in records for issue in row["issues"])
    unresolved = Counter(issue["type"] for row in records for issue in row["issues"] if not issue["resolved"])
    return {"by_type": dict(sorted(types.items())), "by_severity": dict(sorted(severities.items())),
            "unresolved_by_type": dict(sorted(unresolved.items()))}


def _descriptive(records: list[dict]) -> dict:
    totals = [row["timing"]["total_seconds"] for row in records]
    by_condition = {}
    for condition in ("teachback", "omit"):
        rows = [row for row in records if row["condition"]["post_performance"] == condition]
        by_condition[condition] = {"sessions": len(rows), "experience": _experience(rows)}
    return {
        "total_seconds": {
            "median": None if not totals else median(totals),
            "minimum": None if not totals else min(totals),
            "maximum": None if not totals else max(totals),
        },
        "completion_outcomes": dict(sorted(Counter(
            row["completion"]["outcome"] for row in records).items()
        )),
        "drop_off_last_step": dict(sorted(Counter(
            str(row["completion"]["last_step"]) for row in records
            if row["completion"]["outcome"] != "completed"
        ).items())),
        "mastery_decisions": dict(sorted(Counter(
            row["mastery"]["decision"] for row in records).items()
        )),
        "experience_overall": _experience(records),
        "conditions": by_condition,
        "issues": _issue_counts(records),
    }


def _gate_decision(metrics: list[dict], eligible_completed: int, minimum_completed: int) -> str:
    stop_fail = any(row["status"] == "fail" and row["action_if_missed"] == "stop_and_redesign"
                    for row in metrics)
    if stop_fail:
        return "stop_and_redesign"
    if eligible_completed < minimum_completed or any(
            row["status"] == "insufficient_denominator" for row in metrics):
        return "insufficient_evidence"
    if any(row["status"] == "fail" for row in metrics):
        return "revise_and_retest"
    return "go_to_system_revision"


def analyze(records: list[dict], thresholds: dict, evidence_mode: str) -> dict:
    if evidence_mode not in {"synthetic_fixtures", "real_consented_sessions"}:
        raise ValueError("unknown learner-test evidence mode")
    ids = [row["session_id"] for row in records]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate session_id in learner-test records")
    eligible = [row for row in records if row["participant"]["eligible_primary_sample"]]
    eligible_completed = sum(row["completion"]["outcome"] == "completed" for row in eligible)
    metrics = [evaluate_metric(rule, records) for rule in thresholds["gating_metrics"]]
    hypothetical = _gate_decision(
        metrics, eligible_completed, thresholds["sample"]["minimum_eligible_completed_sessions"]
    )
    gate_effect = hypothetical if evidence_mode == "real_consented_sessions" else "simulation_only_no_gate_effect"
    return {
        "schema_version": 1, "study_id": thresholds["study_id"], "evidence_mode": evidence_mode,
        "gate_effect": gate_effect, "hypothetical_decision": hypothetical,
        "sample": {
            "records": len(records), "eligible_records": len(eligible),
            "eligible_completed_sessions": eligible_completed,
            "target_completed_sessions": thresholds["sample"]["target_completed_sessions"],
            "minimum_eligible_completed_sessions": thresholds["sample"]["minimum_eligible_completed_sessions"],
            "double_rated_sessions": sum(row["reliability"]["double_rated"] for row in eligible),
        },
        "gating_metrics": metrics, "descriptive": _descriptive(records),
        "privacy": {
            "raw_answers_included": False, "direct_identifiers_included": False,
            "individual_issue_notes_included": False,
        },
    }
