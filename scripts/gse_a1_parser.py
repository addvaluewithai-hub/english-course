"""Parse the A1 objective tables from the registered Pearson GSE PDF."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


A1_PAGES = {
    "Reading": (9,),
    "Listening": (14, 15),
    "Speaking": (22, 23, 24),
    "Writing": (37,),
}
SOURCE_CODES = {"P", "C", "Ca", "CJa", "CSEa", "N2000a", "Wa"}
SCORE_LINE = re.compile(r"^(?:(2[2-9])\s+)?(Can .+)$")


@dataclass(frozen=True)
class Objective:
    skill: str
    score: str
    page: int
    ordinal_on_page: int
    text: str
    source_code: str
    transcription_notes: tuple[str, ...]


def _clean_text(fragments: list[str]) -> tuple[str, tuple[str, ...]]:
    joined = " ".join(fragment.strip() for fragment in fragments)
    notes: list[str] = []
    if len(fragments) > 1:
        notes.append("Joined source line wraps with single spaces.")
    cleaned = re.sub(r"’\s+([,.!?;:])", r"’\1", joined)
    if cleaned != joined:
        notes.append(
            "Removed extraction-only spaces before punctuation after closing quotation marks."
        )
    return cleaned, tuple(notes)


def _is_header(line: str, page: int, skill: str) -> bool:
    return line in {str(page), skill, "GSE Learning Objectives"} or line.startswith(
        "GSE Learning Objectives for Adult Learners"
    )


def _parse_skill(reader: PdfReader, skill: str, pages: tuple[int, ...]) -> list[Objective]:
    start_heading = f"GSE 22–29/A1: {skill}"
    end_heading = f"GSE 30–35/A2: {skill}"
    objectives: list[Objective] = []
    score: str | None = None
    active = False
    fragments: list[str] = []
    page_for_objective = 0
    ordinals: dict[int, int] = {}

    def finish() -> None:
        nonlocal fragments
        if not fragments:
            return
        text, notes = _clean_text(fragments)
        code_match = re.search(r"\(([^()]*)\)$", text)
        if score is None or code_match is None or code_match.group(1) not in SOURCE_CODES:
            raise ValueError(f"Malformed {skill} objective on page {page_for_objective}: {text}")
        ordinals[page_for_objective] = ordinals.get(page_for_objective, 0) + 1
        objectives.append(
            Objective(
                skill=skill,
                score=score,
                page=page_for_objective,
                ordinal_on_page=ordinals[page_for_objective],
                text=text,
                source_code=code_match.group(1),
                transcription_notes=notes,
            )
        )
        fragments = []

    for page in pages:
        lines = (reader.pages[page - 1].extract_text() or "").splitlines()
        if page != pages[0]:
            active = True
        for raw_line in lines:
            line = raw_line.strip()
            if line == start_heading:
                active = True
                continue
            if line == end_heading:
                finish()
                active = False
                break
            if not active or not line or _is_header(line, page, skill):
                continue
            match = SCORE_LINE.match(line)
            if match:
                finish()
                score = match.group(1) or score
                if score is None:
                    raise ValueError(f"Missing GSE score on page {page}: {line}")
                page_for_objective = page
                fragments = [match.group(2)]
            elif fragments:
                fragments.append(line)
        if active:
            finish()
    return objectives


def extract_objectives(pdf_path: Path) -> list[Objective]:
    reader = PdfReader(pdf_path)
    objectives = [
        objective
        for skill, pages in A1_PAGES.items()
        for objective in _parse_skill(reader, skill, pages)
    ]
    if any(not 22 <= int(item.score) <= 29 for item in objectives):
        raise ValueError("Extraction escaped the A1 GSE 22–29 band")
    return objectives
