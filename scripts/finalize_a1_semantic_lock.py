#!/usr/bin/env python3
"""Finalize A1 manifest and exit contract from the reviewed semantic-lock report."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
A1 = ROOT / "curriculum/levels/a1"
LOCK = A1 / "semantic-lock"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    report = load(LOCK / "semantic-lock-report.json")
    manifest = load(A1 / "manifest.json")
    contract = load(A1 / "exit_contract.json")

    queue = int(report["summary"]["human_review_queue"])
    authorized = bool(report.get("lesson_design_authorized")) and queue == 0
    if authorized and report.get("status") != "semantic_lock_reviewed_locked_v1":
        raise SystemExit("A1 authorization requires semantic_lock_reviewed_locked_v1")

    manifest["lesson_design_authorized"] = authorized
    manifest["delivery_content_production_authorized"] = False
    manifest["delivery_gate_note"] = (
        "Curriculum lesson design is authorized on this independent branch. Mass lesson/media "
        "production remains governed by the separate delivery workstream and does not modify or bypass TEST-002."
    )
    manifest["semantic_lock"] = {
        "status": report["status"],
        "report": "curriculum/levels/a1/semantic-lock/semantic-lock-report.json",
        "human_review_queue": queue,
        "total_primary_items": report["summary"]["total_primary_items"],
    }
    manifest["status"] = (
        "semantic_lock_reviewed_lesson_design_authorized"
        if authorized else "semantic_lock_pending_review"
    )

    contract["status"] = "semantic_inventory_locked_v1" if authorized else "draft_pending_full_inventory_lock"
    contract["inventory_obligations"] = {
        "words": "semantic_lock_v1: 627 productive_required; 185 receptive_required; 88 grammar_owned_required",
        "phrases": "semantic_lock_v1: 114 productive_required; 40 formulaic_productive_required; 45 receptive_required",
        "grammar": "semantic_lock_v1: 92 productive_control_required; 3 formulaic_productive_control_required; 12 embedded_support_required; 2 receptive_control_required",
        "abilities": "semantic_lock_v1: 119 required granular abilities with reviewed performance roles",
        "pronunciation": "semantic_lock_v1: 10 supporting_intelligibility_required strands",
    }
    contract["semantic_lock"] = {
        "status": report["status"],
        "lesson_design_authorized": authorized,
        "human_review_queue": queue,
        "report": "curriculum/levels/a1/semantic-lock/semantic-lock-report.json",
        "completion_is_not_mastery": True,
        "receptive_does_not_imply_productive": True,
        "productive_does_not_imply_all_dictionary_senses": True,
    }

    write(A1 / "manifest.json", manifest)
    write(A1 / "exit_contract.json", contract)
    print(json.dumps({
        "status": report["status"],
        "lesson_design_authorized": authorized,
        "human_review_queue": queue,
    }, indent=2))


if __name__ == "__main__":
    main()
