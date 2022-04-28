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
        context['types'] = [project_type.name for project_type in frappe.get_all('Project Type')]
        context['types'] += [data_type.name for data_type in frappe.get_all('Data Type')]

        context['search_tags'] = []
        context['search_results'] = []
        if not frappe.form_dict:
            return


        P_filters = ["P.docstatus = 1"]
        D_filters = ["D.docstatus = 1"]

        if frappe.form_dict.brand:
            context['search_tags'].append(frappe.form_dict.brand)
            P_filters.append("""P.brand = "{}" """.format(frappe.form_dict.brand))
            D_filters.append("""D.brand = "{}" """.format(frappe.form_dict.brand))
        if frappe.form_dict.agency:
            context['search_tags'].append(frappe.form_dict.agency)
            P_filters.append("""P.agency = "{}" """.format(frappe.form_dict.agency))
            D_filters.append("""D.agency = "{}" """.format(frappe.form_dict.agency))
        if frappe.form_dict.type:
            context['search_tags'].append(frappe.form_dict.type)
            P_filters.append("""P.project_type = "{}" """.format(frappe.form_dict.type))
            D_filters.append("""D.data_type = "{}" """.format(frappe.form_dict.type))
        if frappe.form_dict.month:
            P_filters.append("""P.month = "{}" """.format(frappe.form_dict.month))
            D_filters.append("""D.month = "{}" """.format(frappe.form_dict.month))
        if frappe.form_dict.year:
            P_filters.append("""P.year = "{}" """.format(frappe.form_dict.year))
            D_filters.append("""D.year = "{}" """.format(frappe.form_dict.year))
        context['search_tags'].append('{} {}'.format(frappe.form_dict.month or '', frappe.form_dict.year or '').strip())
        
    

        P_or_filters = []
        D_or_filters = []
        if frappe.form_dict.project_name:
            context['search_tags'].append(frappe.form_dict.project_name)
            for name in frappe.form_dict.project_name.strip().split():
                P_or_filters.append("""P.title like "%{}%" """.format(name))
                D_or_filters.append("""D.title like "%{}%" """.format(name))
        if frappe.form_dict.tags:
            for tag in frappe.form_dict.tags.strip().split(','):
                P_or_filters.append("""P._user_tags like "%{}%" """.format(tag))
                D_or_filters.append("""D._user_tags like "%{}%" """.format(tag))
                context['search_tags'].append('#{}'.format(tag))
        
        clauses = {
            'P_and_where_clauses': ' and '.join(P_filters),
            'P_or_where_clauses': ' and (' + ' or '.join(P_or_filters) +')',
            'D_and_where_clauses': ' and '.join(D_filters),
            'D_or_where_clauses': ' and (' + ' or '.join(D_or_filters) + ')'
        }
        if clauses['P_or_where_clauses'] == ' and ()':
            clauses['P_or_where_clauses'] = ''
        if clauses['D_or_where_clauses'] == ' and ()':
            clauses['D_or_where_clauses'] = ''


        context['search_results'] = frappe.db.sql("""select T.doctype,T.route,T.liked_by,T.name,T.title,T.month_year,B.color,T.brand,T.agency,T.type,T._user_tags,T.description,B.brand_logo,count(V.reference_name) as view_count from (select "Project" as doctype, P.docstatus, P.description, P._user_tags, agency, P.route,P._liked_by as liked_by,P.brand,P.name,P.title,concat(P.month," ",P.year) as month_year, P.project_type as type from `tabProject` as P  left join `tabBrand` as B on P.brand = B.name where {P_and_where_clauses} {P_or_where_clauses}
        union
        select "Datasheet" as doctype,D.docstatus, D.description, D._user_tags, D.agency, D.route,D._liked_by as liked_by,D.brand,D.name,D.title,concat(D.month," ",D.year) as month_year, D.data_type as type from `tabDatasheet` as D  left join `tabBrand` as B on D.brand = B.name where {D_and_where_clauses} {D_or_where_clauses}) as T left join `tabBrand` as B on T.brand = B.name left join `tabView Log` as V on V.reference_name= T.name and V.reference_doctype= T.doctype  group by T.name """.format(**clauses), as_dict=True, debug=1)

        for search_result in context['search_results']:
            search_result['attachments'] = get_attachments(search_result.doctype, search_result.name)
            search_result['is_liked'] = frappe.session.user in json.loads(search_result['liked_by'] or '[]')