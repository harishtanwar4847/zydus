import frappe
import zydus
from frappe.desk.form.load import get_attachments
from frappe.utils import pretty_date, now, add_to_date
import json
from frappe.utils import (cint, flt, has_gravatar, escape_html, format_datetime,
	now_datetime, get_formatted_email, today)


def get_context(context):
    context['no_cache'] = 1
    context['roles'] =  frappe.get_roles(frappe.session.user)
    context['admin_allowed_roles'] = ['KMS Admin']
    # Sauce: https://stackoverflow.com/a/50633946/9403680
    context['admin_access_allowed'] = any(role in context['roles'] for role in context['admin_allowed_roles'])

    if context['admin_access_allowed']:
        context['all_page_length'] = 12
        context['all_page'] = int(frappe.form_dict.all) if frappe.form_dict.all else 1
        context['all_page_offset'] = (context['all_page'] - 1) * context['all_page_length']
        context['all_page_from'] = context['all_page_offset'] + 1
        context['all'] = frappe.db.sql("""select T.modified,T.doctype,T.owner,T.route,T.name,T.title,T.liked_by,T.type,T.agency,T.month_year,B.color,T.brand,T.workflow_state,U.full_name,IF(T.doctype = 'Project','/editproject?edit=','/editdatasheet?edit=') as edit_url from (select modified,docstatus, owner, "Project" as doctype, P.route,P.brand, P.project_type as type,P.agency,P.workflow_state,P._liked_by as liked_by ,P.name,P.p_title as title,concat(P.month," ",P.year) as month_year from `tabProject` as P    union         select modified,docstatus, owner, "Datasheet" as doctype, D.route,D.brand,D.data_type as type,D.agency,D.workflow_state,D._liked_by as liked_by ,D.name,D.d_title as title,concat(D.month," ",D.year) as month_year from `tabDatasheet`as D) as T left join `tabBrand` as B on T.brand = B.name left join `tabUser`as U on U.name = T.owner where T.workflow_state IN ("approved","rejected","pending") order by modified desc limit %(limit)s offset %(offset)s""",{'limit': context['all_page_length'], 'offset': context['all_page_offset']} ,as_dict=True,debug=1)
        context['all_count'] = frappe.db.sql("""  select count(T.name) as count from (select P.name from `tabProject` as P         union         select D.name from `tabDatasheet` as D ) as T""",as_dict=1,debug=1)[0]['count']
        context['all_page_to'] = context['all_page'] * context['all_page_length']
        if context['all_page_to'] > context['all_count']:
            context['all_page_to'] = context['all_count']
        for all in context['all']:
            all['attachments'] = get_attachments(all.doctype,all.name)
            all['is_liked'] = frappe.session.user in json.loads(all['liked_by'] or '[]')

        

        context['approved_page_length'] = 12
        context['approved_page'] = int(frappe.form_dict.approved) if frappe.form_dict.approved else 1
        context['approved_page_offset'] = (context['approved_page'] - 1) * context['approved_page_length']
        context['approved_page_from'] = context['approved_page_offset'] + 1
        context['approved'] = frappe.db.sql("""select T.modified,T.doctype,T.owner,T.route,T.name,T.title,T.liked_by,T.type,T.agency,T.month_year,B.color,T.brand,T.workflow_state,U.full_name from (select modified,docstatus, owner, "Project" as doctype, P.route,P.brand, P.project_type as type,P.agency,P.workflow_state,P._liked_by as liked_by ,P.name,P.p_title as title,concat(P.month," ",P.year) as month_year from `tabProject` as P    union         select modified,docstatus, owner, "Datasheet" as doctype, D.route,D.brand,D.data_type as type,D.agency,D.workflow_state,D._liked_by as liked_by ,D.name,D.d_title as title,concat(D.month," ",D.year) as month_year from `tabDatasheet`as D) as T left join `tabBrand` as B on T.brand = B.name left join `tabUser`as U on U.name = T.owner where T.workflow_state = "approved"  order by modified desc limit %(limit)s offset %(offset)s""",{'limit': context['approved_page_length'], 'offset': context['approved_page_offset']} ,as_dict=True,debug=1)
        context['approved_count'] = frappe.db.sql("""  select count(T.name) as count from (select P.name from `tabProject` as P where P.workflow_state = "approved"        union         select D.name from `tabDatasheet` as D where D.workflow_state = "approved") as T """,as_dict=1,debug=1)[0]['count']
        context['approved_page_to'] = context['approved_page'] * context['approved_page_length']
        if context['approved_page_to'] > context['approved_count']:
            context['approved_page_to'] = context['approved_count']
        for approved in context['approved']:
            approved['attachments'] = get_attachments(approved.doctype,approved.name)
            approved['is_liked'] = frappe.session.user in json.loads(approved['liked_by'] or '[]')

        

        context['pending_page_length'] = 12
        context['pending_page'] = int(frappe.form_dict.pending) if frappe.form_dict.pending else 1
        context['pending_page_offset'] = (context['pending_page'] - 1) * context['pending_page_length']
        context['pending_page_from'] = context['pending_page_offset'] + 1
        context['pending'] = frappe.db.sql("""
        select T.modified,T.doctype,T.owner,T.route,T.name,T.title,T.type,T.liked_by,T.agency,T.month_year,B.color,T.brand,T.workflow_state,U.full_name,IF(T.doctype = 'Project','/editproject?edit=','/editdatasheet?edit=') as edit_url
        from (select modified,docstatus, owner, "Project" as doctype, P.route,P.brand, P.project_type as type,P._liked_by as liked_by,P.agency,P.workflow_state ,P.name,P.p_title as title,concat(P.month," ",P.year) as month_year from `tabProject` as P 
        where P.workflow_state="pending"   union         
        select modified,docstatus, owner, "Datasheet" as doctype, D.route,D.brand,D.data_type as type,D._liked_by as liked_by,D.agency,D.workflow_state ,D.name,D.d_title as title,concat(D.month," ",D.year) as month_year from `tabDatasheet`as D where D.workflow_state="pending" ) as T left join `tabBrand` as B on T.brand = B.name left join `tabUser`as U on U.name = T.owner  order by modified desc limit %(limit)s offset %(offset)s""",{'limit': context['pending_page_length'], 'offset': context['pending_page_offset']} ,as_dict=True,debug=1)
        context['pending_count'] = frappe.db.sql("""  select count(T.name) as count from (select P.name from `tabProject` as P where P.workflow_state = "pending"        union         select D.name from `tabDatasheet` as D where D.workflow_state = "pending") as T """,as_dict=1,debug=1)[0]['count']
        context['pending_page_to'] = context['pending_page'] * context['pending_page_length']
        if context['pending_page_to'] > context['pending_count']:
            context['pending_page_to'] = context['pending_count']
        for pending in context['pending']:
            pending['attachments'] = get_attachments(pending.doctype,pending.name)
            pending['is_liked'] = frappe.session.user in json.loads(pending['liked_by'] or '[]')

        

        context['rejected_page_length'] = 12
        context['rejected_page'] = int(frappe.form_dict.rejected) if frappe.form_dict.rejected else 1
        context['rejected_page_offset'] = (context['rejected_page'] - 1) * context['rejected_page_length']
        context['rejected_page_from'] = context['rejected_page_offset'] + 1
        context['rejected'] = frappe.db.sql("""select T.modified,T.doctype,T.owner,T.route,T.name,T.title,T.type,T.liked_by,T.agency,T.month_year,B.color,T.brand,T.workflow_state,U.full_name from (select modified,docstatus, owner, "Project" as doctype, P.route,P.brand, P.project_type as type,P._liked_by as liked_by,P.agency,P.workflow_state ,P.name,P.p_title as title,concat(P.month," ",P.year) as month_year from `tabProject` as P where P.workflow_state="rejected"   union         select modified,docstatus, owner, "Datasheet" as doctype, D.route,D.brand,D.data_type as type,D._liked_by as liked_by,D.agency,D.workflow_state ,D.name,D.d_title as title,concat(D.month," ",D.year) as month_year from `tabDatasheet`as D where D.workflow_state="rejected" ) as T left join `tabBrand` as B on T.brand = B.name left join `tabUser`as U on U.name = T.owner  order by modified desc limit %(limit)s offset %(offset)s""", {'limit': context['rejected_page_length'], 'offset': context['rejected_page_offset']} ,as_dict=True,debug=1)
        context['rejected_count'] = frappe.db.sql("""  select count(T.name) as count from (select P.name from `tabProject` as P where P.workflow_state = "rejected"        union         select D.name from `tabDatasheet` as D where D.workflow_state = "rejected") as T """,as_dict=1,debug=1)[0]['count']
        context['rejected_page_to'] = context['rejected_page'] * context['rejected_page_length']
        if context['rejected_page_to'] > context['rejected_count']:
            context['rejected_page_to'] = context['rejected_count']
        for rejected in context['rejected']:
            rejected['attachments'] = get_attachments(rejected.doctype,rejected.name)
            rejected['is_liked'] = frappe.session.user in json.loads(rejected['liked_by'] or '[]')
            


        context["notifications"] = frappe.db.get_all("Notification Log",fields=["subject","creation"], filters={'for_user': frappe.session.user}, limit_page_length=5,order_by="modified desc")

        for notification in context['notifications']:
            notification['creations'] = pretty_date(notification['creation'])
            