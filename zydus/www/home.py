import frappe
import zydus

def get_context(context):

    
    context['trending_now_list'] = frappe.db.sql(""" select B.color,B.brand_logo,P.title,concat(P.month," ",P.year) as month_year from `tabProject` as P  left join `tabBrand` as B 
    on P.brand = B.name left join `tabView Log` as V on V.reference_name=P.name group by P.name order by count(V.reference_name) desc limit 6 """,as_dict=True)
   
    for trending_now_list in context['trending_now_list']:
        trending_now_list['number_of_files'] = 8
        print(trending_now_list)
    


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
