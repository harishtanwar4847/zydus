# Copyright (c) 2022, Atrina Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class Project(WebsiteGenerator):
	def get_context(self, context):
		context['roles'] =  frappe.get_roles(frappe.session.user)
		context['allowed_roles'] = ['KMS Uploader', 'KMS Downloader', 'KMS Admin']
		# Sauce: https://stackoverflow.com/a/50633946/9403680
		context['access_allowed'] = any(role in context['roles'] for role in context['allowed_roles'])

		if context['access_allowed']:
			context['_user_tags'] = frappe.db.get_value('Project', self.name, '_user_tags').split(',')[1:]
			context['markets'] = ','.join([market.city for market in self.markets])
			context['attachments'] = frappe.desk.form.load.get_attachments('Project', self.name)
			context['brand_color'] = frappe.db.get_value('Brand', self.brand, 'color')

	def before_submit(self):
		self.is_approved = True
		self.route = 'projects/{}'.format(self.name)
		frappe.db.delete("View Log",{"reference_name":self.name})
			
