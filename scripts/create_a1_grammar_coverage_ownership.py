"""Build the exact A1 grammar inventory, source dispositions, and owners."""

from __future__ import annotations

import copy
import json
from collections import Counter, defaultdict

from scripts.a1_grammar_item_catalog import ITEMS
from scripts.a1_grammar_legacy_crosswalk import CROSSWALK
from scripts.a1_grammar_ownership_contract import (
    EGP, GSE_GRAMMAR, INPUTS, OUTPUT, REPORT, REVIEWED_AT, REVIEWER, ROOT,
    SUPPORT_OWNER_IDS, WORKLIST,
)
from scripts.a1_grammar_ownership_report import render
from scripts.a1_grammar_source_assignments import EGP_ASSIGNMENTS, GSE_ASSIGNMENTS
from scripts.source_disposition_inputs import file_sha256


def _load(path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _a1_sources() -> tuple[list[dict], list[dict]]:
    egp = [row for row in _load(EGP)["records"] if row["Level"] == "A1"]
    gse = [row for row in _load(GSE_GRAMMAR)["records"] if row["interpretation"]["cefr_codes"] == ["a1"]]
    return egp, gse


def _owners(item_ids: tuple[str, ...], item_index: dict[str, dict], disposition: str) -> list[str]:
    if not item_ids:
        transfer_owner = {
            "transfer_phrase_layer": "support.phrase_syllabus",
            "transfer_lexical_layer": "support.lexical_syllabus",
            "transfer_writing_support": "support.written_form_control",
        }
        return [transfer_owner[disposition]]
    values = {
        owner
        for item_id in item_ids
        for field in ("introduction_owner_ids", "recycle_owner_ids")
        for owner in item_index[item_id][field]
    }
    return sorted(values)


def _source_rows(items: list[dict]) -> list[dict]:
    item_index = {row["item_id"]: row for row in items}
    egp, gse = _a1_sources()
    egp_index = {row["id"]: row for row in egp}
    gse_index = {row["record_id"]: row for row in gse}
    rows = []
    for system, assignments, source_index in (
        ("egp", EGP_ASSIGNMENTS, egp_index), ("gse_grammar", GSE_ASSIGNMENTS, gse_index),
    ):
        for record_id, item_ids, disposition, rationale in assignments:
            source = source_index[record_id]
            if system == "egp":
                label = f"{source['SuperCategory']} > {source['SubCategory']} > {source['Guideword']}"
                text = source["Can-do statement"]
            else:
                facts = source["source_facts"]
                label = f"GSE {facts['gse_score_or_range']}: {facts['other_verbatim']['structure']}"
                text = source["source"]["source_text"]
            rows.append({
                "source_system": system, "source_record_id": record_id, "source_level": "A1",
                "source_label": label, "source_text": text, "course_item_ids": list(item_ids),
                "disposition": disposition, "rationale_code": rationale,
                "owner_ids": _owners(item_ids, item_index, disposition),
            })
    return rows


def _items_with_evidence(source_rows: list[dict]) -> list[dict]:
    evidence = defaultdict(lambda: {"egp": [], "gse_grammar": []})
    for row in source_rows:
        for item_id in row["course_item_ids"]:
            evidence[item_id][row["source_system"]].append(row["source_record_id"])
    rows = copy.deepcopy(list(ITEMS))
    for row in rows:
        source = evidence[row["item_id"]]
        row["source_evidence"] = {
            "source_count": len(source["egp"]) + len(source["gse_grammar"]),
            "egp_feature_ids": source["egp"], "gse_grammar_record_ids": source["gse_grammar"],
        }
    return rows


def _legacy_rows(worklist: dict) -> list[dict]:
    rows = []
    for candidate in worklist["candidates"]:
        targets = candidate["current_language_targets"]["grammar"]
        if not targets:
            continue
        rows.append({
            "candidate_id": candidate["candidate_id"], "legacy_target": targets[0],
            "exact_item_ids": list(CROSSWALK[candidate["candidate_id"]]),
        })
    return rows


def build() -> dict:
    worklist = _load(WORKLIST)
    source_rows = _source_rows(list(ITEMS))
    items = _items_with_evidence(source_rows)
    legacy = _legacy_rows(worklist)
    known_candidates = {row["candidate_id"] for row in worklist["candidates"]}
    known_items = {row["item_id"] for row in items}
    used_items = {item for row in source_rows for item in row["course_item_ids"]}
    legacy_items = {item for row in legacy for item in row["exact_item_ids"]}
    grammar_candidate_ids = {
        row["candidate_id"] for row in worklist["candidates"]
        if row["current_language_targets"]["grammar"]
    }
    owner_ids = {owner for row in items for field in ("introduction_owner_ids", "recycle_owner_ids") for owner in row[field]}
    unknown_owners = sorted(owner_ids - known_candidates - SUPPORT_OWNER_IDS)
    assigned_ids = {row["source_record_id"] for row in source_rows}
    egp, gse = _a1_sources()
    source_ids = {row["id"] for row in egp} | {row["record_id"] for row in gse}
    return {
        "schema_version": 1, "dataset_id": "a1_grammar_coverage_ownership", "version": 1,
        "inputs": [{"path": path.relative_to(ROOT).as_posix(), "sha256": file_sha256(path)} for path in INPUTS],
        "policy": {
            "source_role": "EGP and GSE Grammar are evidence inventories, not automatic lesson or mastery checklists.",
            "course_item_role": "The controlled items define exact A1 forms, meanings, limits, contexts, and fresh-task mastery evidence.",
            "ownership_status": "Candidate owners are reconciliation contexts and may move intact when candidates merge or the final sequence changes.",
            "variety_policy": "Internationally intelligible core English is taught; have is the course default while BrE have got is registered as valid.",
            "assessment_policy": "Grammar is assessed through meaning-preserving use in fresh communicative tasks, not rule naming or isolated recall alone.",
        },
        "course_items": items, "source_dispositions": source_rows, "legacy_target_crosswalk": legacy,
        "audit": {
            "egp_a1_source_count": len(egp), "gse_grammar_a1_source_count": len(gse),
            "total_source_count": len(source_ids), "course_item_count": len(items),
            "control_status_counts": dict(sorted(Counter(row["control_status"] for row in items).items())),
            "disposition_counts": dict(sorted(Counter(row["disposition"] for row in source_rows).items())),
            "legacy_target_count": len(legacy), "new_system_item_ids": sorted(known_items - legacy_items),
            "orphan_source_ids": sorted(source_ids - assigned_ids),
            "unknown_course_item_ids": sorted(used_items - known_items), "unknown_owner_ids": unknown_owners,
            "items_without_source_evidence": sorted(known_items - used_items),
            "items_without_recycle_owners": sorted(row["item_id"] for row in items if not row["recycle_owner_ids"]),
            "unmapped_legacy_candidate_ids": sorted(grammar_candidate_ids - set(CROSSWALK)),
            "final_lesson_decisions_made": 0,
        },
        "review": {
            "status": "accepted_exact_language_system_pass", "reviewer": REVIEWER, "reviewed_at": REVIEWED_AT,
            "statement": "All A1 grammar evidence has a disposition and every selected learner item has exact forms, bounded use, owners, recycling, mastery, and an explicit later-level boundary.",
        },
    }


def main() -> int:
    data = build()
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.write_text(render(data), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(data['course_items'])} items; {len(data['source_dispositions'])} sources)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
