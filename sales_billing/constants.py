CUSTOM_FIELDS = {
    "Payment Entry": [
        {
            "fieldname": "column_break_42",
            "fieldtype": "Column Break",
            "insert_after": "get_outstanding_orders",
        },
        {
            "depends_on": 'eval:doc.docstatus == 0 && doc.payment_type == "Receive" && doc.party_type == "Customer" && doc.party',
            "fieldname": "get_invoices_from_sales_billing",
            "fieldtype": "Button",
            "insert_after": "column_break_42",
            "label": "Get Invoices from Sales Billing",
        },
        {
            "fieldname": "sales_billing",
            "fieldtype": "Link",
            "insert_after": "get_invoices_from_sales_billing",
            "label": "Sales Billing",
            "options": "Sales Billing",
        },
        {
            "fieldname": "section_break_44",
            "fieldtype": "Section Break",
            "insert_after": "sales_billing",
        },
    ],
}
