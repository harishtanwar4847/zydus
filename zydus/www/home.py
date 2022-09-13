from distutils.log import debug
import frappe
import zydus
from frappe.desk.form.load import get_attachments
from frappe.utils import pretty_date, now, add_to_date
import json

def get_context(context):
    context['no_cache'] = 1
    context['roles'] =  frappe.get_roles(frappe.session.user)
    context['user_allowed_roles'] = ['KMS Uploader', 'KMS Downloader']
    context['admin_allowed_roles'] = ['KMS Admin']
    # Sauce: https://stackoverflow.com/a/50633946/9403680
    context['user_access_allowed'] = any(role in context['roles'] for role in context['user_allowed_roles'])
    context['admin_access_allowed'] = any(role in context['roles'] for role in context['admin_allowed_roles'])
    if context['admin_access_allowed'] :
        context['trending_now_list'] = frappe.db.sql("""
        select T.modified,T.doctype,T.owner,T.route,T.name,T.title,T.type,T.liked_by,T.agency,T.month_year,B.color,B.brand_logo,T.brand,T.workflow_state,U.full_name,U.full_name,U.user_image
        from (select modified,docstatus, owner, "Project" as doctype, P.route,P.brand, P.project_type as type,P._liked_by as liked_by,P.agency,P.workflow_state ,P.name,P.p_title as title,concat(P.month," ",P.year) as month_year from `tabProject` as P 
        where P.workflow_state="pending"   union         
        select modified,docstatus, owner, "Datasheet" as doctype, D.route,D.brand,D.data_type as type,D._liked_by as liked_by,D.agency,D.workflow_state ,D.name,D.d_title as title,concat(D.month," ",D.year) as month_year from `tabDatasheet`as D where D.workflow_state="pending" ) as T left join `tabBrand` as B on T.brand = B.name left join `tabUser`as U on U.name = T.owner  order by modified desc limit 6 """,as_dict=True,debug=1)
        for trending_now in context['trending_now_list']:
            trending_now['attachments'] = get_attachments(trending_now.doctype,trending_now.name)
            trending_now['is_liked'] = frappe.session.user in json.loads(trending_now['liked_by'] or '[]')

        context['my_uploads'] = frappe.db.sql("""  select T.modified,T.doctype,T.owner,T.route,T.liked_by,T.name,T.title,T.month_year,B.color,T.brand from (select modified,docstatus, owner, "Project" as doctype, P.route,P._liked_by as liked_by,P.brand,P.name,P.p_title as title,concat(P.month," ",P.year) as month_year from `tabProject` as P where owner= %s and P.docstatus = 1        union         select modified,docstatus, owner, "Datasheet" as doctype, D.route, D._liked_by as liked_by,D.brand,D.name,D.d_title as title,concat(D.month," ",D.year) as month_year from `tabDatasheet`as D where owner = %s and D.docstatus = 1) as T left join `tabBrand` as B on T.brand = B.name order by modified desc limit 10 """, (frappe.session.user,frappe.session.user),as_dict=1,debug=1)
        for my_upload in context['my_uploads']:
            my_upload['attachments'] = get_attachments(my_upload.doctype,my_upload.name)
            my_upload['is_liked'] = frappe.session.user in json.loads(my_upload['liked_by'] or '[]')
        
     
        context["reminders"] = frappe.db.sql(""" select U.user_image,U.full_name,T.name,T.title,T.description,T.owner,T.modified_by,T.date from `tabToDo` as T left join `tabUser` as U on T.owner = U.name where status = "open" and (T.created_by = %s or T.owner = %s)order by date asc limit 5 """,(frappe.session.user,frappe.session.user),as_dict=1,debug=1)
       
        

        # due_by calculation
        for reminder in context['reminders']:
            reminder['due_by'] = zydus.pretty_date_future(reminder['date'].strftime("%Y-%m-%d"))
        
        context["notifications"] = frappe.db.get_all("Notification Log",fields=["subject","creation"], filters={'for_user': frappe.session.user}, limit_page_length=5,order_by="modified desc",debug=True)
      
        for notification in context['notifications']:
            notification['creations'] = pretty_date(notification['creation'])

    else:
        context['trending_now_list'] = frappe.db.sql("""select T.owner,T.doctype,T.route,T.liked_by,T.name,T.title,T.month_year,T.workflow_state,B.color,B.brand_logo,U.full_name,U.user_image,count(V.reference_name) as view_count from 
        (select docstatus, "Project" as doctype,P.owner,P.route,P._liked_by as liked_by,P.brand,P.name,P.p_title as title,P.workflow_state,concat(P.month," ",P.year) as month_year from `tabProject` as P 
        union
        select docstatus, "Datasheet" as doctype,D.owner, D.route, D._liked_by as liked_by,D.brand,D.name,D.d_title as title,D.workflow_state,concat(D.month," ",D.year) as month_year from `tabDatasheet`as D) as T left join `tabBrand` as B on T.brand = B.name left join `tabUser`as U on U.name = T.owner left join `tabView Log` as V on V.reference_name= T.name and V.reference_doctype= T.doctype and T.workflow_state = "approved" group by T.name having view_count > 0 order by view_count desc limit 6 """,as_dict=True,debug=1)
        for trending_now in context['trending_now_list']:
            trending_now['attachments'] = get_attachments(trending_now.doctype,trending_now.name)
            trending_now['is_liked'] = frappe.session.user in json.loads(trending_now['liked_by'] or '[]')
        
        context['my_uploads'] = frappe.db.sql("""  select T.modified,T.doctype,T.owner,T.route,T.liked_by,T.name,T.title,T.month_year,B.color,T.brand from (select modified,docstatus, owner, "Project" as doctype, P.route,P._liked_by as liked_by,P.brand,P.name,P.p_title as title,concat(P.month," ",P.year) as month_year from `tabProject` as P where owner= %s and P.docstatus = 1        union         select modified,docstatus, owner, "Datasheet" as doctype, D.route, D._liked_by as liked_by,D.brand,D.name,D.d_title as title,concat(D.month," ",D.year) as month_year from `tabDatasheet`as D where owner = %s and D.docstatus = 1) as T left join `tabBrand` as B on T.brand = B.name order by modified desc limit 10 """, (frappe.session.user,frappe.session.user),as_dict=1,debug=1)
        for my_upload in context['my_uploads']:
            my_upload['attachments'] = get_attachments(my_upload.doctype,my_upload.name)
            my_upload['is_liked'] = frappe.session.user in json.loads(my_upload['liked_by'] or '[]')
        
    
        context["reminders"] = frappe.db.sql(""" select U.user_image,U.full_name,T.name,T.title,T.description,T.owner,T.modified_by,T.date from `tabToDo` as T left join `tabUser` as U on T.owner = U.name where status = "open" and T.owner = %s order by date asc limit 5 """,(frappe.session.user),as_dict=1,debug=1)
      
        # due_by calculation
        for reminder in context['reminders']:
            reminder['due_by'] = zydus.pretty_date_future(reminder['date'].strftime("%Y-%m-%d"))
        
        
        context["notifications"] = frappe.db.get_all("Notification Log",fields=["subject","creation"], filters={'for_user': frappe.session.user}, limit_page_length=5,order_by="modified desc",debug=True)
        # context["notifications"]=frappe.db.sql("""select subject, creation,owner,for_user from 
        # `tabNotification Log` 
        # where (owner = %s and for_user = %s and subject LIKE 'you%%') 
        # OR (owner <> %s and for_user = %s and subject LIKE 'Admin%%') 
        # order by modified desc limit 5""",
        # (frappe.session.user,frappe.session.user,frappe.session.user,frappe.session.user),debug=True)


        for notification in context['notifications']:
            notification['creations'] = pretty_date(notification['creation'])
            
                  