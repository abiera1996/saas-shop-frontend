from django.shortcuts import render, reverse, redirect
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
import datetime, json 
from django.contrib.auth.models import User
from utils.helpers import (
    decode_request_body,  
)
from django.db import transaction
from django.contrib.auth import password_validation, authenticate, login
from django.core.exceptions import ValidationError
from config import settings
from django.db.models import F, Value, CharField, Subquery, OuterRef, Case, When, IntegerField, DateField, \
    FloatField
from django.db.models.functions import Coalesce
from django.db.models import Q, OuterRef
from threading import Thread
from django.template.loader import get_template
from utils import helpers
from dateutil.relativedelta import relativedelta
from django.utils import timezone
import pytz
import string
from utils.api import API


def otp_code_request(request):
    response = {
        'success': False,
        'message': ''
    }
    if request.method == 'POST':
        data = request.POST
        otp = None

        if otp: 
            otp_created = otp.created + relativedelta(minutes=5) 
            otp_created_text = otp_created.strftime("%Y-%m-%d %H:%M:%S")
            otp_created = datetime.datetime.strptime(otp_created_text, "%Y-%m-%d %H:%M:%S")
             
            if otp_created > datetime.datetime.now():
                if not otp.is_used:
                    if not otp.is_invalid:
                        otp.is_used = True
                        otp.save()
                        request.session['show_otp'] = False
                        response = {
                            'success': True,
                            'message': 'OTP successfully verified.'
                        }
                    else:
                        response = {
                            'success': False,
                            'message': 'OTP code is invalid.'
                        }
                else:
                    response = {
                        'success': False,
                        'message': 'OTP code is used.'
                    }
            else:
                response = {
                    'success': False,
                    'message': 'OTP code is expired.'
                }

        else:
            response = {
                'success': False,
                'message': 'OTP doesn\'t exist.'
            }
    return JsonResponse(response)


def otp_code_resend_request(request):
    response = {
        'success': False,
        'message': ''
    }
    if request.method == 'POST':
        data = request.POST 
        # code = id_generator(size=4, chars=string.digits)
        # OTPCode.objects.filter(user=request.user,is_used=False).update(is_invalid=True)
        # otp_code = OTPCode.objects.create(user=request.user,code=code)
        # send_email_otp(request, request.user, code) 
        response = {
            'success': True,
            'message': ''
        }
    return JsonResponse(response)



@require_http_methods(['POST'])
def reminder_off(request):
    try:
        data = decode_request_body(request.body)
    except Exception as e:
        data = request.POST 

    profile = request.user.profile
    profile.is_remind_expired_password = False
    profile.save()
    return JsonResponse({
        'message': 'Successfully updated.'
    }, status=200)


@require_http_methods(['POST'])
def merchant_initial_register(request):
    try:
        data = decode_request_body(request.body)
    except Exception as e:
        data = request.POST
    api = API(request)
    response = api.http_request(
        "/api/merchant/initial-register",
        "post",
        payload=data
    )
    if response.get('status_code') in (200, 201):
        return JsonResponse(response.get('data', {}), status=200)
    return JsonResponse(response, status=response.get('status_code', 400))

@require_http_methods(['POST'])
def merchant_register(request):
    try:
        data = decode_request_body(request.body)
    except Exception as e:
        data = request.POST  
    api = API(request)
    response = api.http_request(
        "/api/merchant/register",
        "post",
        payload=data
    )   

    if response['status_code'] in (200, 201):
        return JsonResponse({
            'message': 'Merchant successfully registered. Please login to continue.'
        }, status=200)
    return JsonResponse(response, status=response['status_code'])

@require_http_methods(['GET'])
def get_countries(request):
    api = API(request)
    response = api.http_request("/api/location/countries", "get")



        data = request.GET
    context = {}
    json_data = []
    
    queryset = Country.objects.all() 
    if data.get('search'):
        search =  data.get('search')
        orm_lookups = ['country__icontains']
        
        queryset = helpers.search_result(queryset, search, orm_lookups, 0, False)
    queryset = helpers.Paginator(queryset).paginate(page=data.get('page',1), limit=data.get('limit', 10))

    for details in queryset.get('data', None):
        json_data.append({
            'id': details.pk,
            'text': details.country
        })

    context = { 'data': json_data, 'page_count': queryset.get('page_count', None) }
    return JsonResponse(context, status=200)

    
    return JsonResponse(response, status=response.get('status_code', 400))

