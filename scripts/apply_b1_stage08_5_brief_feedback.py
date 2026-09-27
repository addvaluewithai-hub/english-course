#!/usr/bin/env python3
"""Apply exact human Stage-08.5 feedback to the authoritative B1 Stage-07 briefs.

NON-DECISIONAL. Every replacement below is an explicit human critic decision already
recorded in the Stage-08.5 override/re-audit artifacts. The script only makes those
specific prose/count reconciliations and fails on unexpected drift.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIEFS = ROOT / "curriculum/levels/b1/design-review/07-lesson-briefs/lesson-briefs.md"

REPLACEMENTS = [
    (
        "Status: **STAGE 07 COMPLETE — 85 / 85 MANUAL AUTHORING-CONTRACT CANDIDATES + 12 ROLLING UNIT CRITICS + WHOLE-LEVEL CRITIC**",
        "Status: **STAGE 07 COMPLETE; STAGE 08.5 FEEDBACK RECONCILED — 85 / 85 MANUAL AUTHORING-CONTRACT CANDIDATES + 12 ROLLING UNIT CRITICS + WHOLE-LEVEL CRITIC**",
    ),
    (
        "These briefs are **authoring-contract candidates, not finished lessons**. Stage 08 must still reconcile every exact item into a formal semantic/control role. Therefore `Foreground candidate` and `Embedded/support candidate` below are design hypotheses grounded in the learner performance and exact Stage-06 placement; they are not yet mastery declarations.",
        "These briefs are **authoring-contract candidates, not finished lessons**. Stage 08 + Stage 08.5 now supply the authoritative exact semantic/control-role boundary. The original `Foreground candidate` and `Embedded/support candidate` labels remain useful design descriptions, but they may not promote any item beyond its locked role; exact Stage-08.5 feedback below supersedes an earlier candidate hypothesis where the critic found a contradiction.",
    ),
    (
        "4. Foreground only what the performance genuinely needs; Stage 08 may downgrade candidates to receptive/support or identify formulaic control.",
        "4. Foreground only what the performance genuinely needs; the Stage-08/8.5 semantic ledger is authoritative, so receptive/support/formulaic items may not be silently promoted by authoring prose.",
    ),
    (
        "9. The 15 Stage-06 raw-load warnings remain pinned. `U10-L02` is explicitly conditional and must be revisited in Stage 08.5.",
        "9. The 15 Stage-06 raw-load warnings remain pinned as diagnostics. Stage 08.5 has now re-audited them role-aware; `U10-L02` is retained without a split after active-load reconciliation.",
    ),
    (
        "10. If Stage 08/8.5 evidence contradicts a brief, reopen the brief/ledger rather than silently promoting support content.",
        "10. If later evidence contradicts the Stage-08/8.5 lock, reopen the brief/ledger explicitly rather than silently promoting support content.",
    ),
    (
        "- **Exact introductions:** abilities **1** · phrases **2** · grammar **0** · words **22** · pronunciation **0** · total **25**.",
        "- **Exact introductions:** abilities **1** · phrases **1** · grammar **0** · words **22** · pronunciation **0** · total **24**.",
    ),
    (
        "- **Exact introductions:** abilities **2** · phrases **1** · grammar **0** · words **19** · pronunciation **0** · total **22**.",
        "- **Exact introductions:** abilities **2** · phrases **2** · grammar **0** · words **19** · pronunciation **0** · total **23**.",
    ),
    (
        "- **Decision:** retain all 7 slots; no Stage-06 reopening required.",
        "- **Stage-08.5 feedback:** the exact ledger was reopened only to swap medication-instruction reception into U9-L05, symptom production into U9-L06, and move `wrong with sb/sth` with symptom communication; lifecycle and zero-new invariants remained intact.\n- **Decision:** retain all 7 slots; no split/merge required after the exact feedback re-audit.",
    ),
    (
        "- **Boundary:** **highest conditional Stage-06 warning: 56 raw rows**. Stage 08 must assign roles conservatively; Stage 08.5 must split/reopen if active teaching-object load is not coherent.",
        "- **Boundary:** the raw Stage-06 count remains **56 source rows**, but Stage 08.5 resolves these to approximately **16 active teaching objects** (C10 + G07/G12 + 8 formulaic phrases + 5 active words); the remaining rows are receptive/support context, so no split is required.",
    ),
    (
        "- U10-L02 is **conditionally retained** only until Stage-08.5 role-aware load review.",
        "- U10-L02 **passes the Stage-08.5 role-aware load review** at approximately 16 active teaching objects and is retained without a split.",
    ),
]


def main() -> None:
    text = BRIEFS.read_text(encoding="utf-8")
    changed = False
    for old, new in REPLACEMENTS:
        if new in text:
            continue
        count = text.count(old)
        if count != 1:
            raise ValueError(f"B1 brief feedback expected one exact old marker, found {count}: {old[:120]!r}")
        text = text.replace(old, new, 1)
        changed = True
    if changed:
        BRIEFS.write_text(text, encoding="utf-8")
    print(f"B1 STAGE-08.5 BRIEF FEEDBACK {'APPLIED' if changed else 'ALREADY RECONCILED'}")


if __name__ == "__main__":
    main()
