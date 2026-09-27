#!/usr/bin/env python3
"""Run B1 semantic expansion while preserving all source activity modes.

NON-SEMANTIC wrapper. It only broadens the mechanical source-mode parser to
recognise the explicit GSE `mediation` mode already handled by the human Stage-08
policy in semantic-decisions.json. It does not choose or infer semantic roles.
"""
from __future__ import annotations

import build_b1_semantic_role_ledger as ledger


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
    ledger.source_mode = source_mode_with_mediation
    ledger.main()


if __name__ == "__main__":
    main()
