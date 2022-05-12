import frappe
from frappe.website.utils import is_signup_enabled
from frappe.utils import (cint, flt, has_gravatar, escape_html, format_datetime,
	now_datetime, get_formatted_email, today)
from frappe import _


@frappe.whitelist(allow_guest=True)
def sign_up():
	if not is_signup_enabled():
		return 0, _('Sign up is disabled')

	user = frappe.db.get("User", {"email": frappe.form_dict.email})
	if user:
		if user.disabled:
			return 0, _("Registered but disabled")
		else:
			return 0, _("Already Registered")
	else:
		if frappe.db.sql("""select count(*) from tabUser where
			HOUR(TIMEDIFF(CURRENT_TIMESTAMP, TIMESTAMP(modified)))=1""")[0][0] > 300:

			return 0, _('Too many users signed up recently, so the registration is disabled. Please try back in an hour')

	files = frappe.request.files
	is_private = False
	fieldname = 'user_image'
	folder = 'Home'
	content = None
	filename = None

	if 'file' in files:
		file = files['file']
		content = file.stream.read()
		filename = file.filename

	frappe.local.uploaded_file = content
	frappe.local.uploaded_filename = filename

	first_name = None
	last_name = None
	full_name_exploded = frappe.form_dict.full_name.split(' ')
	if len(full_name_exploded) > 1:
		last_name = full_name_exploded[-1]
		first_name = ' '.join(full_name_exploded[:-1])
	else:
		first_name = frappe.form_dict.full_name

	user = frappe.get_doc({
		"doctype":"User",
		"email": frappe.form_dict.email,
		"first_name": first_name,
		"last_name": last_name,
		"enabled": 1,
		"new_password": frappe.form_dict.password,
		"user_type": "System User",
		"send_welcome_email": False,
		"designation": frappe.form_dict.designation,
	})
	user.flags.ignore_permissions = True
	user.flags.ignore_password_policy = True
	user.insert()
	
	user_image = '/assets/zydus/images/user_default_image.png'
	if 'file' in files:
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
		user_image = ret.file_url

	user.user_image = user_image
	user.save()

	user.add_roles('KMS Uploader')
	user.add_roles('KMS Downloader')

	return 1, _('Registered Successfully')