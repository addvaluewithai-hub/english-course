"""Combined messages, signs, and forms specifications."""

try:
    from scripts.lesson_message_interaction_specs import INTERACTION_SPECS
    from scripts.lesson_message_mediation_specs import MEDIATION_SPECS
    from scripts.lesson_message_reception_specs import RECEPTION_SPECS
except ModuleNotFoundError:
    from lesson_message_interaction_specs import INTERACTION_SPECS
    from lesson_message_mediation_specs import MEDIATION_SPECS
    from lesson_message_reception_specs import RECEPTION_SPECS


MESSAGE_SPECS = [
    *RECEPTION_SPECS,
    *INTERACTION_SPECS,
    *MEDIATION_SPECS,
]
