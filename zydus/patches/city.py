import frappe
from frappe.core.doctype.data_import.data_import import import_file

def execute():
    path = frappe.get_app_path('zydus','patches','imports','city.csv')
    import_file('City', path, 'Insert',console=True)