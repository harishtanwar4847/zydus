import frappe
from frappe.core.doctype.data_import.data_import import import_file

def execute():
    path = frappe.get_app_path('zydus','patches','imports','brand.csv')
    import_file('Brand', path, 'Insert',console=True)