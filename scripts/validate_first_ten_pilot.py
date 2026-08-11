from jsonschema import Draft202012Validator

from scripts.first_ten_pilot_contract import (
    KIT, PROTOTYPE, REQUIRED_KIT_FILES, REQUIRED_OBSERVER_FILES, SCHEMA, STUDY_ID,
    THRESHOLDS, load_json,
)
from scripts.validate_pilot10_prototype import validate as validate_prototype
from scripts.pilot10_common_validation import validate_package
from scripts.pilot10_package_contract import release
from scripts.pilot10_qa_report import QA_JSON, QA_MD, build_qa, render
from scripts.pilot10_release_contract import build_release_contract


def _schema_errors() -> list[str]:
    schema = load_json(SCHEMA)
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as error:  # pragma: no cover
        return [f"invalid progression schema: {error}"]
    serialized = SCHEMA.read_text(encoding="utf-8").lower()
    forbidden = ('"full_name"', '"email"', '"phone"', '"raw_answer"', '"audio_path"')
    return [f"schema exposes prohibited field: {token}" for token in forbidden if token in serialized]


def _threshold_errors() -> list[str]:
    data = load_json(THRESHOLDS)
    errors = []
    if data["study_id"] != STUDY_ID:
        errors.append("threshold study identity is stale")
    sample = data["sample"]
    if not (sample["maximum_recruited"] >= sample["target_complete_journeys"] >=
            sample["minimum_eligible_complete_journeys"] >= 6):
        errors.append("sample boundaries are inconsistent")
    schedule = data["schedule"]
    if schedule != {"visit_count": 6, "window_days_min": 8, "window_days_max": 12,
                     "maximum_visit_minutes": 60}:
        errors.append("schedule differs from the approved six-visit protocol")
    gates = data["hard_gates"]
    for exact_zero in ("private_records_committed", "unapproved_or_mismatched_media_count",
                       "answer_leakage_before_fresh_mastery_count"):
        if gates[exact_zero] != 0:
            errors.append(f"safety gate is not zero: {exact_zero}")
    expected = ["stop_and_repair", "insufficient_evidence", "revise_and_repilot", "go_to_system_revision"]
    if data["decisions_in_precedence_order"] != expected:
        errors.append("decision precedence changed")
    split = data["split_review"]
    if set(split["lessons"]) != {"U1-L05", "U1-L08"} or split["conditions_required"] != 2:
        errors.append("load-risk split review changed")
    return errors


def _document_errors() -> list[str]:
    protocol = (KIT / "PROTOCOL.md").read_text(encoding="utf-8")
    start = (KIT / "START_HERE_AR.md").read_text(encoding="utf-8")
    consent = (KIT / "CONSENT_AR.md").read_text(encoding="utf-8")
    checklist = (KIT / "FACILITATOR_CHECKLIST.md").read_text(encoding="utf-8")
    errors = []
    for phrase in ("six visits", "8–12 days", "maximum 60 minutes", "U1-L08", "U1-L05",
                   "Private longitudinal records never enter the repository"):
        if phrase not in protocol:
            errors.append(f"protocol omits fixed rule: {phrase}")
    for phrase in ("ست زيارات", "8–12 يوم", "P10-A7K2", "خارج الريبو"):
        if phrase not in start:
            errors.append(f"Arabic start guide omits execution rule: {phrase}")
    for phrase in ("18 سنة", "التوقف", "لا نسجل صوتك", "معلومات وشخصيات"):
        if phrase not in consent:
            errors.append(f"Arabic consent omits boundary: {phrase}")
    for phrase in ("Do not record", "Reconfirm consent", "replacement"):
        if phrase not in checklist:
            errors.append(f"facilitator checklist omits rule: {phrase}")
    return errors


def _observer_errors() -> list[str]:
    errors = []
    index = (PROTOTYPE / "index.html").read_text(encoding="utf-8")
    observer = (PROTOTYPE / "observer.html").read_text(encoding="utf-8")
    scripts = "\n".join((PROTOTYPE / name).read_text(encoding="utf-8")
                        for name in REQUIRED_OBSERVER_FILES if name.startswith("scripts/"))
    if not (PROTOTYPE / "observer.html").is_file():
        errors.append("direct facilitator instrument is missing")
    for phrase in ("لا تكتب اسمًا", "data-lesson", "observer-app.js"):
        if phrase not in observer and phrase not in scripts:
            errors.append(f"observer instrument lacks: {phrase}")
    for phrase in ("contains_direct_identifier: false", "contains_raw_answer: false",
                   "contains_audio: false", "contains_video: false"):
        if phrase not in scripts:
            errors.append(f"observer export omits privacy constant: {phrase}")
    for token in ("textarea", "sendBeacon", "WebSocket", "fetch(\"http", "localStorage"):
        if token in observer or token in scripts:
            errors.append(f"observer may capture or transmit prohibited content: {token}")
    for path in [PROTOTYPE / item for item in REQUIRED_OBSERVER_FILES]:
        if path.suffix in {".js", ".html", ".css"} and len(path.read_text(encoding="utf-8").splitlines()) > 200:
            errors.append(f"observer source exceeds modularity limit: {path.name}")
    return errors


def _content_errors() -> list[str]:
    errors = []
    release_data = release()
    if release_data != build_release_contract():
        errors.append("first-ten release contract is stale")
    for lesson in release_data["lessons"]:
        errors += [f"{lesson['lesson_id']}: {error}" for error in validate_package(lesson["lesson_id"])]
    expected_qa = build_qa()
    if load_json(QA_JSON) != expected_qa or QA_MD.read_text(encoding="utf-8") != render(expected_qa):
        errors.append("first-ten content QA is stale")
    errors += expected_qa["findings"]["validation_errors"]
    return errors


def validate() -> list[str]:
    actual_kit = {path.name for path in KIT.iterdir() if path.is_file()}
    errors = [f"missing pilot kit file: {name}" for name in REQUIRED_KIT_FILES - actual_kit]
    errors += [f"missing observer file: {name}" for name in REQUIRED_OBSERVER_FILES
               if not (PROTOTYPE / name).is_file()]
    if errors:
        return errors
    return (_schema_errors() + _threshold_errors() + _document_errors() + _observer_errors() +
            _content_errors() + validate_prototype())


def main() -> None:
    errors = validate()
    if errors:
        raise SystemExit("FAIL first-ten pilot readiness\n- " + "\n- ".join(errors))
    print("PASS first-ten progression pilot instrument readiness")


if __name__ == "__main__":
    main()
