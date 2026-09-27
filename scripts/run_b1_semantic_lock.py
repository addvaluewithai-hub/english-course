#!/usr/bin/env python3
"""Run the B1 semantic ledger after exact human Stage-08.5 critic overrides.

NON-SEMANTIC wrapper. It preserves the distinct GSE `mediation` source mode and
applies only exact item-role changes declared in
`08.5-role-aware-critic/overrides.json`. Automation may validate/apply/count only;
it must never infer an additional semantic role.
"""
from __future__ import annotations

import json
from pathlib import Path

import build_b1_semantic_role_ledger as ledger

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "curriculum/levels/b1/design-review"
CRITIC = REVIEW / "08.5-role-aware-critic/overrides.json"

RECEPTIVE_CONTEXTUAL = {
    "mastery_mode": "receptive",
    "control_scope": "contextual",
    "exit_evidence": "integrated_required",
}
INTEGRATED_SUPPORT = {
    "mastery_mode": "integrated_support",
    "control_scope": "quality_constraint",
    "exit_evidence": "support_condition",
}


def source_mode_with_mediation(item: dict) -> str:
    modes = item.get("mode_codes") or []
    if len(modes) != 1:
        raise ValueError(
            f"ability {item.get('item_id')} must expose exactly one source mode; got {modes}"
        )
    mode = modes[0]
    if mode not in {"reception", "production", "interaction", "mediation"}:
        raise ValueError(
            f"ability {item.get('item_id')} has unsupported source mode {mode!r}"
        )
    return mode


def main() -> None:
    critic = json.loads(CRITIC.read_text(encoding="utf-8")) if CRITIC.exists() else {"semantic": {}}
    if critic.get("level", "B1") != "B1":
        raise ValueError("B1 Stage-08.5 critic level mismatch")
    semantic = critic.get("semantic", {})

    word_to_receptive = set(semantic.get("word_to_receptive_item_ids", []))
    grammar_to_support = set(semantic.get("grammar_to_support_item_ids", []))
    phrase_to_receptive = set(semantic.get("phrase_to_receptive_item_ids", []))
    all_ids = word_to_receptive | grammar_to_support | phrase_to_receptive
    if len(all_ids) != len(word_to_receptive) + len(grammar_to_support) + len(phrase_to_receptive):
        raise ValueError("Stage-08.5 semantic override assigns one exact item through multiple override groups")

    original_add_semantic = ledger.add_semantic
    applied: set[str] = set()

    def add_semantic_with_critic(
        record: dict,
        role: dict,
        basis: str,
        extra: dict | None = None,
    ) -> dict:
        iid = record["item_id"]
        category = record["category"]
        target = None
        reason_key = None
        if iid in word_to_receptive:
            if category != "word":
                raise ValueError(f"Stage-08.5 word override resolved to {category}: {iid}")
            target = RECEPTIVE_CONTEXTUAL
            reason_key = "word_to_receptive"
        elif iid in grammar_to_support:
            if category != "grammar":
                raise ValueError(f"Stage-08.5 grammar override resolved to {category}: {iid}")
            target = INTEGRATED_SUPPORT
            reason_key = "grammar_to_support"
        elif iid in phrase_to_receptive:
            if category != "phrase":
                raise ValueError(f"Stage-08.5 phrase override resolved to {category}: {iid}")
            target = RECEPTIVE_CONTEXTUAL
            reason_key = "phrase_to_receptive"

        if target is None:
            return original_add_semantic(record, role, basis, extra)

        if role.get("mastery_mode") != "productive":
            raise ValueError(
                f"Stage-08.5 demotion expected productive Stage-08 base role: {iid} -> {role}"
            )
        reason = semantic.get("reasons", {}).get(reason_key)
        if not reason:
            raise ValueError(f"Stage-08.5 override group lacks human reason: {reason_key}")
        out = original_add_semantic(
            record,
            target,
            f"stage08.5.exact_item_override:{reason_key};base={basis}",
            extra,
        )
        out["semantic_decision_source"] = "human_stage08_5_critic"
        out["stage_08_5_reason"] = reason
        applied.add(iid)
        return out

    ledger.source_mode = source_mode_with_mediation
    ledger.add_semantic = add_semantic_with_critic
    ledger.main()

    missing = sorted(all_ids - applied)
    extra = sorted(applied - all_ids)
    if missing or extra:
        raise ValueError(f"Stage-08.5 semantic exact-ID application mismatch: missing={missing} extra={extra}")

    # Add transparent wrapper metadata to the deterministic generated snapshot.
    if ledger.DEFAULT_OUTPUT.exists():
        data = json.loads(ledger.DEFAULT_OUTPUT.read_text(encoding="utf-8"))
        data["status"] = "expanded_from_human_stage08_plus_stage08_5_critic"
        data["stage_08_5_applied"] = {
            "source": "../08.5-role-aware-critic/overrides.json",
            "word_to_receptive_count": len(word_to_receptive),
            "grammar_to_support_count": len(grammar_to_support),
            "phrase_to_receptive_count": len(phrase_to_receptive),
            "total_exact_semantic_overrides": len(all_ids),
        }
        ledger.DEFAULT_OUTPUT.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    if ledger.DEFAULT_REPORT.exists():
        report = ledger.DEFAULT_REPORT.read_text(encoding="utf-8")
        report += (
            "\n## Stage 08.5 exact human critic overlay\n\n"
            f"- word productive → receptive exact overrides: **{len(word_to_receptive)}**\n"
            f"- grammar productive → integrated-support exact overrides: **{len(grammar_to_support)}**\n"
            f"- phrase productive → receptive exact overrides: **{len(phrase_to_receptive)}**\n"
            f"- total exact semantic overrides: **{len(all_ids)}**\n\n"
            "These changes are explicit human critic decisions from `../08.5-role-aware-critic/overrides.json`; automation inferred none.\n"
        )
        ledger.DEFAULT_REPORT.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
