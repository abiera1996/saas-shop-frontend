from django.shortcuts import render, reverse
import json
from django.db.models import Q
import operator
from functools import partial, reduce, update_wrapper
import math
from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse
import string
import random
from django.contrib.humanize.templatetags.humanize import intcomma
from config import settings
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.sessions.models import Session
from dateutil.relativedelta import relativedelta 
from threading import Thread
from django.contrib.auth.hashers import check_password
from datetime import datetime 


MONTHS_NAME = [  
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
]



 
def get_global_context(request, context):
    advertisement = []
    navigations = []
    if request.user.is_authenticated: 
        user_guide_url = '#'
          
        navigations = [
            {
                "title": "Dashboard", 
                "isActive": False,
                "icon":"components/svg/navigation/dashboard.html", 
                "url":reverse('user:dashboard'), 
                "subItems": []
            },
            {
                "title": "Branch / Dept", 
                "isActive": False,
                "icon":"components/svg/navigation/point_of_sale.html", 
                "url":reverse('user:branch'), 
                "subItems": [], 
                "permission_code": ['VWBRNCHS', 'CRT_BRNCH']
            },
            {
                "title": "SRF Creation", 
                "isActive": False,
                "icon":"components/svg/navigation/inventory.html", 
                "url":reverse('user:create_srf'), 
                "subItems": [],
                "permission_code": ['CRT_SRF']
            },
            {
                "title": "VDF Creation", 
                "isActive": False,
                "icon":"components/svg/navigation/inventory.html", 
                "url":reverse('user:create_vdf'), 
                "subItems": [],
                "permission_code": ['CRTVDF']
            },
            {
                "title": "Vehicle Disposal Creation", 
                "isActive": False,
                "icon":"components/svg/navigation/inventory.html", 
                "url":reverse('user:create_disposal'), 
                "subItems": [],
                "permission_code": ['CRTDSPSLFVHCL']
            }, 
            {
                "title": "Masterlist of Vehicles", 
                "isActive": False,
                "icon":"components/svg/navigation/inventory.html", 
                "url":reverse('user:vehicle'), 
                "subItems": [], 
                "permission_code": ['CRTMPRTVHCLE', 'VWVHCLS']
            },
            {
                "title": "Service Request Maintenance Form", 
                "isActive": False,
                "icon":"components/svg/navigation/inventory.html", 
                "url":'$', 
                "subItems":  [ 
                    {"url": reverse('user:srf'), "name":'SRF for approval and actual repair', "isActive": False,
                        "permission_code": ["VWSRF"]},  
                    {"url": reverse('user:srf_complete'), "name":"Completed repairs", "isActive": False,
                        "permission_code": ["VWSRF"]}, 
                    {"url": reverse('user:srf_complete_registration'), "name":"Approved registration", "isActive": False,
                        "permission_code": ["VWSRF"]}, 
                    {"url": reverse('user:rejected_srf'), "name":'Rejected SRF', "isActive": False,
                        "permission_code": ["VWSRF"]},  
                    {"url": reverse('user:srf_kpi'), "name":"SRF KPI", "isActive": False,
                        "permission_code": ["VWSRFKP"]}, 
                    {"url": reverse('user:srf_repair_history'), "name":"Repair and maintenance history", "isActive": False,
                        "permission_code": ["VWRPRNDMNTNNCHSTRY"]}, 
                    {"url": reverse('user:srf_budget'), "name":'Actual repair vs. budget', "isActive": False,
                        "permission_code": ["VWCTLVSBDGT"]}, 
                     {"url": reverse('user:srf_import'), "name":'Import SRF', "isActive": False,
                        "permission_code": ["MPRTCRT_SRF"]}, 
                    {"url": reverse('user:srf_import_previous'), "name":'Import SRF Previous Data', "isActive": False,
                        "permission_code": ["MPRTCRT_SRF_PRVS_DT"]}, 
                ], 
            },
            {
                "title": "Vehicle Dispatch Form", 
                "isActive": False,
                "icon":"components/svg/navigation/inventory.html", 
                "url":'$', 
                "subItems":  [ 
                    {"url": reverse('user:vdf'), "name":"VDF for approval", "isActive": False,
                        "permission_code": ["VWVDF"]}, 
                    {"url": reverse('user:vdf_complete'), "name":"Completed VDF", "isActive": False,
                        "permission_code": ["VWVDF"]}, 
                    {"url": reverse('user:vdf_kpi'), "name":"VDF approval KPI", "isActive": False,
                        "permission_code": ["VWVHVLDSPTCHKP"]}, 
                     {"url": reverse('user:vdf_import'), "name":'Import VDF', "isActive": False,
                        "permission_code": ["MPRTCRT_VDF"]}, 
                    {"url": reverse('user:vdf_import_previous'), "name":'Import VDF Previous Data', "isActive": False,
                        "permission_code": ["MPRTCRT_VDF_PRVS_DT"]}, 
                ]
            },
            {
                "title": "Disposal of Vehicles", 
                "isActive": False,
                "icon":"components/svg/navigation/inventory.html", 
                "url":  "#",   
                "subItems":  [ 
                    {"url": reverse('user:disposal'), "name":"For approval and actual disposal", "isActive": False,
                        "permission_code": ["VWDSPSLFVHCL"]}, 
                    {"url": reverse('user:disposal_vehicle'), "name":"Disposed vehicles", "isActive": False,
                        "permission_code": ["VWDSPSLFVHCL"]}
                ]
            },
            {
                "title": "Gasoline Consumption Monitoring", 
                "isActive": False,
                "icon":"components/svg/navigation/inventory.html", 
                "url": "#", 
                "subItems":  [ 
                    {"url": reverse('user:batch_gasoline_consumption'), "name":"Latest monthly gasoline consumption report", "isActive": False,
                        "permission_code": ["VWGSLN"]}, 
                    {"url": reverse('user:gasoline_consumption_history'), "name":"Gasoline consumption history", "isActive": False,
                        "permission_code": ["VWGSLNHSTRY"]},  
                ]
            },
            {
                "title": "TFleet Vehicle Rental Billing", 
                "isActive": False,
                "icon":"components/svg/navigation/inventory.html", 
                "url": "#", 
                "subItems":  [ 
                    {"url": reverse('user:batch_billing'), "name":"Latest monthly vehicle rental billing report", "isActive": False,
                        "permission_code": ["VWBLLNGS"]}, 
                    {"url": reverse('user:billing_rentals_history'), "name":"Vehicle rental billing history", "isActive": False,
                        "permission_code": ["VWBLLNGHSTRY"]},  
                ]
            },
            {
                "title": "Insurance Monitoring", 
                "isActive": False,
                "icon":"components/svg/navigation/inventory.html", 
                "url": "#", 
                "subItems":  [ 
                    {"url": reverse('user:batch_insurance'), "name":"Batch upload", "isActive": False,
                        "permission_code": ["VWNSRNC"]}, 
                    # {"url": reverse('user:insurance_data'), "name":"Insurance data", "isActive": False,
                    #     "permission_code": ["VWNSRNC"]},  
                    {"url": reverse('user:insurance_status'), "name":"Insurance status", "isActive": False,
                        "permission_code": ["VWNSRNC"]}, 
                    {"url": reverse('user:insurance_vehicle'), "name":"Insurance history", "isActive": False,
                        "permission_code": ["VWNSRNC"]},  
                    {"url": reverse('user:insurance_claims'), "name":"Insurance claims", "isActive": False,
                        "permission_code": ["VWNSRNC"]},  
                ]
            },
             {
                "title": "Vehicle Registration Monitoring", 
                "isActive": False,
                "icon":"components/svg/navigation/inventory.html", 
                "url": "#", 
                "subItems":  [ 
                    {"url": reverse('user:batch_vehicle_registration'), "name":"Batch upload", "isActive": False,
                        "permission_code": ["VWVHCLRGSTRTN"]}, 
                    # {"url": reverse('user:insurance_data'), "name":"Insurance data", "isActive": False,
                    #     "permission_code": ["VWVHCLRGSTRTN"]},  
                    {"url": reverse('user:registration_status'), "name":"Registration status", "isActive": False,
                        "permission_code": ["VWVHCLRGSTRTN"]}, 
                    {"url": reverse('user:registration_vehicle'), "name":"Registration history", "isActive": False,
                        "permission_code": ["VWVHCLRGSTRTN"]},   
                ]
            },
            {
                "title": "divider",
                "isDivider": True
            },
            {
                "title": "Masterlist of Third Party Providers", 
                "isActive": False,
                "icon":"components/svg/navigation/inventory.html", 
                "url": reverse('user:provider_main'),
                "permission_code": ["VWSRVCPRVDR"]
            },
            {
                "title": "Masterlist of Repairs Accredited Suppliers", 
                "isActive": False,
                "icon":"components/svg/navigation/inventory.html", 
                "url": reverse('user:supplier_main'),
                "permission_code": ["VWSSPPLR"]
            }, 
            {
                "title": "Related policies and procedures", 
                "isActive": False,
                "icon":"components/svg/navigation/inventory.html", 
                "url": reverse('user:related_policies'),
            }, 
            {
                "title": "User guide", 
                "isActive": False,
                "icon":"components/svg/navigation/inventory.html", 
                "url": user_guide_url
            }, 
            
            {
                "title": "Settings", 
                "isActive": False,
                "icon":"components/svg/navigation/settings.html", 
                "url":"#", 
                "subItems":  [ 
                    {"url": reverse('user:system_user'), "name":"Users", "isActive": False,
                        "permission_code": ["VWSR"]}, 
                    {"url": reverse('user:user_role'), "name":"User Role", "isActive": False,
                        "permission_code": ["VWSRRL"]}, 
                    
                    {"url": reverse('user:audit_log'), "name":"Audit Logs", "isActive": False,
                        "permission_code": ["VWDTLGS"]}, 
                    {"url": reverse('user:change_password'), "name":"Change Password", "isActive": False},  
                    {"url": reverse('user:approvers'), "name":"Setup Approvers", "isActive": False,
                        "permission_code": ["VWDTLGS"]}, 
                    {"url": reverse('user:setup_user_guide'), "name":"Setup User Guide", "isActive": False,
                        "permission_code": ["VWDTLGS"]}, 
                ]
            },
        ]
    
    # check permission
    if hasattr(request.user, 'profile'):
        permissions = request.user.profile.get_user_has_permission()
        new_navigation = []
        nav = [*navigations]
        for data in nav:
            if 'permission_code' in data:
                if check_array_existence(data['permission_code'], permissions):
                    new_navigation.append(data)
            elif data.get('subItems'):
                sub_nav = list()
                nav_data = {**data}

                for data_sub in nav_data['subItems']:
                    if 'permission_code' in data_sub:
                        if check_array_existence(data_sub['permission_code'], permissions):
                            sub_nav.append(data_sub)
                    else:
                        sub_nav.append(data_sub)
                nav_data['subItems'] = sub_nav
                if len(sub_nav) != 0:
                    new_navigation.append(nav_data)
            else:
                new_navigation.append(data)
        navigations = new_navigation
    
    # check active navigation
    if 'active_navigation' in context:
        for data in navigations:
            if data['title'] == context['active_navigation']['title']:
                data['isActive'] = True
            if data.get('subItems') and context['active_navigation'].get('sub'):
                for data_sub in data['subItems']:
                    if data_sub['name'] == context['active_navigation']['sub']:
                        data_sub['isActive'] = True
 
    global_context = {
        'g_navigations': navigations,
        'g_advertisement': advertisement
    }
    return {**context, **global_context}
    


