"""Repository validation for the TEST-001 package and clickable prototype."""

import json
import re

from jsonschema import Draft202012Validator

from scripts.learner_test_v1_contract import (
    GATING_METRICS, KIT, KIT_ARTIFACTS, LESSON_ID, MANIFEST, PROTOTYPE,
    ROOT, SCHEMA, STUDY_ID, TEMPLATE, THRESHOLDS,
)
from scripts.source_disposition_inputs import file_sha256


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _manifest_errors() -> list[str]:
    data = _load(MANIFEST)
    errors: list[str] = []
    if data["study_id"] != STUDY_ID or data["lesson_id"] != LESSON_ID:
        errors.append("kit manifest has a stale study or lesson identity")
    if data["status"] != "TEST_001_ready_for_real_sessions":
        errors.append("kit manifest is not ready for real sessions")
    if set(data["artifacts"]) != KIT_ARTIFACTS:
        errors.append("kit manifest does not list the complete artifact set")
    for path in data["artifacts"]:
        if not (ROOT / path).is_file():
            errors.append(f"missing learner-test artifact: {path}")
    for row in data["source_inputs"]:
        path = ROOT / row["path"]
        if not path.is_file() or file_sha256(path) != row["sha256"]:
            errors.append(f"learner-test source hash mismatch: {row['path']}")
    boundary = data["data_boundary"]
    if boundary["default_raw_capture"] or boundary["direct_identifiers_allowed"]:
        errors.append("kit manifest permits raw capture or direct identifiers")
    if boundary["individual_record_retention_days_after_TEST_002"] != 90:
        errors.append("kit manifest lacks the agreed 90-day record retention")
    return errors


def _threshold_errors() -> list[str]:
    data = _load(THRESHOLDS)
    errors: list[str] = []
    if data["study_id"] != STUDY_ID or data["status"] != "pre_registered_hypotheses":
        errors.append("success thresholds are not pre-registered for this study")
    sample = data["sample"]
    if sample != {
        "target_completed_sessions": 8,
        "minimum_eligible_completed_sessions": 6,
        "minimum_double_rated_sessions": 2,
    }:
        errors.append("pilot sample boundaries changed")
    metrics = data["gating_metrics"]
    if {row["metric_id"] for row in metrics} != GATING_METRICS:
        errors.append("gating metric set is incomplete or duplicated")
    for row in metrics:
        if row["operator"] not in {">=", "<=", "=="}:
            errors.append(f"unsupported threshold operator: {row['metric_id']}")
        if row["minimum_denominator"] < 2 or not row["definition"]:
            errors.append(f"threshold lacks a usable denominator or definition: {row['metric_id']}")
        if row["action_if_missed"] not in {"revise_and_retest", "stop_and_redesign"}:
            errors.append(f"threshold lacks a controlled failure action: {row['metric_id']}")
    expected_order = ["stop_and_redesign", "insufficient_evidence", "revise_and_retest", "go_to_system_revision"]
    if data["decision_precedence"] != expected_order:
        errors.append("pilot decision precedence changed")
    return errors


def _schema_errors() -> list[str]:
    schema, template = _load(SCHEMA), _load(TEMPLATE)
    errors: list[str] = []
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as error:  # pragma: no cover - exact library message is unstable
        errors.append(f"invalid session JSON Schema: {error}")
        return errors
    for error in Draft202012Validator(schema).iter_errors(template):
        errors.append(f"session template violates schema: {error.message}")
    serialized = json.dumps(template, ensure_ascii=False).lower()
    for forbidden in ("full_name", "phone_number", "email_address", '"raw_answer":', "audio_path"):
        if forbidden in serialized:
            errors.append(f"session template exposes a prohibited field: {forbidden}")
    if template["data_controls"]["contains_raw_answer"] is not False:
        errors.append("session template may retain a raw learner answer")
    return errors


