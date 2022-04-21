
import frappe
import zydus
from frappe.desk.form.load import get_attachments

def get_context(context):
    context['roles'] =  frappe.get_roles(frappe.session.user)
    context['allowed_roles'] = ['KMS Uploader', 'KMS Downloader', 'KMS Admin']
    # Sauce: https://stackoverflow.com/a/50633946/9403680
    context['access_allowed'] = any(role in context['roles'] for role in context['allowed_roles'])

    if context['access_allowed']:
        context['trending_now_list'] = frappe.db.sql("""select T.doctype,T.route,T.liked_by,T.name,T.title,T.month_year,B.color,B.brand_logo,count(V.reference_name) as view_count from 
        (select "Project" as doctype, P.route,P._liked_by as liked_by,P.brand,P.name,P.title,concat(P.month," ",P.year) as month_year from `tabProject` as P 
        union
        select "Datasheet" as doctype, D.data_type, D._liked_by as liked_by,D.brand,D.name,D.title,concat(D.month," ",D.year) as month_year from `tabDatasheet`as D) as T left join `tabBrand` as B on T.brand = B.name left join `tabView Log` as V on V.reference_name= T.name and V.reference_doctype= T.doctype group by T.name having view_count > 0 order by view_count desc limit 16 """,as_dict=True)   
        for trending_now in context['trending_now_list']:
            trending_now['attachments'] = get_attachments("Project",trending_now.name)
            trending_now["four_columns"]=True