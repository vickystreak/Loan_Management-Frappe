# Copyright (c) 2023, vignesh and contributors
# For license information, please see license.txt
from datetime import date
import random
import frappe
from frappe.model.document import Document


class LoanApplication(Document):
	def before_save(self):
		if self.loan_type == "Personal loan":
			self.interest_rate = 12.5
		elif self.loan_type == "Business loan":
			self.interest_rate = 10.85
		elif self.loan_type == "Car loan":
			self.interest_rate = 8.82
		elif self.loan_type == "House loan":
			self.interest_rate = 8.45


@frappe.whitelist()
def create_loan_from_application(loan_application):
	# loan = frappe.get_doc("Loan",)
	loan_app = frappe.get_doc("Loan Application", loan_application)
	loan_number = random.randint(10000,99999)

	if loan_app.status == "Approved":
		if frappe.db.exists("Loan",{"borrower": loan_app.borrower,"loan_type": loan_app.loan_type,"principal_amount": loan_app.principal_amount}):
			frappe.throw('Already the Applicant "loan" had been Approved and Existed')
			
		else:
			# Create a new Loan record in the "Loan" DocType
			new_loan = frappe.new_doc("Loan")
			new_loan.update(
				{
					"borrower": loan_app.borrower,
					"principal_amount": loan_app.principal_amount,
					"interest_rate": loan_app.interest_rate,
					"loan_tenure": loan_app.loan_tenure,
					"loan_type": loan_app.loan_type,
					"monthly_emi": loan_app.monthly_emiexpected,
					"outstanding_balance" : (loan_app.monthly_emiexpected * loan_app.loan_tenure) *12,
					"date_of_loan_approved": date.today(),
					"loan_number" : loan_number,
					"total_loan_amount": (loan_app.monthly_emiexpected * loan_app.loan_tenure) *12,
					"total_no_of_emi": loan_app.loan_tenure * 12,
					"loan_type" : loan_app.loan_type,
				
				# Set other fields as needed for the "Loan" DocType
				}
			 )
			new_loan.insert(ignore_permissions=True)

			return new_loan.name  # Return the name of the newly created Loan record
	else:
		frappe.throw('Loan application must be "Approved" to create a Loan.')
