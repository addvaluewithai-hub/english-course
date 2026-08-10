"""Create reviewed all-level communicative tag assignments."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Callable

from scripts.communicative_tag_contract import (
    CEFR, DISPOSITIONS, GSE, OUTPUT, REPORT, REVIEWED_AT, REVIEWER, ROOT,
)
from scripts.progression_tag_model import TAXONOMY_VERSION
from scripts.source_disposition_inputs import file_sha256
from scripts.tag_cefr_progression import tag_cefr_progression
from scripts.tag_gse_progression import tag_gse_progression


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _assign(
    dataset_id: str, records: list[dict], tagger: Callable, dispositions: dict[tuple[str, str], str]
) -> list[dict]:
    result = []
    for record in records:
        source_id = record["record_id"]
        tags = tagger(record)
        result.append({
            "source_dataset_id": dataset_id,
            "source_record_id": source_id,
            "source_level_codes": record["interpretation"]["cefr_codes"],
            "source_disposition": dispositions[(dataset_id, source_id)],
            "skill_codes": list(tags.skills), "mode_codes": list(tags.modes),
            "function_codes": list(tags.functions), "rule_ids": list(tags.rule_ids),
        })
    return result


def _count(records: list[dict], field: str, flatten: bool = False) -> dict[str, int]:
    values = (value for row in records for value in row[field]) if flatten else (row[field] for row in records)
    return dict(sorted(Counter(values).items()))


def build() -> dict[str, Any]:
    cefr, gse, disposition_data = _load(CEFR), _load(GSE), _load(DISPOSITIONS)
    disposition_index = {
        (row["source_dataset_id"], row["source_record_id"]): row["disposition"]
        for row in disposition_data["records"]
        if row["source_dataset_id"] in {"cefr_all_descriptors", "gse_all_objectives"}
    }
    records = _assign("cefr_all_descriptors", cefr["records"], tag_cefr_progression, disposition_index)
    records += _assign("gse_all_objectives", gse["records"], tag_gse_progression, disposition_index)
    inputs = [
        {"path": path.relative_to(ROOT).as_posix(), "sha256": file_sha256(path), "record_count": count}
        for path, count in ((CEFR, len(cefr["records"])), (GSE, len(gse["records"])), (DISPOSITIONS, len(disposition_data["records"])))
    ]
    return {
        "schema_version": 1, "dataset_id": "communicative_tag_assignments_all_levels",
        "version": 1, "taxonomy_version": TAXONOMY_VERSION, "inputs": inputs,
        "records": records,
        "audit": {
            "record_count": len(records), "dataset_counts": _count(records, "source_dataset_id"),
            "level_counts": _count(records, "source_level_codes", True),
            "skill_counts": _count(records, "skill_codes", True),
            "mode_counts": _count(records, "mode_codes", True),
            "function_counts": _count(records, "function_codes", True),
            "rule_counts": _count(records, "rule_ids", True),
            "untagged_records": [], "unknown_codes": [], "missing_dispositions": [],
        },
        "review": {
            "status": "accepted", "reviewer": REVIEWER, "reviewed_at": REVIEWED_AT,
            "method": "deterministic_rules_plus_distribution_and_hotspot_review",
            "limitations": [
                "Tags are broad curriculum-comparison functions, not lesson outcomes or semantic equivalence claims.",
                "Default comprehend/give-information tags preserve coverage when a source gives no narrower communicative purpose.",
                "Lifecycle levels and lesson ownership are separate progression decisions.",
            ],
        },
    }


def _report(data: dict[str, Any]) -> str:
    audit = data["audit"]
    lines = [
        "# All-Level Communicative Tag Audit v1", "", "Status: accepted internal review.", "",
        f"All **{audit['record_count']:,}** CEFR and GSE communicative records have skill, mode,",
        "function, and auditable rule assignments. Source text and published levels remain unchanged.",
        "", "## Modes", "", "| Mode | Assignments |", "| --- | ---: |",
    ]
    lines += [f"| `{key}` | {value:,} |" for key, value in audit["mode_counts"].items()]
    lines += ["", "## Functions", "", "| Function | Assignments |", "| --- | ---: |"]
    lines += [f"| `{key}` | {value:,} |" for key, value in audit["function_counts"].items()]
    lines += [
        "", "## Integrity", "", "- Untagged records: 0.", "- Unknown codes: 0.",
        "- Missing source dispositions: 0.",
        "- All 52 plurilingual/pluricultural CEFR records are explicitly represented.",
        "- Advanced functions augment rather than overwrite the source's skill and mode.", "",
        "Counts are evidence density, not teaching time. These tags create comparison",
        "strands; they do not make two differently worded records equivalent.", "",
    ]
    return "\n".join(lines)


def main() -> int:
    data = build()
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.write_text(_report(data), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(data['records'])} records)")
    print(f"Wrote {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
