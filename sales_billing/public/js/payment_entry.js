frappe.ui.form.on("Payment Entry", {

	get_invoices_from_sales_billing: function(frm) {
		const fields = [
			{
                fieldtype: "Link",
                label: __("Sales Billing"),
                fieldname: "sales_billing",
                options: "Sales Billing",
                reqd: 0,
				"get_query": function() {
					return {
						"filters": {
                            "company": frm.doc.company,
                            "customer": frm.doc.party,
                            "docstatus": 1,
                            "total_outstanding_amount": [">", 0]
                        }
					}
				}
			},
			{fieldtype:"Check", label: __("Allocate Payment Amount"), fieldname:"allocate_payment_amount", default:1},
		];

		frappe.prompt(fields, function(filters){
			frm.events.get_documents_from_sales_billing(frm, filters);
		}, __("Filters"), __("Get Invoices From Billing"));
	},

	get_documents_from_sales_billing: function(frm, filters) {
		frm.clear_table("references");
		frm.refresh_field("references");

		if(frm.doc.payment_type != "Receive" || frm.doc.party_type != "Customer" || !frm.doc.party) {
			return;
		}

        var sales_billing = filters["sales_billing"];
        frm.set_value("sales_billing", sales_billing);
        if (!sales_billing) { return; }

		frappe.flags.allocate_payment_amount = filters["allocate_payment_amount"];

        // Simply get the selected billing number, and its invoices.
        frappe.db.get_doc(
            "Sales Billing",
            filters["sales_billing"]
        ).then(bill => {
            var invoices = []
            $.each(bill.sales_billing_line, function(i, d) {
                invoices.push(d.sales_invoice);
            })
            // Get invoices data, and 
            frappe.db.get_list("Sales Invoice", {
                fields: ["*"],
                filters: {
                    name: ["in", invoices]
                }
            }).then(records => {
                if (records) {
                    var total_positive_outstanding = 0;
                    var total_negative_outstanding = 0;
                    var voucher_type = "Sales Invoice"

                    $.each(records, function(i, d) {
                        var c = frm.add_child("references");
                        c.reference_doctype = voucher_type;
                        c.reference_name = d.name;
                        c.due_date = d.due_date
                        c.total_amount = d.grand_total;
                        c.outstanding_amount = d.outstanding_amount;
                        c.allocated_amount = d.allocated_amount;

                        if(!in_list(frm.events.get_order_doctypes(frm), voucher_type)) {
                            if(flt(d.outstanding_amount) > 0)
                                total_positive_outstanding += flt(d.outstanding_amount);
                            else
                                total_negative_outstanding += Math.abs(flt(d.outstanding_amount));
                        }
                    });

                    if(total_positive_outstanding > total_negative_outstanding) {
                        if (!frm.doc.paid_amount) {
                            frm.set_value("paid_amount",
                                total_positive_outstanding - total_negative_outstanding);
                        }
                    }
                }

                frm.events.allocate_party_amount_against_ref_docs(frm, frm.doc.paid_amount, true);

            })
        })
	},
})