def decode_request_body(body):
    body_unicode = body.decode('utf-8')
    body = json.loads(body_unicode)
    return body


def search_result(queryset, search, orm_lookups, search_max=10, limit_data=True):
    
    for bit in search.split():
        or_queries = [Q(**{orm_lookup: bit})
                    for orm_lookup in orm_lookups]
        queryset = queryset.filter(reduce(operator.or_, or_queries))
    if limit_data:
        return queryset[0:search_max]
    else:
        return queryset


def id_generator(size=25, chars=string.ascii_lowercase + string.digits):
    """
    Generate random string
    """
    return ''.join(random.choice(chars) for _ in range(size))


class Paginator:
    def __init__(self, queryset, page_ranged=True):
        self.queryset = queryset
        self.page_ranged = page_ranged

    def paginate(self, page=1, limit=10, span=2):
        page = int(page)
        limit = int(limit)
        span = int(span)

        offset = (page - 1) * limit

        count = len(self.queryset)

        try:
            page_count = math.ceil(count / limit)
        except:
            page_count = 1

        has_next = page < page_count
        has_prev = page > 1

        record_from = offset + 1
        record_to = offset + limit if offset + limit <= count else count

        if self.page_ranged:
            max_range = page + span if page + span <= page_count else page_count
            min_range = page - span if page - span >= 1 else 1

            pages = range(min_range, max_range + 1)

        else:
            pages = range(1, page_count + 1)
        
        return {
            "limit": limit,
            "record_count": count,
            "page_count": page_count,
            "record_from": record_from,
            "record_to": record_to,
            "pages": list(pages),
            "page": page,
            "has_next": has_next,
            "has_prev": has_prev,
            "data": self.queryset[offset:offset + limit],
            "page_details": {
                'num_pages': list(pages),
                'prev': (int(record_from) - 1) if has_prev else None,
                'next': record_to if has_next else None,
                'page_count': page_count,
                'count': count,
                'page':  page,
                'limit': limit,
            }
        }


