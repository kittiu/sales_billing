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

frappe.ui.form.on('Sales Billing', {
    refresh: function (frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Create Multi-Payments'), function () {
                let fields = [
                    {
                        label: 'Total Outstanding Amount',
                        fieldname: 'total_outstanding',
                        fieldtype: 'Currency',
                        default: frm.doc.total_outstanding_amount || 0,
                        read_only: 1
                    },
                    { fieldtype: 'Column Break' },
                    {
                        label: 'Posting Date',
                        fieldname: 'posting_date',
                        fieldtype: 'Date',
                        default: frappe.datetime.nowdate(),
                        reqd: 1
                    },
                    {
                        fieldtype: 'Section Break',
                    },
                    {
                        fieldtype: 'Table',
                        fieldname: 'payment_details',
                        label: 'Payment Details',
                        fields: [
                            {
                                label: 'Mode of Payment',
                                fieldname: 'mode_of_payment',
                                fieldtype: 'Link',
                                options: 'Mode of Payment',
                                in_list_view: 1,
                                reqd: 1
                            },
                            {
                                label: 'Party Bank Account',
                                fieldname: 'party_bank_account',
                                fieldtype: 'Link',
                                options: 'Bank Account',
                            },
                            {
                                label: 'Company Bank Account',
                                fieldname: 'company_bank_account',
                                fieldtype: 'Link',
                                options: 'Bank Account',
                            },
                            {
                                label: 'Cheque/Reference No',
                                fieldname: 'chequereference_no',
                                fieldtype: 'Data',
                                in_list_view: 1
                            },
                            {
                                label: 'Cheque/Reference Date',
                                fieldname: 'chequereference_date',
                                fieldtype: 'Date',
                                in_list_view: 1
                            },
                            {
                                label: 'Paid Amount',
                                fieldname: 'paid_amount',
                                fieldtype: 'Currency',
                                in_list_view: 1,
                                reqd: 1,
                                change: function (e, field) {
                                    let total_paid_amount = 0;
                                    field.grid.get_data().forEach((row) => {
                                        total_paid_amount += row.paid_amount || 0;
                                    });

                                    let remaining_outstanding = frm.doc.total_outstanding_amount - total_paid_amount;

                                    d.fields_dict.total_outstanding.set_value(remaining_outstanding);
                                }
                            }
                        ],
                    }
                ];
                fields.push(
                    { fieldtype: "Section Break" },
                    {
                        fieldtype: "Check",
                        label: __("Allocate Payment Amount"),
                        fieldname: "allocate_payment_amount",
                        default: 1,
                    }
                );

                let d = new frappe.ui.Dialog({
                    title: __('Create Multi-Payments'),
                    fields: fields,
                    primary_action_label: __('Create Multi-Payments'),
                    primary_action: function (values) {
                        frappe.flags.allocate_payment_amount = values.allocate_payment_amount;

                        let total_paid_amount = values.payment_details.reduce((acc, row) => acc + (row.paid_amount || 0), 0);
                        if (total_paid_amount > values.total_outstanding) {
                            frappe.msgprint(__('Total Paid Amount cannot be greater than Total Outstanding Amount.'));
                            return; 
                        }
                        frappe.call({
                            method: "sales_billing.sales_billing.doctype.sales_billing.sales_billing.create_payment_receipt",
                            args: {
                                payment_details: values.payment_details,
                                sales_billing_name: frm.doc.name,
                                posting_date: values.posting_date
                            },
                            callback: function (r) {
                                console.log(r); 
                            
                                if (!r.exc && r.message) {
                                    let receipt_names = r.message.payment_receipt_names;
                            
                                    if (receipt_names && receipt_names.length > 0) {
                                        let links = receipt_names.map(name => {
                                            return `<a href="/app/payment-receipt/${name}" target="_blank">${name}</a>`;
                                        });
                                        frappe.msgprint(__('Payment Receipts Created: {0}', [links.join(", ")]));
                                    } else {
                                        frappe.msgprint(__('Payment Receipts created successfully, but the names could not be retrieved.'));
                                    }
                                    d.hide(); 
                                }
                            }
                        });
                    }
                });

                d.show();
            }).addClass('btn-primary');
        }
    }
});

