# Copyright (c) 2022, Atrina Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
import json

class Datasheet(WebsiteGenerator):
	def get_context(self, context):
		context['no_cache'] = 1
		context['roles'] =  frappe.get_roles(frappe.session.user)
		context['allowed_roles'] = ['KMS Uploader', 'KMS Downloader', 'KMS Admin']
		# Sauce: https://stackoverflow.com/a/50633946/9403680
		context['access_allowed'] = any(role in context['roles'] for role in context['allowed_roles'])

		if context['access_allowed']:
			context['_user_tags'] = (frappe.db.get_value('Datasheet', self.name, '_user_tags') or "").split(',')
			if len(context['_user_tags']) > 1:
				context['_user_tags'] = context['_user_tags'][1:]
			context['attachments'] = frappe.desk.form.load.get_attachments('Datasheet', self.name)
			context['brand_color'] = frappe.db.get_value('Brand', self.brand, 'color')

		context['is_liked'] = frappe.session.user in json.loads((frappe.db.get_value('Datasheet', self.name, ['_liked_by']) or "[]"))
			
		context['userinfo']=frappe.db.sql(""" select D.name,U.user_image,U.full_name from `tabUser` as U  left join `tabDatasheet` as D on  U.name = D.owner where D.name = %s """,(self.name),as_dict=1,debug=1)

	def before_submit(self):
		frappe.db.delete("View Log",{"reference_doctype": "Datasheet", "reference_name":self.name})
