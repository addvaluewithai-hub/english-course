"""Human-readable intent and role for each controlled function code."""


INTENTS = {
    "comprehend_information": "Understand stated meaning and factual content.",
    "follow_instructions": "Understand and act on directions, commands, or instructions.",
    "locate_information": "Find or extract a required detail from input.",
    "interpret_attitude_or_implication": "Interpret stance, intention, tone, or implied meaning.",
    "describe": "Describe people, objects, places, routines, experiences, or situations.",
    "narrate": "Recount events as an intelligible sequence with relevant detail.",
    "give_information": "State or present information without a required exchange.",
    "ask_for_information": "Request a specific fact, confirmation, or explanation.",
    "exchange_information": "Ask, answer, check, and reciprocally share information.",
    "introduce": "Introduce oneself, another person, or a topic appropriately.",
    "socialize": "Establish and maintain social contact with suitable politeness.",
    "express_preference": "Express and compare likes, dislikes, and preferences.",
    "express_feeling": "Express and respond to feelings and emotional reactions.",
    "express_ability": "State and qualify ability, possibility, or lack of ability.",
    "express_opinion": "State and develop a personal view or position.",
    "request": "Ask for an action, item, help, attention, or service.",
    "respond_to_request_or_offer": "Accept, decline, or otherwise respond to requests and offers.",
    "offer_or_invite": "Make offers and invitations with appropriate detail and register.",
    "transact": "Obtain goods or services and complete practical transactions.",
    "correspond": "Exchange written or online messages for a communicative purpose.",
    "complete_form": "Supply accurate information in paper or online forms.",
    "clarify_or_repair": "Signal difficulty, clarify, reformulate, and repair communication.",
    "infer_meaning": "Infer unfamiliar meaning using linguistic or contextual cues.",
    "explain": "Make reasons, processes, relationships, or complex information clear.",
    "justify_or_argue": "Support, defend, or challenge a position with reasons and evidence.",
    "compare": "Identify and communicate relevant similarities and differences.",
    "evaluate": "Judge options, evidence, or sources against relevant criteria.",
    "summarize": "Condense input while preserving its main points and relationships.",
    "synthesize": "Integrate information or arguments from multiple sources into a coherent whole.",
    "speculate_or_hypothesize": "Express degrees of possibility, prediction, and hypothesis.",
    "advise_or_recommend": "Give or seek advice and recommend a course of action.",
    "negotiate_or_resolve": "Negotiate conditions, seek compromise, and resolve disagreement.",
    "present_or_address_audience": "Plan and deliver communication for an audience.",
    "report_or_review": "Produce an appropriate report, review, or factual account.",
    "analyze_or_criticize": "Analyse evidence or a text and produce reasoned criticism.",
    "mediate_information": "Relay, process, or reshape information for another person.",
    "translate": "Translate meaning appropriately across languages at the required precision.",
    "facilitate_interaction": "Enable others to contribute and help a group construct meaning.",
    "reproduce_language": "Copy, spell, repeat, or read supplied language accurately enough.",
    "control_language_form": "Control grammar, lexis, sound, spelling, and form in communication.",
    "manage_discourse": "Organise, connect, signal, and develop discourse for the audience.",
}

RECEPTIVE = {
    "comprehend_information", "follow_instructions", "locate_information",
    "interpret_attitude_or_implication", "infer_meaning",
}
MEDIATION = {"mediate_information", "translate", "facilitate_interaction"}
SUPPORT = {"clarify_or_repair", "reproduce_language"}
LANGUAGE_SYSTEM = {"control_language_form"}


def strand_role(function_code: str) -> str:
    if function_code in RECEPTIVE:
        return "receptive"
    if function_code in MEDIATION:
        return "mediation"
    if function_code in SUPPORT:
        return "support_strategy"
    if function_code in LANGUAGE_SYSTEM:
        return "language_system_support"
    return "communicative"


def title(function_code: str) -> str:
    return function_code.replace("_", " ").title()
