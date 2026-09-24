#!/usr/bin/env python3
"""Keep the Stage-07 handoff aligned with curriculum vs delivery authorization."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "curriculum/levels/a1/design-review/07-lesson-briefs/lesson-briefs.md"
OLD = (
    "Lesson/script production may now use this file as the **human instructional contract** "
    "and the coverage ledger as the **exact source-record contract**. Neither file alone is "
    "sufficient: the brief controls pedagogical purpose/boundaries; the ledger controls exact "
    "coverage and lifecycle traceability."
)
NEW = (
    "A1 curriculum lesson design and controlled authoring planning may now use this file as the "
    "**human instructional contract** and the coverage ledger as the **exact source-record "
    "contract**. Neither file alone is sufficient: the brief controls pedagogical "
    "purpose/boundaries; the ledger controls exact coverage and lifecycle traceability. This "
    "curriculum authorization does **not** authorize mass lesson-package, audio, image, or video "
    "production; those remain governed by the separate delivery workstream and `TEST-002`."
)


def main() -> None:
    text = PATH.read_text(encoding="utf-8")
    if NEW in text:
        print("Stage-07 handoff already current.")
        return
    if OLD not in text:
        raise SystemExit("Expected Stage-07 handoff paragraph not found; review manually")
    PATH.write_text(text.replace(OLD, NEW, 1), encoding="utf-8")
    print("Stage-07 handoff boundary updated.")


if __name__ == "__main__":
    main()
