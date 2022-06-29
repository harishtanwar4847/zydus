import frappe
import zydus
from frappe.desk.form.load import get_attachments
from frappe.utils import pretty_date, now, add_to_date

def get_context(context):
	context['no_cache'] = 1
	context['roles'] =  frappe.get_roles(frappe.session.user)
	context['allowed_roles'] = ['KMS Uploader', 'KMS Downloader', 'KMS Admin']
	# Sauce: https://stackoverflow.com/a/50633946/9403680
	context['access_allowed'] = any(role in context['roles'] for role in context['allowed_roles'])

	if context['access_allowed']:
		# context['approval_all'] = frappe.db.sql("""select T.modified,T.doctype,T.owner,T.route,T.name,T.title,T.type,T.agency,T.month_year,B.color,T.brand,T.workflow_state,U.full_name from (select modified,docstatus, owner, "Project" as doctype, P.route,P.brand, P.project_type as type,P.agency,P.workflow_state ,P.name,P.p_title as title,concat(P.month," ",P.year) as month_year from `tabProject` as P    union         select modified,docstatus, owner, "Datasheet" as doctype, D.route,D.brand,D.data_type as type,D.agency,D.workflow_state ,D.name,D.d_title as title,concat(D.month," ",D.year) as month_year from `tabDatasheet`as D) as T left join `tabBrand` as B on T.brand = B.name left join `tabUser`as U on U.name = T.owner  order by modified desc limit 10""",as_dict=True,debug=1)

		context['pending_list'] = frappe.db.sql("""select T.modified,T.doctype,T.owner,T.route,T.name,T.title,T.type,T.agency,T.month_year,B.color,T.brand,T.workflow_state,U.full_name from (select modified,docstatus, owner, "Project" as doctype, P.route,P.brand, P.project_type as type,P.agency,P.workflow_state ,P.name,P.p_title as title,concat(P.month," ",P.year) as month_year from `tabProject` as P where P.workflow_state="pending"   union         select modified,docstatus, owner, "Datasheet" as doctype, D.route,D.brand,D.data_type as type,D.agency,D.workflow_state ,D.name,D.d_title as title,concat(D.month," ",D.year) as month_year from `tabDatasheet`as D where D.workflow_state="pending" ) as T left join `tabBrand` as B on T.brand = B.name left join `tabUser`as U on U.name = T.owner  order by modified desc limit 10""",as_dict=True,debug=1)
		for pending_list in context['pending_list']:
			pending_list['attachments'] = get_attachments(pending_list.doctype,pending_list.name)

		context['rejected_list'] = frappe.db.sql("""select T.modified,T.doctype,T.owner,T.route,T.name,T.title,T.type,T.liked_by,T.agency,T.month_year,B.color,T.brand,T.workflow_state,U.full_name from (select modified,docstatus, owner, "Project" as doctype, P.route,P.brand, P.project_type as type,P._liked_by as liked_by,P.agency,P.workflow_state ,P.name,P.p_title as title,concat(P.month," ",P.year) as month_year from `tabProject` as P where P.workflow_state="rejected"   union         select modified,docstatus, owner, "Datasheet" as doctype, D.route,D.brand,D.data_type as type,D._liked_by as liked_by,D.agency,D.workflow_state ,D.name,D.d_title as title,concat(D.month," ",D.year) as month_year from `tabDatasheet`as D where D.workflow_state="rejected" ) as T left join `tabBrand` as B on T.brand = B.name left join `tabUser`as U on U.name = T.owner  order by modified desc limit 10""",as_dict=True,debug=1)
		for rejected_list in context['rejected_list']:
			rejected_list['attachments'] = get_attachments(rejected_list.doctype,rejected_list.name)
			rejected_list['is_liked'] = frappe.session.user in json.loads(rejected_list['liked_by'] or '[]')


		context["notifications"] = frappe.db.get_all("Notification Log",fields=["subject","creation"], filters={'for_user': frappe.session.user}, limit_page_length=5,order_by="modified desc")

		for notification in context['notifications']:
			notification['creations'] = pretty_date(notification['creation'])
			