"""Combined social-contact and collaboration specifications."""

try:
    from scripts.lesson_social_collaboration_specs import COLLABORATION_SPECS
    from scripts.lesson_social_interaction_specs import INTERACTION_SPECS
    from scripts.lesson_social_production_specs import PRODUCTION_SPECS
    from scripts.lesson_social_response_specs import RESPONSE_SPECS
except ModuleNotFoundError:
    from lesson_social_collaboration_specs import COLLABORATION_SPECS
    from lesson_social_interaction_specs import INTERACTION_SPECS
    from lesson_social_production_specs import PRODUCTION_SPECS
    from lesson_social_response_specs import RESPONSE_SPECS


SOCIAL_SPECS = [
    *INTERACTION_SPECS,
    *PRODUCTION_SPECS,
    *RESPONSE_SPECS,
    *COLLABORATION_SPECS,
]
