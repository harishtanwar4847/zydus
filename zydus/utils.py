import frappe

def before_insert(doc,method):
    l_owner = frappe.get_doc(doc.reference_doctype,doc.reference_name)
    doc.reference_owner = l_owner.owner