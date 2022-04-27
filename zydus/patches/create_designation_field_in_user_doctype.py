from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def execute():
    df = dict(fieldname='designation', label='Designation', fieldtype='Data')
    create_custom_field('User', df)