def pagination_result(queryset, page, limit):
    queryset = Paginator(queryset).paginate(page=page, limit=limit)
    return {
        'pagination': {
            'num_pages': queryset.get('pages'),
            'prev': (int(queryset.get('record_from')) - 1) if queryset.get('has_prev') else None,
            'next': queryset.get('record_to') if queryset.get('has_next') else None,
            'count': queryset.get('page_count'),
            'page': queryset.get('page'),
            'limit': queryset.get('limit'),
        }
    }


def get_or_none(classmodel, **kwargs):
    try:
        obj = classmodel.objects.get(**kwargs)
        return obj
    except:
        return None
    

def check_array_existence(array1, array2):
    for element in array1:
        if element in array2:
            return True
    return False


def default_zero(id, max_length):
    length = len(str(id))
    if length < max_length:
        str_id = '0' * (max_length - length) + str(id)
        return str_id
    else:
        return str(id)
    

def concatenate_zeroes(number, length_zero=5):
    # Convert the number to a string
    number_str = str(number)
    
    # Calculate the number of zeroes needed
    num_zeroes = length_zero - len(number_str)
    
    # Concatenate the zeroes before the number
    concatenated_number = "0" * num_zeroes + number_str
    
    return concatenated_number


def moneyfy(val, suffix=""):
    if val:
        val = float(val)
        val = "%s%s" % (intcomma(int(val)), ("%0.2f" % val)[-3:])
    else:
        val = "0.00"

    return "%s%s" % (suffix,val )


