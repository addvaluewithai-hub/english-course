"""Generate the final U1-L03 package from the accepted gold prototype."""

import json
from pathlib import Path

from scripts.gold_v1_contract import (
    FINAL_DECISIONS, GRAMMAR, LEGACY, LEXICAL, OUTPUT, PRONUNCIATION,
    QA_OUTPUT, QA_REPORT, SCOPE_SEQUENCE,
)
from scripts.gold_v1_package_builders import (
    activities, ai_contract, assessment, content, manifest, pronunciation_map,
)
from scripts.gold_v1_qa_report import build_qa, render
from scripts.gold_v1_source_packet import build as build_source_packet
from scripts.gold_v1_transcript import migrate_transcript


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_outputs() -> dict[str, str | dict]:
    scope, final, grammar, lexical, pronunciation = map(
        _load, (SCOPE_SEQUENCE, FINAL_DECISIONS, GRAMMAR, LEXICAL, PRONUNCIATION)
    )
    lesson = next(
        lesson for unit in scope["units"] for lesson in unit["lessons"]
        if lesson["final_owner_id"] == "lesson_candidate.give_short_self_introduction"
    )
    outputs: dict[str, str | dict] = {
        "lesson-manifest.json": manifest(_load(LEGACY / "lesson-manifest.json"), lesson),
        "source-packet.json": build_source_packet(scope, final, grammar, lexical, pronunciation),
        "content.json": content(_load(LEGACY / "content.json")),
        "activities.json": activities(_load(LEGACY / "activities.json")),
        "assessment.json": assessment(_load(LEGACY / "assessment.json")),
        "ai-contract.json": ai_contract(_load(LEGACY / "ai-contract.json")),
        "ASSET_BRIEFS.md": (LEGACY / "ASSET_BRIEFS.md").read_text(encoding="utf-8").replace(
            "each pronunciation contrast", "each pronunciation focus"
        ),
        "video/scene.txt": (LEGACY / "video" / "scene.txt").read_text(encoding="utf-8"),
        "video/sample-context.txt": (LEGACY / "video" / "sample-context.txt").read_text(encoding="utf-8"),
        "video/transcript.txt": migrate_transcript(
            (LEGACY / "video" / "transcript.txt").read_text(encoding="utf-8")
        ),
        "video/pronunciation-map.json": pronunciation_map(
            _load(LEGACY / "video" / "pronunciation-map.json")
        ),
    }
    readme = (LEGACY / "video" / "README.md").read_text(encoding="utf-8")
    readme = readme.replace("for lesson 1", "for final lesson U1-L03")
    live_rule = "- Reject a take if markup is spoken, `live` is pronounced `/laɪv/` in `I live in`, or English keeps an Arabic accent after code-switching."
    readme = readme.replace(live_rule, "- Reject a take if markup is spoken or English keeps an Arabic accent after code-switching.")
    outputs["video/README.md"] = readme
    return outputs


def main() -> int:
    outputs = build_outputs()
    for relative, value in outputs.items():
        path = OUTPUT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(value, dict):
            _write_json(path, value)
        else:
            path.write_text(value, encoding="utf-8")
    qa = build_qa()
    _write_json(QA_OUTPUT, qa)
    QA_REPORT.write_text(render(qa), encoding="utf-8")
    print(f"Wrote {OUTPUT} ({len(outputs)} package files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
