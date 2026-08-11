from __future__ import annotations

import re
from pathlib import Path

from scripts.pilot10_package_contract import ROOT, release


PROTOTYPE = ROOT / "prototype/first-ten"
REQUIRED = {
    "index.html",
    "media/README.md",
    "observer.html",
    "README.md",
    "scripts/activity-view.js",
    "scripts/api.js",
    "scripts/app.js",
    "scripts/catalog-view.js",
    "scripts/config.js",
    "scripts/dom.js",
    "scripts/lesson-view.js",
    "scripts/learner-support.js",
    "scripts/observer-app.js",
    "scripts/observer-config.js",
    "scripts/observer-record.js",
    "scripts/observer-validation.js",
    "scripts/observer-view.js",
    "scripts/state.js",
    "scripts/unit-review.js",
    "styles/components.css",
    "styles/layout.css",
    "styles/observer.css",
    "styles/tokens.css",
}


def validate() -> list[str]:
    errors = []
    actual = {path.relative_to(PROTOTYPE).as_posix() for path in PROTOTYPE.rglob("*") if path.is_file()}
    if actual != REQUIRED:
        errors.append(f"prototype file set differs: expected {len(REQUIRED)}, found {len(actual)}")
    index = (PROTOTYPE / "index.html").read_text(encoding="utf-8")
    for relative in re.findall(r'(?:src|href)="([^"]+)"', index):
        if relative.startswith(("http://", "https://", "#")):
            continue
        if not (PROTOTYPE / relative).is_file():
            errors.append(f"index references missing asset: {relative}")
    scripts = "\n".join(path.read_text(encoding="utf-8") for path in (PROTOTYPE / "scripts").glob("*.js"))
    if "localStorage" not in scripts or "english-course:first-ten:progress:v1" not in scripts:
        errors.append("device-local progress contract is missing")
    state = (PROTOTYPE / "scripts/state.js").read_text(encoding="utf-8")
    for forbidden in ("answer", "textarea", "masteryDraft", "email", "phone"):
        if forbidden in state:
            errors.append(f"local state may retain learner content: {forbidden}")
    if any(token in scripts for token in ("fetch(\"http", "fetch('http", "WebSocket", "sendBeacon")):
        errors.append("prototype contains an external transport")
    app = (PROTOTYPE / "scripts/app.js").read_text(encoding="utf-8")
    if "U1-L09" not in app or 'review: "unit1"' not in app or 'lesson: "U2-L01"' not in app:
        errors.append("Unit 1 review is not routed between lessons 9 and 10")
    api = (PROTOTYPE / "scripts/api.js").read_text(encoding="utf-8")
    if "a1-first-10-lessons-pilot-v1.json" not in api:
        errors.append("prototype does not read the locked release")
    lesson_view = (PROTOTYPE / "scripts/lesson-view.js").read_text(encoding="utf-8")
    for phrase in ("data-video-done", "renderActivity", "data-mastery-done", "data-save-feedback"):
        if phrase not in lesson_view:
            errors.append(f"student flow omits required stage: {phrase}")
    for lesson in release()["lessons"]:
        if not (ROOT / lesson["content_path"] / "lesson-manifest.json").is_file():
            errors.append(f"prototype release package is missing: {lesson['lesson_id']}")
    for path in (PROTOTYPE / "scripts").glob("*.js"):
        if len(path.read_text(encoding="utf-8").splitlines()) > 200:
            errors.append(f"prototype script exceeds modularity limit: {path.name}")
    return errors


def main() -> None:
    errors = validate()
    if errors:
        raise SystemExit("FAIL first-ten prototype\n- " + "\n- ".join(errors))
    print("PASS first-ten local prototype readiness")


if __name__ == "__main__":
    main()
