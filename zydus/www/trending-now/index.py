import frappe
import zydus

def get_context(context):
    context['trending_now_list'] = frappe.db.sql(""" select B.color,B.brand_logo,P.title,concat(P.month," ",P.year) as month_year from `tabProject` as P  left join `tabBrand` as B 
    on P.brand = B.name left join `tabView Log` as V on V.reference_name=P.name group by P.name order by count(V.reference_name) desc limit 16 """,as_dict=True)
   
    for trending_now in context['trending_now_list']:
        trending_now['number_of_files'] = 8
        trending_now["four_columns"]=True
