import frappe
from frappe.core.doctype.data_import.data_import import import_file

def execute():
    path = frappe.get_app_path('zydus','patches','imports','project_type.csv')
    import_file('Project Type', path, 'Insert',console=True)