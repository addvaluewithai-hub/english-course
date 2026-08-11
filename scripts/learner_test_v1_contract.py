"""Paths and fixed identities for the first real-learner test kit."""

from scripts.a1_reconciliation_contract import ROOT


KIT = ROOT / "research" / "learner-test-v1"
PROTOTYPE = ROOT / "prototype" / "gold-lesson"
MANIFEST = KIT / "kit-manifest.json"
THRESHOLDS = KIT / "success-thresholds.json"
SCHEMA = KIT / "session-record.schema.json"
TEMPLATE = KIT / "session-record.template.json"
STUDY_ID = "gold_lesson_u1_l03_pilot_v1"
LESSON_ID = "U1-L03"

KIT_ARTIFACTS = {
    "research/learner-test-v1/PROTOCOL.md",
    "research/learner-test-v1/CONSENT_AR.md",
    "research/learner-test-v1/FACILITATOR_CHECKLIST.md",
    "research/learner-test-v1/success-thresholds.json",
    "research/learner-test-v1/session-record.schema.json",
    "research/learner-test-v1/session-record.template.json",
    "prototype/gold-lesson/index.html",
    "prototype/gold-lesson/observer.html",
}

GATING_METRICS = {
    "informed_consent_compliance",
    "privacy_or_safety_incidents",
    "severe_accessibility_blockers",
    "completed_fresh_attempt_without_full_model",
    "demonstrated_full_outcome",
    "major_instruction_confusion",
    "severe_arabic_or_level_clarity_issues",
    "important_correction_retry_success",
    "mastery_decision_agreement",
}
