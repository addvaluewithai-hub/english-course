"""Controlled candidate clusters for the Phase 2 curriculum audit."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ClusterDefinition:
    cluster_id: str
    title: str
    role: str
    goal: str
    prior_unit: str | None
    prior_fit: str


CLUSTERS = (
    ClusterDefinition(
        "identity_personal_information", "Identity and personal information",
        "candidate_unit", "Exchange and record basic personal information.",
        "Identity", "natural",
    ),
    ClusterDefinition(
        "people_relationships", "People and relationships", "candidate_unit",
        "Talk about family, friends, known people, jobs, and possessions.",
        "People & Relationships", "natural",
    ),
    ClusterDefinition(
        "routines_time_leisure", "Routines, time, and leisure", "candidate_unit",
        "Understand and express routines, schedules, interests, abilities, and weather.",
        "Everyday Life", "natural",
    ),
    ClusterDefinition(
        "home_objects_descriptions", "Home, objects, and descriptions", "candidate_unit",
        "Locate and describe familiar homes, objects, pictures, and surroundings.",
        None, "overlap",
    ),
    ClusterDefinition(
        "places_directions_travel", "Places, directions, and travel", "candidate_unit",
        "Understand and manage basic locations, routes, transport, and travel details.",
        "Places & Movement", "natural",
    ),
    ClusterDefinition(
        "food_shopping_services", "Food, shopping, and services", "candidate_unit",
        "Handle immediate needs, prices, purchases, food, and basic services.",
        "Needs & Transactions", "natural",
    ),
    ClusterDefinition(
        "messages_signs_forms", "Messages, signs, and forms", "candidate_unit",
        "Understand or produce practical notices, messages, correspondence, and forms.",
        "Reading, Signs & Forms", "overlap",
    ),
    ClusterDefinition(
        "social_contact_collaboration", "Social contact and collaboration", "candidate_unit",
        "Use basic politeness, feelings, reactions, and collaborative exchanges.",
        "Simple Communication", "overlap",
    ),
    ClusterDefinition(
        "communication_strategies", "Communication strategies", "cross_cutting_support",
        "Repair, relay, translate, and facilitate meaning across candidate units.",
        "Simple Communication", "forced",
    ),
    ClusterDefinition(
        "language_foundations", "Language foundations", "cross_cutting_support",
        "Support intelligible comprehension and control across candidate units.",
        "Simple Communication", "forced",
    ),
)

CLUSTER_IDS = tuple(cluster.cluster_id for cluster in CLUSTERS)
CLUSTER_BY_ID = {cluster.cluster_id: cluster for cluster in CLUSTERS}


def ordered_cluster_ids(values: set[str]) -> list[str]:
    """Return unique cluster ids in the documented curriculum order."""
    unknown = values - set(CLUSTER_IDS)
    if unknown:
        raise ValueError(f"Unknown candidate clusters: {sorted(unknown)}")
    return [cluster_id for cluster_id in CLUSTER_IDS if cluster_id in values]
