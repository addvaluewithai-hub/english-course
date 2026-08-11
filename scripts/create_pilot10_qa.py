import json

from scripts.pilot10_qa_report import QA_JSON, QA_MD, build_qa, render


def main() -> None:
    qa = build_qa()
    QA_JSON.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    QA_MD.write_text(render(qa), encoding="utf-8")
    print(f"WROTE {QA_JSON} and {QA_MD}")


if __name__ == "__main__":
    main()
