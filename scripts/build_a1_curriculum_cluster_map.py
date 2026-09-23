#!/usr/bin/env python3
"""Build an evidence-backed A1 curriculum cluster map before unit/lesson design.

This script does NOT authorize lessons and does NOT treat the legacy 45 capabilities as a
fixed sequence. It uses reviewed legacy candidate clusters only as evidence for natural
homes, then audits the complete A1 source-of-truth inventory in both directions:

  cluster -> required content
  required content -> at least one natural cluster home

Unmapped items remain explicit orphans; ambiguous items keep multiple candidate homes.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
A1 = ROOT / "curriculum/levels/a1"
OUT = A1 / "curriculum-map"


def read(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    return json.loads(p.read_text(encoding="utf-8"))


def write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def walk_dicts(node: Any) -> Iterable[dict[str, Any]]:
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk_dicts(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk_dicts(value)


def norm(value: str) -> str:
    value = value.lower().replace("…", "...").replace("’", "'")
    value = re.sub(r"[.!?,;:()\[\]{}\"“”]", " ", value)
    value = value.replace("...", " ")
    value = re.sub(r"\b(sb|sth)\b", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def normalize_source_record_id(value: str) -> str:
    # Legacy candidate evidence sometimes omits the explicit level segment.
    return value.replace(".a1.", ".")


def candidate_indexes(worklist: dict[str, Any]):
    candidates = worklist["candidates"]
    by_id = {c["candidate_id"]: c for c in candidates}
    cluster_candidates: dict[str, set[str]] = defaultdict(set)
    function_clusters: dict[str, set[str]] = defaultdict(set)
    evidence_clusters: dict[str, set[str]] = defaultdict(set)
    cluster_meta: dict[str, dict[str, Any]] = {}

    for c in candidates:
        cluster_ids = c.get("cluster_ids", [])
        for cluster in cluster_ids:
            cluster_candidates[cluster].add(c["candidate_id"])
            cluster_meta.setdefault(cluster, {"cluster_id": cluster})
        for fn in c.get("function_codes", []):
            function_clusters[fn].update(cluster_ids)
        evidence = c.get("evidence", {})
        ids = list(evidence.get("record_ids", []))
        ids.extend(evidence.get("level_fit", {}).get("matched_all_level_record_ids", []))
        for rid in ids:
            evidence_clusters[normalize_source_record_id(rid)].update(cluster_ids)
    return by_id, cluster_candidates, function_clusters, evidence_clusters, cluster_meta


def map_abilities(abilities: dict[str, Any], evidence_clusters, function_clusters):
    rows = []
    for a in abilities["items"]:
        rid = normalize_source_record_id(a["source_record_id"])
        exact = sorted(evidence_clusters.get(rid, set()))
        if exact:
            clusters = exact
            basis = "exact_reviewed_candidate_source_evidence"
        else:
            clusters_set = set()
            for fn in a.get("function_codes", []):
                clusters_set.update(function_clusters.get(fn, set()))
            clusters = sorted(clusters_set)
            basis = "same_reviewed_communicative_function" if clusters else "unmapped"
        rows.append({
            "item_id": a["item_id"],
            "source_text": a["source_text"],
            "function_codes": a.get("function_codes", []),
            "skill_codes": a.get("skill_codes", []),
            "mode_codes": a.get("mode_codes", []),
            "candidate_cluster_ids": clusters,
            "mapping_basis": basis,
        })
    return rows


def lexical_dispositions(ownership: dict[str, Any]) -> dict[str, dict[str, Any]]:
    found = {}
    for row in walk_dicts(ownership):
        if str(row.get("source_record_id", "")).startswith("oxford.o3000.") and "disposition" in row:
            found[row["source_record_id"]] = row
    return found


def course_item_cluster_index(ownership: dict[str, Any], candidate_by_id: dict[str, Any]):
    out: dict[str, set[str]] = defaultdict(set)
    for item in ownership["course_items"]:
        locations = []
        if item.get("introduction_location"):
            locations.append(item["introduction_location"])
        locations.extend(item.get("recycle_locations", []))
        for cid in locations:
            candidate = candidate_by_id.get(cid)
            if candidate:
                out[item["lexical_item_id"]].update(candidate.get("cluster_ids", []))
    return out


def map_words(words, lexical_ownership, lexical_item_clusters):
    dispositions = lexical_dispositions(lexical_ownership)
    rows = []
    for w in words["items"]:
        review = dispositions.get(w["item_id"], {})
        owners = review.get("course_item_ids", [])
        clusters = set()
        for owner in owners:
            clusters.update(lexical_item_clusters.get(owner, set()))
        basis = "reviewed_lexical_owner_to_candidate_cluster" if clusters else "unmapped"
        if review.get("disposition") == "grammar_system_owned":
            basis = "grammar_owned_cross_cutting"
        rows.append({
            "item_id": w["item_id"],
            "headword": w["headword"],
            "part_of_speech": w.get("part_of_speech"),
            "previous_reviewed_disposition": review.get("disposition"),
            "reviewed_lexical_owner_ids": owners,
            "candidate_cluster_ids": sorted(clusters),
            "mapping_basis": basis,
        })
    return rows


def phrase_member_index(lexical_ownership: dict[str, Any]):
    out: dict[str, set[str]] = defaultdict(set)
    for item in lexical_ownership["course_items"]:
        for value in list(item.get("members", [])) + list(item.get("collocations_or_frames", [])):
            if isinstance(value, str) and norm(value):
                out[norm(value)].add(item["lexical_item_id"])
    return out


def href_lemma(href: str | None) -> str | None:
    if not href:
        return None
    m = re.search(r"/definition/english/([^#/?]+)", href)
    if not m:
        return None
    return m.group(1).replace("-", " ").lower()


def word_headword_clusters(word_rows):
    out: dict[str, set[str]] = defaultdict(set)
    for row in word_rows:
        if row["candidate_cluster_ids"]:
            out[norm(row["headword"])].update(row["candidate_cluster_ids"])
    return out


def map_phrases(phrases, lexical_ownership, lexical_item_clusters, word_rows):
    member_index = phrase_member_index(lexical_ownership)
    headword_clusters = word_headword_clusters(word_rows)
    rows = []
    for p in phrases["items"]:
        pnorm = norm(p["phrase"])
        exact_owners = sorted(member_index.get(pnorm, set()))
        clusters = set()
        for owner in exact_owners:
            clusters.update(lexical_item_clusters.get(owner, set()))
        if clusters:
            basis = "normalized_exact_reviewed_chunk_member"
        else:
            lemma = href_lemma(p.get("source_ref", {}).get("href"))
            if lemma:
                clusters.update(headword_clusters.get(norm(lemma), set()))
            basis = "source_headword_natural_home" if clusters else "unmapped"
        rows.append({
            "item_id": p["item_id"],
            "phrase": p["phrase"],
            "reviewed_exact_owner_ids": exact_owners,
            "source_headword": href_lemma(p.get("source_ref", {}).get("href")),
            "candidate_cluster_ids": sorted(clusters),
            "mapping_basis": basis,
        })
    return rows


def grammar_course_cluster_index(grammar_ownership, candidate_by_id):
    out: dict[str, set[str]] = defaultdict(set)
    for item in grammar_ownership["course_items"]:
        cids = list(item.get("introduction_owner_ids", [])) + list(item.get("recycle_owner_ids", []))
        for cid in cids:
            candidate = candidate_by_id.get(cid)
            if candidate:
                out[item["item_id"]].update(candidate.get("cluster_ids", []))
    return out


def map_grammar(grammar, grammar_ownership, candidate_by_id):
    feature_owners: dict[str, set[str]] = defaultdict(set)
    for item in grammar_ownership["course_items"]:
        for fid in item.get("source_evidence", {}).get("egp_feature_ids", []):
            feature_owners[fid].add(item["item_id"])
    course_clusters = grammar_course_cluster_index(grammar_ownership, candidate_by_id)
    rows = []
    for g in grammar["items"]:
        raw_id = g["item_id"].removeprefix("egp.")
        owners = sorted(feature_owners.get(raw_id, set()))
        clusters = set()
        for owner in owners:
            clusters.update(course_clusters.get(owner, set()))
        rows.append({
            "item_id": g["item_id"],
            "guideword": g.get("guideword"),
            "can_do": g.get("can_do"),
            "reviewed_grammar_owner_ids": owners,
            "candidate_cluster_ids": sorted(clusters),
            "mapping_basis": "reviewed_grammar_owner_to_candidate_cluster" if clusters else "unmapped",
        })
    return rows


def make_cluster_records(cluster_meta, cluster_candidates, candidate_by_id, mapped_groups):
    clusters = {}
    for cluster_id in sorted(cluster_meta):
        cands = sorted(cluster_candidates.get(cluster_id, set()))
        function_codes = sorted({
            fn for cid in cands for fn in candidate_by_id[cid].get("function_codes", [])
        })
        skills = sorted({
            s for cid in cands for s in candidate_by_id[cid].get("skill_codes", [])
        })
        modes = sorted({
            m for cid in cands for m in candidate_by_id[cid].get("mode_codes", [])
        })
        clusters[cluster_id] = {
            "cluster_id": cluster_id,
            "status": "candidate_natural_home_not_sequence_lock",
            "legacy_candidate_ids_as_evidence": cands,
            "function_codes": function_codes,
            "skill_codes": skills,
            "mode_codes": modes,
            "mapped_item_ids": {name: [] for name in mapped_groups},
        }
    for group_name, rows in mapped_groups.items():
        for row in rows:
            for cid in row["candidate_cluster_ids"]:
                if cid in clusters:
                    clusters[cid]["mapped_item_ids"][group_name].append(row["item_id"])
    for cluster in clusters.values():
        cluster["counts"] = {k: len(v) for k, v in cluster["mapped_item_ids"].items()}
    return list(clusters.values())


def coverage(rows):
    mapped = [r for r in rows if r["candidate_cluster_ids"]]
    unmapped = [r for r in rows if not r["candidate_cluster_ids"]]
    ambiguous = [r for r in rows if len(r["candidate_cluster_ids"]) > 1]
    return {
        "total": len(rows),
        "mapped": len(mapped),
        "unmapped": len(unmapped),
        "ambiguous_multiple_homes": len(ambiguous),
        "mapping_basis_counts": dict(sorted(Counter(r["mapping_basis"] for r in rows).items())),
    }


def main():
    words = read(A1 / "words.json")
    phrases = read(A1 / "phrases.json")
    grammar = read(A1 / "grammar.json")
    abilities = read(A1 / "abilities.json")
    lexical_ownership = read("data/reviewed/a1-lexical-chunk-ownership-v1.json")
    grammar_ownership = read("data/reviewed/a1-grammar-coverage-ownership-v1.json")
    worklist = read("data/reviewed/a1-reconciliation-worklist-v1.json")

    candidate_by_id, cluster_candidates, function_clusters, evidence_clusters, cluster_meta = candidate_indexes(worklist)
    lexical_item_clusters = course_item_cluster_index(lexical_ownership, candidate_by_id)

    ability_rows = map_abilities(abilities, evidence_clusters, function_clusters)
    word_rows = map_words(words, lexical_ownership, lexical_item_clusters)
    phrase_rows = map_phrases(phrases, lexical_ownership, lexical_item_clusters, word_rows)
    grammar_rows = map_grammar(grammar, grammar_ownership, candidate_by_id)

    groups = {
        "abilities": ability_rows,
        "words": word_rows,
        "phrases": phrase_rows,
        "grammar": grammar_rows,
    }
    cluster_rows = make_cluster_records(cluster_meta, cluster_candidates, candidate_by_id, groups)

    report = {
        "schema_version": 1,
        "level": "A1",
        "status": "cluster_map_v0_needs_architecture_review",
        "lesson_design_authorized": False,
        "principles": {
            "inventory_is_fixed_input": True,
            "mapping_is_two_way": True,
            "legacy_candidate_sequence_is_not_binding": True,
            "unmapped_items_must_not_be_silently_dropped": True,
            "review_lessons_are_not_default_orphan_dump": True,
            "recycling_is_not_designed_yet": True,
        },
        "coverage": {name: coverage(rows) for name, rows in groups.items()},
        "cluster_count": len(cluster_rows),
        "cluster_loads": sorted(
            [
                {
                    "cluster_id": c["cluster_id"],
                    **c["counts"],
                    "total_mapped_refs": sum(c["counts"].values()),
                }
                for c in cluster_rows
            ],
            key=lambda x: (-x["total_mapped_refs"], x["cluster_id"]),
        ),
        "orphans": {
            name: [
                {
                    "item_id": r["item_id"],
                    "display": r.get("headword") or r.get("phrase") or r.get("guideword") or r.get("source_text"),
                    "mapping_basis": r["mapping_basis"],
                }
                for r in rows if not r["candidate_cluster_ids"]
            ]
            for name, rows in groups.items()
        },
    }

    payload = {
        "schema_version": 1,
        "level": "A1",
        "status": report["status"],
        "lesson_design_authorized": False,
        "mapping_policy": {
            "abilities": "Exact reviewed candidate evidence first; otherwise same reviewed communicative function.",
            "words": "Reviewed lexical ownership to candidate cluster; grammar-owned words remain cross-cutting until grammar placement.",
            "phrases": "Exact reviewed chunk match first; otherwise Oxford source-headword natural home. No fuzzy semantic matching.",
            "grammar": "Exact EGP feature to reviewed grammar owner, then owner candidate clusters.",
        },
        "clusters": cluster_rows,
        "item_mappings": groups,
        "evidence_sources": [
            "curriculum/levels/a1/abilities.json",
            "curriculum/levels/a1/words.json",
            "curriculum/levels/a1/phrases.json",
            "curriculum/levels/a1/grammar.json",
            "data/reviewed/a1-reconciliation-worklist-v1.json",
            "data/reviewed/a1-lexical-chunk-ownership-v1.json",
            "data/reviewed/a1-grammar-coverage-ownership-v1.json",
        ],
    }

    write(OUT / "cluster-map-v0.json", payload)
    write(OUT / "cluster-coverage-report-v0.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
