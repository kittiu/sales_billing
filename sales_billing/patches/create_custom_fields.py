
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from sales_billing.constants import CUSTOM_FIELDS

def execute():
    create_custom_fields(CUSTOM_FIELDS, ignore_validate=True)
