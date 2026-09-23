#!/usr/bin/env python3
"""Acquire a reproducible General Learner C2 vocabulary snapshot from Pearson GSE Toolkit."""
from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = "https://www.english.com/gse/teacher-toolkit/user/api/v1/vocabulary/search"
REFERER = "https://www.english.com/gse/teacher-toolkit/user/vocabulary"
OUT = ROOT / "data/derived/gse-vocabulary-c2-gl.json"
AUDIT = ROOT / "data/derived/gse-vocabulary-c2-gl-audit.json"
UA = "Mozilla/5.0 curriculum-source-audit/1.0"
PAGE_SIZE = 100
FILTERS = {
    "gseRange": {"from": "85", "to": "90"},
    "topics": [],
    "audiences": ["GL"],
    "grammaticalCategories": [],
}


def fetch_page(page: int) -> dict[str, Any]:
    params = {
        "page": str(page),
        "size": str(PAGE_SIZE),
        "sort": "gse",
        "query_string": "*",
        "filters": json.dumps(FILTERS, separators=(",", ":")),
    }
    url = ENDPOINT + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "application/json, text/plain, */*",
            "Referer": REFERER,
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        if response.status != 200:
            raise SystemExit(f"Unexpected HTTP status {response.status} for page {page}")
        return json.loads(response.read().decode("utf-8"))


def normalize_record(source: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "itemId",
        "expression",
        "definition",
        "example",
        "audience",
        "cefr",
        "gse",
        "grammaticalCategories",
        "collos",
        "variants",
        "topics",
        "region",
        "temporaryGse",
        "expression_bre",
    )
    return {key: source[key] for key in keep if key in source}


def numeric_gse(value: Any) -> int:
    match = re.match(r"\s*(\d+)", str(value))
    if not match:
        raise ValueError(f"Cannot parse GSE score: {value!r}")
    return int(match.group(1))


def collo_text(collo: Any) -> str | None:
    if isinstance(collo, str):
        text = collo.strip()
        return text or None
    if isinstance(collo, dict):
        for key in ("expression", "collocation", "text", "value", "word"):
            value = collo.get(key)
            if value:
                return str(value).strip() or None
    return None


def main() -> None:
    first = fetch_page(1)
    expected = int(first["count"])
    if expected <= 0:
        raise SystemExit("Pearson returned no C2 General Learner vocabulary records")

    records = [normalize_record(row) for row in first["data"]]
    page = 2
    while len(records) < expected:
        payload = fetch_page(page)
        if int(payload["count"]) != expected:
            raise SystemExit(f"Count drift on page {page}: {payload['count']} != {expected}")
        batch = [normalize_record(row) for row in payload["data"]]
        if not batch:
            raise SystemExit(f"Pagination ended early at page {page}; have {len(records)} of {expected}")
        records.extend(batch)
        page += 1

    by_id: dict[str, dict[str, Any]] = {}
    for row in records:
        item_id = row.get("itemId")
        if not item_id:
            raise SystemExit("Encountered C2 record without itemId")
        by_id.setdefault(item_id, row)
    records = list(by_id.values())
    if len(records) != expected:
        raise SystemExit(f"Expected {expected} unique itemIds, got {len(records)}")

    for row in records:
        if row.get("audience") != "GL":
            raise SystemExit(f"Non-GL record leaked into C2 snapshot: {row.get('itemId')}")
        gse = numeric_gse(row["gse"])
        if not 85 <= gse <= 90:
            raise SystemExit(f"Out-of-range GSE record: {row.get('itemId')}={row.get('gse')}")
        if not str(row.get("cefr", "")).startswith("C2"):
            raise SystemExit(f"Non-C2 CEFR record: {row.get('itemId')}={row.get('cefr')}")

    pos = Counter()
    multiword = 0
    records_with_collos = 0
    collation_rows = 0
    distinct_collos: set[str] = set()
    temporary_rows = 0
    marked_score_rows = 0
    phrase_records: list[dict[str, Any]] = []
    collocation_samples: list[dict[str, Any]] = []
    multiword_variants: list[dict[str, Any]] = []

    for row in records:
        categories = row.get("grammaticalCategories", [])
        for category in categories:
            pos[category] += 1
        expression = str(row.get("expression", "")).strip()
        if len(expression.split()) > 1:
            multiword += 1
        if any(category in {"phrase", "phrasal verb"} for category in categories):
            phrase_records.append({
                "itemId": row["itemId"],
                "expression": expression,
                "gse": row.get("gse"),
                "categories": categories,
                "definition": row.get("definition", ""),
            })

        collos = row.get("collos") or []
        if collos:
            records_with_collos += 1
            collocation_samples.append({
                "owner_itemId": row["itemId"],
                "owner_expression": expression,
                "gse": row.get("gse"),
                "collos": collos,
            })
        collation_rows += len(collos)
        for collo in collos:
            text = collo_text(collo)
            if text:
                distinct_collos.add(text.casefold())

        for variant in row.get("variants") or []:
            if isinstance(variant, str):
                variant_text = variant.strip()
            elif isinstance(variant, dict):
                variant_text = str(variant.get("variant") or variant.get("expression") or "").strip()
            else:
                variant_text = ""
            if variant_text and len(variant_text.split()) > 1:
                multiword_variants.append({
                    "owner_itemId": row["itemId"],
                    "owner_expression": expression,
                    "gse": row.get("gse"),
                    "variant": variant_text,
                })

        if row.get("temporaryGse") is True:
            temporary_rows += 1
        if str(row.get("gse", "")).strip() != str(numeric_gse(row.get("gse"))):
            marked_score_rows += 1

    canonical = json.dumps(records, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    dataset_hash = hashlib.sha256(canonical).hexdigest().upper()
    payload = {
        "schema_version": 1,
        "dataset_id": "pearson_gse_vocabulary_c2_general_learner",
        "source": {
            "provider": "Pearson GSE Teacher Toolkit",
            "endpoint": ENDPOINT,
            "referer": REFERER,
            "query": {
                "gse_from": 85,
                "gse_to": 90,
                "audience": "GL",
                "query_string": "*",
                "sort": "gse",
            },
        },
        "record_count": len(records),
        "normalized_records_sha256": dataset_hash,
        "status": "official_api_snapshot_pending_inventory_reconciliation_and_license_gate",
        "records": records,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    scores = [numeric_gse(r["gse"]) for r in records]
    audit = {
        "schema_version": 1,
        "dataset_id": payload["dataset_id"],
        "record_count": len(records),
        "gse_min": min(scores),
        "gse_max": max(scores),
        "grammatical_category_counts": dict(pos.most_common()),
        "multiword_expression_records": multiword,
        "single_token_expression_records": len(records) - multiword,
        "records_with_collocations": records_with_collos,
        "collocation_rows": collation_rows,
        "distinct_collocation_strings_detected": len(distinct_collos),
        "temporary_gse_flagged_records": temporary_rows,
        "marked_gse_score_records": marked_score_rows,
        "source_phrase_or_phrasal_verb_records": phrase_records,
        "collocation_owner_records": collocation_samples,
        "multiword_variants": multiword_variants,
        "normalized_records_sha256": dataset_hash,
        "license_gate": "Pearson permission/contact required before commercial use of GSE components",
    }
    AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "record_count": len(records),
        "phrase_records": len(phrase_records),
        "records_with_collocations": records_with_collos,
        "collocation_rows": collation_rows,
        "multiword_variants": len(multiword_variants),
        "dataset_hash": dataset_hash,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
