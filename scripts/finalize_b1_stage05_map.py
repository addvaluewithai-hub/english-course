#!/usr/bin/env python3
"""Apply the explicit human B1 Stage-05 C18 writing correction.

The human decision is: C18 review/simple-essay writing must have an explicit
instructional slot rather than being hidden inside transfer. This finalizer is
idempotent and only applies that reviewed textual/map correction; it does not
infer curriculum structure.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "curriculum/levels/b1/design-review/05-curriculum-map/curriculum-map.md"


def once(text: str, old: str, new: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise ValueError(f"B1 Stage-05 expected text not found: {old[:100]!r}")
    return text.replace(old, new, 1)


def main() -> None:
    text = PATH.read_text(encoding="utf-8")

    text = once(text, "Baseline shape emerging from manual mapping: **12 units / 84 lesson slots**",
                "Baseline shape emerging from manual mapping: **12 units / 85 lesson slots**")
    text = once(text, "The **84-slot** baseline emerged", "The **85-slot** baseline emerged")
    text = once(text, "- **84 lesson slots total**", "- **85 lesson slots total**")
    text = once(text, "- **68 instructional / focused-retrieval slots**", "- **69 instructional / focused-retrieval slots**")

    text = once(text,
        "# Unit 10 — Explain and Present Familiar Topics\n**6 slots**",
        "# Unit 10 — Explain, Write, and Present Familiar Topics\n**7 slots**")

    old_block = """### U10-L03 — Take useful notes and plan a short presentation
Extract key points from a clear familiar source/talk, select what to include and create brief speaking notes rather than a full script.

### U10-L04 — Deliver a short presentation intelligibly
Use prominence, word stress, chunking and audience-facing organisation; accent imitation is not required.

### U10-L05 — Handle straightforward audience questions
Understand a factual follow-up, clarify/rephrase if needed and answer briefly without reading a prepared paragraph.

### U10-L06 — Fresh presentation + Q&A transfer
New familiar topic/source set: plan from notes → present → answer questions → repair one unclear point. **Zero planned new required content.**

**Unit critic:** presentation is not generic speaking; notes, audience structure, intelligibility and Q&A create a real evidence boundary."""

    new_block = """### U10-L03 — Write a short review or familiar-topic essay
Organise a straightforward connected written response with a clear viewpoint/main point, supporting reasons/examples, paragraphing and reference. This gives C18 review/simple-essay writing an explicit instructional home rather than hiding genre work inside transfer.

### U10-L04 — Take useful notes and plan a short presentation
Extract key points from a clear familiar source/talk, select what to include and create brief speaking notes rather than a full script.

### U10-L05 — Deliver a short presentation intelligibly
Use prominence, word stress, chunking and audience-facing organisation; accent imitation is not required.

### U10-L06 — Handle straightforward audience questions
Understand a factual follow-up, clarify/rephrase if needed and answer briefly without reading a prepared paragraph.

### U10-L07 — Fresh presentation + Q&A transfer
New familiar topic/source set: plan from notes → present → answer questions → repair one unclear point. **Zero planned new required content.**

**Unit critic:** C18 review/essay writing now has an explicit instructional home; presentation remains distinct from generic speaking, with notes, audience structure, intelligibility and Q&A as its evidence boundary."""
    text = once(text, old_block, new_block)

    text = once(text,
        "Narrative writing lives in U4, practical writing in U9, presentation notes in U10, correspondence/online interaction in U11, and reasoned/source-based writing can appear in U3/U6/U12.",
        "Narrative writing lives in U4, practical writing in U9, review/simple-essay writing and presentation notes live explicitly in U10, correspondence/online interaction in U11, and reasoned/source-based writing can also recur in U3/U6/U12.")

    text = once(text,
        "The **12-unit / 84-slot** shape is a consequence",
        "The **12-unit / 85-slot** shape is a consequence")
    text = once(text,
        "baseline curriculum map: **12 units / 84 lesson slots**;",
        "baseline curriculum map: **12 units / 85 lesson slots**;")

    PATH.write_text(text, encoding="utf-8")
    print("B1 Stage-05 map finalized at 12 units / 85 lessons with explicit C18 review/essay slot.")


if __name__ == "__main__":
    main()
