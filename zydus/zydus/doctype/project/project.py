# Copyright (c) 2022, Atrina Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
<<<<<<< HEAD
from frappe.model.document import Document

class Project(Document):
	def on_submit(self):
		if self.workflow_state == "Approved":
			frappe.db.delete("View Log",{"reference_name":self.name})
			
=======
from frappe.website.website_generator import WebsiteGenerator


class Project(WebsiteGenerator):
	def get_context(self, context):
		context['roles'] =  frappe.get_roles(frappe.session.user)
		context['allowed_roles'] = ['KMS Uploader', 'KMS Downloader', 'KMS Admin']
		# Sauce: https://stackoverflow.com/a/50633946/9403680
		context['access_allowed'] = any(role in context['roles'] for role in context['allowed_roles'])

		if context['access_allowed']:
			pass
>>>>>>> develop
