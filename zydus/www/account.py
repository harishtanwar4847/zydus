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
        context['trending_now_list'] = frappe.db.sql("""select B.color,P.name,B.brand_logo,P.title,count(V.reference_name) as view,concat(P.month," ",P.year) as month_year from `tabProject` as P  left join `tabBrand` as B on P.brand = B.name left join `tabView Log` as V on V.reference_name=P.name and V.reference_doctype="Project" group by P.name order by count(V.reference_name) desc limit 6 """,as_dict=True)
        for trending_now in context['trending_now_list']:
            trending_now['number_of_files'] = len(get_attachments("Project",trending_now.name))
            
        context["reminders"]=frappe.db.get_list("ToDo",fields=["name","title","description","owner","modified_by","date"], order_by ='date asc',debug=1,filters={"owner":frappe.session.user,"status":"open"},limit_page_length=10)

    # due_by calculation
        for reminder in context['reminders']:
            reminder['due_by'] = zydus.pretty_date_future(reminder['date'].strftime("%Y-%m-%d"))

    
        context['favourites'] = frappe.db.sql("""  select T.doctype,T.owner,T.route,T.liked_by,T.name,T.title,T.month_year,B.color,T.brand from (select docstatus, owner, "Project" as doctype, P.route,P._liked_by as liked_by,P.brand,P.name,P.title,concat(P.month," ",P.year) as month_year from `tabProject` as P where owner= %s and P.docstatus = 1 and P._liked_by like  %s    union         select docstatus, owner, "Datasheet" as doctype, D.route, D._liked_by as liked_by,D.brand,D.name,D.title,concat(D.month," ",D.year) as month_year from `tabDatasheet`as D where owner = %s and D.docstatus = 1 and D._liked_by like  %s  ) as T left join `tabBrand` as B on T.brand = B.name  order by modified desc limit 10; """, (frappe.session.user,"%{}%".format(frappe.session.user),frappe.session.user,"%{}%".format(frappe.session.user)),as_dict=1,debug=1)
        for favourite in context['favourites']:
            favourite['attachments'] = get_attachments(favourite.doctype,favourite.name)
            favourite['is_liked'] = frappe.session.user in json.loads(favourite['liked_by'] or '[]')
            

    