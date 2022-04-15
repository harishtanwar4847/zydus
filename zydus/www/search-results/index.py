import frappe
import zydus
from frappe.desk.form.load import get_attachments
from frappe.utils import pretty_date, now, add_to_date

def get_context(context):
    context['roles'] =  frappe.get_roles(frappe.session.user)
    context['allowed_roles'] = ['KMS Uploader', 'KMS Downloader', 'KMS Admin']
    # Sauce: https://stackoverflow.com/a/50633946/9403680
    context['access_allowed'] = any(role in context['roles'] for role in context['allowed_roles'])

    if context['access_allowed']:
        context['search_results'] = [
            {'brand': 'Nutralite', 'color': '#0000FF', 'title': 'asdfalskj', 'project_type': 'lkajsdlkfj', 'agency': 'alksjdfk', 'date': 'Jan 2022', 'number_of_files': 1, 'description': 'lkasjdflkajsdlkf'},
            {'brand': 'Nutralite', 'color': '#000FFF', 'title': 'asdfalskj', 'project_type': 'lkajsdlkfj', 'agency': 'alksjdfk', 'date': 'Jan 2022', 'number_of_files': 2, 'description': 'lkasjdflkajsdlkf'},
            {'brand': 'Nutralite', 'color': '#00A0FF', 'title': 'asdfalskj', 'project_type': 'lkajsdlkfj', 'agency': 'alksjdfk', 'date': 'Jan 2022', 'number_of_files': 1, 'description': 'lkasjdflkajsdlkf'},
            {'brand': 'Nutralite', 'color': '#0000FF', 'title': 'asdfalskj', 'project_type': 'lkajsdlkfj', 'agency': 'alksjdfk', 'date': 'Jan 2022', 'number_of_files': 3, 'description': 'lkasjdflkajsdlkf'},
            {'brand': 'Nutralite', 'color': '#00FF0FF', 'title': 'asdfalskj', 'project_type': 'lkajsdlkfj', 'agency': 'alksjdfk', 'date': 'Jan 2022', 'number_of_files': 1, 'description': 'lkasjdflkajsdlkf'},
            {'brand': 'Nutralite', 'color': '#0000FF', 'title': 'asdfalskj', 'project_type': 'lkajsdlkfj', 'agency': 'alksjdfk', 'date': 'Jan 2022', 'number_of_files': 4, 'description': 'lkasjdflkajsdlkf'},
            {'brand': 'Nutralite', 'color': '#0000FF', 'title': 'asdfalskj', 'project_type': 'lkajsdlkfj', 'agency': 'alksjdfk', 'date': 'Jan 2022', 'number_of_files': 1, 'description': 'lkasjdflkajsdlkf'},
            {'brand': 'Nutralite', 'color': '#0000FF', 'title': 'asdfalskj', 'project_type': 'lkajsdlkfj', 'agency': 'alksjdfk', 'date': 'Jan 2022', 'number_of_files': 5, 'description': 'lkasjdflkajsdlkf'},
        ]
            
                  