from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.utils import timezone
from utils.decorators import (
    require_not_logged
)
from utils.helpers import (
    get_global_context,
    get_or_none
)
import datetime
from django.contrib.auth import password_validation

def homepage(request):
    return render(request, template_name='screens/homepage.html')

# Create your views here.
@require_not_logged
def login(request):  
    context = {
        'title': 'FMS - Login'
    }
    context = get_global_context(request, context)
    return render(request, template_name='screens/authentication/login.html', context=context)


def logout_account(request): 
    logout(request)
    callback = request.GET.get('callback', None)
    if callback:
        return redirect(callback)
    return redirect('main:login')


@require_not_logged
def forgot_password(request): 
    context = {
        'title': 'FMS - Forgot Password'
    }
    context = get_global_context(request, context)
    return render(request, template_name='screens/authentication/forgot_password.html', context=context)


def reset_view(request, code):

    context = {
        'title':'Bitss - Reset Password'
    }
    context.update({
        'code': code,
        'is_used': False,
        'is_authenticated':False
    })
    if 'access_token' in request.session:
        context.update({
            'is_authenticated':True
        })
    else:
     
        return redirect('main:login_page')
    context.update({
        'password_validation_text': password_validation._password_validators_help_text_html()
    })
    
    context = get_global_context(request, context)
    
    return render(request, template_name='screens/authentication/reset_password.html', context=context)

def merchant_register_complete(request, code):
    context = {
        'title': 'FMS - Complete Registration',
        'code': code
    }
    context = get_global_context(request, context)
    return render(request, template_name='screens/authentication/register_completion.html', context=context)

