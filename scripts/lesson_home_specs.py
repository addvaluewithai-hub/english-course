"""Combined home, objects, and descriptions specifications."""

try:
    from scripts.lesson_home_exchange_specs import EXCHANGE_SPECS
    from scripts.lesson_home_reception_specs import RECEPTION_SPECS
    from scripts.lesson_home_spoken_specs import SPOKEN_SPECS
    from scripts.lesson_home_written_specs import WRITTEN_SPECS
except ModuleNotFoundError:
    from lesson_home_exchange_specs import EXCHANGE_SPECS
    from lesson_home_reception_specs import RECEPTION_SPECS
    from lesson_home_spoken_specs import SPOKEN_SPECS
    from lesson_home_written_specs import WRITTEN_SPECS


HOME_SPECS = [
    *RECEPTION_SPECS,
    SPOKEN_SPECS[0],
    EXCHANGE_SPECS[0],
    SPOKEN_SPECS[1],
    EXCHANGE_SPECS[1],
    *WRITTEN_SPECS,
]
