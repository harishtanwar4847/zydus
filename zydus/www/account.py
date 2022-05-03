import frappe
import zydus
import json
from frappe.desk.form.load import get_attachments
from frappe.utils import pretty_date, now, add_to_date

def get_context(context):
    context['roles'] =  frappe.get_roles(frappe.session.user)
    context['allowed_roles'] = ['KMS Uploader', 'KMS Downloader', 'KMS Admin']
    # Sauce: https://stackoverflow.com/a/50633946/9403680
    context['access_allowed'] = any(role in context['roles'] for role in context['allowed_roles'])

    if context['access_allowed']:
        context['trending_now_list'] = frappe.db.sql("""select B.color,P.name,B.brand_logo,P.title,count(V.reference_name) as view,concat(P.month," ",P.year) as month_year from `tabProject` as P  left join `tabBrand` as B on P.brand = B.name left join `tabView Log` as V on V.reference_name=P.name and V.reference_doctype="Project" group by P.name order by count(V.reference_name) desc limit 6 """,as_dict=True)
        for trending_now in context['trending_now_list']:
            trending_now['number_of_files'] = len(get_attachments("Project",trending_now.name))

        
        context['my_uploads'] = frappe.db.sql("""  select T.doctype,T.owner,T.route,T.liked_by,T.name,T.title,T.month_year,B.color,T.brand,T.workflow_state from (select docstatus, owner, "Project" as doctype, P.route,P._liked_by as liked_by,P.brand,P.name,P.title,concat(P.month," ",P.year) as month_year,P.workflow_state from `tabProject` as P where owner= %s        union         select docstatus, owner, "Datasheet" as doctype, D.route, D._liked_by as liked_by,D.brand,D.name,D.title,concat(D.month," ",D.year) as month_year,D.workflow_state  from `tabDatasheet`as D where owner = %s) as T left join `tabBrand` as B on T.brand = B.name order by modified desc limit 10 """, (frappe.session.user,frappe.session.user),as_dict=1,debug=1)
        for my_upload in context['my_uploads']:
            my_upload['attachments'] = get_attachments(my_upload.doctype,my_upload.name)
            my_upload['is_liked'] = frappe.session.user in json.loads(my_upload['liked_by'] or '[]')
            

        context["my_notifications"] = frappe.db.get_all("Notification Log",fields=["subject","creation"])

        for my_notification in context['my_notifications']:
            my_notification['creations'] = pretty_date(my_notification['creation'])

        context["notifications"] = frappe.db.get_all("Notification Log",fields=["subject","creation"],limit_page_length=5)

        for notification in context['notifications']:
            notification['creations'] = pretty_date(notification['creation'])