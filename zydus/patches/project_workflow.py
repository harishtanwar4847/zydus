import frappe
from frappe.core.doctype.data_import.data_import import import_file

def execute():
    path = frappe.get_app_path('zydus','patches','imports','project_workflow.csv')
    import_file('Workflow', path, 'Insert',console=True)