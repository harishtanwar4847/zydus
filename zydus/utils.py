import frappe

def before_insert_comment(doc,method):
    if doc.reference_doctype in ("Project","Datasheet") and doc.comment_type == "Comment":
        l_owner = frappe.get_doc(doc.reference_doctype,doc.reference_name)
        doc.reference_owner = l_owner.owner
        if doc.reference_doctype == "Project":
            doc.project_name = l_owner.p_title
        if doc.reference_doctype == "Datasheet":
            doc.datasheet_name = l_owner.d_title