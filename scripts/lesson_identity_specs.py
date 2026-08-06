"""Combined identity candidate specifications in a provisional working order."""

try:
    from scripts.lesson_identity_exchange_specs import EXCHANGE_SPECS
    from scripts.lesson_identity_output_specs import OUTPUT_SPECS
    from scripts.lesson_identity_reception_specs import RECEPTION_SPECS
except ModuleNotFoundError:
    from lesson_identity_exchange_specs import EXCHANGE_SPECS
    from lesson_identity_output_specs import OUTPUT_SPECS
    from lesson_identity_reception_specs import RECEPTION_SPECS


IDENTITY_SPECS = [
    *RECEPTION_SPECS,
    OUTPUT_SPECS[0],
    EXCHANGE_SPECS[0],
    OUTPUT_SPECS[1],
    OUTPUT_SPECS[2],
    EXCHANGE_SPECS[1],
    EXCHANGE_SPECS[2],
]
