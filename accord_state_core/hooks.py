app_name = "accord_state_core"
app_title = "Accord State Core"
app_publisher = "Wikki"
app_description = "Minimal backend-only Accord state app for ERPNext"
app_email = "wikki@example.com"
app_license = "mit"

required_apps = ["erpnext"]

after_install = "accord_state_core.install.after_install"
after_migrate = "accord_state_core.install.after_migrate"
