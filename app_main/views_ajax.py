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
def merchant_register(request):
    try:
        data = decode_request_body(request.body)
    except Exception as e:
        data = request.POST  
    response = API().http_request(
        "auth/set-credentials",
        "post",
        payload=data
    )  
    if response.status_code in (200, 201):
        return JsonResponse({
            'message': 'Merchant successfully registered. Please login to continue.'
        }, status=200)
    return JsonResponse({
        'message': response.json().get('message', 'Failed to registration.')
    }, status=200)

@require_http_methods(['POST'])
def login_request(request):
    try:
        data = decode_request_body(request.body)
    except Exception as e:
        data = request.POST 
    username = data.get('username', '')
    password = data.get('password', '')
     
    username_data = User.objects.filter(username=username)
 
    user = authenticate(request, username=username, password=password)
    if user is None:
        error_msg = 'Username or password is incorrect.' 

        if username_data.exists():
            username_data = username_data[0]
            # if  hasattr(username_data, 'profile'):
            #     profile = username_data.profile
            #     password_attempt = profile.password_attempt + 1
            #     profile.password_attempt = password_attempt
                
            #     if password_attempt == 5:
            #         profile.unlocke_date = relativedelta(minutes=15) + datetime.datetime.now()
            #         error_msg = 'Your account is currently locked.'
            #     elif password_attempt > 5:
            #         error_msg = 'Your account is currently locked.'
            #     profile.save()
        else:
            username_data = None
        create_activity(request, username_data, 'Login', f'Failed login ({error_msg})', data={
            'username': username
        })
        return JsonResponse({
            'message': error_msg
        }, status=400)
    
    if not hasattr(user, 'profile'):
        if user.is_superuser:  
            # role = Role.objects.get(role_code='DMN_1')
            # Profile.objects.create(
            #     user=user,
            #     role=role
            # )
            pass
        else:
            create_activity(request, user, 'Login', 'Failed login (Invalid user to login)')
            return JsonResponse({
                'message': 'Invalid user to login.'
            }, status=400)
    else:
        if not user.is_superuser:  
            if user.profile.status != 'active' or user.profile.user_role.status != 'active':
                create_activity(request, user, 'Login', 'Failed login (User is deactivated)')
                return JsonResponse({
                    'message': 'User is deactivated.'
                }, status=400)

    profile = user.profile
    # profile.password_attempt = 0
    # profile.save()
    # if profile.unlocke_date:
    #     if profile.unlocke_date > datetime.datetime.now():
    #         now = datetime.datetime.now()
    #         time_left = profile.unlocke_date - now
    #         minutes_left = int(time_left.total_seconds() // 60)
    #         seconds_left = int(time_left.total_seconds() % 60)
    #         create_activity(request, user, 'Login', f'Failed login (Account is currently locked. Wait {minutes_left} minutes and {seconds_left} seconds to unlocked.)')
    #         return JsonResponse({
    #             'message': f'Your account is currently locked. Please wait {minutes_left} minutes and {seconds_left} seconds.'
    #         }, status=400)
    

    # today = datetime.date.today()

    # if user.profile.password_expiration:
    #     days_until_expiration = (user.profile.password_expiration - today).days
   
    #     if days_until_expiration <= 0:
    #         create_activity(request, user, 'Login', 'Failed login (expired password)')
    #         return JsonResponse({
    #             'message': 'Your password has expired. Please reset your password or use forgot password to reset password.'
    #         }, status=400)
    #     elif days_until_expiration <= 10:
    #         profile = user.profile
    #         profile.is_remind_expired_password = True
    #         profile.save()
    
    # try:
    #     password_validation.validate_password(password)
    # except ValidationError as e: 
    #     code = get_code(user) 
    #     reset_url = settings.BASE_URL + 'auth/reset/'+ code 
    #     return JsonResponse({
    #             'isResetPassword': True,
    #             'reset_url': reset_url
    #         }, status=400)
    
    # if not user.is_superuser and profile.is_auth_otp:  
    #     request.session['show_otp'] = True
    #     code = id_generator(size=4, chars=string.digits)
    #     OTPCode.objects.filter(user=user,is_used=False).update(is_invalid=True)
    #     otp_code = OTPCode.objects.create(user=user,code=code)
    #     email_status, email_response = send_email_otp(request, user, code)
    #     if not email_status:
    #         create_activity(request, user, 'Login', f'Failed login ({email_response})')
    #         return JsonResponse({
    #                 'message':  email_response
    #             }, status=400)
                
    login(request, user) 
    request.session['role_code'] = user.profile.role.role_code
    if user.profile.role.role_code == 'SYSTMSR_1':
        request.session['user_role_code'] = user.profile.user_role.role_code 
    create_activity(request, user, 'Login', 'Successfully login')
    return JsonResponse({
        'message': 'Successfully login.'
    }, status=200)


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


 