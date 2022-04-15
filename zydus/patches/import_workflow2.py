import frappe
from frappe.core.doctype.data_import.data_import import import_file

def execute():
    path = frappe.get_app_path('zydus','patches','imports','updated_workflow_action_master.csv')
    import_file('Workflow Action Master', path, 'Insert',console=True)
    path = frappe.get_app_path('zydus','patches','imports','updated_workflow.csv')
    import_file('Workflow', path, 'Insert',console=True)