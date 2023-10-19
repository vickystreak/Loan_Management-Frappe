# Copyright (c) 2023, vignesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Payment(Document):
    def before_submit(self):
        loan_doc = frappe.get_doc("Loan", {"name": self.loan})
        loan_doc.outstanding_balance -= self.emi_amount
        loan_doc.emi_paid = (loan_doc.total_loan_amount - loan_doc.outstanding_balance) / self.emi_amount
        loan_doc.save()


@frappe.whitelist()
def generate_receipt_for_payment(payment):
    emi_payment = frappe.get_doc("Payment", payment)
    if emi_payment.payment_status == "Paid":
        # Create a new receipt record in the payment receipt doctype
        payment_receipt = frappe.new_doc("Payment Receipt")
        payment_receipt.update(
            {
                "loan": emi_payment.loan,
                "emi_payment_date": emi_payment.payment_date,
                "emi_amount": emi_payment.emi_amount,
                
            }
        )
        payment_receipt.insert(ignore_permissions=True)
        return payment_receipt.name
    else:
        frappe.throw('Payment must be "Paid" to generate payment receipt.')
