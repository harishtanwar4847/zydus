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
        filters = ["P.docstatus = 1"]
        or_filters = []
        if frappe.form_dict.q:
            for x in frappe.form_dict.q.strip().split():
                or_filters.append("""P.brand like "%{}%" """.format(x))
                or_filters.append("""P.agency like "%{}%" """.format(x))
                or_filters.append("""P.project_type like "%{}%" """.format(x))
                or_filters.append("""P.month like "%{}%" """.format(x))
                or_filters.append("""P.year like "%{}%" """.format(x))
                or_filters.append("""P.title like "%{}%" """.format(x))
                or_filters.append("""P._user_tags like "%{}%" """.format(x))
        
        clauses = {
            'and_where_clauses': ' and '.join(filters),
            'or_where_clauses': ' or '.join(or_filters)
        }

        context['search_results'] = frappe.db.sql("""select P.docstatus, P.description, P._user_tags, project_type, agency, P.route,P._liked_by as liked_by,P.brand,P.name,P.title,concat(P.month," ",P.year) as month_year, B.brand_logo, B.color, P.project_type from `tabProject` as P  
        left join `tabBrand` as B on P.brand = B.name 
        where {and_where_clauses} and ({or_where_clauses})
        group by P.name """.format(**clauses), as_dict=True, debug=1)

        for search_result in context['search_results']:
            search_result['attachments'] = get_attachments('Project', search_result.name)
            search_result['is_liked'] = frappe.session.user in json.loads(search_result['liked_by'] or '')
            
                  