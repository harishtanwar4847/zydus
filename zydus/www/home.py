import frappe

def get_context(context):
    context['trending_now_list'] = [
        {"color": "#4F9DD9", "logo": "/assets/zydus/images/company_logo.png", "title": "Digital Maketing - Facebook", "month_year": "Jan 2022", "number_of_files": 1},
        {"color": "#FF0000", "logo": "/assets/zydus/images/company_logo.png", "title": "Digital Maketing - Facebook", "month_year": "Jan 2022", "number_of_files": 2},
        {"color": "#00FF00", "logo": "/assets/zydus/images/company_logo.png", "title": "Digital Maketing - Facebook", "month_year": "Jan 2022", "number_of_files": 3},
        {"color": "#0000FF", "logo": "/assets/zydus/images/company_logo.png", "title": "Digital Maketing - Facebook", "month_year": "Jan 2022", "number_of_files": 1},
        {"color": "#FF00FF", "logo": "/assets/zydus/images/company_logo.png", "title": "Digital Maketing - Facebook", "month_year": "Jan 2022", "number_of_files": 1},
        {"color": "#000000", "logo": "/assets/zydus/images/company_logo.png", "title": "Digital Maketing - Facebook", "month_year": "Jan 2022", "number_of_files": 1}, 
    ]