
import frappe
import zydus
from frappe.desk.form.load import get_attachments

def get_context(context):
    context['roles'] =  frappe.get_roles(frappe.session.user)
    context['allowed_roles'] = ['KMS Uploader', 'KMS Downloader', 'KMS Admin']
    # Sauce: https://stackoverflow.com/a/50633946/9403680
    context['access_allowed'] = any(role in context['roles'] for role in context['allowed_roles'])

    if context['access_allowed']:
        context['trending_now_list'] = frappe.db.sql("""select P.route,B.color,P.name,B.brand_logo,P.title,count(V.reference_name) as view,concat(P.month," ",P.year) as month_year from `tabProject` as P  left join `tabBrand` as B on P.brand = B.name left join `tabView Log` as V on V.reference_name=P.name and V.reference_doctype="Project" group by P.name having count(V.reference_name) > 0 order by count(V.reference_name) desc limit 16 """,as_dict=True)   
        for trending_now in context['trending_now_list']:
            trending_now['attachments'] = get_attachments("Project",trending_now.name)
            trending_now["four_columns"]=True