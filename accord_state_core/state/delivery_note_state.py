import frappe

DELIVERY_FLOW_STATE_SUBMITTED = 1
CUSTOMER_STATE_PENDING = 1
CUSTOMER_STATE_CONFIRMED = 3
CUSTOMER_STATE_REJECTED = 2


FIELD_SPECS = (
    {
        "fieldname": "accord_flow_state",
        "label": "Accord Flow State",
        "fieldtype": "Int",
        "insert_after": "remarks",
        "hidden": 1,
    },
    {
        "fieldname": "accord_customer_state",
        "label": "Accord Customer State",
        "fieldtype": "Int",
        "insert_after": "accord_flow_state",
        "hidden": 1,
    },
    {
        "fieldname": "accord_customer_reason",
        "label": "Accord Customer Reason",
        "fieldtype": "Small Text",
        "insert_after": "accord_customer_state",
        "hidden": 1,
    },
    {
        "fieldname": "accord_delivery_actor",
        "label": "Accord Delivery Actor",
        "fieldtype": "Data",
        "insert_after": "accord_customer_reason",
        "hidden": 1,
    },
    {
        "fieldname": "accord_status_section",
        "label": "Accord Status",
        "fieldtype": "Section Break",
        "insert_after": "posting_time",
        "hidden": 0,
    },
    {
        "fieldname": "accord_ui_status",
        "label": "Accord UI Status",
        "fieldtype": "Select",
        "insert_after": "accord_status_section",
        "options": "pending\nconfirm\nrejected",
        "hidden": 0,
    },
)


def ensure_delivery_note_state_fields():
    for spec in FIELD_SPECS:
        _ensure_custom_field("Delivery Note", spec)


def sync_delivery_note_ui_status():
    names = frappe.get_all("Delivery Note", pluck="name")
    for name in names:
        doc = frappe.get_doc("Delivery Note", name)
        next_status = _delivery_note_ui_status(doc)
        current_status = (doc.get("accord_ui_status") or "").strip()
        if current_status == next_status:
            continue
        frappe.db.set_value(
            "Delivery Note",
            doc.name,
            "accord_ui_status",
            next_status,
            update_modified=False,
        )


def _ensure_custom_field(dt: str, spec: dict):
    existing_name = frappe.db.exists("Custom Field", {"dt": dt, "fieldname": spec["fieldname"]})
    if existing_name:
        doc = frappe.get_doc("Custom Field", existing_name)
        changed = False
        for key, value in (
            ("label", spec["label"]),
            ("fieldtype", spec["fieldtype"]),
            ("insert_after", spec["insert_after"]),
            ("hidden", spec.get("hidden", 0)),
            ("read_only", 1),
            ("allow_on_submit", 1),
            ("no_copy", 1),
            ("options", spec.get("options", "")),
        ):
            if doc.get(key) != value:
                doc.set(key, value)
                changed = True
        if changed:
            doc.save(ignore_permissions=True)
        return

    doc = frappe.get_doc(
        {
            "doctype": "Custom Field",
            "dt": dt,
            "fieldname": spec["fieldname"],
            "label": spec["label"],
            "fieldtype": spec["fieldtype"],
            "insert_after": spec["insert_after"],
            "hidden": spec.get("hidden", 0),
            "read_only": 1,
            "allow_on_submit": 1,
            "no_copy": 1,
            "options": spec.get("options", ""),
        }
    )
    doc.insert(ignore_permissions=True)


def _parse_int(value, default):
    try:
        if value is None:
            return default
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return default
        return int(value)
    except Exception:
        return default


def _delivery_note_ui_status(doc):
    current_status = (doc.get("accord_ui_status") or "").strip()
    if int(doc.docstatus or 0) != 1:
        return ""

    flow_state = _parse_int(doc.get("accord_flow_state"), 0)
    customer_state = _parse_int(doc.get("accord_customer_state"), CUSTOMER_STATE_PENDING)
    reason = (doc.get("accord_customer_reason") or "").strip()

    if flow_state != DELIVERY_FLOW_STATE_SUBMITTED:
        return "pending"
    if customer_state == CUSTOMER_STATE_REJECTED or reason:
        return "rejected"
    if customer_state == CUSTOMER_STATE_CONFIRMED or current_status == "confirm":
        return "confirm"
    return "pending"
