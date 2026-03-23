# Accord State Core

Accord State Core is a minimal backend-only ERPNext custom app used to maintain Accord-specific workflow fields on `Delivery Note`.

This app is intentionally small:

- no desk workspace
- no page UI
- no website routes
- no separate business UI layer
- only installable hooks and field/state helpers

## Purpose

The app exists to keep ERP-side workflow metadata stable for the mobile delivery flow.

Its responsibility is:

- ensure required custom fields exist on `Delivery Note`
- keep the visible UI status field available on the ERP form
- keep internal workflow fields available for backend state handling
- backfill UI status for existing `Delivery Note` records after migrate

This app does not own mobile business logic by itself. It provides ERP field structure that the mobile backend can safely rely on.

## Managed Delivery Note Fields

Current managed fields:

- `accord_flow_state`
- `accord_customer_state`
- `accord_customer_reason`
- `accord_delivery_actor`
- `accord_status_section`
- `accord_ui_status`

Current intent:

- internal fields are hidden
- `accord_ui_status` is visible and read-only
- `accord_ui_status` is placed in `Details`, after `posting_time`

Current expected UI status values:

- `pending`
- `confirm`
- `rejected`

## Hooks

Relevant hook file:

- [accord_state_core/hooks.py](/home/wikki/local.git/erpnext_n1/erp/apps/accord_state_core/accord_state_core/hooks.py)

Current hooks:

- `after_install`
- `after_migrate`

Both call into install helpers so field setup stays aligned even if the environment drifts.

## Install / Migrate Behavior

Relevant files:

- [accord_state_core/install.py](/home/wikki/local.git/erpnext_n1/erp/apps/accord_state_core/accord_state_core/install.py)
- [accord_state_core/state/delivery_note_state.py](/home/wikki/local.git/erpnext_n1/erp/apps/accord_state_core/accord_state_core/state/delivery_note_state.py)

Current behavior:

1. ensure custom fields exist
2. ensure field properties match the expected layout
3. sync `accord_ui_status` for existing `Delivery Note` rows

## Current Business Semantics

Important rule:

- `customer confirm` must not create a return document
- `customer reject` must result in a real ERP return flow

This app only manages fields and UI status support for that flow. The actual return creation is handled in the mobile backend.

## Repo Shape

Important files:

- `accord_state_core/hooks.py`
- `accord_state_core/install.py`
- `accord_state_core/state/delivery_note_state.py`
- `accord_state_core/modules.txt`

The nested package:

- `accord_state_core/accord_state_core/__init__.py`

exists so Frappe module loading works correctly during migrate.

## Notes

- this app is meant to stay small
- field management here is preferred over editing ERPNext core
- if mobile delivery workflow semantics change, this README should be updated together with the hook/state code
