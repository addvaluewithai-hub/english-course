"""Add row-level provenance to the existing artifact-tool EGP snapshots."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALL_LEVELS = ROOT / "data/derived/egp-all-levels.json"
A1_ONLY = ROOT / "data/derived/egp-a1.json"
RAW_FILE = "sources/raw/grammar/english-grammar-profile-online.xlsx"
RAW_SHA256 = "2D3F59DB3192E322FC2308CAE780AC389E1CF72F95C4CBDEAA087598A08BEF36"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    all_data = _load(ALL_LEVELS)
    raw_levels = {
        row["spreadsheet_row"]: row["raw_level"]
        for row in all_data["normalization_audit"]["changed_rows"]
    }
    provenance = {}
    for spreadsheet_row, record in enumerate(all_data["records"], 2):
        source = {
            "spreadsheet_row": spreadsheet_row,
            "raw_level_text": raw_levels.get(spreadsheet_row, record["Level"]),
        }
        record["_source"] = source
        provenance[record["id"]] = source
    all_data["source"]["source_file_sha256"] = RAW_SHA256
    _write(ALL_LEVELS, all_data)

    a1_data = _load(A1_ONLY)
    a1_data["schema_version"] = "1.0.0"
    a1_data["dataset_id"] = "egp_a1"
    a1_data["source"] = {
        "raw_file": RAW_FILE,
        "source_file_sha256": RAW_SHA256,
        "sheet": "Data",
    }
    for record in a1_data["records"]:
        record["_source"] = provenance[record["id"]]
    _write(A1_ONLY, a1_data)


if __name__ == "__main__":
    main()
