# Copyright (c) 2022, Atrina Technologies Pvt Ltd and contributors
# For license information, please see license.txt

from ast import If
import frappe
import os
from frappe.website.website_generator import WebsiteGenerator
import json
from frappe.utils import pretty_date, now, add_to_date
import zydus


class Project(WebsiteGenerator):
	def get_context(self, context):
		context['no_cache'] = 1	
		context['roles'] =  frappe.get_roles(frappe.session.user)	
		context['user_allowed_roles'] = ['KMS Uploader', 'KMS Downloader']
		context['admin_allowed_roles'] = ['KMS Admin']
		context['user_access_allowed'] = any(role in context['roles'] for role in context['user_allowed_roles'])
		context['admin_access_allowed'] = any(role in context['roles'] for role in context['admin_allowed_roles'])
		context['_user_tags'] = (frappe.db.get_value('Project', self.name, '_user_tags') or "").split(',')
		if len(context['_user_tags']) > 1:
			context['_user_tags'] = context['_user_tags'][1:]
		context['markets'] = ','.join([market.city for market in self.markets])
		context['attachments'] = frappe.desk.form.load.get_attachments('Project', self.name)
		for attachment in context['attachments']:
			file_ext=attachment['file_name']
			attachment['ext']=file_ext.rsplit('.', 1)[1]		 
		context['is_liked'] = frappe.session.user in json.loads((frappe.db.get_value('Project', self.name, ['_liked_by']) or "[]"))	
		context['userinfo']=frappe.db.sql(""" select P.name,U.user_image,U.full_name from `tabUser` as U  left join `tabProject` as P on  U.name = P.owner where P.name = %s """,(self.name),as_dict=1,debug=1)
		context['brand_color'] = frappe.db.get_value('Brand', self.brand, 'color')
		context.var =frappe.db.get_value("User",frappe.session.user,"full_name")
		context["comments"]=frappe.db.sql(""" select C.content,C.reference_name,C.reference_doctype,C.comment_by,C.creation from `tabComment` as C left join `tabProject`  as P on reference_name = P.name where C.reference_name = %s and C.content != "" and C.comment_type="Comment" order by C.creation desc limit 10""",(context.doc.name),as_dict=True)
		for comment in context['comments']:
			comment['creations'] = pretty_date(comment['creation'])

	def before_submit(self):
		frappe.db.delete("View Log",{"reference_doctype": "Project", "reference_name":self.name})
			
