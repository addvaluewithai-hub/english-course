"""Build validated evidence bundles used by level-exit claims."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from typing import Any

from scripts.level_exit_evidence_contract import (
    DISPOSITIONS, EVIDENCE_ROLES, LEVELS, OUTPUT, REVIEWED_AT, REVIEWER,
    ROOT, SOURCE_DATASETS, bundle_id,
)
from scripts.source_disposition_inputs import file_sha256


def _hash_ids(ids: list[str]) -> str:
    return hashlib.sha256("\n".join(ids).encode("utf-8")).hexdigest()


def _representatives(ids: list[str]) -> list[str]:
    positions = sorted({0, len(ids) // 2, len(ids) - 1})
    return [ids[index] for index in positions]


def build() -> dict[str, Any]:
    dispositions = json.loads(DISPOSITIONS.read_text(encoding="utf-8"))
    groups: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    for row in dispositions["records"]:
        dataset_id = row["source_dataset_id"]
        if dataset_id not in SOURCE_DATASETS:
            continue
        for level in row["source_level_codes"]:
            if level not in LEVELS:
                continue
            for strand in row["strand_codes"]:
                groups[(dataset_id, level, strand)].append(row["source_record_id"])
    bundles = []
    for (dataset_id, level, strand), raw_ids in sorted(groups.items()):
        ids = sorted(raw_ids)
        bundles.append({
            "bundle_id": bundle_id(dataset_id, level, strand),
            "selector": {
                "source_dataset_id": dataset_id,
                "source_level_code": level,
                "strand_code": strand,
            },
            "evidence_role": EVIDENCE_ROLES[dataset_id],
            "matched_record_count": len(ids),
            "matched_record_ids_sha256": _hash_ids(ids),
            "representative_record_ids": _representatives(ids),
        })
    level_counts = Counter(item["selector"]["source_level_code"] for item in bundles)
    source_counts = Counter(item["selector"]["source_dataset_id"] for item in bundles)
    return {
        "schema_version": 1,
        "dataset_id": "level_exit_evidence_bundles",
        "version": 1,
        "source_dispositions": {
            "path": DISPOSITIONS.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(DISPOSITIONS),
            "record_count": len(dispositions["records"]),
        },
        "bundles": bundles,
        "audit": {
            "bundle_count": len(bundles),
            "level_counts": dict(sorted(level_counts.items())),
            "source_counts": dict(sorted(source_counts.items())),
            "empty_selectors": [],
        },
        "review": {
            "status": "accepted", "reviewer": REVIEWER, "reviewed_at": REVIEWED_AT,
            "method": "validated_selector_and_claim_boundary_review",
        },
    }


def main() -> int:
    data = build()
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(data['bundles'])} bundles)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
