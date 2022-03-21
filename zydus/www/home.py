import frappe
import zydus

def get_context(context):
    context['trending_now_list'] = [
        {"color": "#4F9DD9", "logo": "/assets/zydus/images/company_logo.png", "title": "Digital Maketing - Facebook", "month_year": "Jan 2022", "number_of_files": 1},
        {"color": "#FF0000", "logo": "/assets/zydus/images/company_logo.png", "title": "Digital Maketing - Facebook", "month_year": "Jan 2022", "number_of_files": 2},
        {"color": "#00FF00", "logo": "/assets/zydus/images/company_logo.png", "title": "Digital Maketing - Facebook", "month_year": "Jan 2022", "number_of_files": 3},
        {"color": "#0000FF", "logo": "/assets/zydus/images/company_logo.png", "title": "Digital Maketing - Facebook", "month_year": "Jan 2022", "number_of_files": 1},
        {"color": "#FF00FF", "logo": "/assets/zydus/images/company_logo.png", "title": "Digital Maketing - Facebook", "month_year": "Jan 2022", "number_of_files": 1},
        {"color": "#000000", "logo": "/assets/zydus/images/company_logo.png", "title": "Digital Maketing - Facebook", "month_year": "Jan 2022", "number_of_files": 1}, 
    ]

    context['my_uploads'] = [
        {"color": "#4F9DD9", "brand": "Everyuth", "title": "Digital Maketing - Facebook", "month_year": "Jan 2022", "number_of_files": 1},
        {"color": "#FF0000", "brand": "Everyuth", "title": "Digital Maketing - Facebook", "month_year": "Jan 2022", "number_of_files": 2},
        {"color": "#00FF00", "brand": "Everyuth", "title": "Digital Maketing - Facebook", "month_year": "Jan 2022", "number_of_files": 3},
        {"color": "#0000FF", "brand": "Everyuth", "title": "Digital Maketing - Facebook", "month_year": "Jan 2022", "number_of_files": 1},
        {"color": "#FF00FF", "brand": "Everyuth", "title": "Digital Maketing - Facebook", "month_year": "Jan 2022", "number_of_files": 1},
        {"color": "#000000", "brand": "Everyuth", "title": "Digital Maketing - Facebook", "month_year": "Jan 2022", "number_of_files": 1}, 
    ]

    context['reminders'] = [
        {"active": True, "owner": "guest", "modified_by": "Administrator", "title": "Urgent", "description": "Send the client list", "date": "2022-03-31"},
        {"active": True, "owner": "guest", "modified_by": "guest", "title": "Urgent", "description": "Send the client list", "date": "2022-03-30"},
        {"active": True, "owner": "guest", "modified_by": "Administrator", "title": "Urgent", "description": "Send the client list", "date": "2022-03-21"},
        {"active": False, "owner": "guest", "modified_by": "guest", "title": "Urgent", "description": "Send the client list", "date": "2022-03-20"},
        {"active": True, "owner": "guest", "modified_by": "guest", "title": "Urgent", "description": "Send the client list", "date": "2022-03-31"},
    ]

    # due_by calculation
    for reminder in context['reminders']:
        reminder['due_by'] = zydus.pretty_date_future(reminder['date'])
