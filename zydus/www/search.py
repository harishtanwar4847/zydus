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
        context['brands'] = [brand.name for brand in frappe.get_all('Brand')]
        context['agencies'] = [agency.name for agency in frappe.get_all('Agency')]
        context['project_types'] = [project_type.name for project_type in frappe.get_all('Project Type')]

        context['search_tags'] = []
        context['search_results'] = []
        if not frappe.form_dict:
            return


        filters = ["P.docstatus = 1"]
        if frappe.form_dict.brand:
            context['search_tags'].append(frappe.form_dict.brand)
            filters.append("""P.brand = "{}" """.format(frappe.form_dict.brand))
        if frappe.form_dict.agency:
            context['search_tags'].append(frappe.form_dict.agency)
            filters.append("""P.agency = "{}" """.format(frappe.form_dict.agency))
        if frappe.form_dict.project_type:
            context['search_tags'].append(frappe.form_dict.project_type)
            filters.append("""P.project_type = "{}" """.format(frappe.form_dict.project_type))
        if frappe.form_dict.month:
            filters.append("""P.month = "{}" """.format(frappe.form_dict.month))
        if frappe.form_dict.year:
            filters.append("""P.year = "{}" """.format(frappe.form_dict.year))
        context['search_tags'].append('{} {}'.format(frappe.form_dict.month or '', frappe.form_dict.year or '').strip())
        
        
        or_filters = []
        if frappe.form_dict.project_name:
            context['search_tags'].append(frappe.form_dict.project_name)
            for name in frappe.form_dict.project_name.strip().split():
                or_filters.append("""P.title like "%{}%" """.format(name))
        if frappe.form_dict.tags:
            for tag in frappe.form_dict.tags.strip().split(','):
                or_filters.append("""P._user_tags like "%{}%" """.format(tag))
                context['search_tags'].append('#{}'.format(tag))
        
        clauses = {
            'and_where_clauses': ' and '.join(filters),
            'or_where_clauses': 'and (' + ' or '.join(or_filters) + ')'
        }
        if clauses['or_where_clauses'] == 'and ()':
            clauses['or_where_clauses'] = ''

        context['search_results'] = frappe.db.sql("""select P.docstatus, P.description, P._user_tags, project_type, agency, P.route,P._liked_by as liked_by,P.brand,P.name,P.title,concat(P.month," ",P.year) as month_year, B.brand_logo, B.color, P.project_type from `tabProject` as P  
        left join `tabBrand` as B on P.brand = B.name 
        where {and_where_clauses} {or_where_clauses}
        group by P.name """.format(**clauses), as_dict=True, debug=1)

        for search_result in context['search_results']:
            search_result['attachments'] = get_attachments('Project', search_result.name)
            search_result['is_liked'] = frappe.session.user in json.loads(search_result['liked_by'] or '')