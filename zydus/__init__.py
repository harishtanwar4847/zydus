from six import string_types
import datetime
from frappe.utils.data import DATE_FORMAT, nowdate

__version__ = '0.2.0-dev'

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

