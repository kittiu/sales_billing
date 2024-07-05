from . import __version__ as app_version

app_name = "sales_billing"
app_title = "Sales Billing"
app_publisher = "FLO"
app_description = "Summary of sales invoices to send to customer in batch"
app_email = "kittiu@ecosoft.co.th"
app_license = "MIT"

fixtures = [
    {
		"dt": "Custom Field",
		"filters": [("name", "in", [
			"Payment Entry-sales_billing",
            "Payment Entry-section_break_44",
            "Payment Entry-column_break_42",
            "Payment Entry-get_invoices_from_sales_billing",
		])],
	},
    {
		"dt": "DocType Link",
		"filters": [["link_doctype", "in", ["Sales Billing"]]],
	},
	{
		"dt": "Property Setter",
		"filters": [["name", "in", [
			"Withholding Tax Cert-main-default_print_format",
			"Account-account_type-options",
		]]],
	},
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/sales_billing/css/sales_billing.css"
# app_include_js = "/assets/sales_billing/js/sales_billing.js"

# include js, css files in header of web template
# web_include_css = "/assets/sales_billing/css/sales_billing.css"
# web_include_js = "/assets/sales_billing/js/sales_billing.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "sales_billing/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_js = {
	"Payment Entry" : "public/js/payment_entry.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "sales_billing.utils.jinja_methods",
#	"filters": "sales_billing.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "sales_billing.install.before_install"
# after_install = "sales_billing.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "sales_billing.uninstall.before_uninstall"
# after_uninstall = "sales_billing.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "sales_billing.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

doc_events = {
    "Payment Entry": {
        "on_submit": [
            "sales_billing.sales_billing.doctype.sales_billing.sales_billing.update_sales_billing_outstanding_amount",
        ],
        "on_cancel":[
            "sales_billing.sales_billing.doctype.sales_billing.sales_billing.update_sales_billing_outstanding_amount",
        ],
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"sales_billing.tasks.all"
#	],
#	"daily": [
#		"sales_billing.tasks.daily"
#	],
#	"hourly": [
#		"sales_billing.tasks.hourly"
#	],
#	"weekly": [
#		"sales_billing.tasks.weekly"
#	],
#	"monthly": [
#		"sales_billing.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "sales_billing.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "sales_billing.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "sales_billing.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"sales_billing.auth.validate"
# ]