def check_exiting(data_list, check_data, exclude_row):
    for index, fields in data_list:
        new_index  = index - 1
        if new_index != exclude_row:
            for item in fields:
                if item == check_data:
                    return True, f"Row: {exclude_row} ({check_data}) has same value in Row:{new_index} value."
    return False, "Not existing"


def anti_vowel(c):
    newstr = c
    vowels = ('a', 'e', 'i', 'o', 'u')
    for x in c.lower():
        if x in vowels:
            newstr = newstr.replace(x,"")

    return newstr.upper()


def check_plural(count, val):
    if count > 1:
        val += 's'
    return val


def get_time_span(start_date, end_date, type=None):
    if end_date and start_date:
        c = end_date-start_date 
        if type == 'minutes':
            return c.seconds / 60
        elif type == 'days': 
            try:
                start_date = start_date.date()
            except:
                pass
            try:
                end_date = end_date.date()
            except:
                pass
            c = end_date-start_date 
            return c.days
        else:
            span_string = '' 
            if c.days >= 0:
                if c.days != 0:
                    span_string += str(int(c.days)) + check_plural(int(c.days), ' day') + ' '

                minutes = divmod(c.total_seconds(), 60)  
                hours = divmod(minutes[0], 60)  

                if type == 'full_format':
                    span_string = ''
                    h = 0
                    if c.days != 0:
                        h = int(c.days) * 24
                    if hours[0] != 0 or h != 0:
                        span_string += str(int(hours[0]) + h) + ':'
                    else:
                        span_string += '0:'

                    if hours[1] != 0:
                        span_string += str(int(hours[1])) + ':'
                    else:
                        span_string += '00:'
                    if minutes[1] != 0:
                        span_string += str(int(minutes[1]))
                    else:
                        span_string += '00'
                else:
                    if hours[0] != 0:
                        span_string += str(int(hours[0])) + check_plural(int(hours[0]), ' hour') + ' '
                    if hours[1] != 0:
                        span_string += str(int(hours[1])) + check_plural(int(hours[1]), ' minute') + ' '
                    if minutes[1] != 0:
                        span_string += str(int(minutes[1])) + check_plural(int(minutes[1]), ' second')
                return  span_string
            return ''
    return ''


def is_number(val):
    try:
        float(str(val).replace(',', ''))
        return True
    except:
        return False
    

def is_whole_number(val):
    try:
        
        return float(str(val).replace(',', '')).is_integer()
    except:
        return False
     
 
def force_logout_user(user):
    """
    This function will force logout the user
    """ 

    two_hours = relativedelta(hours=2)
    fifteen_minutes = relativedelta(minutes=15) 
    if user.last_login:
        expiry = user.last_login + fifteen_minutes
        sessions = Session.objects.filter(expire_date__gt=expiry - two_hours,expire_date__lt=expiry + two_hours)
        [s.delete() for s in sessions if s.get_decoded().get('_auth_user_hash') == user.get_session_auth_hash()]

 

def get_status_html(status):
    style_status = '' 
    if status == 'approved':
        style_status = "color:white;background:#00af50;"
    elif status == 'rejected':
        style_status = "color:white;background:#fe0000;"
    elif status  == 'pending':
        style_status = "color:white;background:#ffc000;"
    elif status  == 'locked':
        style_status = "color:white;background:#0071c1;"
    status = status.capitalize()
    
    return f"""
    <div class="capitalize" style="{style_status}padding: 5px 12px; border-radius: 1rem;text-align:center;">
        {status}
    </div>
    """


def send_email_otp(request, user, code, update_session=True):
    #send email
    html = get_template('email_template/otp_code.html') 
     
    otp_created_text = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    if update_session:
        request.session['otp_type'] = 'email'
        request.session['otp_time'] = otp_created_text
    context = {
        'code': code
    }
    email = user.email
    email_status, email_response = send_email(
        'OTP Code', 
        html.render(context),
        [email]
    )
    print("----------------------")
    return email_status, email_response
    
 
