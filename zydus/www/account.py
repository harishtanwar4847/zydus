from datetime import datetime
from sqlite3 import sqlite_version
from urllib import response
import frappe
from frappe import sessions
import zydus
import json
from frappe.desk.form.load import get_attachments
from frappe.utils import pretty_date,now,add_to_date
import json 
import frappe
from frappe.website.utils import is_signup_enabled
from frappe.utils import (cint, flt, has_gravatar, escape_html, format_datetime,
	now_datetime, get_formatted_email, today)
from frappe import _
from frappe.utils.password import update_password

def get_context(context):
	context['no_cache'] = 1	
	context['roles'] =  frappe.get_roles(frappe.session.user)	
	context['user_allowed_roles'] = ['KMS Uploader', 'KMS Downloader']
	context['admin_allowed_roles'] = ['KMS Admin']
	context['user_access_allowed'] = any(role in context['roles'] for role in context['user_allowed_roles'])
	context['admin_access_allowed'] = any(role in context['roles'] for role in context['admin_allowed_roles'])
	where_clause = ""
	if context['admin_access_allowed']:
		where_clause= "(T.created_by = '{session_user}' or T.owner = '{session_user}')".format(session_user=frappe.session.user)
	else:
		where_clause= "(T.owner = '{session_user}')".format(session_user=frappe.session.user)
	context['reminders_page_length'] = 8
	context['reminders_page'] = int(frappe.form_dict.reminders) if frappe.form_dict.reminders else 1
	context['reminders_page_offset'] = (context['reminders_page'] - 1) * context['reminders_page_length']
	context['reminders_page_from'] = context['reminders_page_offset'] + 1
	context["reminders"] = frappe.db.sql(""" select U.user_image,U.full_name,T.name,T.title,T.description,T.owner,T.modified_by,T.date from `tabToDo` as T left join `tabUser` as U on T.owner = U.name where status = "open" and {} order by date asc limit %(limit)s offset %(offset)s""".format(where_clause),{'owner': frappe.session.user, 'limit': context['reminders_page_length'], 'offset': context['reminders_page_offset']} ,as_dict=1)
	context['reminders_count'] = frappe.db.sql("""  select count(T.name) as count from `tabToDo` as T where status = "open" and {} """.format(where_clause),as_dict=1)[0]['count']
	context['reminders_page_to'] = context['reminders_page'] * context['reminders_page_length']
	if context['reminders_page_to'] > context['reminders_count']:
		context['reminders_page_to'] = context['reminders_count']
	# context["reminders"] = frappe.db.sql(""" select U.user_image,U.full_name,T.name,T.title,T.description,T.owner,T.modified_by,T.date from `tabToDo` as T left join `tabUser` as U on T.owner = U.name where status = "open" and {} order by date asc limit 5 """.format(where_clause),as_dict=1)
	context['trending_now_list'] = frappe.db.sql("""select B.color,P.name,B.brand_logo,P.p_title as title,count(V.reference_name) as view,concat(P.month," ",P.year) as month_year from `tabProject` as P  left join `tabBrand` as B on P.brand = B.name left join `tabView Log` as V on V.reference_name=P.name and V.reference_doctype="Project" group by P.name order by count(V.reference_name) desc limit 6 """,as_dict=True)
	for trending_now in context['trending_now_list']:
		trending_now['number_of_files'] = len(get_attachments("Project",trending_now.name))
	context['Users_page_length'] = 12
	context['Users_page'] = int(frappe.form_dict.Users) if frappe.form_dict.Users else 1
	context['Users_page_offset'] = (context['Users_page'] - 1) * context['Users_page_length']
	context['Users_page_from'] = context['Users_page_offset']
	context["Users"] = frappe.db.get_list("User",fields=["username","user_image","full_name","designation","email","creation","enabled","access_given"],order_by ='creation desc', limit_page_length=context['Users_page_length'], limit_start=context['Users_page_from'])
	context["Users_count"] = frappe.db.get_list("User",fields=["count(name) as count"])[0]['count']
	context['Users_page_to'] = context['Users_page'] * context['Users_page_length']
	if context['Users_page_to'] > context['Users_count']:
		context['Users_page_to'] = context['Users_count']
	# context["Users"]=frappe.db.get_list("User",fields=["username","user_image","full_name","designation","email","creation","enabled","access_given"],limit_page_length=15)
    #due_by calculation for users
	for User in context['Users']:
		User['creation'] = pretty_date(User['creation'])
		User['UID']="-".join(User["email"].split('@'))
		roles=frappe.db.get_values("Has Role",{"parent":User["email"]},"role",as_dict=1)
		User["roles"]=[i.get("role") for i in roles]
	context['Employees'] = frappe.get_all('User',fields="full_name,name")
	context['favourites_page_length'] = 12
	context['favourites_page'] = int(frappe.form_dict.favourites) if frappe.form_dict.favourites else 1
	context['favourites_page_offset'] = (context['favourites_page'] - 1) * context['favourites_page_length']
	context['favourites_page_from'] = context['favourites_page_offset'] + 1
	context['favourites'] = frappe.db.sql("""  select T.modified,T.doctype,T.owner,T.route,T.liked_by,T.name,T.title,T.month_year,B.color,T.brand from (select modified,docstatus, owner, "Project" as doctype, P.route,P._liked_by as liked_by,P.brand,P.name,P.p_title as title,concat(P.month," ",P.year) as month_year from `tabProject` as P where  P.docstatus = 1 and P._liked_by like  %s    union         select modified,docstatus, owner, "Datasheet" as doctype, D.route, D._liked_by as liked_by,D.brand,D.name,D.d_title as title,concat(D.month," ",D.year) as month_year from `tabDatasheet`as D where  D.docstatus = 1 and D._liked_by like  %s  ) as T left join `tabBrand` as B on T.brand = B.name  order by modified desc limit 10; """, ("%{}%".format(frappe.session.user),"%{}%".format(frappe.session.user)),as_dict=1)
	context['favourites_count'] = frappe.db.sql("""  select count(T.name) as count from (select P.name from `tabProject` as P where  P.docstatus = 1 and P._liked_by like  %s    union         select D.name from `tabDatasheet`as D where  D.docstatus = 1 and D._liked_by like  %s  ) as T ; """, ("%{}%".format(frappe.session.user),"%{}%".format(frappe.session.user)),as_dict=1)[0]['count']
	context['favourites_page_to'] = context['favourites_page'] * context['favourites_page_length']
	if context['favourites_page_to'] > context['favourites_count']:
		context['favourites_page_to'] = context['favourites_count']
	for favourite in context['favourites']:
		favourite['attachments'] = get_attachments(favourite.doctype,favourite.name)
		favourite['is_liked'] = frappe.session.user in json.loads(favourite['liked_by'] or '[]')
	context['my_uploads_page_length'] = 12
	context['my_uploads_page'] = int(frappe.form_dict.my_uploads) if frappe.form_dict.my_uploads else 1
	context['my_uploads_page_offset'] = (context['my_uploads_page'] - 1) * context['my_uploads_page_length']
	context['my_uploads_page_from'] = context['my_uploads_page_offset'] + 1
	context['my_uploads'] = frappe.db.sql("""  select T.modified,T.doctype,T.owner,T.route,T.liked_by,T.name,T.title,T.month_year,B.color,T.brand,T.workflow_state from (select modified,docstatus, owner, "Project" as doctype, P.route,P._liked_by as liked_by,P.brand,P.name,P.p_title as title,concat(P.month," ",P.year) as month_year,P.workflow_state from `tabProject` as P where owner= %(owner)s        union         select modified,docstatus, owner, "Datasheet" as doctype, D.route, D._liked_by as liked_by,D.brand,D.name,D.d_title as title ,concat(D.month," ",D.year) as month_year,D.workflow_state  from `tabDatasheet`as D where owner = %(owner)s) as T left join `tabBrand` as B on T.brand = B.name where T.workflow_state IN ("approved","rejected","pending") order by modified desc limit %(limit)s offset %(offset)s """, {'owner': frappe.session.user, 'limit': context['my_uploads_page_length'], 'offset': context['my_uploads_page_offset']} ,as_dict=1)
	context['my_uploads_count'] = frappe.db.sql("""  select count(T.name) as count from (select P.name from `tabProject` as P where owner= %s        union         select D.name from `tabDatasheet` as D where owner = %s) as T""", (frappe.session.user,frappe.session.user),as_dict=1)[0]['count']
	context['my_uploads_page_to'] = context['my_uploads_page'] * context['my_uploads_page_length']
	if context['my_uploads_page_to'] > context['my_uploads_count']:
		context['my_uploads_page_to'] = context['my_uploads_count']
	for my_upload in context['my_uploads']:
		my_upload['attachments'] = get_attachments(my_upload.doctype,my_upload.name)
		my_upload['is_liked'] = frappe.session.user in json.loads(my_upload['liked_by'] or '[]')		
	context['my_notifications_page_length'] = 12
	context['my_notifications_page'] = int(frappe.form_dict.notifications) if frappe.form_dict.notifications else 1
	context['my_notifications_page_offset'] = (context['my_notifications_page'] - 1) * context['my_notifications_page_length']
	context['my_notifications_page_from'] = context['my_notifications_page_offset'] + 1
	context["my_notifications"] = frappe.db.get_all("Notification Log",fields=["subject","creation", "read", "name"], filters={'for_user': frappe.session.user}, limit_page_length=context['my_notifications_page_length'], limit_start=context['my_notifications_page_from'])
	context["my_notifications_count"] = frappe.db.get_all("Notification Log",fields=["count(name) as count"], filters={'for_user': frappe.session.user})[0]['count']
	context['my_notifications_page_to'] = context['my_notifications_page'] * context['my_notifications_page_length']
	if context['my_notifications_page_to'] > context['my_notifications_count']:
		context['my_notifications_page_to'] = context['my_notifications_count']
	for my_notification in context['my_notifications']:
		my_notification['creations'] = pretty_date(my_notification['creation'])
	context["notifications"] = frappe.db.get_all("Notification Log",fields=["subject","creation"],limit_page_length=5,order_by="modified desc")
	for notification in context['notifications']:
		notification['creations'] = pretty_date(notification['creation'])
		# due_by calculation for reminders
	for reminder in context['reminders']:
		reminder['due_by'] = zydus.pretty_date_future(reminder['date'].strftime("%Y-%m-%d"))

