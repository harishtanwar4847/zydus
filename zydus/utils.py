import frappe

def before_insert(doc,method):
    if doc.reference_doctype in ("Project","Datasheet") and doc.comment_type == "Comment":
        l_owner = frappe.get_doc(doc.reference_doctype,doc.reference_name)
        doc.reference_owner = l_owner.owner