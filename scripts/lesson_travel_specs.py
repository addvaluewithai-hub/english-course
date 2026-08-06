"""Combined places, directions, and travel specifications."""

try:
    from scripts.lesson_travel_context_listening_specs import CONTEXT_LISTENING_SPECS
    from scripts.lesson_travel_listening_specs import LISTENING_SPECS
    from scripts.lesson_travel_reading_specs import READING_SPECS
    from scripts.lesson_travel_transaction_specs import TRANSACTION_SPECS
    from scripts.lesson_travel_wayfinding_specs import WAYFINDING_SPECS
    from scripts.lesson_travel_written_specs import WRITTEN_SPECS
except ModuleNotFoundError:
    from lesson_travel_context_listening_specs import CONTEXT_LISTENING_SPECS
    from lesson_travel_listening_specs import LISTENING_SPECS
    from lesson_travel_reading_specs import READING_SPECS
    from lesson_travel_transaction_specs import TRANSACTION_SPECS
    from lesson_travel_wayfinding_specs import WAYFINDING_SPECS
    from lesson_travel_written_specs import WRITTEN_SPECS


TRAVEL_SPECS = [
    *READING_SPECS,
    *LISTENING_SPECS,
    *CONTEXT_LISTENING_SPECS,
    *WAYFINDING_SPECS,
    *TRANSACTION_SPECS,
    *WRITTEN_SPECS,
]
