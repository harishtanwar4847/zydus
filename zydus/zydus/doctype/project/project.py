# Copyright (c) 2022, Atrina Technologies Pvt Ltd and contributors
# For license information, please see license.txt

from ast import If
import frappe
import os
from frappe.website.website_generator import WebsiteGenerator
import json


class Project(WebsiteGenerator):
	def get_context(self, context):
		context['no_cache'] = 1
		context['roles'] =  frappe.get_roles(frappe.session.user)
		context['allowed_roles'] = ['KMS Uploader', 'KMS Downloader', 'KMS Admin']
		# Sauce: https://stackoverflow.com/a/50633946/9403680
		context['access_allowed'] = any(role in context['roles'] for role in context['allowed_roles'])
		
		if context['access_allowed']:
			context['_user_tags'] = (frappe.db.get_value('Project', self.name, '_user_tags') or "").split(',')
			if len(context['_user_tags']) > 1:
				context['_user_tags'] = context['_user_tags'][1:]
			context['markets'] = ','.join([market.city for market in self.markets])
			context['attachments'] = frappe.desk.form.load.get_attachments('Project', self.name)
			for attachment in context['attachments']:
				file_ext=attachment['file_name']
				attachment['ext']=file_ext.rsplit('.', 1)[1]
				 
			context['userinfo']=frappe.db.sql(""" select P.name,U.user_image,U.full_name from `tabUser` as U  left join `tabProject` as P on  U.name = P.owner where P.name = %s """,(self.name),as_dict=1,debug=1)
		
			context['brand_color'] = frappe.db.get_value('Brand', self.brand, 'color')

	def before_submit(self):
		frappe.db.delete("View Log",{"reference_doctype": "Project", "reference_name":self.name})
			
