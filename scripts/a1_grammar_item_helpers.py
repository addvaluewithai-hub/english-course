"""Small helpers shared by the modular A1 grammar item catalogs."""


PREFIX = "lesson_candidate."


def owner(value: str) -> str:
    return value if value.startswith("support.") else PREFIX + value


def item(
    item_id: str,
    title: str,
    control_status: str,
    exact_forms: tuple[str, ...],
    meaning_use: str,
    introduction_owners: tuple[str, ...],
    recycle_owners: tuple[str, ...],
    mastery_evidence: str,
    not_yet: str,
) -> dict:
    return {
        "item_id": f"grammar.{item_id}",
        "title": title,
        "control_status": control_status,
        "exact_forms": list(exact_forms),
        "meaning_use": meaning_use,
        "introduction_owner_ids": [owner(value) for value in introduction_owners],
        "recycle_owner_ids": [owner(value) for value in recycle_owners],
        "mastery_evidence": mastery_evidence,
        "not_yet": not_yet,
        "decision_status": "accepted_for_a1_reconciliation",
    }
