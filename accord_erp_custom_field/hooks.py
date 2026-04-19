app_name = "accord_erp_custom_field"
app_title = "Accord ERP Custom Field"
app_publisher = "Wikki"
app_description = "ERPNext custom field app for the Accord mobile workflow"
app_email = "wikki@example.com"
app_license = "mit"

required_apps = ["erpnext"]

after_install = "accord_erp_custom_field.install.after_install"
after_migrate = "accord_erp_custom_field.install.after_migrate"
