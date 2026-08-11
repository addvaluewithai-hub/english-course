import json

from scripts.pilot10_qa_report import QA_JSON, QA_MD, build_qa, render


def main() -> None:
    actual = json.loads(QA_JSON.read_text(encoding="utf-8"))
    expected = build_qa()
    errors = []
    if actual != expected:
        errors.append("QA JSON is stale")
    if QA_MD.read_text(encoding="utf-8") != render(expected):
        errors.append("QA report is stale")
    if expected["findings"]["validation_errors"]:
        errors.extend(expected["findings"]["validation_errors"])
    if errors:
        raise SystemExit("FAIL first-ten QA\n- " + "\n- ".join(errors))
    print("PASS first-ten content QA for continuous prototype")


if __name__ == "__main__":
    main()
