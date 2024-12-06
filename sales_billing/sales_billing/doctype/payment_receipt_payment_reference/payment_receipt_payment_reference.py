# Copyright (c) 2024, FLO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PaymentReceiptPaymentReference(Document):
    @property
    def mode_of_payment(self):
        if self.payment_entry:
            payment_entry = frappe.get_doc("Payment Entry", self.payment_entry)
            if payment_entry:
                return payment_entry.mode_of_payment
        return ""
    
    @property
    def party_bank_account(self):
        if self.payment_entry:
            payment_entry = frappe.get_doc("Payment Entry", self.payment_entry)
            if payment_entry:
                return payment_entry.party_bank_account
        return ""
    @property
    def company_bank_account(self):
        if self.payment_entry:
            payment_entry = frappe.get_doc("Payment Entry", self.payment_entry)
            if payment_entry:
                return payment_entry.bank_account
        return ""
    @property
    def chequereference_no(self):
        if self.payment_entry:
            payment_entry = frappe.get_doc("Payment Entry", self.payment_entry)
            if payment_entry:
                return payment_entry.reference_no
        return ""
    @property
    def chequereference_date(self):
        if self.payment_entry:
            payment_entry = frappe.get_doc("Payment Entry", self.payment_entry)
            if payment_entry:
                return payment_entry.reference_date
        return None
    @property
    def posting_date(self):
        if self.payment_entry:
            payment_entry = frappe.get_doc("Payment Entry", self.payment_entry)
            if payment_entry:
                return payment_entry.posting_date  
        return None
    @property
    def paid_amount(self):
        if self.payment_entry:
            payment_entry = frappe.get_doc("Payment Entry", self.payment_entry)
            if payment_entry:
                return payment_entry.paid_amount
        return 0
    @property
    def status(self):
        if self.payment_entry:
            payment_entry = frappe.get_doc("Payment Entry", self.payment_entry)
            if payment_entry:
                return payment_entry.status
        return None
