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

@frappe.whitelist()
def create_payment_entry_line(payment_details, sales_billing_name, posting_date):
    import json
    try:
        payment_details = json.loads(payment_details)
    except Exception:
        frappe.throw(_("Failed to parse payment details. Please check your input."))

    sales_billing = frappe.get_doc('Sales Billing', sales_billing_name)
    customer = sales_billing.customer
    company_currency = frappe.get_value('Company', sales_billing.company, 'default_currency')
    company = sales_billing.company

    total_outstanding_amount = sales_billing.total_outstanding_amount
    total_paid_amount = sum(detail['paid_amount'] for detail in payment_details)

    outstanding_amount = total_outstanding_amount - total_paid_amount

    payment_receipts = [] 
    payment_entries = [] 

    payment_receipt = frappe.get_doc({
        'doctype': 'Payment Receipt',
        'date': posting_date,
        'sales_billing': sales_billing_name,
        'customer': customer
    })

    for detail in payment_details:
        payment_receipt.append('payment_entry_line', {
            'mode_of_payment': detail['mode_of_payment'],
            'party_bank_account': detail.get('party_bank_account'),
            'company_bank_account': detail.get('company_bank_account'),
            'cheque_reference_no': detail.get('cheque_reference_no'),
            'cheque_reference_date': detail.get('cheque_reference_date'),
            'posting_date': detail.get('posting_date'),
            'paid_amount': detail['paid_amount'],
            'payment_entry': ''  
        })
        
        if sales_billing.sales_billing_line:
            for line in sales_billing.get("sales_billing_line", []):
                sales_invoice = line.get('sales_invoice')
                if sales_invoice:
                    payment_receipt.append('payment_references', {
                        'sales_billing': sales_billing_name,
                        'sales_invoice': sales_invoice,
                        'allocated_amount': detail['paid_amount'],
                        'outstanding_amount': outstanding_amount
                    })

        paid_to = frappe.get_value("Company", company, "default_receivable_account")
        paid_to_account_currency = company_currency

        payment_entry = frappe.get_doc({
            'doctype': 'Payment Entry',
            'payment_type': 'Receive',
            'party_type': 'Customer',
            'party': customer,
            'posting_date': posting_date,
            'mode_of_payment': detail['mode_of_payment'],
            'paid_amount': detail['paid_amount'],
            'amount': detail['paid_amount'], 
            'received_amount': detail['paid_amount'],  
            'company': company,
            'target_exchange_rate': 1 if company_currency == sales_billing.currency else 1,
            'paid_to': paid_to,
            'account_currency': paid_to_account_currency
        })
        
        payment_entry.append('references', {
            'reference_doctype': 'Sales Invoice',
            'reference_name': sales_invoice,
            'allocated_amount': detail['paid_amount'],
            'outstanding_amount': outstanding_amount
        })

        payment_entry.insert()
        payment_entries.append(payment_entry.name)

        payment_receipt.payment_entry_line[-1].payment_entry = payment_entry.name

    payment_receipt.insert()
    payment_receipts.append(payment_receipt.name)

    return {
        'message': _("Payment Receipts and Payment Entries Created"),
        'payment_receipts': payment_receipts,  
        'payment_entries': payment_entries, 
        'outstanding_amount': outstanding_amount
    }