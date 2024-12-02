from frappe import _

def get_data():
    return {
        "fieldname": "payment_receipt",
        "internal_and_external_links": {
			"Sales Invoice": ["payment_references", "sales_invoice"],
            "Sales Billing": ["payment_references", "sales_invoice"],
            "Payment Entry": ["payment_entry_line", "sales_invoice"],
		},
        "transactions": [
            {"label": _("Reference"), "items": ["Sales Invoice","Sales Billing"]},  
            {"label": _("Payment"), "items": ["Payment Entry"]},  
        ],
    }
