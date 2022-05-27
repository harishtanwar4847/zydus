import frappe
import zydus
from frappe.desk.form.load import get_attachments
from frappe.utils import pretty_date, now, add_to_date

def get_context(context):
    context['roles'] =  frappe.get_roles(frappe.session.user)
    context['allowed_roles'] = ['KMS Uploader', 'KMS Downloader', 'KMS Admin']
    # Sauce: https://stackoverflow.com/a/50633946/9403680
    context['access_allowed'] = any(role in context['roles'] for role in context['allowed_roles'])

    if context['access_allowed']:
        context['faqs'] = frappe.get_all('FAQ', fields=['name', 'question', 'answer'])  


        context["notifications"] = frappe.db.get_all("Notification Log",fields=["subject","creation"], filters={'for_user': frappe.session.user}, limit_page_length=5)

        for notification in context['notifications']:
            notification['creations'] = pretty_date(notification['creation'])
            
