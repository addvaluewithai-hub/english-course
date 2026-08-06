"""Extract reviewed CEFR A1 table cells from the authoritative PDF text layer."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import fitz

try:
    from scripts.cefr_a1_specs import TABLE_SPECS, TableSpec
except ModuleNotFoundError:
    from cefr_a1_specs import TABLE_SPECS, TableSpec


LEVELS = {"C2", "C1", "B2", "B1", "A2", "A1", "Pre-A1"}
STARTERS = ("Can ", "Can, ", "Has ", "Shows ", "Uses ", "Pronunciation ")


@dataclass(frozen=True)
class Descriptor:
    page: int
    mode: str
    skill: str
    scale: str
    ordinal_in_scale: int
    text: str
    transcription_notes: tuple[str, ...]


def _clean(parts: list[str]) -> tuple[str, tuple[str, ...]]:
    raw = " ".join(part.strip() for part in parts if part.strip()).replace("\xad", "")
    text = re.sub(r"\s+", " ", raw).strip()
    joined = re.sub(r"(?<=\w)([-/])\s+(?=\w)", r"\1", text)
    notes = []
    if joined != text:
        notes.append("Removed extraction-only spacing after a line-final hyphen or slash.")
    if len(parts) > 1:
        notes.append("Joined visual line wraps without changing the published wording.")
    return joined, tuple(notes)


def _page_lines(page: fitz.Page) -> list[dict]:
    output = []
    for block_index, block in enumerate(page.get_text("dict")["blocks"]):
        for line in block.get("lines", []):
            text = "".join(span["text"] for span in line["spans"]).strip()
            if text:
                output.append({"block": block_index, "text": text, **line})
    return output


def _anchors(lines: list[dict], vertical: bool) -> list[dict]:
    selected = [
        line for line in lines
        if line["text"] == "A1" and ((line["dir"][1] < -0.9) == vertical)
    ]
    axis = 0 if vertical else 1
    return sorted(selected, key=lambda line: line["bbox"][axis])


def _level_centers(lines: list[dict], vertical: bool) -> list[tuple[float, str]]:
    axis = 0 if vertical else 1
    centers = []
    for line in lines:
        if line["text"] not in LEVELS or ((line["dir"][1] < -0.9) != vertical):
            continue
        centers.append(((line["bbox"][axis] + line["bbox"][axis + 2]) / 2, line["text"]))
    return sorted(centers)


def _row_bounds(
    page: fitz.Page, lines: list[dict], anchor: dict, vertical: bool
) -> tuple[float, float]:
    axis = 0 if vertical else 1
    center = (anchor["bbox"][axis] + anchor["bbox"][axis + 2]) / 2
    rules = []
    for drawing in page.get_drawings():
        rect = drawing["rect"]
        if vertical and rect.height > 300 and rect.width < 2:
            rules.append((rect.x0 + rect.x1) / 2)
        if not vertical and rect.width > 300 and rect.height < 2:
            rules.append((rect.y0 + rect.y1) / 2)
    before_rules = [value for value in rules if value < center - 0.1]
    after_rules = [value for value in rules if value > center + 0.1]
    if before_rules and after_rules:
        return max(before_rules), min(after_rules)
    levels = _level_centers(lines, vertical)
    before = [value for value, _ in levels if value < center - 0.1]
    after = [value for value, _ in levels if value > center + 0.1]
    margin = 60 if vertical else 45
    low = (max(before) + center) / 2 if before else center - margin
    high = (min(after) + center) / 2 if after else center + margin
    return low, high


def _split_groups(lines: list[dict], vertical: bool) -> list[tuple[str, tuple[str, ...]]]:
    axis = 0 if vertical else 1
    groups: list[list[str]] = []
    for block in sorted({line["block"] for line in lines}):
        block_lines = sorted(
            (line for line in lines if line["block"] == block),
            key=lambda line: line["bbox"][axis],
        )
        current: list[str] = []
        previous = None
        for line in block_lines:
            position = line["bbox"][axis]
            if current and previous is not None and position - previous > 11.8:
                groups.append(current)
                current = []
            current.append(line["text"])
            previous = position
        if current:
            groups.append(current)
    cleaned = [_clean(group) for group in groups]
    return [item for item in cleaned if item[0].startswith(STARTERS)]


def _horizontal(page: fitz.Page, spec: TableSpec) -> list[list[tuple[str, tuple[str, ...]]]]:
    lines = _page_lines(page)
    anchor = _anchors(lines, False)[spec.anchor]
    low, high = _row_bounds(page, lines, anchor, False)
    content = [
        line for line in lines
        if line["dir"][0] > 0.9
        and line["bbox"][0] >= 110
        and low + 3 <= (line["bbox"][1] + line["bbox"][3]) / 2 <= high - 3
    ]
    return [_split_groups(content, False)]


def _rotated(page: fitz.Page, spec: TableSpec) -> list[list[tuple[str, tuple[str, ...]]]]:
    lines = _page_lines(page)
    anchor = _anchors(lines, True)[spec.anchor]
    low, high = _row_bounds(page, lines, anchor, True)
    column_count = len(spec.scales)
    edges = [735 - index * (665 / column_count) for index in range(column_count + 1)]
    columns = []
    for index in range(column_count):
        upper, lower = edges[index], edges[index + 1]
        content = [
            line for line in lines
            if line["dir"][1] < -0.9
            and low + 3 <= (line["bbox"][0] + line["bbox"][2]) / 2 <= high - 3
            and lower <= (line["bbox"][1] + line["bbox"][3]) / 2 <= upper
        ]
        columns.append(_split_groups(content, True))
    return columns


def extract_descriptors(
    pdf_path: Path,
) -> tuple[list[Descriptor], dict[tuple[str, str, str], int]]:
    document = fitz.open(pdf_path)
    descriptors = []
    inventory = {}
    for spec in TABLE_SPECS:
        groups = _rotated(document[spec.page - 1], spec) if spec.rotated else _horizontal(document[spec.page - 1], spec)
        if len(groups) != len(spec.scales):
            raise ValueError(f"Column mismatch on page {spec.page}: {spec.scales}")
        for scale, expected, items in zip(spec.scales, spec.expected_counts, groups):
            inventory[(spec.mode, spec.skill, scale)] = len(items)
            if len(items) != expected:
                raise ValueError(f"{scale} on page {spec.page}: expected {expected}, found {len(items)}")
            for ordinal, (text, notes) in enumerate(items, 1):
                descriptors.append(Descriptor(spec.page, spec.mode, spec.skill, scale, ordinal, text, notes))
    return descriptors, inventory
