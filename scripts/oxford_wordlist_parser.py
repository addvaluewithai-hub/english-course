"""Parse Oxford levelled word-list PDFs using their visual line geometry."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import fitz


LIST_LEVELS = {
    "oxford_3000": {"A1", "A2", "B1", "B2"},
    "oxford_5000": {"B2", "C1"},
}
LEVEL_TO_CODE = {"A1": "a1", "A2": "a2", "B1": "b1", "B2": "b2", "C1": "c1"}


@dataclass(frozen=True)
class WordEntry:
    list_id: str
    page: int
    ordinal_on_page: int
    level_text: str
    cefr_code: str
    source_text: str
    headword_source: str
    headword: str
    homograph_number: str | None
    qualifier: str | None
    part_of_speech: str


def _column(x: float) -> int:
    if x < 130:
        return 0
    if x < 260:
        return 1
    if x < 390:
        return 2
    return 3


def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def _parse_headword(value: str) -> tuple[str, str | None, str | None]:
    qualifier = None
    qualifier_match = re.match(r"^(.*?)\s+(\([^()]+\))$", value)
    if qualifier_match:
        value, qualifier = qualifier_match.groups()
    homograph = None
    homograph_match = re.match(r"^(.*?)(\d+)$", value)
    if homograph_match:
        value, homograph = homograph_match.groups()
    return value, homograph, qualifier


def _page_lines(page: fitz.Page) -> list[dict]:
    lines = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            spans = line["spans"]
            if spans:
                lines.append({"spans": spans, "bbox": line["bbox"]})
    return sorted(lines, key=lambda line: (_column(line["bbox"][0]), line["bbox"][1]))


def _is_heading(line: dict, levels: set[str]) -> str | None:
    text = _normalise("".join(span["text"] for span in line["spans"]))
    first = line["spans"][0]
    if text in levels and first["font"] == "UtopiaStd-Bold" and first["size"] >= 17:
        return text
    return None


def _entry_parts(line: dict) -> tuple[str, str, str] | None:
    spans = line["spans"]
    italic_at = next(
        (index for index, span in enumerate(spans) if span["font"].endswith("It")), None
    )
    if italic_at is None or spans[0]["font"] != "MyriadPro-Regular":
        return None
    headword = _normalise("".join(span["text"] for span in spans[:italic_at]))
    part_of_speech = _normalise("".join(span["text"] for span in spans[italic_at:]))
    source_text = _normalise("".join(span["text"] for span in spans))
    if not headword or not part_of_speech:
        return None
    return source_text, headword, part_of_speech


def extract_wordlist(pdf_path: Path, list_id: str) -> list[WordEntry]:
    levels = LIST_LEVELS[list_id]
    document = fitz.open(pdf_path)
    active_level = None
    entries = []
    for page_number, page in enumerate(document, 1):
        ordinal = 0
        for line in _page_lines(page):
            heading = _is_heading(line, levels)
            if heading:
                active_level = heading
                continue
            parts = _entry_parts(line)
            if parts is None:
                continue
            if active_level is None:
                raise ValueError(f"Word entry precedes level heading on page {page_number}")
            source_text, headword_source, part_of_speech = parts
            headword, homograph, qualifier = _parse_headword(headword_source)
            ordinal += 1
            entries.append(
                WordEntry(
                    list_id, page_number, ordinal, active_level, LEVEL_TO_CODE[active_level],
                    source_text, headword_source, headword, homograph, qualifier, part_of_speech,
                )
            )
    return entries
