from accord_erp_custom_field.state.delivery_note_state import (
    ensure_delivery_note_state_fields,
)
from accord_erp_custom_field.state.delivery_note_state import (
    sync_delivery_note_ui_status,
)


def after_install():
    ensure_delivery_note_state_fields()
    sync_delivery_note_ui_status()


def after_migrate():
    ensure_delivery_note_state_fields()
    sync_delivery_note_ui_status()
