"""Parse the rotated grammar inventory tables in the Pearson GSE guide."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import fitz


TABLE_PAGES = range(7, 39)
LEVEL_HEADING = re.compile(r"^(A1|A2|A2\+|B1|B1\+|B2|B2\+|C1) \((\d{2})-(\d{2})\)$")
LEVEL_TO_CODE = {
    "A1": "a1", "A2": "a2", "A2+": "a2", "B1": "b1",
    "B1+": "b1", "B2": "b2", "B2+": "b2", "C1": "c1",
}
EXPECTED_RANGES = {
    "A1": (22, 29), "A2": (30, 35), "A2+": (36, 42), "B1": (43, 50),
    "B1+": (51, 58), "B2": (59, 66), "B2+": (67, 75), "C1": (76, 84),
}
COLUMNS = {
    "objective": (615, 790),
    "structure": (448, 615),
    "example": (283, 448),
    "categories": (114, 283),
}


@dataclass(frozen=True)
class GrammarEntry:
    page: int
    ordinal_on_page: int
    level_text: str
    printed_level_heading: str
    cefr_code: str
    score: int
    objective: str
    structure: str
    example: str
    categories: str
    transcription_notes: tuple[str, ...]


def _lines(page: fitz.Page) -> list[dict]:
    output = []
    for block_index, block in enumerate(page.get_text("dict")["blocks"]):
        for line in block.get("lines", []):
            text = "".join(span["text"] for span in line["spans"]).strip()
            if text:
                output.append({"block": block_index, "text": text, **line})
    return output


def _cell(lines: list[dict], low_x: float, high_x: float, low_y: float, high_y: float) -> str:
    selected = []
    for line in lines:
        x = (line["bbox"][0] + line["bbox"][2]) / 2
        y = (line["bbox"][1] + line["bbox"][3]) / 2
        if line["dir"][1] < -0.9 and low_x <= x < high_x and low_y <= y < high_y:
            selected.append(line)
    selected.sort(key=lambda line: (line["bbox"][0], -line["bbox"][1], line["block"]))
    return re.sub(r"\s+", " ", " ".join(line["text"] for line in selected)).strip()


def extract_entries(pdf_path: Path) -> list[GrammarEntry]:
    document = fitz.open(pdf_path)
    entries = []
    active_level = None
    active_heading = None
    for page_number in TABLE_PAGES:
        lines = _lines(document[page_number - 1])
        page_headings = [line for line in lines if LEVEL_HEADING.match(line["text"])]
        if page_headings:
            if len(page_headings) != 1:
                raise ValueError(f"Multiple grammar level headings on page {page_number}")
            new_heading = page_headings[0]["text"]
            new_level = LEVEL_HEADING.match(new_heading).group(1)
            heading_x = (page_headings[0]["bbox"][0] + page_headings[0]["bbox"][2]) / 2
        else:
            new_heading = new_level = heading_x = None
        if active_level is None and new_level is None:
            raise ValueError(f"Missing grammar level context on page {page_number}")
        anchors = []
        for line in lines:
            if line["dir"][1] >= -0.9 or not re.fullmatch(r"\d{2}", line["text"]):
                continue
            y = (line["bbox"][1] + line["bbox"][3]) / 2
            if y < 120:
                anchors.append(((line["bbox"][0] + line["bbox"][2]) / 2, int(line["text"])))
        anchors.sort()
        for index, (center, score) in enumerate(anchors):
            uses_new_heading = heading_x is not None and center > heading_x
            level = new_level if uses_new_heading else active_level
            heading = new_heading if uses_new_heading else active_heading
            if level is None or heading is None:
                raise ValueError(f"Grammar row precedes its first level heading on page {page_number}")
            following = anchors[index + 1][0] if index + 1 < len(anchors) else center + 40
            high_x = following - 1
            if not uses_new_heading and heading_x is not None and heading_x > center:
                high_x = min(high_x, heading_x - 1)
            low_x = center - 1
            fields = {
                name: _cell(lines, low_x, high_x, low_y, high_y)
                for name, (low_y, high_y) in COLUMNS.items()
            }
            if not fields["objective"].startswith("Can "):
                raise ValueError(f"Malformed grammar objective on page {page_number}: {fields}")
            minimum, maximum = EXPECTED_RANGES[level]
            if not minimum <= score <= maximum:
                raise ValueError(f"GSE {score} conflicts with {level} on page {page_number}")
            notes = ["Joined visual line wraps within each rotated table cell."]
            printed = LEVEL_HEADING.match(heading)
            if (int(printed.group(2)), int(printed.group(3))) != (minimum, maximum):
                notes.append("Printed level-heading range conflicts with its row scores; both are preserved.")
            entries.append(
                GrammarEntry(
                    page_number, index + 1, level, heading, LEVEL_TO_CODE[level], score,
                    fields["objective"], fields["structure"], fields["example"],
                    fields["categories"], tuple(notes),
                )
            )
        if new_level is not None:
            active_level, active_heading = new_level, new_heading
    return entries
