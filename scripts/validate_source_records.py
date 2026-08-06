"""Validate curriculum source-record datasets without changing them."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = PROJECT_ROOT / "schemas" / "curriculum"
SCHEMA_FILES = (
    "source-evidence.schema.json",
    "source-record.schema.json",
    "source-record-collection.schema.json",
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def build_validator() -> Draft202012Validator:
    schemas = [_load_json(SCHEMA_DIR / name) for name in SCHEMA_FILES]
    registry = Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in schemas
    )
    for schema in schemas:
        Draft202012Validator.check_schema(schema)
    return Draft202012Validator(
        schemas[-1], registry=registry, format_checker=FormatChecker()
    )


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _semantic_errors(
    data: dict[str, Any], dataset_path: Path, project_root: Path
) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    file_hashes: dict[Path, str] = {}
    reviewed_dir = (project_root / "data" / "reviewed").resolve()

    for index, record in enumerate(data.get("records", [])):
        prefix = f"records[{index}]"
        record_id = record.get("record_id")
        if record_id in seen:
            errors.append(f"{prefix}.record_id: duplicate {record_id!r}")
        seen.add(record_id)

        source = record.get("source", {})
        raw_rel = source.get("raw_file", "")
        raw_path = (project_root / raw_rel).resolve()
        try:
            raw_path.relative_to((project_root / "sources" / "raw").resolve())
        except ValueError:
            errors.append(f"{prefix}.source.raw_file: escapes sources/raw")
        else:
            if not raw_path.is_file():
                errors.append(f"{prefix}.source.raw_file: file does not exist")
            else:
                file_hashes.setdefault(raw_path, _sha256_file(raw_path))
                expected = str(source.get("source_file_sha256", "")).lower()
                if file_hashes[raw_path].lower() != expected:
                    errors.append(f"{prefix}.source_file_sha256: hash mismatch")

        text = source.get("source_text", "")
        if not text.strip():
            errors.append(f"{prefix}.source.source_text: text is blank")
        text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if text_hash.lower() != str(source.get("source_text_sha256", "")).lower():
            errors.append(f"{prefix}.source_text_sha256: hash mismatch")

        location = source.get("location", {})
        kind = location.get("kind")
        if kind == "pdf_page":
            if not raw_rel.lower().endswith(".pdf"):
                errors.append(f"{prefix}.source.location: PDF locator needs a PDF")
            if location.get("page_end", 0) < location.get("page", 0):
                errors.append(f"{prefix}.source.location: page range is reversed")
        elif kind == "spreadsheet_row":
            if Path(raw_rel).suffix.lower() not in {".xlsx", ".xls", ".csv", ".tsv"}:
                errors.append(f"{prefix}.source.location: row locator needs tabular data")
            if location.get("row_end", 0) < location.get("row", 0):
                errors.append(f"{prefix}.source.location: row range is reversed")

        interpretation = record.get("interpretation", {})
        inclusion = interpretation.get("inclusion_status")
        reason = interpretation.get("exclusion_reason")
        if inclusion == "excluded" and not reason:
            errors.append(f"{prefix}.interpretation: exclusion needs a reason")
        if inclusion != "excluded" and reason is not None:
            errors.append(f"{prefix}.interpretation: reason is only for exclusions")

        review = record.get("review", {})
        status = review.get("status")
        reviewer = review.get("reviewer")
        reviewed_at = review.get("reviewed_at")
        if status in {"accepted", "rejected"} and (not reviewer or not reviewed_at):
            errors.append(f"{prefix}.review: final state needs reviewer and time")
        if status in {"unreviewed", "needs_review"} and (reviewer or reviewed_at):
            errors.append(f"{prefix}.review: pending state cannot claim completed review")
        issues = review.get("issues", [])
        error_issues = [issue for issue in issues if issue.get("severity") == "error"]
        if status == "accepted" and error_issues:
            errors.append(f"{prefix}.review: accepted record has an error issue")
        if status == "rejected" and not error_issues:
            errors.append(f"{prefix}.review: rejected record needs an error issue")
        if dataset_path.resolve().is_relative_to(reviewed_dir) and status != "accepted":
            errors.append(f"{prefix}.review: reviewed datasets require accepted records")
    return errors


def validate_dataset(path: Path, project_root: Path = PROJECT_ROOT) -> list[str]:
    data = _load_json(path)
    validator = build_validator()
    schema_errors = [
        f"{'.'.join(str(part) for part in error.absolute_path) or '$'}: {error.message}"
        for error in sorted(validator.iter_errors(data), key=lambda item: list(item.path))
    ]
    if schema_errors:
        return schema_errors
    return _semantic_errors(data, path, project_root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--check-schemas", action="store_true")
    args = parser.parse_args()
    if args.check_schemas:
        build_validator()
        print(f"Validated {len(SCHEMA_FILES)} schemas.")
    if not args.paths and not args.check_schemas:
        parser.error("provide a dataset path or --check-schemas")

    failed = False
    for path in args.paths:
        errors = validate_dataset(path)
        if errors:
            failed = True
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {path}")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
