"""Semantic rules that JSON Schema alone cannot express for pilot records."""


def semantic_errors(record: dict) -> list[str]:
    errors: list[str] = []
    participant, consent = record["participant"], record["consent"]
    completion, mastery = record["completion"], record["mastery"]
    if not participant["adult_confirmed"] or not participant["arabic_speaking"]:
        errors.append("session lacks the adult Arabic-speaking eligibility confirmations")
    if not all((consent["voluntary_confirmed"], consent["data_boundary_confirmed"],
                consent["participation_agreed"])):
        errors.append("session lacks complete informed consent")
    number = int(record["session_id"].split("-")[-1])
    expected = "teachback" if number % 2 else "omit"
    if record["condition"]["post_performance"] != expected:
        errors.append("post-performance condition violates odd/even allocation")
    supports = record["supports"]
    if "none" in supports and len(supports) != 1:
        errors.append("none cannot be combined with another support")
    if "construct_changed" in supports and mastery["evidence_valid"]:
        errors.append("construct-changing support cannot yield valid mastery evidence")
    if mastery["full_model_visible"] and mastery["evidence_valid"]:
        errors.append("an answer-bearing model invalidates mastery evidence")
    ratings = mastery["ratings"].values()
    if mastery["decision"] == "demonstrated":
        if not mastery["evidence_valid"] or mastery["full_model_visible"]:
            errors.append("demonstrated requires valid independent evidence")
        if not completion["fresh_task_attempted"] or any(value != 2 for value in ratings):
            errors.append("demonstrated requires a fresh attempt and level 2 on all dimensions")
    if completion["outcome"] == "safety_paused" and mastery["decision"] != "not_rated":
        errors.append("a safety-paused session cannot receive a mastery judgment")
    if completion["outcome"] == "completed" and completion["last_step"] != 9:
        errors.append("completed session must reach step 9")
    correction = record["correction"]
    if correction["successful_immediate_retries"] > correction["important_corrections"]:
        errors.append("successful retries exceed important corrections")
    controls = record["data_controls"]
    if controls["contains_raw_answer"] or controls["contains_direct_identifier"]:
        errors.append("record contains prohibited raw or identifying data")
    if not controls["withdrawal_route_given"]:
        errors.append("participant did not receive the withdrawal route")
    if any(not issue["note"].strip() for issue in record["issues"]):
        errors.append("an issue has an empty de-identified note")
    return errors
