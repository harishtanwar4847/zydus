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
        P_filters = ["P.docstatus = 1"]
        P_or_filters = []
        if frappe.form_dict.q:
            for x in frappe.form_dict.q.strip().split():
                or_filters.append("""P.brand like "%{}%" """.format(x))
                or_filters.append("""P.agency like "%{}%" """.format(x))
                #or_filters.append("""P.project_type like "%{}%" """.format(x))
                or_filters.append("""P.month like "%{}%" """.format(x))
                or_filters.append("""P.year like "%{}%" """.format(x))
                or_filters.append("""P.title like "%{}%" """.format(x))
                or_filters.append("""P._user_tags like "%{}%" """.format(x))
        D_filters = ["D.docstatus = 1"]
        D_or_filters = []
        if frappe.form_dict.q:
            for x in frappe.form_dict.q.strip().split():
                or_filters.append("""D.brand like "%{}%" """.format(x))
                or_filters.append("""D.agency like "%{}%" """.format(x))
                or_filters.append("""D.month like "%{}%" """.format(x))
                or_filters.append("""D.year like "%{}%" """.format(x))
                or_filters.append("""D.title like "%{}%" """.format(x))
                or_filters.append("""D._user_tags like "%{}%" """.format(x))
        
        clauses = {
            'P_and_where_clauses': ' P_and '.join(filters),
            'P_or_where_clauses': ' P_or '.join(or_filters),
            'D_and_where_clauses': ' D_and '.join(filters),
            'D_or_where_clauses': ' D_or '.join(or_filters),
        }

        context['search_results'] = frappe.db.sql("""select T.doctype,T.route,T.liked_by,T.name,T.title,T.month_year,B.color,B.brand_logo,count(V.reference_name) as view_count from 
        (select docstatus, "Project" as doctype, P.route,P._liked_by as liked_by,P.brand,P.name,P.title,concat(P.month," ",P.year) as month_year,P.agency,P._user_tags from `tabProject` as P   where {P_and_where_clauses} and ({P_or_where_clauses})
        union
        select docstatus, "Datasheet" as doctype, D.data_type, D._liked_by as liked_by,D.brand,D.name,D.title,concat(D.month," ",D.year) as month_year,D.agency,D._user_tags from `tabDatasheet`as D   where {D_and_where_clauses} and ({D_or_where_clauses})) as T left join `tabBrand` as B on T.brand = B.name left join `tabView Log` as V on V.reference_name= T.name and V.reference_doctype= T.doctype and T.docstatus = 1 group by T.name having view_count > 0 order by view_count desc
        group by T.name """.format(**clauses), as_dict=True, debug=1)

        for search_result in context['search_results']:
            search_result['attachments'] = get_attachments('Project', search_result.name)
            search_result['liked_by'] = ','.join(json.loads(search_result['liked_by'] or '[]'))
            
                  