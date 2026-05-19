from django.shortcuts import render, reverse, redirect
from django.utils import timezone
from utils import options
import datetime 
from django.contrib.auth.models import User


def export_filter_modal(request):  
    print(request.GET)
    years = [ {
        'name': 'Select Year',
        'value': ''
    }] 
    for year in range(datetime.datetime.now().year, 2018, -1):
        years.append( {
            'name': year,
            'value': year
        }) 

    context = {
        'data': request.GET,
        'filter_items': options.SRF_OPTION,
        'filter_items_vdf': options.VDF_OPTIONS,
        'months_option': options.MONTHS_OPTION,
        'years_option': years
    }
    return render(request, template_name='screens/users/_modals/main/export_filter.html', context=context)


def export_pdf_modal(request):  
    years = [ {
        'name': 'Select Year',
        'value': ''
    }] 
    for year in range(datetime.datetime.now().year, 2018, -1):
        years.append( {
            'name': year,
            'value': year
        }) 
    
    context = {
        'data': request.GET,
        'filter_items': options.SRF_OPTION,
        'filter_items_vdf': options.VDF_OPTIONS,
        'months_option': options.MONTHS_OPTION,
        'years_option': years
    }
    return render(request, template_name='screens/users/_modals/main/export_pdf_modal.html', context=context)


