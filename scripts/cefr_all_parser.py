"""Extract every CEFR illustrative descriptor table from Pre-A1 through C2."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import fitz

try:
    from scripts.cefr_a1_parser import _clean, _page_lines
    from scripts.cefr_all_scale_map import metadata_for
except ModuleNotFoundError:
    from cefr_a1_parser import _clean, _page_lines
    from cefr_all_scale_map import metadata_for


LEVEL_TO_CODE = {
    "Pre-A1": "pre_a1",
    "A1": "a1",
    "A2": "a2",
    "A2+": "a2",
    "B1": "b1",
    "B1+": "b1",
    "B2": "b2",
    "B2+": "b2",
    "C1": "c1",
    "C2": "c2",
}
TABLE_PAGES = range(48, 143)


@dataclass(frozen=True)
class Descriptor:
    page: int
    level_text: str
    cefr_code: str
    mode: str
    skill: str
    scale: str
    ordinal_in_level_scale: int
    text: str
    transcription_notes: tuple[str, ...]


@dataclass(frozen=True)
class _Draft:
    page: int
    level_text: str
    mode: str
    skill: str
    scale: str
    text: str
    notes: tuple[str, ...]


def _cell_groups(page: fitz.Page, rect: tuple[float, ...], vertical: bool):
    axis = 0 if vertical else 1
    selected = []
    for line in _page_lines(page):
        direction_matches = line["dir"][1] < -0.9 if vertical else line["dir"][0] > 0.9
        x = (line["bbox"][0] + line["bbox"][2]) / 2
        y = (line["bbox"][1] + line["bbox"][3]) / 2
        if direction_matches and rect[0] <= x <= rect[2] and rect[1] <= y <= rect[3]:
            selected.append(line)
    raw_groups = []
    for block in sorted({line["block"] for line in selected}):
        lines = sorted(
            (line for line in selected if line["block"] == block),
            key=lambda line: line["bbox"][axis],
        )
        current = []
        previous = None
        for line in lines:
            position = line["bbox"][axis]
            if current and previous is not None and position - previous > 11.8:
                raw_groups.append(_clean(current))
                current = []
            current.append(line["text"])
            previous = position
        if current:
            raw_groups.append(_clean(current))
    groups = []
    for text, notes in raw_groups:
        if text and not text.startswith("No descriptors available"):
            if text.startswith(("- ", "– ", "• ")) and groups:
                prior_text, prior_notes = groups[-1]
                merged_notes = prior_notes + notes + ("Joined a bullet continuation in the same source cell.",)
                groups[-1] = (f"{prior_text} {text}", merged_notes)
            else:
                groups.append((text, notes))
    return groups


def _clean_cell(value: str | None) -> str:
    return " ".join((value or "").split())


def _horizontal(page: fitz.Page, table) -> list[_Draft]:
    matrix = table.extract()
    scale = _clean_cell(matrix[0][1])
    meta = metadata_for(scale, page.number + 1)
    drafts = []
    level = None
    for row_index in range(1, len(matrix)):
        label = _clean_cell(matrix[row_index][0])
        if label in LEVEL_TO_CODE:
            level = label
        if level is None:
            continue
        rect = table.rows[row_index].cells[1]
        if rect is None:
            continue
        for text, notes in _cell_groups(page, rect, False):
            drafts.append(
                _Draft(page.number + 1, level, meta.mode, meta.skill, scale, text, notes)
            )
    return drafts


def _rotated(page: fitz.Page, table) -> list[_Draft]:
    matrix = table.extract()
    labels = []
    level = None
    for value in matrix[-1][2:]:
        label = _clean_cell(value)
        if label in LEVEL_TO_CODE:
            level = label
        labels.append(level)
    drafts = []
    for row_index in range(len(matrix) - 1):
        scale = _clean_cell(matrix[row_index][1])
        if not scale:
            continue
        meta = metadata_for(scale, page.number + 1)
        for column, level in enumerate(labels, 2):
            if level is None or column >= len(table.rows[row_index].cells):
                continue
            rect = table.rows[row_index].cells[column]
            if rect is None:
                continue
            for text, notes in _cell_groups(page, rect, True):
                drafts.append(
                    _Draft(page.number + 1, level, meta.mode, meta.skill, scale, text, notes)
                )
    return drafts


def _has_levels(matrix: list[list[str | None]]) -> bool:
    return any(_clean_cell(cell) in LEVEL_TO_CODE for row in matrix for cell in row)


def extract_descriptors(pdf_path: Path) -> list[Descriptor]:
    document = fitz.open(pdf_path)
    drafts = []
    for page_number in TABLE_PAGES:
        page = document[page_number - 1]
        for table in page.find_tables().tables:
            matrix = table.extract()
            if not _has_levels(matrix):
                continue
            if table.col_count == 2:
                drafts.extend(_horizontal(page, table))
            else:
                drafts.extend(_rotated(page, table))
    ordinals: dict[tuple[str, str, str], int] = defaultdict(int)
    descriptors = []
    for item in drafts:
        key = (item.mode, item.scale, item.level_text)
        ordinals[key] += 1
        descriptors.append(
            Descriptor(
                item.page,
                item.level_text,
                LEVEL_TO_CODE[item.level_text],
                item.mode,
                item.skill,
                item.scale,
                ordinals[key],
                item.text,
                item.notes,
            )
        )
    return descriptors
