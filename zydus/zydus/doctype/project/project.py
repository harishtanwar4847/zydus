# Copyright (c) 2022, Atrina Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Project(Document):
	def on_submit(self):
		if self.workflow_state == "Approved":
			frappe.db.delete("View Log",{"reference_name":self.name})
			
