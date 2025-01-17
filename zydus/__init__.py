from six import string_types
import datetime
from frappe.utils.data import DATE_FORMAT, nowdate
import frappe

__version__ = '1.4.1'

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
