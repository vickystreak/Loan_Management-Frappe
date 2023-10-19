// Copyright (c) 2023, vignesh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Loan Application", {
  loan_type: function (frm) {
    if (frm.doc.loan_type == "Personal loan") {
      frm.set_value({
        interest_rate: 12.5,
      });
    } else if (frm.doc.loan_type == "Business loan") {
      frm.set_value({
        interest_rate: 10.85,
      });
    } else if (frm.doc.loan_type == "Car loan") {
      frm.set_value({
        interest_rate: 8.82
      })
    } else if (frm.doc.loan_type == "Home loan") {
      frm.set_value({
        interest_rate: 8.45
      })
    }
  },

  principal_amount: function (frm) {
    let p = frm.doc.principal_amount;
    let r = frm.doc.interest_rate / (12 * 100);
    let n = frm.doc.loan_tenure * 12;
    frm.set_value({
      monthly_emiexpected: Math.round(
        (p * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1)
      ),
    });
  },

  loan_tenure: function (frm) {
    let p = frm.doc.principal_amount;
    let r = frm.doc.interest_rate / (12 * 100);
    let n = frm.doc.loan_tenure * 12;
    frm.set_value({
      monthly_emiexpected: Math.round(
        (p * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1)
      ),
    });
  },

  interest_rate: function (frm) {
    let p = frm.doc.principal_amount;
    let r = frm.doc.interest_rate / (12 * 100);
    let n = frm.doc.loan_tenure * 12;
    frm.set_value({
      monthly_emiexpected: Math.round(
        (p * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1)
      ),
    });
  },

  refresh: function (frm) {
    frm
      .add_custom_button(__("Approve Loan"), function () {
        // Check if the status is 'Approved'
        if (frm.doc.status === "Approved") {
          // Create a new Loan document
          frappe.call({
            method:
              "loan_management.loan_management.doctype.loan_application.loan_application.create_loan_from_application",
            args: {
              loan_application: frm.doc.name,
            },
            callback: function (r) {
              if (r.message) {
                frappe.msgprint(__("Loan document created."));
              }
            },
          });
        } else {
          frappe.msgprint(
            __('Loan application must be "Approved" to create a Loan.')
          );
        }
      })
      .addClass("btn-primary");
  },
});
