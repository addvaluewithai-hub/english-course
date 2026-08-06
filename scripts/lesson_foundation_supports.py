"""Cross-cutting support definitions for the final evidence bands."""

from __future__ import annotations

from typing import Any

try:
    from scripts.lesson_candidate_factory import evidence_ref
except ModuleNotFoundError:
    from lesson_candidate_factory import evidence_ref


BASIC_ADDITIONS = [
    ("cefr.cv2020.p131.general_linguistic_range.02", "Basic one-clause structures support A1 performances without becoming a standalone lesson."),
    ("cefr.cv2020.p131.vocabulary_range.01", "Situation-bound basic vocabulary supports A1 performances without fixing lesson word lists."),
]
REPAIR_ADDITIONS = [
    ("gse.adult.2022.p22.005", "Asking for spelling or written form is interaction-management support."),
    ("gse.adult.2022.p24.002", "Asking for attention is a cross-cutting interaction-management move."),
    ("cefr.cv2020.p069.compensating.01", "Gesture-supported expression of a need is a communication-compensation option."),
    ("cefr.cv2020.p142.fluency.01", "Pausing, searching, articulating, and repair are permitted A1 communication behavior."),
]
RECEPTIVE_IDS = [
    "gse.adult.2022.p09.007", "gse.adult.2022.p09.011",
    "gse.adult.2022.p09.014", "gse.adult.2022.p14.002",
    "gse.adult.2022.p14.012", "gse.adult.2022.p15.001",
    "gse.adult.2022.p15.006", "gse.adult.2022.p15.012",
    "gse.adult.2022.p15.016", "cefr.cv2020.p048.overall_oral_comprehension.01",
    "cefr.cv2020.p054.overall_reading_comprehension.01",
    "cefr.cv2020.p057.reading_for_information_and_argument.01",
    "cefr.cv2020.p060.identifying_cues_and_inferring_spoken_signed_and.01",
    "cefr.cv2020.p060.identifying_cues_and_inferring_spoken_signed_and.02",
]
NUMBER_IDS = ["gse.adult.2022.p09.001", "gse.adult.2022.p14.013"]
SPOKEN_IDS = [
    "gse.adult.2022.p22.020", "gse.adult.2022.p22.024",
    "cefr.cv2020.p135.sound_articulation.01",
    "cefr.cv2020.p135.sound_articulation.02",
    "cefr.cv2020.p135.prosodic_features.01",
]
WRITTEN_IDS = [
    "gse.adult.2022.p37.003", "gse.adult.2022.p37.006",
    "gse.adult.2022.p37.009", "cefr.cv2020.p066.overall_written_production.02",
    "cefr.cv2020.p101.processing_text_in_writing.02",
    "cefr.cv2020.p136.orthographic_control.03",
    "cefr.cv2020.p141.coherence_and_cohesion.01",
]
NUMBER_CANDIDATES = {
    "lesson_candidate.locate_written_personal_details",
    "lesson_candidate.understand_spoken_contact_details",
    "lesson_candidate.complete_personal_details_form",
    "lesson_candidate.understand_a_simple_meeting_arrangement",
    "lesson_candidate.identify_spoken_time_and_date_details",
    "lesson_candidate.locate_place_and_time_in_slow_recordings",
    "lesson_candidate.identify_key_details_in_a_slow_station_announcement",
    "lesson_candidate.identify_a_price_in_slow_spoken_service_information",
    "lesson_candidate.relay_names_numbers_and_prices_from_slow_speech",
}


def add_foundation_supports(
    lesson_map: dict[str, Any], index: dict[str, tuple[str, dict[str, Any]]]
) -> None:
    basic, repair = lesson_map["support_definitions"][:2]
    _append_refs(basic, BASIC_ADDITIONS, index)
    _append_refs(repair, REPAIR_ADDITIONS, index)
    repair["title"] = "Interaction management, clarification, and repair"

    _add_filtered_support(
        lesson_map, index, "support.receptive_processing",
        "Slow, supported reception and meaning inference", RECEPTIVE_IDS,
        lambda candidate: bool({"reading", "listening"} & set(candidate["skill_codes"])),
        filter_relation_by_skill=True,
    )
    _add_filtered_support(
        lesson_map, index, "support.number_processing",
        "Recognition of common cardinal numbers", NUMBER_IDS,
        lambda candidate: candidate["candidate_id"] in NUMBER_CANDIDATES,
        filter_relation_by_skill=True,
    )
    _add_filtered_support(
        lesson_map, index, "support.spoken_intelligibility",
        "Guided sound, stress, rhythm, and intelligible delivery", SPOKEN_IDS,
        lambda candidate: "speaking" in candidate["skill_codes"],
    )
    _add_filtered_support(
        lesson_map, index, "support.written_form_control",
        "Basic written form, copying, punctuation, and connection", WRITTEN_IDS,
        lambda candidate: "writing" in candidate["skill_codes"],
    )


def _append_refs(
    support: dict[str, Any], additions: list[tuple[str, str]],
    index: dict[str, tuple[str, dict[str, Any]]],
) -> None:
    for record_id, note in additions:
        support["evidence_refs"].append(
            evidence_ref(index, record_id, "cross_cutting", "full", note)
        )


def _add_filtered_support(
    lesson_map: dict[str, Any], index: dict[str, tuple[str, dict[str, Any]]],
    support_id: str, title: str, record_ids: list[str], selector: Any,
    filter_relation_by_skill: bool = False,
) -> None:
    candidate_ids = []
    for candidate in lesson_map["candidates"]:
        if not selector(candidate):
            continue
        relation_ids = record_ids
        if filter_relation_by_skill:
            skills = set(candidate["skill_codes"])
            relation_ids = [
                record_id for record_id in record_ids
                if skills & set(index[record_id][1]["interpretation"]["skill_codes"])
            ]
        if not relation_ids:
            continue
        candidate_ids.append(candidate["candidate_id"])
        candidate["relationships"]["concurrent_support"].append({
            "support_id": support_id,
            "rationale": f"{title} accompanies this source-input or output channel.",
            "evidence_record_ids": relation_ids,
        })
    lesson_map["support_definitions"].append({
        "support_id": support_id,
        "title": title,
        "evidence_refs": [
            evidence_ref(
                index, record_id, "cross_cutting", "full",
                f"This source record defines {title.lower()} as reusable support.",
            )
            for record_id in record_ids
        ],
        "applies_to_candidate_ids": candidate_ids,
    })
