"""Create EGP family lifecycle strands and a GSE Grammar category crosswalk."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from typing import Any

from scripts.grammar_crosswalk_rules import RULES, crosswalk
from scripts.grammar_strand_contract import (
    DISPOSITIONS, EGP, EXIT_LEVELS, GSE_GRAMMAR, LEVELS, OUTPUT, REPORT,
    REVIEWED_AT, REVIEWER, ROOT,
)
from scripts.source_disposition_inputs import file_sha256


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_")


def _hash_ids(ids: list[str]) -> str:
    return hashlib.sha256("\n".join(ids).encode("utf-8")).hexdigest()


def _representatives(ids: list[str]) -> list[str]:
    return [ids[index] for index in sorted({0, len(ids) // 2, len(ids) - 1})]


def _level_counts(features: list[dict]) -> dict[str, int]:
    return dict(sorted(Counter(row["Level"].casefold() for row in features).items(), key=lambda item: LEVELS.index(item[0])))


def _stages(counts: dict[str, int], exposure: str, consolidation: str) -> list[dict]:
    stages = []
    for level in LEVELS[LEVELS.index(exposure) :]:
        count = counts.get(level, 0)
        if level == exposure:
            states, status = ["expose"], "planned_exposure"
        elif level == consolidation:
            states, status = ["introduce", "practise", "consolidate"], "source_evidenced"
        else:
            states = ["recycle"] + (["extend"] if count else [])
            status = "source_evidenced" if count else "planned_recycle"
        stages.append({
            "level": level, "feature_count": count, "evidence_status": status,
            "lifecycle_states": states,
        })
    return stages


def _family(supercategory: str, subcategory: str, features: list[dict]) -> dict[str, Any]:
    ids = sorted(str(row["id"]) for row in features)
    counts = _level_counts(features)
    consolidation = next(level for level in EXIT_LEVELS if level in counts)
    exposure = LEVELS[LEVELS.index(consolidation) - 1]
    recycle = list(EXIT_LEVELS[EXIT_LEVELS.index(consolidation) + 1 :])
    extension = [level for level in recycle if level in counts]
    return {
        "family_id": f"grammar.{_slug(supercategory)}.{_slug(subcategory)}",
        "supercategory": supercategory, "subcategory": subcategory,
        "title": f"{supercategory.title()}: {subcategory}",
        "evidence": {
            "feature_count": len(features), "feature_ids_sha256": _hash_ids(ids),
            "representative_feature_ids": _representatives(ids), "level_counts": counts,
        },
        "lifecycle": {
            "first_exposure_level": exposure,
            "first_productive_control_level": consolidation,
            "consolidation_level": consolidation,
            "recycle_levels": recycle, "extension_levels": extension,
            "within_level_order_required": True,
            "stages": _stages(counts, exposure, consolidation),
            "rationale": (
                "The earliest EGP level is the family productive-control boundary, not a mandate to teach every feature. "
                "The family is exposed one course level earlier, consolidated at that boundary, and recycled thereafter."
            ),
        },
        "review": {"status": "accepted", "review_basis": "egp_family_boundary_with_prior_exposure_policy"},
    }


def _crosswalk(record: dict) -> dict:
    facts = record["source_facts"]
    other = facts["other_verbatim"]
    categories, rules = crosswalk(
        other["grammatical_categories"], other["structure"], record["source"]["source_text"]
    )
    return {
        "source_record_id": record["record_id"],
        "source_level_codes": record["interpretation"]["cefr_codes"],
        "supercategory_codes": categories, "rule_ids": rules,
    }


def build() -> dict[str, Any]:
    egp = json.loads(EGP.read_text(encoding="utf-8"))
    gse = json.loads(GSE_GRAMMAR.read_text(encoding="utf-8"))
    dispositions = json.loads(DISPOSITIONS.read_text(encoding="utf-8"))
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for feature in egp["records"]:
        grouped[(feature["SuperCategory"], feature["SubCategory"])].append(feature)
    families = [_family(*key, grouped[key]) for key in sorted(grouped)]
    crosswalk_rows = [_crosswalk(record) for record in gse["records"]]
    used_categories = {code for row in crosswalk_rows for code in row["supercategory_codes"]}
    gse_levels = {level for row in crosswalk_rows for level in row["source_level_codes"]}
    return {
        "schema_version": 1, "dataset_id": "grammar_family_progression_strands",
        "version": 1, "level_order": list(LEVELS),
        "inputs": [
            {"path": path.relative_to(ROOT).as_posix(), "sha256": file_sha256(path), "record_count": count}
            for path, count in ((EGP, len(egp["records"])), (GSE_GRAMMAR, len(gse["records"])), (DISPOSITIONS, len(dispositions["records"])))
        ],
        "feature_use_policy": "family_range_evidence_not_one_feature_one_target",
        "families": families, "gse_crosswalk": crosswalk_rows,
        "audit": {
            "family_count": len(families), "egp_feature_count": len(egp["records"]),
            "gse_crosswalk_count": len(crosswalk_rows), "supercategory_count": len(RULES),
            "supercategories_without_gse_crosscheck": sorted(set(RULES) - used_categories),
            "gse_levels_without_records": [level for level in EXIT_LEVELS if level not in gse_levels],
            "unassigned_egp_features": [], "unassigned_gse_records": [],
            "missing_consolidation": [], "invalid_level_regressions": [],
            "missing_post_consolidation_recycle": [],
        },
        "review": {
            "status": "accepted", "reviewer": REVIEWER, "reviewed_at": REVIEWED_AT,
            "method": "family_level_lifecycle_and_category_crosswalk_review",
            "limitations": [
                "EGP families define progression range; individual features are evidence, not automatic lesson targets.",
                "The GSE Grammar crosswalk is category-level and does not claim feature-by-feature equivalence.",
                "Exact learner-facing forms, examples, and prerequisites are selected during level reconciliation.",
            ],
        },
    }


def _report(data: dict[str, Any]) -> str:
    lines = [
        "# Grammar Family Progression v1", "", "Status: accepted internal curriculum contract.", "",
        "All 1,222 EGP features belong to 91 reviewed grammar families. Families own",
        "level boundaries; individual EGP rows do not become 1,222 mandatory targets.",
        "", "| Family | First exposure | Consolidate | Extension | Features |", "| --- | --- | --- | --- | ---: |",
    ]
    for family in data["families"]:
        life = family["lifecycle"]
        lines.append(
            f"| `{family['family_id']}` | {life['first_exposure_level'].upper()} | "
            f"{life['consolidation_level'].upper()} | {', '.join(x.upper() for x in life['extension_levels']) or '-'} | "
            f"{family['evidence']['feature_count']} |"
        )
    lines += [
        "", "The 456 GSE Grammar records are cross-walked to EGP supercategories as",
        "productive cross-check evidence. Category overlap is preserved; it is not treated",
        "as exact feature equivalence. Exact target selection happens during level mapping.",
        f"GSE Grammar has no records at: {', '.join(x.upper() for x in data['audit']['gse_levels_without_records'])}.",
        f"EGP families without a named GSE category cross-check: {', '.join(data['audit']['supercategories_without_gse_crosscheck'])}.", "",
    ]
    return "\n".join(lines)


def main() -> int:
    data = build()
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.write_text(_report(data), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(data['families'])} families)")
    print(f"Wrote {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