def filter_modal(request):  
    print(request.GET)
    params = request.GET
    request.GET._mutable = True
    years = [ {
        'name': 'Select Year',
        'value': ''
    }] 
    for year in range(datetime.datetime.now().year, 2018, -1):
        years.append( {
            'name': year,
            'value': str(year)
        }) 

    if params.get('insurance_expiry_date_to'):
        params['insurance_expiry_date_to'] = datetime.datetime.strptime(params['insurance_expiry_date_to'] , '%m-%d-%Y').date()  

    if params.get('insurance_expiry_date_from'):
        params['insurance_expiry_date_from'] = datetime.datetime.strptime(params['insurance_expiry_date_from'] , '%m-%d-%Y').date()  

    if params.get('start_break_date_from'):
        params['start_break_date_from'] = datetime.datetime.strptime(params['start_break_date_from'] , '%m-%d-%Y').date()  
    
    if params.get('start_break_date_to'):
        params['start_break_date_to'] = datetime.datetime.strptime(params['start_break_date_to'] , '%m-%d-%Y').date()  
    
    if params.get('prepare_date_from'):
        params['prepare_date_from'] = datetime.datetime.strptime(params['prepare_date_from'] , '%m-%d-%Y').date()  

    if params.get('prepare_date_to'):
        params['prepare_date_to'] = datetime.datetime.strptime(params['prepare_date_to'] , '%m-%d-%Y').date()  

    if params.get('actual_repair_date_from'):
        params['actual_repair_date_from'] = datetime.datetime.strptime(params['actual_repair_date_from'] , '%m-%d-%Y').date()  

    if params.get('actual_repair_date_to'):
        params['actual_repair_date_to'] = datetime.datetime.strptime(params['actual_repair_date_to'] , '%m-%d-%Y').date() 

    if params.get('effective_date_from'):
        params['effective_date_from'] = datetime.datetime.strptime(params['effective_date_from'] , '%m-%d-%Y').date() 

    if params.get('effective_date_to'):
        params['effective_date_to'] = datetime.datetime.strptime(params['effective_date_to'] , '%m-%d-%Y').date() 
  
    if params.get('tfleetmanager_date_from'):
        params['tfleetmanager_date_from'] = datetime.datetime.strptime(params['tfleetmanager_date_from'] , '%m-%d-%Y').date()  

    if params.get('tfleetmanager_date_to'):
        params['tfleetmanager_date_to'] = datetime.datetime.strptime(params['tfleetmanager_date_to'] , '%m-%d-%Y').date() 
    
    if params.get('grouphead_date_from'):
        params['grouphead_date_from'] = datetime.datetime.strptime(params['grouphead_date_from'] , '%m-%d-%Y').date()  

    if params.get('grouphead_date_to'):
        params['grouphead_date_to'] = datetime.datetime.strptime(params['grouphead_date_to'] , '%m-%d-%Y').date() 

    if params.get('uploaded_date_from'):
        params['uploaded_date_from'] = datetime.datetime.strptime(params['uploaded_date_from'] , '%m-%d-%Y').date()  

    if params.get('uploaded_date_to'):
        params['uploaded_date_to'] = datetime.datetime.strptime(params['uploaded_date_to'] , '%m-%d-%Y').date() 

    if params.get('covered_date_from'):
        params['covered_date_from'] = datetime.datetime.strptime(params['covered_date_from'] , '%m-%d-%Y').date()  

    if params.get('covered_date_to'):
        params['covered_date_to'] = datetime.datetime.strptime(params['covered_date_to'] , '%m-%d-%Y').date() 

    if params.get('approval_date_from'):
        params['approval_date_from'] = datetime.datetime.strptime(params['approval_date_from'] , '%m-%d-%Y').date()  

    if params.get('approval_date_to'):
        params['approval_date_to'] = datetime.datetime.strptime(params['approval_date_to'] , '%m-%d-%Y').date() 

    if params.get('date_from'):
        params['date_from'] = datetime.datetime.strptime(params['date_from'] , '%m-%d-%Y').date()  

    if params.get('date_to'):
        params['date_to'] = datetime.datetime.strptime(params['date_to'] , '%m-%d-%Y').date() 
    
    
    if params.get('activity_date_from'):
        params['activity_date_from'] = datetime.datetime.strptime(params['activity_date_from'] , '%m-%d-%Y').date()  

    if params.get('activity_date_to'):
        params['activity_date_to'] = datetime.datetime.strptime(params['activity_date_to'] , '%m-%d-%Y').date() 
    
    activity_value_date = ''
    if params.get('activity_date_from') and params.get('activity_date_to'):
        activity_value_date = params['activity_date_from'].strftime("%m/%d/%Y") + " - " +  params['activity_date_to'].strftime("%m/%d/%Y") 


    covered_value_date = ''
    if params.get('covered_date_from') and params.get('covered_date_to'):
        covered_value_date = params['covered_date_from'].strftime("%m/%d/%Y") + " - " +  params['covered_date_to'].strftime("%m/%d/%Y") 

    approval_value_date = ''
    if params.get('approval_date_from') and params.get('approval_date_to'):
        approval_value_date = params['approval_date_from'].strftime("%m/%d/%Y") + " - " +  params['approval_date_to'].strftime("%m/%d/%Y") 

    actual_repair_value_date = ''
    if params.get('actual_repair_date_from') and params.get('actual_repair_date_to'):
        actual_repair_value_date = params['actual_repair_date_from'].strftime("%m/%d/%Y") + " - " +  params['actual_repair_date_to'].strftime("%m/%d/%Y") 
    
    if params.get('latest_renewal_date_from'):
        params['latest_renewal_date_from'] = datetime.datetime.strptime(params['latest_renewal_date_from'] , '%m-%d-%Y').date()  

    if params.get('latest_renewal_date_to'):
        params['latest_renewal_date_to'] = datetime.datetime.strptime(params['latest_renewal_date_to'] , '%m-%d-%Y').date() 

    latest_renewal_value_date = ''
    if params.get('latest_renewal_date_from') and params.get('latest_renewal_date_to'):
        latest_renewal_value_date = params['latest_renewal_date_from'].strftime("%m/%d/%Y") + " - " +  params['latest_renewal_date_to'].strftime("%m/%d/%Y") 


    if params.get('next_renewal_date_from'):
        params['next_renewal_date_from'] = datetime.datetime.strptime(params['next_renewal_date_from'] , '%m-%d-%Y').date()  

    if params.get('next_renewal_date_to'):
        params['next_renewal_date_to'] = datetime.datetime.strptime(params['next_renewal_date_to'] , '%m-%d-%Y').date() 

    next_renewal_value_date = ''
    if params.get('next_renewal_date_from') and params.get('next_renewal_date_to'):
        next_renewal_value_date = params['next_renewal_date_from'].strftime("%m/%d/%Y") + " - " +  params['next_renewal_date_to'].strftime("%m/%d/%Y") 
        
    SRF_OPTION = [
         {"name": "FILTER BY STATUS", "isHeader":True},
            {"name": "Select All Status", "value": ""},
             {"name": "Complete", "value": "complete"},
              {"name": "Rejected", "value": "rejected"}
    ]
     
    VDF_OPTIONS = [
         {"name": "FILTER BY STATUS", "isHeader":True},
            {"name": "Select All Status", "value": ""}
    ]
    
        
    context = {
        'data': request.GET,
        'filter_items': SRF_OPTION,
        'filter_items_vdf': VDF_OPTIONS,
        'reason_for_rental_list': options.reason_for_rental_list, 
        'months_option': options.MONTHS_OPTION,
        'years_option': years, 
        'status_option': options.status_option, 
        'category_option': options.category_option,
        'params':params,
        'repair_status_option': options.repair_status_option, 
        'covered_value_date': covered_value_date,
        'activity_value_date':activity_value_date,
        'approval_value_date': approval_value_date,
        'actual_repair_value_date': actual_repair_value_date,
        'latest_renewal_value_date': latest_renewal_value_date,
        'next_renewal_value_date': next_renewal_value_date
    }
    return render(request, template_name='screens/users/_modals/main/filter_modal.html', context=context)


def dashboard_list_modal(request):  
    years = [ {
        'name': 'Select Year',
        'value': ''
    }] 
    for year in range(datetime.datetime.now().year, 2018, -1):
        years.append( {
            'name': year,
            'value': year
        }) 
    
    context = {
        'data': request.GET,
        'filter_items': options.SRF_OPTION,
        'filter_items_vdf': options.VDF_OPTIONS,
        'months_option': options.MONTHS_OPTION,
        'years_option': years,
        'params': request.GET
    }
    return render(request, template_name='screens/users/_modals/main/dashboard_list.html', context=context)


def user_guide_upload(request):   
    context = {
        'data': request.GET, 
    }
    return render(request, template_name='screens/users/_modals/main/user_guide_upload.html', context=context)
