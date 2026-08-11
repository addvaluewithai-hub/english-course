from jsonschema import Draft202012Validator

from scripts.first_ten_pilot_contract import SCHEMA, STATION_IDS, VISIT_PLAN, load_json


def _attempt_errors(attempt: dict, path: str) -> list[str]:
    errors = []
    ratings = list(attempt["ratings"].values())
    if attempt["attempted"] and any(value is None for value in ratings):
        errors.append(f"{path}: attempted performance lacks four ratings")
    if not attempt["attempted"]:
        if attempt["decision"] != "not_rated" or any(value is not None for value in ratings):
            errors.append(f"{path}: unattempted performance must remain unrated")
    if attempt["decision"] == "demonstrated":
        if attempt["answer_model_visible"] or any(value != 2 for value in ratings):
            errors.append(f"{path}: demonstrated requires four independent level-2 ratings")
    secondary = attempt["secondary_decision"]
    if secondary is None and attempt["exact_agreement"] is not None:
        errors.append(f"{path}: agreement exists without a secondary decision")
    if secondary is not None and attempt["exact_agreement"] != (secondary == attempt["decision"]):
        errors.append(f"{path}: evaluator agreement is inconsistent")
    return errors


def _visit_errors(record: dict, require_complete: bool) -> list[str]:
    errors = []
    visits = record["visits"]
    numbers = [row["visit_number"] for row in visits]
    if numbers != sorted(set(numbers)):
        errors.append("visits must be unique and sorted")
    days = [row["day_number"] for row in visits]
    if days != sorted(days):
        errors.append("visit day numbers regress")
    for visit in visits:
        number = visit["visit_number"]
        if not visit["consent_reaffirmed"]:
            errors.append(f"visit {number}: consent was not reaffirmed")
        actual = [row["lesson_id"] for row in visit["lesson_records"]]
        if visit["completion"] == "completed" and actual != VISIT_PLAN[number]:
            errors.append(f"visit {number}: completed lesson set differs from protocol")
        if sum(row["duration_seconds"] for row in visit["lesson_records"]) > visit["duration_seconds"]:
            errors.append(f"visit {number}: lesson time exceeds visit time")
        for lesson in visit["lesson_records"]:
            prefix = f"visit {number}/{lesson['lesson_id']}"
            errors += _attempt_errors(lesson["primary"], f"{prefix}/primary")
            errors += _attempt_errors(lesson["replacement"], f"{prefix}/replacement")
            if lesson["replacement"]["attempted"] and not lesson["primary"]["attempted"]:
                errors.append(f"{prefix}: replacement precedes primary attempt")
            issues = lesson["issue_codes"]
            if "none" in issues and len(issues) > 1:
                errors.append(f"{prefix}: none is combined with another issue")
        station_ids = {row["station_id"] for row in visit["unit1_stations"]}
        if number != 6 and station_ids:
            errors.append(f"visit {number}: Unit 1 stations occur before the final visit")
        if number == 6 and visit["completion"] == "completed" and station_ids != STATION_IDS:
            errors.append("visit 6: the three Unit 1 stations are incomplete")
    if require_complete:
        if numbers != list(VISIT_PLAN):
            errors.append("complete journey must contain all six visits")
        elif any(row["completion"] != "completed" for row in visits):
            errors.append("complete journey contains a non-completed visit")
        if not any(row["delayed_probes"] for row in visits[3:]):
            errors.append("complete journey lacks a delayed probe in visits 4-6")
    return errors


def validate_record(record: dict, require_complete: bool = False) -> list[str]:
    schema = load_json(SCHEMA)
    errors = [f"schema: {error.message}" for error in Draft202012Validator(schema).iter_errors(record)]
    if errors:
        return errors
    if record["evidence_mode"] == "real_observation":
        if not all(record["eligibility"].values()):
            errors.append("real observation is not fully eligible")
        if not all(record["initial_consent"].values()):
            errors.append("real observation lacks valid initial consent")
        if not record["media"]["all_transcript_matched"] or not record["media"]["all_listened"]:
            errors.append("real observation uses unapproved or unreviewed media")
    errors += _visit_errors(record, require_complete)
    withdrawal = record["withdrawal"]
    if withdrawal["status"] == "withdrew" and not withdrawal["reason_code"]:
        errors.append("withdrawal lacks a controlled reason")
    if withdrawal["status"] != "withdrew" and withdrawal["reason_code"] is not None:
        errors.append("withdrawal reason exists for a non-withdrawn journey")
    if require_complete and withdrawal["status"] != "completed":
        errors.append("complete journey is not marked completed")
    return errors
