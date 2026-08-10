"""Paths and controlled values for exact A1 pronunciation ownership."""

from scripts.a1_lexical_ownership_contract import OUTPUT as LEXICAL_OWNERSHIP
from scripts.a1_reconciliation_contract import ROOT
from scripts.a1_reconciliation_contract import OUTPUT as WORKLIST


PROGRESSION = ROOT / "data" / "reviewed" / "pronunciation-progression-strands-v1.json"
OUTPUT = ROOT / "data" / "reviewed" / "a1-pronunciation-ownership-v1.json"
REPORT = ROOT / "docs" / "A1_PRONUNCIATION_OWNERSHIP_V1.md"
SCHEMA = ROOT / "schemas" / "curriculum" / "a1-pronunciation-ownership.schema.json"
INPUTS = (PROGRESSION, WORKLIST, LEXICAL_OWNERSHIP)
REVIEWED_AT = "2026-08-10T15:28:00+03:00"
REVIEWER = "codex_primary_curriculum_agent"

CONTROL_STATUSES = ("receptive_and_productive", "receptive_with_guided_imitation")
RISK_DISPOSITIONS = ("selected_monitor_target", "monitor_if_observed_not_pre_taught")
SUPPORT_OWNER_IDS = {"support.a1_exit_pronunciation_probe"}
