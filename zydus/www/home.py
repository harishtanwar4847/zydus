import frappe
import zydus
from frappe.desk.form.load import get_attachments
from frappe.utils import pretty_date, now, add_to_date
import json

def get_context(context):
    context['roles'] =  frappe.get_roles(frappe.session.user)
    context['allowed_roles'] = ['KMS Uploader', 'KMS Downloader', 'KMS Admin']
    # Sauce: https://stackoverflow.com/a/50633946/9403680
    context['access_allowed'] = any(role in context['roles'] for role in context['allowed_roles'])

    if context['access_allowed']:
        context['trending_now_list'] = frappe.db.sql("""select T.doctype,T.route,T.liked_by,T.name,T.title,T.month_year,B.color,B.brand_logo,count(V.reference_name) as view_count from 
        (select docstatus, "Project" as doctype, P.route,P._liked_by as liked_by,P.brand,P.name,P.title,concat(P.month," ",P.year) as month_year from `tabProject` as P 
        union
        select docstatus, "Datasheet" as doctype, D.route, D._liked_by as liked_by,D.brand,D.name,D.title,concat(D.month," ",D.year) as month_year from `tabDatasheet`as D) as T left join `tabBrand` as B on T.brand = B.name left join `tabView Log` as V on V.reference_name= T.name and V.reference_doctype= T.doctype and T.docstatus = 1 group by T.name having view_count > 0 order by view_count desc limit 6 """,as_dict=True)
        for trending_now in context['trending_now_list']:
            trending_now['attachments'] = get_attachments(trending_now.doctype,trending_now.name)
            trending_now['is_liked'] = frappe.session.user in json.loads(trending_now['liked_by'] or '[]')

        context['my_uploads'] = frappe.db.sql("""  select T.doctype,T.owner,T.route,T.liked_by,T.name,T.title,T.month_year,B.color,T.brand from (select docstatus, owner, "Project" as doctype, P.route,P._liked_by as liked_by,P.brand,P.name,P.title,concat(P.month," ",P.year) as month_year from `tabProject` as P where owner= %s and P.docstatus = 1        union         select docstatus, owner, "Datasheet" as doctype, D.route, D._liked_by as liked_by,D.brand,D.name,D.title,concat(D.month," ",D.year) as month_year from `tabDatasheet`as D where owner = %s and D.docstatus = 1) as T left join `tabBrand` as B on T.brand = B.name order by modified desc limit 10 """, (frappe.session.user,frappe.session.user),as_dict=1,debug=1)
        for my_upload in context['my_uploads']:
            my_upload['attachments'] = get_attachments(my_upload.doctype,my_upload.name)
            my_upload['is_liked'] = frappe.session.user in json.loads(my_upload['liked_by'] or '[]')
        
        context["reminders"]=frappe.db.get_list("ToDo",fields=["name","title","description","owner","modified_by","date"], order_by ='date asc',debug=1,filters={"owner":frappe.session.user,"status":"open"},limit_page_length=5)
        
      
        # due_by calculation
        for reminder in context['reminders']:
            reminder['due_by'] = zydus.pretty_date_future(reminder['date'].strftime("%Y-%m-%d"))
        
        
        context["notifications"] = frappe.db.get_all("Notification Log",fields=["subject","creation"], filters={'for_user': frappe.session.user}, limit_page_length=5)

        for notification in context['notifications']:
            notification['creations'] = pretty_date(notification['creation'])
            
                  