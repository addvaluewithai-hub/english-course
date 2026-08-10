"""Pearson GSE band metadata used by all-level objective extraction."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GseBand:
    key: str
    minimum: int
    maximum: int
    source_level: str
    cefr_code: str


BANDS = (
    GseBand("below_a1", 10, 21, "Below A1", "pre_a1"),
    GseBand("a1", 22, 29, "A1", "a1"),
    GseBand("a2", 30, 35, "A2", "a2"),
    GseBand("a2_plus", 36, 42, "A2(+)", "a2"),
    GseBand("b1", 43, 50, "B1", "b1"),
    GseBand("b1_plus", 51, 58, "B1(+)", "b1"),
    GseBand("b2", 59, 66, "B2", "b2"),
    GseBand("b2_plus", 67, 75, "B2(+)", "b2"),
    GseBand("c1", 76, 84, "C1", "c1"),
    GseBand("c2", 85, 90, "C2", "c2"),
)

BAND_BY_RANGE = {(band.minimum, band.maximum): band for band in BANDS}
BAND_BY_KEY = {band.key: band for band in BANDS}
SKILLS = ("Reading", "Listening", "Speaking", "Writing")
OBJECTIVE_PAGES = range(9, 45)
