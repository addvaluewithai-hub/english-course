"""Parse every scored objective table in the Pearson GSE Adult PDF."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

try:
    from scripts.gse_level_bands import BAND_BY_RANGE, GseBand, OBJECTIVE_PAGES, SKILLS
except ModuleNotFoundError:
    from gse_level_bands import BAND_BY_RANGE, GseBand, OBJECTIVE_PAGES, SKILLS


HEADING = re.compile(
    r"^GSE (\d{2})–(\d{2})/(Below A1|A1|A2|A2\(\+\)|B1|B1\(\+\)|"
    r"B2|B2\(\+\)|C1|C2): (Reading|Listening|Speaking|Writing)$"
)
OBJECTIVE_START = re.compile(r"^(?:(\d{2})\s+)?(Can .+)$")
SOURCE_CODE = re.compile(r"\(([A-Za-z][A-Za-z0-9]*)\)$")
EXPECTED_SOURCE_CODES = {
    "P", "C", "Ca", "CJa", "CSEa", "N2000", "N2000a", "N2007a", "Wa"
}


@dataclass(frozen=True)
class Objective:
    skill: str
    band: GseBand
    score: int
    page: int
    ordinal_in_section_on_page: int
    text: str
    source_code: str
    transcription_notes: tuple[str, ...]

    @property
    def scale_text(self) -> str:
        return (
            f"GSE {self.band.minimum}–{self.band.maximum}/"
            f"{self.band.source_level}: {self.skill}"
        )


def _clean_text(fragments: list[str]) -> tuple[str, tuple[str, ...]]:
    joined = " ".join(fragment.strip() for fragment in fragments)
    notes: list[str] = []
    if len(fragments) > 1:
        notes.append("Joined source line wraps with single spaces.")
    cleaned = re.sub(r"’\s+([,.!?;:])", r"’\1", joined)
    if cleaned != joined:
        notes.append("Removed extraction-only spaces before punctuation after quotes.")
    return cleaned, tuple(notes)


def _is_page_furniture(line: str, page: int) -> bool:
    return (
        line in {str(page), "GSE Learning Objectives", *SKILLS}
        or line.startswith("GSE Learning Objectives for Adult Learners")
    )


def extract_objectives(pdf_path: Path) -> list[Objective]:
    reader = PdfReader(pdf_path)
    objectives: list[Objective] = []
    band: GseBand | None = None
    skill: str | None = None
    score: int | None = None
    fragments: list[str] = []
    start_page = 0
    ordinals: dict[tuple[int, str, str], int] = {}

    def finish() -> None:
        nonlocal fragments
        if not fragments:
            return
        if band is None or skill is None or score is None:
            raise ValueError(f"Objective lacks section metadata on page {start_page}")
        text, notes = _clean_text(fragments)
        code_match = SOURCE_CODE.search(text)
        if code_match is None or code_match.group(1) not in EXPECTED_SOURCE_CODES:
            raise ValueError(f"Malformed {skill} objective on page {start_page}: {text}")
        key = (start_page, band.key, skill)
        ordinals[key] = ordinals.get(key, 0) + 1
        objectives.append(
            Objective(
                skill=skill,
                band=band,
                score=score,
                page=start_page,
                ordinal_in_section_on_page=ordinals[key],
                text=text,
                source_code=code_match.group(1),
                transcription_notes=notes,
            )
        )
        fragments = []

    for page in OBJECTIVE_PAGES:
        lines = (reader.pages[page - 1].extract_text() or "").splitlines()
        for raw_line in lines:
            line = raw_line.strip()
            heading = HEADING.match(line)
            if heading:
                finish()
                minimum, maximum = int(heading.group(1)), int(heading.group(2))
                band = BAND_BY_RANGE[(minimum, maximum)]
                if heading.group(3) != band.source_level:
                    raise ValueError(f"Unexpected level label on page {page}: {line}")
                skill = heading.group(4)
                score = None
                continue
            if not line or _is_page_furniture(line, page) or band is None:
                continue
            match = OBJECTIVE_START.match(line)
            if match:
                finish()
                score = int(match.group(1)) if match.group(1) else score
                if score is None or not band.minimum <= score <= band.maximum:
                    raise ValueError(f"Invalid score for {band.key} on page {page}: {line}")
                start_page = page
                fragments = [match.group(2)]
            elif fragments:
                fragments.append(line)
        finish()

    return objectives
