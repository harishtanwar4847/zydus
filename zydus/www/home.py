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
        context['trending_now_list'] = frappe.db.sql("""select B.color,P.name,B.brand_logo,P.title,count(V.reference_name) as view,concat(P.month," ",P.year) as month_year from `tabProject` as P  left join `tabBrand` as B on P.brand = B.name left join `tabView Log` as V on V.reference_name=P.name and V.reference_doctype="Project" group by P.name having count(V.reference_name) > 0 order by count(V.reference_name) desc limit 6 """,as_dict=True)
        for trending_now in context['trending_now_list']:
            trending_now['number_of_files'] = len(get_attachments("Project",trending_now.name))

        context['my_uploads'] = frappe.db.sql(""" select title,color,brand,count(file_name) as number_of_files,concat(month," ",year)as month_year from `tabProject` left join `tabBrand` on tabProject.brand = tabBrand.name left join `tabFile` on `tabFile`.attached_to_name = `tabProject`.name and `tabFile`.attached_to_doctype = "Project" group by `tabProject`.name  limit 10 """,as_dict=1)
        
        context["reminders"]=frappe.db.get_list("ToDo",fields=["title","description","owner","modified_by","date"],debug=1,filters={"owner":frappe.session.user,"status":"open"},limit_page_length=5)
        
      
        # due_by calculation
        for reminder in context['reminders']:
            reminder['due_by'] = zydus.pretty_date_future(reminder['date'].strftime("%Y-%m-%d"))
        
        
        context["notifications"] = frappe.db.get_all("Notification Log",fields=["subject","creation"],limit_page_length=5)

        for notification in context['notifications']:
            notification['creations'] = pretty_date(notification['creation'])
            
                  