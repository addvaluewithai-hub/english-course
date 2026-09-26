#!/usr/bin/env python3
"""Run the A2 semantic ledger after applying exact human Stage-08.5 overrides.

This wrapper is mechanical only. The base semantic decisions remain preserved in
Stage 08; the later human critic records exact review-row role changes in
08.5-role-aware-critic/overrides.json. This script validates and applies them,
then delegates exact expansion/reporting to build_a2_semantic_role_ledger.py.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import build_a2_semantic_role_ledger as semantic

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "curriculum/levels/a2/design-review"
BASE = REVIEW / "08-semantic-lock/semantic-decisions.json"
CRITIC = REVIEW / "08.5-role-aware-critic/overrides.json"
MERGED = Path("/tmp/a2-semantic-decisions-effective.json")
ALL_WORD_ROWS = set(range(1, 872))


def number_spec(rows: set[int]) -> str:
    return ", ".join(str(x) for x in sorted(rows))


def main() -> None:
    decisions = json.loads(BASE.read_text(encoding="utf-8"))
    critic = json.loads(CRITIC.read_text(encoding="utf-8")) if CRITIC.exists() else {"semantic": {}}
    merged = copy.deepcopy(decisions)

    word_decisions = merged["words"]
    productive = semantic.expand_number_spec(word_decisions["productive_review_rows"])
    support = semantic.expand_number_spec(word_decisions["integrated_support_review_rows"])
    receptive = ALL_WORD_ROWS - productive - support

    critic_semantic = critic.get("semantic", {})
    to_receptive = semantic.expand_number_spec(critic_semantic.get("word_to_receptive_review_rows", ""))
    to_productive = semantic.expand_number_spec(critic_semantic.get("word_to_productive_review_rows", ""))
    to_support = semantic.expand_number_spec(critic_semantic.get("word_to_support_review_rows", ""))

    if (to_receptive | to_productive | to_support) - ALL_WORD_ROWS:
        raise ValueError("Stage-08.5 word semantic override outside review rows 1..871")
    if to_receptive & to_productive or to_receptive & to_support or to_productive & to_support:
        raise ValueError("Stage-08.5 word semantic override assigns one row to multiple target roles")

    # V1 critic semantics: explicit demotions must actually demote an existing
    # productive record. Promotions/support moves are also validated against the
    # role they are leaving, so the wrapper cannot silently reinterpret a row.
    bad_demotions = sorted(to_receptive - productive)
    if bad_demotions:
        raise ValueError(f"Stage-08.5 receptive override rows were not productive in Stage 08: {bad_demotions}")
    bad_promotions = sorted(to_productive - receptive)
    if bad_promotions:
        raise ValueError(f"Stage-08.5 productive override rows were not receptive in Stage 08: {bad_promotions}")
    bad_support = sorted(to_support - receptive)
    if bad_support:
        raise ValueError(f"Stage-08.5 support override rows were not receptive in Stage 08: {bad_support}")

    productive = (productive - to_receptive) | to_productive
    support = support | to_support
    receptive = ALL_WORD_ROWS - productive - support

    if productive & support or productive & receptive or support & receptive:
        raise ValueError("effective Stage-08.5 word roles overlap")
    if productive | support | receptive != ALL_WORD_ROWS:
        raise ValueError("effective Stage-08.5 word roles do not cover all 871 review rows")

    word_decisions["productive_review_rows"] = number_spec(productive)
    word_decisions["integrated_support_review_rows"] = number_spec(support)
    word_decisions["remaining_rows_role"] = "receptive_contextual"
    word_decisions["expected_counts"] = {
        "productive": len(productive),
        "integrated_support": len(support),
        "receptive_contextual": len(receptive),
    }
    merged["status"] = "human_semantic_decisions_v1_plus_stage_08_5_critic"
    merged["stage_08_5_applied"] = {
        "source": "../08.5-role-aware-critic/overrides.json",
        "word_to_receptive_count": len(to_receptive),
        "word_to_productive_count": len(to_productive),
        "word_to_support_count": len(to_support),
    }

    MERGED.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    semantic.DECISIONS_PATH = MERGED
    semantic.main()


if __name__ == "__main__":
    main()
