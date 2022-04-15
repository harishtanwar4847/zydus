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
        context['trending_now_list'] = frappe.db.sql("""select P.route,P._liked_by as liked_by,B.color,P.name,B.brand_logo,P.title,count(V.reference_name) as view,concat(P.month," ",P.year) as month_year from `tabProject` as P  left join `tabBrand` as B on P.brand = B.name left join `tabView Log` as V on V.reference_name=P.name and V.reference_doctype="Project" group by P.name having count(V.reference_name) > 0 order by count(V.reference_name) desc limit 6 """,as_dict=True)
        for trending_now in context['trending_now_list']:
            trending_now['attachments'] = get_attachments("Project",trending_now.name)

        context['my_uploads'] = frappe.db.sql(""" select P.name,P._liked_by as liked_by,route,title,color,brand,concat(month," ",year)as month_year from `tabProject` P left join `tabBrand` on P.brand = tabBrand.name group by P.name  limit 10 """,as_dict=1)
        for my_upload in context['my_uploads']:
            my_upload['attachments'] = get_attachments("Project",my_upload.name)
        
        context["reminders"]=frappe.db.get_list("ToDo",fields=["title","description","owner","modified_by","date"],debug=1,filters={"owner":frappe.session.user,"status":"open"},limit_page_length=5)
        
      
        # due_by calculation
        for reminder in context['reminders']:
            reminder['due_by'] = zydus.pretty_date_future(reminder['date'].strftime("%Y-%m-%d"))
        
        
        context["notifications"] = frappe.db.get_all("Notification Log",fields=["subject","creation"],limit_page_length=5)

        for notification in context['notifications']:
            notification['creations'] = pretty_date(notification['creation'])
            
                  