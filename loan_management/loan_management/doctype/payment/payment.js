// Copyright (c) 2023, vignesh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Payment", {
  refresh: function (frm) {
    frm
      .add_custom_button("Generate Receipt", function () {
        // Check if the Payment status is Paid
        if (frm.doc.payment_status == "Paid") {
          frappe.call({
            method:
              "loan_management.loan_management.doctype.payment.payment.generate_receipt_for_payment",
            args: { payment: frm.doc.name },
            callback: function (r) {
              if (r.message) {
                frappe.msgprint(__("Payment receipt generated."));
              }
            },
          });
        } else {
          frappe.msgprint(
            __('Payment status must be "Paid" to generate the receipt ')
          );
        }
      })
      .addClass("btn-primary");
  },
});
