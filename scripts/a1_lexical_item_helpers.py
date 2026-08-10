"""Helpers for readable, modular A1 lexical-item catalogs."""


PREFIX = "lesson_candidate."


def owner(value: str) -> str:
    return value if value.startswith("support.") else PREFIX + value


def lexical_item(
    item_id: str,
    canonical_form: str,
    members: tuple[str, ...],
    meaning_or_function: str,
    function_ids: tuple[str, ...],
    introduction: str,
    recycle: tuple[str, ...],
    source_headwords: tuple[str, ...],
    productive_expectation: str,
    frames: tuple[str, ...] = (),
    risks: tuple[str, ...] = (),
    item_type: str = "lexical_set",
    register: str = "neutral",
    first_exposure: str = "a1",
) -> dict:
    return {
        "lexical_item_id": f"lexical.{item_id}", "canonical_form": canonical_form,
        "item_type": item_type, "members": list(members),
        "meaning_or_function": meaning_or_function,
        "communicative_owner_ids": list(function_ids),
        "introduction_location": owner(introduction),
        "first_exposure_level": first_exposure, "first_guided_production_level": "a1",
        "consolidation_level": "a1", "recycle_locations": [owner(value) for value in recycle],
        "receptive_expectation": "Recognise the selected meaning or function in fresh supported A1 input.",
        "productive_expectation": productive_expectation, "register": register,
        "collocations_or_frames": list(frames), "arabic_learner_risks": list(risks),
        "decision_rationale": "Selected for an approved A1 outcome and planned for retrieval in a distinct later context.",
        "review": {"status": "accepted_for_a1_reconciliation"},
        "_source_headwords": list(source_headwords),
    }


def chunk_item(*args, **kwargs) -> dict:
    kwargs.setdefault("item_type", "chunk_set")
    kwargs.setdefault("register", "neutral_polite")
    return lexical_item(*args, **kwargs)
