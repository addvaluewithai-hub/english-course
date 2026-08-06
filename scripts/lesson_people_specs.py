"""Combined people-and-relationships specifications in a provisional order."""

try:
    from scripts.lesson_people_exchange_specs import EXCHANGE_SPECS
    from scripts.lesson_people_reception_specs import RECEPTION_SPECS
    from scripts.lesson_people_spoken_specs import SPOKEN_SPECS
    from scripts.lesson_people_written_specs import WRITTEN_SPECS
except ModuleNotFoundError:
    from lesson_people_exchange_specs import EXCHANGE_SPECS
    from lesson_people_reception_specs import RECEPTION_SPECS
    from lesson_people_spoken_specs import SPOKEN_SPECS
    from lesson_people_written_specs import WRITTEN_SPECS


PEOPLE_SPECS = [
    *RECEPTION_SPECS,
    SPOKEN_SPECS[0],
    SPOKEN_SPECS[1],
    EXCHANGE_SPECS[0],
    SPOKEN_SPECS[2],
    *WRITTEN_SPECS,
    EXCHANGE_SPECS[1],
]
