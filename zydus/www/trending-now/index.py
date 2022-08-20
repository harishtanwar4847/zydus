
import frappe
import zydus
from frappe.desk.form.load import get_attachments
import json

def get_context(context):
    context['no_cache'] = 1
    context['roles'] =  frappe.get_roles(frappe.session.user)
    context['allowed_roles'] = ['KMS Uploader', 'KMS Downloader', 'KMS Admin']
    # Sauce: https://stackoverflow.com/a/50633946/9403680
    context['access_allowed'] = any(role in context['roles'] for role in context['allowed_roles'])

    if context['access_allowed']:
        # context['trending_now_list'] = frappe.db.sql("""select T.owner,T.doctype,T.route,T.liked_by,T.name,T.title,T.month_year,T.workflow_state,B.color,B.brand_logo,U.full_name,U.user_image,count(V.reference_name) as view_count from 
        # (select docstatus, "Project" as doctype,P.owner,P.route,P._liked_by as liked_by,P.brand,P.name,P.p_title as title,P.workflow_state,concat(P.month," ",P.year) as month_year from `tabProject` as P 
        # union
        # select docstatus, "Datasheet" as doctype,D.owner, D.route, D._liked_by as liked_by,D.brand,D.name,D.d_title as title,D.workflow_state,concat(D.month," ",D.year) as month_year from `tabDatasheet`as D) as T left join `tabBrand` as B on T.brand = B.name left join `tabUser`as U on U.name = T.owner left join `tabView Log` as V on V.reference_name= T.name and V.reference_doctype= T.doctype and T.workflow_state = "pending" group by T.name having view_count > 0 order by view_count desc limit 16 """,as_dict=True,debug=1)
        context['trending_now_list'] = frappe.db.sql("""
        select T.modified,T.doctype,T.owner,T.route,T.name,T.title,T.type,T.liked_by,T.agency,T.month_year,B.color,T.brand,T.workflow_state,U.full_name,U.full_name,U.user_image
        from (select modified,docstatus, owner, "Project" as doctype, P.route,P.brand, P.project_type as type,P._liked_by as liked_by,P.agency,P.workflow_state ,P.name,P.p_title as title,concat(P.month," ",P.year) as month_year from `tabProject` as P 
        where P.workflow_state="pending"   union         
        select modified,docstatus, owner, "Datasheet" as doctype, D.route,D.brand,D.data_type as type,D._liked_by as liked_by,D.agency,D.workflow_state ,D.name,D.d_title as title,concat(D.month," ",D.year) as month_year from `tabDatasheet`as D where D.workflow_state="pending" ) as T left join `tabBrand` as B on T.brand = B.name left join `tabUser`as U on U.name = T.owner  order by modified desc limit 16 """,as_dict=True,debug=1)
        for trending_now in context['trending_now_list']:
            trending_now['attachments'] = get_attachments(trending_now.doctype, trending_now.name)
            trending_now['is_liked'] = frappe.session.user in json.loads(trending_now['liked_by'] or '[]')
            trending_now["four_columns"]=True