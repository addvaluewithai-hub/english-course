"""Reviewed CEFR table inventory for the CUR-003 A1 extraction scope."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TableSpec:
    page: int
    anchor: int
    mode: str
    skill: str
    scales: tuple[str, ...]
    expected_counts: tuple[int, ...]
    rotated: bool = False


def _s(
    page: int,
    mode: str,
    skill: str,
    scale: str,
    count: int,
    anchor: int = 0,
) -> TableSpec:
    return TableSpec(page, anchor, mode, skill, (scale,), (count,))


TABLE_SPECS = (
    _s(48, "Reception", "Oral comprehension", "Overall oral comprehension", 2),
    _s(49, "Reception", "Oral comprehension", "Understanding conversation between other people", 2),
    _s(51, "Reception", "Oral comprehension", "Understanding as a member of a live audience", 1),
    _s(51, "Reception", "Oral comprehension", "Understanding announcements and instructions", 3, 1),
    _s(52, "Reception", "Oral comprehension", "Understanding audio (or signed) media and recordings", 1),
    _s(53, "Reception", "Audio-visual comprehension", "Watching TV, film and video", 1),
    _s(54, "Reception", "Reading comprehension", "Overall reading comprehension", 1),
    _s(55, "Reception", "Reading comprehension", "Reading correspondence", 2),
    _s(56, "Reception", "Reading comprehension", "Reading for orientation", 4),
    _s(57, "Reception", "Reading comprehension", "Reading for information and argument", 2),
    _s(58, "Reception", "Reading comprehension", "Reading instructions", 1),
    _s(59, "Reception", "Reading comprehension", "Reading as a leisure activity", 2),
    _s(60, "Reception", "Reception strategies", "Identifying cues and inferring (spoken, signed and written)", 2),
    _s(62, "Production", "Oral production", "Overall oral production", 1),
    _s(63, "Production", "Oral production", "Sustained monologue: describing experience", 2),
    _s(63, "Production", "Oral production", "Sustained monologue: giving information", 1, 1),
    _s(64, "Production", "Oral production", "Sustained monologue: putting a case (e.g. in a debate)", 0),
    _s(65, "Production", "Oral production", "Public announcements", 0),
    _s(66, "Production", "Oral production", "Addressing audiences", 1),
    _s(66, "Production", "Written production", "Overall written production", 2, 1),
    _s(67, "Production", "Written production", "Creative writing", 3),
    _s(68, "Production", "Written production", "Reports and essays", 0),
    _s(69, "Production", "Production strategies", "Planning", 0),
    _s(69, "Production", "Production strategies", "Compensating", 1, 1),
    _s(70, "Production", "Production strategies", "Monitoring and repair", 0),
    _s(72, "Interaction", "Oral interaction", "Overall oral interaction", 1),
    _s(73, "Interaction", "Oral interaction", "Understanding an interlocutor", 2),
    _s(74, "Interaction", "Oral interaction", "Conversation", 4),
    _s(75, "Interaction", "Oral interaction", "Informal discussion (with friends)", 1),
    _s(76, "Interaction", "Oral interaction", "Formal discussion (meetings)", 0),
    _s(77, "Interaction", "Oral interaction", "Goal-oriented co-operation", 3),
    _s(78, "Interaction", "Oral interaction", "Obtaining goods and services", 3),
    _s(79, "Interaction", "Oral interaction", "Information exchange", 6),
    _s(80, "Interaction", "Oral interaction", "Interviewing and being interviewed", 2),
    _s(81, "Interaction", "Oral interaction", "Using telecommunications", 0),
    _s(82, "Interaction", "Written interaction", "Overall written interaction", 1),
    _s(83, "Interaction", "Written interaction", "Correspondence", 3),
    _s(84, "Interaction", "Written interaction", "Notes, messages and forms", 2),
    _s(86, "Online interaction", "Online interaction", "Online conversation and discussion", 2),
    _s(87, "Online interaction", "Online interaction", "Goal-oriented online transactions and collaboration", 1),
    _s(88, "Interaction", "Interaction strategies", "Turntaking", 0),
    _s(89, "Interaction", "Interaction strategies", "Co-operating", 0),
    _s(89, "Interaction", "Interaction strategies", "Asking for clarification", 2, 1),
    _s(92, "Mediation", "Overall mediation", "Overall mediation", 1),
    TableSpec(95, 0, "Mediation", "Mediating a text", ("Relaying specific information in speech or sign", "Relaying specific information in writing"), (1, 1), True),
    TableSpec(97, 0, "Mediation", "Mediating a text", ("Explaining data in speech or sign", "Explaining data in writing"), (0, 0), True),
    TableSpec(101, 0, "Mediation", "Mediating a text", ("Processing text in speech or sign", "Processing text in writing"), (1, 2), True),
    TableSpec(104, 0, "Mediation", "Mediating a text", ("Translating a written text in speech or sign", "Translating a written text in writing"), (1, 1), True),
    _s(105, "Mediation", "Mediating a text", "Note-taking (lectures, seminars, meetings, etc.)", 0),
    _s(107, "Mediation", "Mediating a text", "Expressing a personal response to creative texts (including literature)", 1),
    _s(108, "Mediation", "Mediating a text", "Analysis and criticism of creative texts (including literature)", 0),
    TableSpec(111, 0, "Mediation", "Mediating concepts", ("Facilitating collaborative interaction with peers", "Collaborating to construct meaning"), (1, 1), True),
    TableSpec(113, 0, "Mediation", "Mediating concepts", ("Managing interaction", "Encouraging conceptual talk"), (0, 1), True),
    _s(115, "Mediation", "Mediating communication", "Facilitating pluricultural space", 1),
    _s(116, "Mediation", "Mediating communication", "Acting as an intermediary in informal situations (with friends and colleagues)", 1),
    _s(117, "Mediation", "Mediating communication", "Facilitating communication in delicate situations and disagreements", 1),
    TableSpec(120, 0, "Mediation", "Mediation strategies", ("Linking to previous knowledge", "Adapting language", "Breaking down complicated information"), (0, 0, 0), True),
    TableSpec(122, 0, "Mediation", "Mediation strategies", ("Amplifying a dense text", "Streamlining a text"), (0, 0), True),
    _s(131, "Communicative language competences", "Linguistic competence", "General linguistic range", 2),
    _s(131, "Communicative language competences", "Linguistic competence", "Vocabulary range", 1, 1),
    _s(132, "Communicative language competences", "Linguistic competence", "Grammatical accuracy", 1),
    _s(133, "Communicative language competences", "Linguistic competence", "Vocabulary control", 0),
    TableSpec(135, 0, "Communicative language competences", "Linguistic competence", ("Overall phonological control", "Sound articulation", "Prosodic features"), (1, 2, 1), True),
    _s(136, "Communicative language competences", "Linguistic competence", "Orthographic control", 3),
    _s(137, "Communicative language competences", "Sociolinguistic competence", "Sociolinguistic appropriateness", 1),
    _s(138, "Communicative language competences", "Pragmatic competence", "Flexibility", 0),
    _s(139, "Communicative language competences", "Pragmatic competence", "Turntaking", 0),
    _s(140, "Communicative language competences", "Pragmatic competence", "Thematic development", 0),
    _s(141, "Communicative language competences", "Pragmatic competence", "Coherence and cohesion", 1),
    _s(142, "Communicative language competences", "Pragmatic competence", "Propositional precision", 1),
    _s(142, "Communicative language competences", "Pragmatic competence", "Fluency", 1, 1),
)
