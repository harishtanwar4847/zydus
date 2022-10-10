import frappe
from frappe.core.doctype.data_import.data_import import import_file

def execute():
    path = frappe.get_app_path('zydus','patches','imports','workflow_action_master_submit.csv')
    import_file('Workflow Action Master', path, 'Insert',console=True)