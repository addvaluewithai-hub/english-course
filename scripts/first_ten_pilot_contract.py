from pathlib import Path

from scripts.pilot10_package_contract import ROOT


KIT = ROOT / "research/first-ten-pilot-v1"
PROTOTYPE = ROOT / "prototype/first-ten"
SCHEMA = KIT / "progression-record.schema.json"
THRESHOLDS = KIT / "success-thresholds.json"
STUDY_ID = "a1_first_10_progression_pilot_v1"
RELEASE_ID = "a1_first_10_lessons_pilot_v1"
VISIT_PLAN = {
    1: ["U1-L01", "U1-L02"],
    2: ["U1-L03", "U1-L04"],
    3: ["U1-L05", "U1-L06"],
    4: ["U1-L07"],
    5: ["U1-L08", "U1-L09"],
    6: ["U2-L01"],
}
STATION_IDS = {"UNIT1-STATION-01", "UNIT1-STATION-02", "UNIT1-STATION-03"}
DECISIONS = {"demonstrated", "practiced", "needs_review", "not_rated"}
REQUIRED_KIT_FILES = {
    "README.md", "START_HERE_AR.md", "CONSENT_AR.md", "FACILITATOR_CHECKLIST.md",
    "PROTOCOL.md", "ANALYSIS_RUNBOOK.md", "success-thresholds.json",
    "progression-record.schema.json",
}
REQUIRED_OBSERVER_FILES = {
    "observer.html", "styles/observer.css", "scripts/observer-app.js",
    "scripts/observer-config.js", "scripts/observer-record.js",
    "scripts/observer-validation.js", "scripts/observer-view.js",
}


def load_json(path: Path):
    import json

    return json.loads(path.read_text(encoding="utf-8"))
