"""Helpers for modular, exact A1 pronunciation target catalogs."""


PREFIX = "lesson_candidate."


def owner(value: str) -> str:
    return value if value.startswith("support.") else PREFIX + value


def target(
    target_id: str,
    strand_id: str,
    title: str,
    control_status: str,
    feature_or_contrast: str,
    examples: tuple[tuple[str, str], ...],
    meaning_risk: str,
    introduction: str,
    recycle: tuple[str, ...],
    mastery_evidence: str,
    risk_ids: tuple[str, ...],
    not_yet: str,
) -> dict:
    return {
        "target_id": f"a1_pronunciation.{target_id}", "strand_id": f"pronunciation.{strand_id}",
        "title": title, "control_status": control_status,
        "feature_or_contrast": feature_or_contrast,
        "course_examples": [{"text": text, "reference_ipa": ipa} for text, ipa in examples],
        "meaning_risk": meaning_risk, "introduction_location": owner(introduction),
        "recycle_locations": [owner(value) for value in recycle],
        "mastery_evidence": mastery_evidence,
        "arabic_risk_hypothesis_ids": list(risk_ids), "not_yet": not_yet,
        "teaching_reference": "General American broad IPA for modelling only",
        "assessment_tolerance": "Accept any stable intelligible variety; require repair only when the target distinction or key detail is lost.",
    }
