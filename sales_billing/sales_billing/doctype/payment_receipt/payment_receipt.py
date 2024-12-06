# Copyright (c) 2024, FLO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PaymentReceipt(Document):
    def before_save(self):
        self.update_total_sales_invoice_amount()
        self.update_total_paid_amount()

    def update_total_sales_invoice_amount(self):
        total_sales_invoice_amount = 0
        for row in self.billing_references:
            total_sales_invoice_amount += row.grand_total
        self.total_sales_invoice_amount = total_sales_invoice_amount

    def update_total_paid_amount(self):
        total_paid_amount = 0
        for row in self.payment_references:
            total_paid_amount += row.paid_amount
        self.total_paid_amount = total_paid_amount