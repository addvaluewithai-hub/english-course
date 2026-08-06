"""Combined food, shopping, and services specifications."""

try:
    from scripts.lesson_service_message_specs import MESSAGE_SPECS
    from scripts.lesson_service_reception_specs import RECEPTION_SPECS
    from scripts.lesson_service_request_specs import REQUEST_SPECS
    from scripts.lesson_service_transaction_specs import TRANSACTION_SPECS
except ModuleNotFoundError:
    from lesson_service_message_specs import MESSAGE_SPECS
    from lesson_service_reception_specs import RECEPTION_SPECS
    from lesson_service_request_specs import REQUEST_SPECS
    from lesson_service_transaction_specs import TRANSACTION_SPECS


SERVICE_SPECS = [
    *RECEPTION_SPECS,
    *REQUEST_SPECS,
    *TRANSACTION_SPECS,
    *MESSAGE_SPECS,
]
