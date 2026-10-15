#!/usr/bin/env python3
"""Inspect or validate the six canonical, Markdown-backed lesson production queues.

Usage:
  python3 interactive-content-production/tools/production_status.py validate
  python3 interactive-content-production/tools/production_status.py next A1
  python3 interactive-content-production/tools/production_status.py next B1

This program never claims, edits, or marks a lesson done on its own. Claim via
a reviewed PR changing the row; GitHub PR conflicts are the concurrency guard.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATUS = ROOT / "interactive-content-production" / "status"
LEVELS = ("A1", "A2", "B1", "B2", "C1", "C2")
BRIEFS = {
    "A1": ("07", 62), "A2": ("09", 83),
    "B1": ("07", 85), "B2": ("07", 95),
}
VALID = {"not-started", "claimed", "in-progress", "qa-pending", "review-needed",
         "done", "blocked", "pilot-only"}
ROW = re.compile(r"^\| (U\d+-L\d+) \| (\d+) \| (.*?) \| ([a-z-]+) \| (.*?) \| (.*?) \|$")
HEADING = re.compile(r"^#{2,3}\s+(U(\d+)-L\d+)\s+[—–-]\s+(.+)$", re.M)


def rows(level: str):
    path = STATUS / (level + ".md")
    content = path.read_text(encoding="utf-8")
    return [dict(id=m[1], unit=int(m[2]), title=m[3].replace("\\|", "|"),
                 status=m[4], evidence=m[5], agent=m[6])
            for line in content.splitlines() if (m := ROW.match(line))]


def validate():
    checked = {}
    for level in LEVELS:
        path = STATUS / (level + ".md")
        assert path.is_file(), f"Missing status file: {path}"
        items = rows(level)
        if level not in BRIEFS:
            assert not items, f"{level}: invented lesson slots before curriculum authorization"
            assert "**BLOCKED**" in path.read_text(encoding="utf-8"), f"{level}: missing gate"
            checked[level] = {"lessons": 0, "curriculum": "blocked"}
            continue
        number, expected = BRIEFS[level]
        source = ROOT / f"curriculum/levels/{level.lower()}/design-review/{number}-lesson-briefs/lesson-briefs.md"
        src = [(m[1], m[3].strip()) for m in HEADING.finditer(source.read_text(encoding="utf-8"))]
        assert len(src) == expected, f"{level}: expected {expected} canonical briefs, found {len(src)}"
        assert len(items) == len(src), f"{level}: expected {len(src)} rows, got {len(items)}"
        assert len({r["id"] for r in items}) == len(items), f"{level}: duplicate IDs"
        for found, (sid, title) in zip(items, src):
            assert found["id"] == sid, f"{level}: misordered or missing {sid}"
            assert found["title"] == title, f"{level} {sid}: title drift; update from canon"
            assert found["unit"] == int(sid.split("-")[0][1:]), f"{level} {sid}: unit mismatch"
            assert found["status"] in VALID, f"{level} {sid}: unknown status"
            if found["status"] in ("claimed", "in-progress", "qa-pending", "review-needed", "done"):
                assert found["evidence"] != "—" and found["agent"] != "—", f"{level} {sid}: missing owner/evidence"
            if found["status"] == "done":
                assert "http" in found["evidence"], f"{level} {sid}: missing linked QA + approval proof"
        checked[level] = {"lessons": len(items),
                          "not_started": sum(x["status"] == "not-started" for x in items),
                          "done": sum(x["status"] == "done" for x in items)}
    print(json.dumps({"status": "valid", "levels": checked}, ensure_ascii=False, indent=2))


def next_lesson(level: str):
    assert level in LEVELS, "Level must be one of " + ", ".join(LEVELS)
    manifest = json.loads((ROOT / f"curriculum/levels/{level.lower()}/manifest.json").read_text(encoding="utf-8"))
    if not manifest.get("lesson_design_authorized"):
        print(json.dumps({"level": level, "state": "BLOCKED_CURRICULUM",
                          "reason": "Unit/lesson architecture not authorized; do not invent lessons."}))
        return
    items = rows(level)
    candidate = next((r for r in items if r["status"] == "not-started"), None)
    if candidate is None:
        print(json.dumps({"level":level,"state":"NO_UNCLAIMED_LESSONS",
                          "note":"Review QA-pending and in-progress PRs; never duplicate claims."}))
        return
    idx = items.index(candidate)
    result = {
        "level": level,
        "state": "SUGGESTED_NOT_CLAIMED",
        "lesson": candidate,
        "position": idx + 1,
        "total": len(items),
        "source": f"curriculum/levels/{level.lower()}/design-review/{BRIEFS[level][0]}-lesson-briefs/lesson-briefs.md",
        "delivery_authorized_in_manifest": manifest.get("delivery_content_production_authorized") is True,
        "instruction": "Check open PRs. Make a scoped product branch, claim this row with owner/PR link, then follow production skill P0-P6. No mass release."
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "validate":
        validate()
    elif len(sys.argv) == 3 and sys.argv[1] == "next":
        next_lesson(sys.argv[2].upper())
    else:
        raise SystemExit(__doc__)
