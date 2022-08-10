
import frappe
from frappe.utils import pretty_date, now, add_to_date

def get_context(context): 
    context['no_cache'] = 1
    context['roles'] =  frappe.get_roles(frappe.session.user)
    context['allowed_roles'] = ['KMS Uploader', 'KMS Downloader', 'KMS Admin']
    # Sauce: https://stackoverflow.com/a/50633946/9403680
    context['access_allowed'] = any(role in context['roles'] for role in context['allowed_roles'])


    if context['access_allowed']:
        context.doc=frappe.get_doc("Project",frappe.form_dict.edit)
        context.user_tag=str(context.doc._user_tags).split(",")[1:]
        context.market=[i.city for i in context.doc.markets]
        context.color=frappe.get_value("Brand",{"name":context.doc.brand},"color")
        context.username=frappe.get_value("User",{"email":context.doc.owner},"full_name")
        context.image=frappe.get_value("User",{"email":context.doc.owner},"user_image")
        context['attachments'] = frappe.desk.form.load.get_attachments('Project', frappe.form_dict.edit)
        for attachment in context['attachments']:
            file_ext=attachment['file_name']
            attachment['ext']=file_ext.rsplit('.', 1)[1]

        context['brands'] = [brand.name for brand in frappe.get_all('Brand')]
        context['agencies'] = [agency.name for agency in frappe.get_all('Agency')]
        context['project_types'] = [project_type.name for project_type in frappe.get_all('Project Type')]
        context['data_types'] = [data_type.name for data_type in frappe.get_all('Data Type')]
        context['cities'] = [city.name for city in frappe.get_all('City')]
        context["edit_projects"]=frappe.db.get_list("Project",fields=["name","p_title","brand"],filters={"owner":frappe.session.user})
        context["notifications"] = frappe.db.get_all("Notification Log",fields=["subject","creation"], filters={'for_user': frappe.session.user}, limit_page_length=5)

        for notification in context['notifications']:
            notification['creations'] = pretty_date(notification['creation'])

        

        
    