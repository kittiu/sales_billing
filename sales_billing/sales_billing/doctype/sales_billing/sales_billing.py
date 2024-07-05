# Copyright (c) 2023, FLO and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class SalesBilling(Document):

	def validate(self):
		invoices = [i.sales_invoice for i in self.sales_billing_line]
		if len(invoices) > len(list(set(invoices))):
			frappe.throw(_("Please do not select same sales invoice more than once!"))
		total_outstanding_amount = sum([i.outstanding_amount for i in self.sales_billing_line])
		total_billing_amount = sum([i.grand_total for i in self.sales_billing_line])
		self.total_outstanding_amount = total_outstanding_amount
		self.total_billing_amount = total_billing_amount


@frappe.whitelist()
def get_due_billing(customer=None, currency=None, tax_type=None, threshold_type=None, threshold_date=None):
	if not (customer, currency, tax_type, threshold_date):
		return {}
	filters = {
		"customer": customer,
		"currency": currency,
		"docstatus": 1,
		"outstanding_amount": [">", 0],
	}
	if tax_type:
		filters["taxes_and_charges"] = tax_type
	if threshold_type == "Due Date":
		filters["posting_date"] = ["<=", threshold_date]
	if threshold_type == "Invoice Date":
		filters["due_date"] = ["<=", threshold_date]
	invoices = frappe.get_list(
		"Sales Invoice",
		filters=filters,
		pluck="name"
	)
	return invoices

def update_sales_billing_outstanding_amount(doc, method):
    # Document: Payment Entry
    total_outstanding_amount = 0
    if not doc.sales_billing:
        return
    bill = frappe.get_doc("Sales Billing", doc.sales_billing)
    for bill_line in bill.sales_billing_line:
        invoice = frappe.get_doc("Sales Invoice", bill_line.sales_invoice)
        bill_line.outstanding_amount = invoice.outstanding_amount
        total_outstanding_amount += invoice.outstanding_amount
    bill.total_outstanding_amount = total_outstanding_amount
    bill.save()
