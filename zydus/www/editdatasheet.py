from datetime import date
import frappe
from frappe.utils import pretty_date, now, add_to_date
import zydus
def get_context(context): 
    context['no_cache'] = 1
    context['roles'] =  frappe.get_roles(frappe.session.user)
    context['user_allowed_roles'] = ['KMS Uploader', 'KMS Downloader']
    context['admin_allowed_roles'] = ['KMS Admin']
    context['user_access_allowed'] = any(role in context['roles'] for role in context['user_allowed_roles'])
    context['admin_access_allowed'] = any(role in context['roles'] for role in context['admin_allowed_roles'])
    context.doc=frappe.get_doc("Datasheet",frappe.form_dict.edit)
    context.user_tag=str(context.doc._user_tags).split(",")[1:]
    context.color=frappe.get_value("Brand",{"name":context.doc.brand},"color")
    context.username=frappe.get_value("User",{"email":context.doc.owner},"full_name")
    context.image=frappe.get_value("User",{"email":context.doc.owner},"user_image")
    context.userfullname =frappe.db.get_value("User",frappe.session.user,"full_name")
    context['attachments'] = frappe.desk.form.load.get_attachments('Datasheet', frappe.form_dict.edit)
    for attachment in context['attachments']:
        file_ext=attachment['file_name']
        attachment['ext']=file_ext.rsplit('.', 1)[1]
    context['brands'] = [brand.name for brand in frappe.get_all('Brand')]
    context['agencies'] = [agency.name for agency in frappe.get_all('Agency')]
    context['data_types'] = [data_type.name for data_type in frappe.get_all('Data Type')]
    context["edit_datasheets"]=frappe.db.get_list("Datasheet",fields=["name","d_title","brand"],filters={"owner":frappe.session.user})
    context["notifications"] = frappe.db.get_all("Notification Log",fields=["subject","creation"], filters={'for_user': frappe.session.user}, limit_page_length=5)
    for notification in context['notifications']:
        notification['creations'] = pretty_date(notification['creation'])
    context["all_comments"]=frappe.db.sql(""" select C.content,C.reference_name,C.reference_doctype,C.comment_by,C.creation from `tabComment` as C left join `tabDatasheet`  as D on reference_name = D.name where C.reference_name = %s and C.content != "" and C.comment_type="Comment" order by C.creation desc limit 10""",(context.doc.name),as_dict=True)
    for comment in context['all_comments']:
        comment['creations'] = pretty_date(comment['creation'])
    
        

    