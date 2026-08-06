"""Apply controlled tags without changing source evidence or clustering."""

from __future__ import annotations

import copy
from typing import Any

try:
    from scripts.tag_cefr import tag_cefr
    from scripts.tag_gse import tag_gse
except ModuleNotFoundError:
    from tag_cefr import tag_cefr
    from tag_gse import tag_gse


SOURCE_TAGGERS = {
    "pearson.gse_adult_general_english_2022": tag_gse,
    "coe.cefr_companion_2020_en": tag_cefr,
}


def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    """Return a tagged copy while leaving source facts and source text untouched."""
    normalized = copy.deepcopy(record)
    source_id = normalized["source"]["source_id"]
    try:
        decision = SOURCE_TAGGERS[source_id](normalized)
    except KeyError as exc:
        raise ValueError(f"Unsupported curriculum source: {source_id!r}") from exc
    interpretation = normalized["interpretation"]
    interpretation["skill_codes"] = list(decision.skills)
    interpretation["mode_codes"] = list(decision.modes)
    interpretation["function_codes"] = list(decision.functions)
    for ambiguity in decision.ambiguities:
        if ambiguity not in interpretation["ambiguities"]:
            interpretation["ambiguities"].append(ambiguity)
    return normalized


def normalize_collection(
    collection: dict[str, Any], *, reviewer: str | None = None, reviewed_at: str | None = None
) -> dict[str, Any]:
    if (reviewer is None) != (reviewed_at is None):
        raise ValueError("reviewer and reviewed_at are required together")
    normalized = copy.deepcopy(collection)
    normalized["records"] = [normalize_record(record) for record in collection["records"]]
    for record in normalized["records"]:
        if reviewer:
            record["review"].update(
                {"status": "accepted", "reviewer": reviewer, "reviewed_at": reviewed_at}
            )
    return normalized
