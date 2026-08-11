"""Compute the nine pre-registered learner-test gate metrics."""

SEVERITY = {"info": 0, "minor": 1, "major": 2, "severe": 3}


def _eligible(records: list[dict]) -> list[dict]:
    return [row for row in records if row["participant"]["eligible_primary_sample"]]


def _has_issue(record: dict, types: set[str], minimum: str, unresolved: bool = False) -> bool:
    return any(
        issue["type"] in types
        and SEVERITY[issue["severity"]] >= SEVERITY[minimum]
        and (not unresolved or not issue["resolved"])
        for issue in record["issues"]
    )


def _ratio(numerator: int, denominator: int) -> float | None:
    return None if denominator == 0 else round(numerator / denominator, 4)


def metric_counts(metric_id: str, records: list[dict]) -> tuple[int, int, float | int | None]:
    eligible = _eligible(records)
    if metric_id == "informed_consent_compliance":
        numerator = sum(all((row["consent"]["voluntary_confirmed"],
                             row["consent"]["data_boundary_confirmed"],
                             row["consent"]["participation_agreed"])) for row in eligible)
        return numerator, len(eligible), _ratio(numerator, len(eligible))
    if metric_id == "privacy_or_safety_incidents":
        numerator = sum(
            _has_issue(row, {"privacy"}, "major")
            or _has_issue(row, {"safety"}, "major", unresolved=True)
            for row in eligible
        )
        return numerator, len(eligible), numerator
    if metric_id == "severe_accessibility_blockers":
        numerator = sum(_has_issue(row, {"accessibility"}, "severe", unresolved=True) for row in eligible)
        return numerator, len(eligible), numerator
    if metric_id == "completed_fresh_attempt_without_full_model":
        numerator = sum(row["completion"]["fresh_task_attempted"] and
                        not row["mastery"]["full_model_visible"] for row in eligible)
        return numerator, len(eligible), _ratio(numerator, len(eligible))
    if metric_id == "demonstrated_full_outcome":
        attempts = [row for row in eligible if row["completion"]["fresh_task_attempted"]
                    and row["mastery"]["evidence_valid"]]
        numerator = sum(row["mastery"]["decision"] == "demonstrated" for row in attempts)
        return numerator, len(attempts), _ratio(numerator, len(attempts))
    if metric_id == "major_instruction_confusion":
        numerator = sum(_has_issue(row, {"instruction_confusion"}, "major") for row in eligible)
        return numerator, len(eligible), _ratio(numerator, len(eligible))
    if metric_id == "severe_arabic_or_level_clarity_issues":
        numerator = sum(_has_issue(row, {"arabic_clarity", "level_fit"}, "severe", unresolved=True)
                        for row in eligible)
        return numerator, len(eligible), numerator
    if metric_id == "important_correction_retry_success":
        denominator = sum(row["correction"]["important_corrections"] for row in eligible)
        numerator = sum(row["correction"]["successful_immediate_retries"] for row in eligible)
        return numerator, denominator, _ratio(numerator, denominator)
    if metric_id == "mastery_decision_agreement":
        double = [row for row in eligible if row["reliability"]["double_rated"]]
        numerator = sum(row["reliability"]["exact_decision_agreement"] for row in double)
        return numerator, len(double), _ratio(numerator, len(double))
    raise KeyError(metric_id)


def _passes(value: float | int, operator: str, threshold: float | int) -> bool:
    if operator == ">=":
        return value >= threshold
    if operator == "<=":
        return value <= threshold
    return value == threshold


def evaluate_metric(rule: dict, records: list[dict]) -> dict:
    numerator, denominator, value = metric_counts(rule["metric_id"], records)
    passes = value is not None and _passes(value, rule["operator"], rule["threshold"])
    if not passes and rule["action_if_missed"] == "stop_and_redesign":
        status = "fail"
    elif denominator < rule["minimum_denominator"]:
        status = "insufficient_denominator"
    else:
        status = "pass" if passes else "fail"
    return {
        "metric_id": rule["metric_id"], "numerator": numerator,
        "denominator": denominator, "value": value, "operator": rule["operator"],
        "threshold": rule["threshold"], "minimum_denominator": rule["minimum_denominator"],
        "status": status, "action_if_missed": rule["action_if_missed"],
    }
