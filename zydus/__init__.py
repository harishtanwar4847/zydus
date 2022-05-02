from six import string_types
import datetime
from frappe.utils.data import DATE_FORMAT, nowdate
import frappe

__version__ = '0.2.5-dev'

# Sauce: frappe.utils.data.pretty_date
def pretty_date_future(iso_datetime):
	"""
		Takes an ISO time and returns a string representing how
		long ago the date represents.
		Ported from PrettyDate by John Resig
	"""
	from frappe import _
	if not iso_datetime: return ''
	import math

	if isinstance(iso_datetime, string_types):
		iso_datetime = datetime.datetime.strptime(iso_datetime, DATE_FORMAT)
	now_dt = datetime.datetime.strptime(nowdate(), DATE_FORMAT)
	dt_diff = iso_datetime - now_dt

	# available only in python 2.7+
	# dt_diff_seconds = dt_diff.total_seconds()

	dt_diff_seconds = dt_diff.days * 86400.0 + dt_diff.seconds

	dt_diff_days = math.floor(dt_diff_seconds / 86400.0)

	# differnt cases
	if dt_diff_days <= 0:
		return _('Today')
	elif dt_diff_days <= 1:
		return _('Tomorrow')
	elif dt_diff_days > 1:
		return iso_datetime.strftime('%d/%m')

def get_attachments_custom(dt, dn):
	return frappe.get_all("File", fields=["name", "file_name", "file_url", "is_private", "file_size"],
		filters = {"attached_to_name": dn, "attached_to_doctype": dt})

from frappe.desk.form import load
load.get_attachments = get_attachments_custom

def add_default_image_in_user_before_insert(doc, method):
	doc.user_image = '/assets/zydus/images/user_default_image.png'

from frappe.auth import LoginManager
from frappe.website.utils import get_home_page
def set_user_info_custom(self, resume=False):
	# set sid again
	frappe.local.cookie_manager.init_cookies()

	self.full_name = " ".join(filter(None, [self.info.first_name,
		self.info.last_name]))

	if self.info.user_type=="Website User":
		frappe.local.cookie_manager.set_cookie("system_user", "no")
		if not resume:
			frappe.local.response["message"] = "No App"
			frappe.local.response["home_page"] = '/' + get_home_page()
	else:
		frappe.local.cookie_manager.set_cookie("system_user", "yes")
		if not resume:
			frappe.local.response['message'] = 'Logged In'
			frappe.local.response["home_page"] = "/home"

	if not resume:
		frappe.response["full_name"] = self.full_name

	# redirect information
	redirect_to = frappe.cache().hget('redirect_after_login', self.user)
	if redirect_to:
		frappe.local.response["redirect_to"] = redirect_to
		frappe.cache().hdel('redirect_after_login', self.user)


	frappe.local.cookie_manager.set_cookie("full_name", self.full_name)
	frappe.local.cookie_manager.set_cookie("user_id", self.user)
	frappe.local.cookie_manager.set_cookie("user_image", self.info.user_image or "")

LoginManager.set_user_info = set_user_info_custom