def _document_errors() -> list[str]:
    protocol = " ".join((KIT / "PROTOCOL.md").read_text(encoding="utf-8").split())
    consent = " ".join((KIT / "CONSENT_AR.md").read_text(encoding="utf-8").split())
    checklist = " ".join((KIT / "FACILITATOR_CHECKLIST.md").read_text(encoding="utf-8").split())
    runbook = " ".join((KIT / "ANALYSIS_RUNBOOK.md").read_text(encoding="utf-8").split())
    errors: list[str] = []
    for phrase in ("eight completed", "six is the minimum", "teachback", "omit",
                   "without a complete answer model", "Double-rate at least two"):
        if phrase not in protocol:
            errors.append(f"protocol omits a fixed test rule: {phrase}")
    for phrase in ("18 سنة", "معلومات خيالية", "التوقف في أي وقت", "90 يومًا", "موافقة منفصلة"):
        if phrase not in consent:
            errors.append(f"Arabic consent omits required information: {phrase}")
    for phrase in ("Do not start raw", "Ask for the final response aloud", "cannot by itself prove"):
        if phrase not in checklist:
            errors.append(f"facilitator checklist omits a safety or construct rule: {phrase}")
    for phrase in ("simulation_only_no_gate_effect", "real_consented_sessions", "outside this repository"):
        if phrase not in runbook:
            errors.append(f"analysis runbook omits a data or evidence boundary: {phrase}")
    return errors


def _prototype_errors() -> list[str]:
    index = (PROTOTYPE / "index.html").read_text(encoding="utf-8")
    data = (PROTOTYPE / "scripts/data.js").read_text(encoding="utf-8")
    views = (PROTOTYPE / "scripts/views.js").read_text(encoding="utf-8")
    app = (PROTOTYPE / "scripts/app.js").read_text(encoding="utf-8")
    research = (PROTOTYPE / "scripts/research.js").read_text(encoding="utf-8")
    observer = (PROTOTYPE / "scripts/observer.js").read_text(encoding="utf-8")
    errors: list[str] = []
    required = ("observer.html", "consentDialog", "timingDialog", "U1-L03", "scripts/research.js")
    if any(item not in index for item in required):
        errors.append("prototype index lacks its v1 consent, timing, or observer route")
    if index.index("scripts/research.js") > index.index("scripts/app.js"):
        errors.append("research controls load after the lesson app")
    if data.count("{ id:") != 9:
        errors.append("prototype does not expose the nine tested sections")
    if "../../gold/introduce-yourself" in views or "lessons/u1-l03/video/transcript.txt" not in views:
        errors.append("prototype points to a stale gold transcript")
    for phrase in ("My name is", "form-choice", "قل إجابتك بصوتك أولًا"):
        if phrase not in views:
            errors.append(f"prototype omits final U1-L03 behavior: {phrase}")
    for phrase in ("lessonResearch.stepChanged", "lessonResearch.mark", "lessonResearch.init"):
        if phrase not in app:
            errors.append(f"prototype lacks local research hook: {phrase}")
    if "if (step === 5) updatePlan();" not in app:
        errors.append("personal planning initialization uses a stale pre-migration step")
    for forbidden in ("fetch(", "localStorage", "coachAnswer", "masteryAnswer"):
        if forbidden in research:
            errors.append(f"timing module may capture or transmit an answer: {forbidden}")
    if "contains_raw_answer: false" not in research or "contains_direct_identifier: false" not in research:
        errors.append("timing export does not declare both privacy boundaries")
    if "raw_capture: false" not in observer or "contains_raw_answer: false" not in observer:
        errors.append("observer export does not hard-code the no-raw-data boundary")
    for phrase in ("double_rated", "secondary_ratings", "exact_decision_agreement", "resolved:"):
        if phrase not in observer:
            errors.append(f"observer export omits TEST-002 evidence: {phrase}")
    for path in PROTOTYPE.rglob("*"):
        if path.is_file() and path.suffix in {".html", ".css", ".js"}:
            if len(path.read_text(encoding="utf-8").splitlines()) > 200:
                errors.append(f"prototype source exceeds 200 lines: {path.relative_to(ROOT)}")
    return errors


def validate() -> list[str]:
    required = [MANIFEST, THRESHOLDS, SCHEMA, TEMPLATE, KIT / "PROTOCOL.md",
                KIT / "CONSENT_AR.md", KIT / "FACILITATOR_CHECKLIST.md"]
    missing = [path for path in required if not path.is_file()]
    if missing:
        return [f"missing TEST-001 file: {path.relative_to(ROOT)}" for path in missing]
    return (_manifest_errors() + _threshold_errors() + _schema_errors() +
            _document_errors() + _prototype_errors())
