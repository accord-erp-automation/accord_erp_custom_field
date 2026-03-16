from accord_state_core.state.delivery_note_state import ensure_delivery_note_state_fields


def after_install():
    ensure_delivery_note_state_fields()

