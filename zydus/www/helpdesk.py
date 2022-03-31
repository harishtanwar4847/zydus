from ast import Pass
import frappe
import zydus
from frappe.desk.form.load import get_attachments

def get_context(context):
    context['roles'] =  frappe.get_roles(frappe.session.user)
    context['allowed_roles'] = ['KMS Uploader', 'KMS Downloader', 'KMS Admin']
    # Sauce: https://stackoverflow.com/a/50633946/9403680
    context['access_allowed'] = any(role in context['roles'] for role in context['allowed_roles'])

    if context['access_allowed']:
         context['Help_Desk'] =frappe.db.sql("""select full_name,designation,email,mobile_number from `tabHelp Desk` """,as_dict=True)
        
             
         
             