@frappe.whitelist()
def notification_read_unread(docnames, mark_as_read):
	notifs = (docnames or '').split(',')
	print(bool)
	read_value = 1 if int(mark_as_read) else 0
	frappe.db.sql('update `tabNotification Log` set `read` = %s where name in %s',(read_value, tuple(notifs)))



# edit profile API
@frappe.whitelist(allow_guest=True)
def edit_profile():
	print("**frappe.form_dict.confirm_password**",frappe.form_dict)
	user = frappe.get_doc('User', frappe.session.user)
	# frappe.logger().info("req data")
	# frappe.logger().info(frappe.form_dict)

	files = frappe.request.files
	is_private = False
	fieldname = 'user_image'
	folder = 'Home'
	content = None
	filename = None

	# if 'file' in files:
	# 	file = files['file']
	# 	content = file.stream.read()
	# 	filename = file.filename

	frappe.local.uploaded_file = content
	frappe.local.uploaded_filename = filename

	first_name = None
	last_name =  None
	full_name_exploded = frappe.form_dict.full_name.split(' ')
	# frappe.logger().info(full_name)
	if len(full_name_exploded) > 1:
		last_name = full_name_exploded[-1]
		first_name = ' '.join(full_name_exploded[:-1])
	else:
		first_name = frappe.form_dict.full_name

	user.first_name = first_name
	user.last_name = last_name
	user.designation = frappe.form_dict.designation
	
	# user_image = '/assets/zydus/images/user_default_image.png'
	if 'file' in files:
		file = files['file']
		content = file.stream.read()
		filename = file.filename
		ret = frappe.get_doc({
			"doctype": "File",
			"attached_to_doctype": 'User',
			"attached_to_name": user.name,
			"attached_to_field": fieldname,
			"folder": folder,
			"file_name": filename,
			# "file_url": file_url,
			"is_private": cint(is_private),
			"content": content
		})
		ret.save(ignore_permissions=True)
		user.user_image = ret.file_url

		# user_image = ret.file_url

	
	user.save()
	if frappe.form_dict.confirm_password:
		update_password(frappe.session.user,frappe.form_dict.confirm_password)
	#user.new_password = frappe.form_dict.confirm_password
	frappe.db.commit()
	
	frappe.logger().info("**********************")
	frappe.logger().info(user)

	return 1, _('Updated Successfully')

@frappe.whitelist()
def update_Roles(**kwargs):
	data = kwargs
	name="@".join(data.get("name").split('-'))
	roles=kwargs.get("roles").split(',')[0:-1]
	user_roles = [{"doctype": "Has Role", "role": i } for i in roles]
	frappe.set_value('User',name,"roles",user_roles)
	if user_roles:
		frappe.set_value('User',name,"access_given",1)
	else:
		frappe.set_value('User',name,"access_given",0)
	sql=(""" 
	delete from `tabHas Role` where parent='{}', role IN {}
	""".format(name,tuple(data.get("removeroles").split(','))))
	
	print("tuplee",tuple(data.get("removeroles").split(',')))
	# frappe.db.commit()
	response = {
		"message":"success",
		"User":frappe.get_doc("User",name),
	}
	return response



