
import frappe
import zydus
from frappe.desk.form.load import get_attachments
import json

def get_context(context):
    context['no_cache'] = 1
    context['roles'] =  frappe.get_roles(frappe.session.user)
    context['user_allowed_roles'] = ['KMS Uploader', 'KMS Downloader']
    context['admin_allowed_roles'] = ['KMS Admin']
    # Sauce: https://stackoverflow.com/a/50633946/9403680
    context['user_access_allowed'] = any(role in context['roles'] for role in context['user_allowed_roles'])
    context['admin_access_allowed'] = any(role in context['roles'] for role in context['admin_allowed_roles'])
    
    where_clause=""
    viewlog_left_join = ""
    order_by=""
    view_count=""
    if context['admin_access_allowed']:
        where_clause= "pending"
        order_by= "modified"
    else:
        where_clause= "approved"
        viewlog_left_join = "left join `tabView Log` as V on V.reference_name= T.name and V.reference_doctype= T.doctype group by T.name having view_count > 0"
        order_by= "view_count"
        view_count= ", count(V.reference_name) as view_count" 

    context['trending_now_list'] = frappe.db.sql("""
        select T.modified,T.doctype,T.owner,T.route,T.name,T.title,T.type,T.liked_by,T.agency,T.month_year,B.color,B.brand_logo,T.brand,T.workflow_state,U.full_name,U.full_name,U.user_image {view_count} 
        from (select modified,docstatus, owner, "Project" as doctype, P.route,P.brand, P.project_type as type,P._liked_by as liked_by,P.agency,P.workflow_state ,P.name,P.p_title as title,concat(P.month," ",P.year) as month_year from `tabProject` as P where P.workflow_state="{where_clause}" union 
        select modified,docstatus, owner, "Datasheet" as doctype, D.route,D.brand,D.data_type as type,D._liked_by as liked_by,D.agency,D.workflow_state ,D.name,D.d_title as title,concat(D.month," ",D.year) as month_year from `tabDatasheet`as D where D.workflow_state="{where_clause}" ) as T left join `tabBrand` as B on T.brand = B.name left join `tabUser`as U on U.name = T.owner  {viewlog_left_join} order by {order_by} desc limit 16 """.format(view_count=view_count,where_clause=where_clause,viewlog_left_join=viewlog_left_join,order_by=order_by),as_dict=True)
    for trending_now in context['trending_now_list']:
        trending_now['attachments'] = get_attachments(trending_now.doctype, trending_now.name)
        trending_now['is_liked'] = frappe.session.user in json.loads(trending_now['liked_by'] or '[]')
        trending_now["four_columns"]=True
    
    context["notifications"] = frappe.db.get_all("Notification Log",fields=["subject","creation"], filters={'for_user': frappe.session.user}, limit_page_length=5,order_by="modified desc") 
    for notification in context['notifications']:
        notification['creations'] = pretty_date(notification['creation'])
