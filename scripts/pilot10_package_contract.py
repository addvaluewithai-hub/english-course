from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE_PATH = ROOT / "data/reviewed/a1-first-10-lessons-pilot-v1.json"
SCOPE_PATH = ROOT / "data/reviewed/a1-scope-and-sequence-v1.json"
FINAL_PATH = ROOT / "data/reviewed/a1-final-candidate-decisions-v1.json"
GRAMMAR_PATH = ROOT / "data/reviewed/a1-grammar-coverage-ownership-v1.json"
LEXICAL_PATH = ROOT / "data/reviewed/a1-lexical-chunk-ownership-v1.json"
PRONUNCIATION_PATH = ROOT / "data/reviewed/a1-pronunciation-ownership-v1.json"
SOURCE_INPUTS = (
    RELEASE_PATH,
    SCOPE_PATH,
    FINAL_PATH,
    GRAMMAR_PATH,
    LEXICAL_PATH,
    PRONUNCIATION_PATH,
)
EXPECTED_FILES = {
    "lesson-manifest.json",
    "source-packet.json",
    "content.json",
    "activities.json",
    "assessment.json",
    "ai-contract.json",
    "ASSET_BRIEFS.md",
    "video/scene.txt",
    "video/sample-context.txt",
    "video/transcript.txt",
    "video/pronunciation-map.json",
    "video/README.md",
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def release() -> dict:
    return read_json(RELEASE_PATH)


def lesson_contract(lesson_id: str) -> dict:
    return next(row for row in release()["lessons"] if row["lesson_id"] == lesson_id)


def input_records(extra: tuple[Path, ...] = ()) -> list[dict]:
    return [
        {"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path)}
        for path in SOURCE_INPUTS + extra
    ]


def package_path(contract: dict) -> Path:
    return ROOT / contract["content_path"]


def item_evidence(item_id: str) -> dict:
    if item_id.startswith("grammar."):
        row = next(
            x for x in read_json(GRAMMAR_PATH)["course_items"] if x["item_id"] == item_id
        )
        evidence = row["source_evidence"]
        refs = evidence["egp_feature_ids"] + evidence["gse_grammar_record_ids"]
        return {
            "item_id": item_id,
            "label": row["title"],
            "bounded_scope": row["meaning_use"],
            "source_refs": refs,
            "later_boundary": row["not_yet"],
        }
    if item_id.startswith("lexical."):
        row = next(
            x for x in read_json(LEXICAL_PATH)["course_items"]
            if x["lexical_item_id"] == item_id
        )
        return {
            "item_id": item_id,
            "label": row["canonical_form"],
            "bounded_scope": row["productive_expectation"],
            "source_refs": row["source_refs"],
            "later_boundary": f"Consolidation: {row['consolidation_level']}",
        }
    row = next(
        x for x in read_json(PRONUNCIATION_PATH)["targets"] if x["target_id"] == item_id
    )
    return {
        "item_id": item_id,
        "label": row["title"],
        "bounded_scope": row["feature_or_contrast"],
        "source_refs": row["source_refs"],
        "later_boundary": row["not_yet"],
    }


def exact_records(contract: dict, role: str) -> list[dict]:
    return [item_evidence(item_id) for item_id in contract["exact_item_roles"][role]]
