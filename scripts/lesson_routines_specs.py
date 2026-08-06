"""Combined routines, time, and leisure specifications in a working order."""

try:
    from scripts.lesson_routines_exchange_specs import EXCHANGE_SPECS
    from scripts.lesson_routines_reception_specs import RECEPTION_SPECS
    from scripts.lesson_routines_spoken_specs import SPOKEN_SPECS
    from scripts.lesson_routines_written_specs import WRITTEN_SPECS
except ModuleNotFoundError:
    from lesson_routines_exchange_specs import EXCHANGE_SPECS
    from lesson_routines_reception_specs import RECEPTION_SPECS
    from lesson_routines_spoken_specs import SPOKEN_SPECS
    from lesson_routines_written_specs import WRITTEN_SPECS


ROUTINES_SPECS = [
    *RECEPTION_SPECS,
    EXCHANGE_SPECS[0],
    SPOKEN_SPECS[0],
    SPOKEN_SPECS[1],
    EXCHANGE_SPECS[1],
    SPOKEN_SPECS[2],
    SPOKEN_SPECS[3],
    *WRITTEN_SPECS,
    EXCHANGE_SPECS[2],
]
