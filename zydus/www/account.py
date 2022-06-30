import frappe
import zydus
import json
from frappe.desk.form.load import get_attachments
from frappe.utils import pretty_date, now, add_to_date
import json 
import frappe
from frappe.website.utils import is_signup_enabled
from frappe.utils import (cint, flt, has_gravatar, escape_html, format_datetime,
	now_datetime, get_formatted_email, today)
from frappe import _
from frappe.utils.password import update_password

def get_context(context):
	context['no_cache'] = 1
	# print(frappe.get_fullname())
	# frappe.logger().info(frappe.get_fullname())
	
	
	context['roles'] =  frappe.get_roles(frappe.session.user)
	context['allowed_roles'] = ['KMS Uploader', 'KMS Downloader', 'KMS Admin']
	# Sauce: https://stackoverflow.com/a/50633946/9403680
	context['access_allowed'] = any(role in context['roles'] for role in context['allowed_roles'])

	if context['access_allowed']:
		context['trending_now_list'] = frappe.db.sql("""select B.color,P.name,B.brand_logo,P.p_title as title,count(V.reference_name) as view,concat(P.month," ",P.year) as month_year from `tabProject` as P  left join `tabBrand` as B on P.brand = B.name left join `tabView Log` as V on V.reference_name=P.name and V.reference_doctype="Project" group by P.name order by count(V.reference_name) desc limit 6 """,as_dict=True)
		for trending_now in context['trending_now_list']:
			trending_now['number_of_files'] = len(get_attachments("Project",trending_now.name))
			
		context["reminders"]=frappe.db.get_list("ToDo",fields=["name","title","description","owner","modified_by","date"], order_by ='date asc',debug=1,filters={"owner":frappe.session.user,"status":"open"},limit_page_length=10)

		# due_by calculation for reminders
		for reminder in context['reminders']:
			reminder['due_by'] = zydus.pretty_date_future(reminder['date'].strftime("%Y-%m-%d"))

		context["Users"]=frappe.db.get_list("User",fields=["user_image","full_name","designation","email","creation"],debug=1,limit_page_length=15)
        # due_by calculation for users
		for User in context['Users']:
			User['creation'] = pretty_date(User['creation'])


		context['favourites_page_length'] = 12
		context['favourites_page'] = int(frappe.form_dict.favourites) if frappe.form_dict.favourites else 1
		context['favourites_page_offset'] = (context['favourites_page'] - 1) * context['favourites_page_length']
		context['favourites_page_from'] = context['favourites_page_offset'] + 1
		context['favourites'] = frappe.db.sql("""  select T.modified,T.doctype,T.owner,T.route,T.liked_by,T.name,T.title,T.month_year,B.color,T.brand from (select modified,docstatus, owner, "Project" as doctype, P.route,P._liked_by as liked_by,P.brand,P.name,P.p_title as title,concat(P.month," ",P.year) as month_year from `tabProject` as P where  P.docstatus = 1 and P._liked_by like  %s    union         select modified,docstatus, owner, "Datasheet" as doctype, D.route, D._liked_by as liked_by,D.brand,D.name,D.d_title as title,concat(D.month," ",D.year) as month_year from `tabDatasheet`as D where  D.docstatus = 1 and D._liked_by like  %s  ) as T left join `tabBrand` as B on T.brand = B.name  order by modified desc limit 10; """, ("%{}%".format(frappe.session.user),"%{}%".format(frappe.session.user)),as_dict=1,debug=1)
		context['favourites_count'] = frappe.db.sql("""  select count(T.name) as count from (select P.name from `tabProject` as P where  P.docstatus = 1 and P._liked_by like  %s    union         select D.name from `tabDatasheet`as D where  D.docstatus = 1 and D._liked_by like  %s  ) as T ; """, ("%{}%".format(frappe.session.user),"%{}%".format(frappe.session.user)),as_dict=1,debug=1)[0]['count']
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
		context['my_uploads'] = frappe.db.sql("""  select T.modified,T.doctype,T.owner,T.route,T.liked_by,T.name,T.title,T.month_year,B.color,T.brand,T.workflow_state from (select modified,docstatus, owner, "Project" as doctype, P.route,P._liked_by as liked_by,P.brand,P.name,P.p_title as title,concat(P.month," ",P.year) as month_year,P.workflow_state from `tabProject` as P where owner= %(owner)s        union         select modified,docstatus, owner, "Datasheet" as doctype, D.route, D._liked_by as liked_by,D.brand,D.name,D.d_title as title ,concat(D.month," ",D.year) as month_year,D.workflow_state  from `tabDatasheet`as D where owner = %(owner)s) as T left join `tabBrand` as B on T.brand = B.name order by modified desc limit %(limit)s offset %(offset)s """, {'owner': frappe.session.user, 'limit': context['my_uploads_page_length'], 'offset': context['my_uploads_page_offset']} ,as_dict=1,debug=1)
		context['my_uploads_count'] = frappe.db.sql("""  select count(T.name) as count from (select P.name from `tabProject` as P where owner= %s        union         select D.name from `tabDatasheet` as D where owner = %s) as T""", (frappe.session.user,frappe.session.user),as_dict=1,debug=1)[0]['count']
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

