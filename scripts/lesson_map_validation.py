"""Compose schema and semantic validation for the A1 lesson map."""

from __future__ import annotations

from pathlib import Path

try:
    from scripts.lesson_map_evidence import evidence_errors
    from scripts.lesson_map_io import SOURCE_PATHS, load, schema_errors, source_index
    from scripts.lesson_map_relationships import relationship_errors
except ModuleNotFoundError:
    from lesson_map_evidence import evidence_errors
    from lesson_map_io import SOURCE_PATHS, load, schema_errors, source_index
    from lesson_map_relationships import relationship_errors


def validation_errors(
    path: Path, source_paths: tuple[Path, ...] = SOURCE_PATHS
) -> list[str]:
    lesson_map = load(path)
    errors = schema_errors(lesson_map)
    if errors:
        return errors
    collections = [load(source_path) for source_path in source_paths]
    index, index_errors = source_index(collections)
    errors.extend(index_errors)
    errors.extend(evidence_errors(lesson_map, index))
    included_ids = {
        record_id for record_id, (_, record) in index.items()
        if record["interpretation"]["inclusion_status"] == "included"
    }
    errors.extend(relationship_errors(lesson_map, included_ids))
    return errors
