"""Resolve CEFR table scale titles to curriculum modes and skills."""

from __future__ import annotations

from dataclasses import dataclass

try:
    from scripts.cefr_a1_specs import TABLE_SPECS
except ModuleNotFoundError:
    from cefr_a1_specs import TABLE_SPECS


@dataclass(frozen=True)
class ScaleMeta:
    page: int
    mode: str
    skill: str


_ALIASES = {
    "Goal-oriented co-operation (cooking together, discussing a document, organising an event, etc.)":
        "Goal-oriented co-operation",
}

_EXTRA = {
    "Building on pluricultural repertoire": ScaleMeta(
        125, "Plurilingual and pluricultural competence", "Pluricultural competence"
    ),
    "Plurilingual comprehension": ScaleMeta(
        127, "Plurilingual and pluricultural competence", "Plurilingual competence"
    ),
    "Building on plurilingual repertoire": ScaleMeta(
        128, "Plurilingual and pluricultural competence", "Plurilingual competence"
    ),
}


def _spec_index() -> dict[str, list[ScaleMeta]]:
    index: dict[str, list[ScaleMeta]] = {}
    for spec in TABLE_SPECS:
        for scale in spec.scales:
            index.setdefault(scale, []).append(ScaleMeta(spec.page, spec.mode, spec.skill))
    for scale, meta in _EXTRA.items():
        index.setdefault(scale, []).append(meta)
    return index


SCALE_INDEX = _spec_index()


def metadata_for(scale: str, page: int) -> ScaleMeta:
    lookup = _ALIASES.get(scale, scale)
    options = SCALE_INDEX.get(lookup)
    if not options:
        raise ValueError(f"Unregistered CEFR scale on page {page}: {scale}")
    return min(options, key=lambda item: abs(item.page - page))
