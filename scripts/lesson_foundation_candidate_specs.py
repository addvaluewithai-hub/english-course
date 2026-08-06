"""Assessable candidates from the foundation and strategy evidence bands."""

try:
    from scripts.lesson_foundation_spec_helpers import evidence, foundation_spec
    from scripts.lesson_identity_spec_helpers import BASIC_RECEPTIVE, BASIC_WRITTEN
except ModuleNotFoundError:
    from lesson_foundation_spec_helpers import evidence, foundation_spec
    from lesson_identity_spec_helpers import BASIC_RECEPTIVE, BASIC_WRITTEN


FOUNDATION_CANDIDATE_SPECS = [
    foundation_spec(
        candidate_id="lesson_candidate.follow_short_written_everyday_instructions",
        clusters=["language_foundations"],
        situation="a simple familiar making or everyday task",
        action="follow a short written instruction sequence",
        content="two or three basic steps in the correct order",
        success="the stated task is completed without skipping or reversing a step",
        statement="In a fresh familiar task, the learner can follow two or three short written instructions in order.",
        evidence_items=[
            evidence(
                "gse.adult.2022.p09.008", "anchor",
                "The objective anchors basic written instructions for making something simple.",
            ),
            evidence(
                "gse.adult.2022.p09.013", "supporting",
                "The objective broadens the same bounded performance to a straightforward task.",
            ),
        ],
        skill_codes=["reading"], mode_codes=["reception"],
        function_codes=["follow_instructions"],
        rationale="Both objectives require acting on a short written sequence; one fresh task can assess them together.",
        fresh_task="A different familiar task with two or three reordered basic instructions.",
        level_2={
            "comprehension": "Identifies each required action and its order.",
            "outcome_performance": "Completes every required step in the stated order.",
            "interaction_or_transfer": "Acts on changed instructions rather than recalling the practice sequence.",
        },
        critical_failure="A required step is skipped, reversed, or replaced with a different action.",
        permitted_support=["A simple picture of materials that does not reveal the action order."],
        delayed_probe="Use a different familiar task and changed step order after a delay.",
        scope_rationale="One familiar purpose and two or three short written steps.",
        risks=["Provide an accessible non-physical response route without revealing the sequence."],
        basic_support_ids=BASIC_RECEPTIVE,
    ),
    foundation_spec(
        candidate_id="lesson_candidate.understand_outline_of_an_illustrated_short_story",
        clusters=["language_foundations"],
        situation="a short illustrated story on a familiar everyday theme",
        action="identify its outline",
        content="the main situation and the basic event sequence",
        success="the selected outline matches the text and image-supported sequence",
        statement="From a fresh short illustrated story, the learner can identify the main situation and basic event sequence.",
        evidence_items=[evidence(
            "cefr.cv2020.p059.reading_as_a_leisure_activity.02", "anchor",
            "The descriptor directly anchors outline understanding when images support the content.",
        )],
        skill_codes=["reading"], mode_codes=["reception"],
        function_codes=["comprehend_information"],
        rationale="One illustrated story and one outline judgment form a bounded leisure-reading performance.",
        fresh_task="A different short illustrated story with a changed familiar situation and sequence.",
        level_2={
            "comprehension": "Connects the short text and images to the main situation.",
            "outcome_performance": "Selects or orders the outline that matches the basic events.",
            "interaction_or_transfer": "Succeeds with a different story and image sequence.",
        },
        critical_failure="The chosen outline changes the main situation or reverses the basic sequence.",
        permitted_support=["Images supplied with the story and rereading of the same short text."],
        delayed_probe="Use a different illustrated story on a familiar theme after a delay.",
        scope_rationale="One very short story, strong image support, and a basic outline.",
        risks=["Images may support inference but must not make the text irrelevant."],
        basic_support_ids=BASIC_RECEPTIVE,
    ),
    foundation_spec(
        candidate_id="lesson_candidate.translate_simple_written_phrases_with_a_dictionary",
        clusters=["communication_strategies"],
        situation="a familiar everyday written item in declared Language A",
        action="write the meaning in declared Language B",
        content="one or two simple words or phrases",
        success="the practical meaning is conveyed without a material reversal",
        statement="Using a dictionary, the learner can write the practical meaning of one or two fresh everyday phrases in Language B.",
        evidence_items=[
            evidence(
                "cefr.cv2020.p101.processing_text_in_writing.01", "supporting",
                "The descriptor anchors conveying familiar everyday phrase meaning in writing with dictionary help.",
            ),
            evidence(
                "cefr.cv2020.p104.translating_a_written_text_in_writing.01", "anchor",
                "The descriptor directly anchors dictionary-assisted written translation of simple words and phrases.",
            ),
        ],
        skill_codes=["reading", "writing"], mode_codes=["mediation"],
        function_codes=["mediate_information", "translate"],
        rationale="Both descriptors support one dictionary-assisted written transfer of short everyday meaning.",
        fresh_task="A changed everyday item with one or two different simple phrases and a declared language pair.",
        level_2={
            "comprehension": "Identifies the relevant everyday meaning in Language A.",
            "outcome_performance": "Writes a usable Language B rendering without reversing the practical meaning.",
            "interaction_or_transfer": "Handles changed phrases rather than reproducing the practice set.",
            "control_or_repair": "Uses the dictionary to check an isolated item and flags uncertainty when meanings compete.",
        },
        critical_failure="The written rendering reverses or obscures the practical everyday meaning.",
        permitted_support=["A bilingual dictionary that does not provide the full phrase translation."],
        delayed_probe="Use different simple phrases, a changed written item, and the same declared language pair.",
        scope_rationale="One or two short phrases and one dictionary-assisted written rendering.",
        risks=["Declare both languages and do not claim professional or exact translation accuracy."],
        basic_support_ids=BASIC_WRITTEN,
    ),
]