@require_http_methods(['GET'])
def get_states(request):
    api = API(request)
    country_id = request.GET.get('country', '')
    response = api.http_request(f"/api/location/states?country_id={country_id}", "get")
    return JsonResponse(response, status=response.get('status_code', 400))

@require_http_methods(['GET'])
def get_cities(request):
    api = API(request)
    state_id = request.GET.get('state', '')
    response = api.http_request(f"/api/location/cities?state_id={state_id}", "get")
    return JsonResponse(response, status=response.get('status_code', 400))

@require_http_methods(['POST'])
def login_request(request):
    try:
        data = decode_request_body(request.body)
    except Exception as e:
        data = request.POST 
    username = data.get('username', '')
    password = data.get('password', '')
    # 1. Call your backend API directly
    api = API()
    response = api.http_request(
        "/api/login/", # <-- Change to your actual backend login endpoint
        "post",
        payload={"username": username, "password": password}
    )
    # 2. Check if login was successful
    if response.get('status_code') in (200, 201):
        api_data = response.get('data', {}) 
        # Extract user details and token from your API response
        user_info = api_data.get('user', {})
        
        # 3. Save everything you need into the session
        request.session['user_data'] = {
            'id': user_info.get('id'),
            'username': user_info.get('username'),
            'first_name': user_info.get('first_name'),
            'last_name': user_info.get('last_name'),
            'email': user_info.get('email'),
            'role_code': user_info.get('role_code'),
            'token': api_data.get('token'), # Save the auth token for future API calls
        }
        
        return JsonResponse({'message': 'Successfully logged in.'}, status=200)
    
    else:
        # Login failed
        error_msg = response.get('message', 'Username or password is incorrect.')
        return JsonResponse({'message': error_msg}, status=400)


@require_http_methods(['POST'])
def forgot_password_request(request):
    try:
        data = decode_request_body(request.body)
    except Exception as e:
        data = request.POST  

    user = User.objects.filter(username=data['username'])
    if not user.exists():
        return JsonResponse({
            'message': 'The username does not exist.'
        }, status=400)
    email_status, email_response = send_forgot_password(user[0])
    if email_status:
        return JsonResponse({
            'message': 'Reset password link sent to your email successfully.'
        }, status=200)
    else:
        return JsonResponse({
            'message': email_response
        }, status=400)


@require_http_methods(['POST'])
def reset_password_request(request):
    from django.contrib.auth.hashers import make_password
    try:
        data = decode_request_body(request.body)
    except Exception as e:
        data = request.POST  

    try:
        password_validation.validate_password(data['password'])
    except ValidationError as e: 
        return JsonResponse({
            'error': {
                "password": [e.messages]
            }
        }, status=400)
    
    if data['password'] != data['retype_password']:
        return JsonResponse({
            'error': {
                "retype_password": ['Passwords do not match.' ]
            }
        }, status=400)
 
    activation = None
    if activation:
        if activation.is_used:
            #Account already activated 
            return JsonResponse({
                'message': "Code already used."
            }, status=400)
    else:
        #Code didn't exist.
        #Redirect to login.
        return JsonResponse({
                'message': "Invalid code."  
            }, status=400) 

    activation = None
    if activation:
        user = activation.user
        if is_repeated_password(user, data.get('password')):
            return JsonResponse({
                'message': "You cannot reuse an old password."
            }, status=400)
        
        user.set_password(data.get('password'))
        profile =None
        if profile.exists():
            profile = profile[0]
            profile.current_password = data.get('password')
            profile.save()
        from django.contrib.auth.hashers import make_password
        hashed_password = make_password(data.get('password'))

        # UserOldPassword.objects.create(
        #     user=user,
        #     oldpassword=hashed_password
        # )
        profile.password_expiration = relativedelta(days=90) + datetime.date.today()
        profile.is_remind_expired_password = False
        activation.is_used = True
        activation.save()
        profile.save()
        user.save() 
        create_activity(request, user, 'Login', 'Reset password by users')
        return JsonResponse({
            'message': 'Password successfully reset.',
            'first_name': user.first_name
        }, status=200)
    else:
        return JsonResponse({
            'message': "Invalid code."  
        }, status=400)   


 