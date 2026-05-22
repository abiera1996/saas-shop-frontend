"""easev2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 
from config import settings 
from . import views, views_subpages, views_table_subpages, views_modal, views_ajax

app_name = 'main'

urlpatterns = [
    path('', views.homepage, name='login'),
    path('authentication', views.login, name='login'),
    path('forgot-password', views.forgot_password, name='forgot_password'),
    path('logout', views.logout_account, name='logout'),
    path('auth/reset/<str:code>', views.reset_view, name="reset_view"),
    path('merchant-register-complete/<str:code>', views.merchant_register_complete, name='merchant_register_complete'),
]


urlpatterns_subpage = [

]


urlpatterns_table = [
    path('subpage-table-import', views_table_subpages.table_import, name='table_import'),
    path('subpage-table-items-import', views_table_subpages.table_item_import, name='table_item_import'),
    
    path('subpage-table-user-guide', views_table_subpages.table_user_guide, name='table_user_guide'),
    path('subpage-table-items-user-guide', views_table_subpages.table_item_user_guide, name='table_item_user_guide'),

    path('subpage-table-policy_procedure', views_table_subpages.table_policy_procedure, name='table_policy_procedure'),
    path('subpage-table-items-policy_procedure', views_table_subpages.table_item_policy_procedure, name='table_item_policy_procedure'),
]

urlpatterns_modals = [
    path('modal-filter', views_modal.filter_modal, name='filter_modal'),
    path('modal-export-filter', views_modal.export_filter_modal, name='export_filter_modal'),
    path('modal-export-pdf', views_modal.export_pdf_modal, name='export_pdf_modal'),
    path('modal-dashboard-list', views_modal.dashboard_list_modal, name='dashboard_list_modal'),
    path('modal-user-guide-upload', views_modal.user_guide_upload, name='user_guide_upload'),
    
]


urlpatterns_ajax = [
    path('ajax/forget-password-request', views_ajax.forgot_password_request, name='forgot_password_request'),
    path('ajax/reset-password-request', views_ajax.reset_password_request, name='reset_password_request'),
    path('ajax/login-request', views_ajax.login_request, name='login_request'),
    path('ajax/merchant-initial-register-request', views_ajax.merchant_initial_register, name='merchant_initial_register'),
    path('ajax/merchant-register-request', views_ajax.merchant_register, name='merchant_register'),
    path('ajax/location/countries', views_ajax.get_countries, name='get_countries'),
    path('ajax/location/states', views_ajax.get_states, name='get_states'),
    path('ajax/location/cities', views_ajax.get_cities, name='get_cities'),
    path('ajax/reminder_off', views_ajax.reminder_off, name='reminder_off'),
    path('otp-code-resend/request/', views_ajax.otp_code_resend_request, name="otp_code_resend_request"),
    path('otp-code/request/', views_ajax.otp_code_request, name="otp_code_request"),
    
]


urlpatterns = urlpatterns + urlpatterns_subpage + urlpatterns_table + urlpatterns_modals + urlpatterns_ajax