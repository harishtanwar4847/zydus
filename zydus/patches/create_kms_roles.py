import frappe

def execute():
    roles = ['KMS Admin', 'KMS Uploader', 'KMS Downloader']
    for role in roles:
        try:
            frappe.get_doc({'doctype': 'Role', 'role_name': role}).insert()
        except:
            pass

        frappe.db.commit()