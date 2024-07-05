// Copyright (c) 2023, FLO and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sales Billing", {

    refresh(frm) {
        frm.fields_dict["sales_billing_line"].grid.get_field("sales_invoice").get_query = function(doc, cdt, cdn) {
            return {
                filters: {
                    'customer': ["=", doc.customer],
                    'docstatus': 1
                }
            }
        }
    },

    // Add Multiple Button
    onload_post_render: function(frm) {
		frm.get_field("sales_billing_line").grid.set_multiple_add("sales_invoice");
	},

	get_sales_invoices(frm) {
        if (frm.doc.threshold_date) {
            return frm.call({
                method: "sales_billing.sales_billing.doctype.sales_billing.sales_billing.get_due_billing",
                args: {
                    customer: frm.doc.customer,
                    currency: frm.doc.currency,
					tax_type: frm.doc.tax_type,
                    threshold_type: frm.doc.threshold_type,
                    threshold_date: frm.doc.threshold_date
                },
                callback: function(r) {
                    console.log(r.message)
                    let invoices = []
                    for (let i of r.message) {
                        invoices.push({sales_invoice: i})
                    }
                    frm.set_value("sales_billing_line", invoices)
                    frm.set_value("invoice_count", invoices.length)
                    frm.refresh_field('sales_billing_line');
                }
            });
        }
    }
})


frappe.ui.form.on("Sales Billing Line", {

    sales_billing_line_add(frm, cdt, cdn) {
        frm.set_value("invoice_count", frm.doc.invoice_count + 1)
    },
    sales_billing_line_remove(frm, cdt, cdn) {
        frm.set_value("invoice_count", frm.doc.invoice_count - 1)
    }

})