from django.shortcuts import render, reverse, redirect
from utils import helpers
 
from django.utils import timezone
import json, base64

def table_import(request): 
    subpage_url = reverse('main:table_item_import')
    context = {
        'table_id': 'table_import',
        'subpage_url': subpage_url,
        'request_data': dict(zip(request.GET.keys(), request.GET.values())),
        'is_hide_pagination': False,
        'data_lists': {
            'column': [ 
                {
                    'name': 'Batch Number',
                    'is_sorted': False
                }, 
                {
                    'name': 'Total Data',
                    'is_sorted': False
                }, 
                {
                    'name': 'Status',
                    'is_sorted': False
                }, 
                {
                    'name': 'Import Date',
                    'is_sorted': False
                }, {
                    'name': 'Action',
                    'is_sorted': False
                }, 
            ]
        }
    }
    return render(request, template_name='components/tables/main_table1.html', context=context)


def table_item_import(request): 
    data = request.GET
    table_id = data.get('table_id')

    queryset =  None

    _type = data.get("type", "") 
    if _type != "":
        queryset = queryset.filter(type=_type) 

    queryset =  helpers.Paginator(queryset).paginate(
        page=data.get('page',1), 
        limit=data.get('limit',5)
    )

    column_count = data.get('column_count',1)
    context = {
        'table_id': table_id,
        'data_lists': {
            'pages': queryset['page_details'],
            'column_count': column_count,
            'data': [],
            'empty': {
                'icon': 'bx bxs-user-detail',
                'message': 'No Import Files Available'
            }
        },
        'is_hide_pagination': data.get('is_hide_pagination', '') in ('true', 'True')  
    }
    
    for details in queryset.get('data', []): 
        action = ""
        if details.status == 'valid':
            action = f"""
                <a href="#" class="dropdown-item import-file flex justify-center items-center" data-id="{details.pk}">
                    <i class='bx bxs-file-import' ></i>&nbsp;Import File
                </a>
            """
        elif details.status == 'has invalid row':
            encoded = base64.b64encode((details.error_messages).encode()).decode('ascii')

            action = f"""
                <a href="#" onclick="downloadTextFile('{details.type}.txt', '{encoded}')" class="dropdown-item flex justify-center items-center" data-id="{details.pk}"
                data-val="{encoded}">
                    <i class='bx bx-download'></i>&nbsp;Download Error
                </a>
            """
            action += f"""
                <a href="#" class="dropdown-item copy-error-file flex justify-center items-center" data-id="{details.pk}"
                data-val="{encoded}">
                    <i class='bx bxs-copy' ></i>&nbsp;Copy Error 
                </a>
            """
        
        style_status = ''
        if details.status == 'valid':
            style_status = "color:#0265dc;background:#d9e8fa;"
        elif details.status == 'success':
            style_status = "color:#36dc02;background:#d9fae2;"
        elif details.status == 'has invalid row':
            style_status = "color:#ff6262;background:#ffe8e8;"
        elif details.status  == 'pending':
            style_status = "color:#e9a700;background:#faecc9;"

        context['data_lists']['data'].append([  
                {
                    'type': 'value',
                    'value': details.batch_number if details.batch_number else 'For Success only',
                },
                {
                    'type': 'value',
                    'value': details.total_data,
                },
                {
                    'type': 'value',
                    'value': f"""
                        <div class="capitalize" style="{style_status}padding: 5px 12px; border-radius: 1rem;text-align:center;">
                            {details.status}
                        </div>
                    """, 
                    'td_class': 'whitespace-nowrap'
                },
                {
                    'type': 'value',
                    'value': details.date_created.strftime('%m-%d-%Y'), 
                    'td_class': 'whitespace-nowrap'
                },
                {
                    'type': 'html',
                    'value': action if details.status not in ('success', 'pending') else ''
                }
                
            ])  
    return render(request, template_name='components/tables/table_data/table_item3.html', context=context)



def table_user_guide(request): 
    subpage_url = reverse('main:table_item_user_guide')
    context = {
        'table_id': 'table_user_guide',
        'subpage_url': subpage_url,
        'request_data': dict(zip(request.GET.keys(), request.GET.values())),
        'is_hide_pagination': False,
        'data_lists': {
            'column': [ 
                {
                    'name': 'File Name',
                    'is_sorted': False
                }, 
                {
                    'name': 'Date time uploaded',
                    'is_sorted': False
                }
            ]
        }
    }
    return render(request, template_name='components/tables/main_table1.html', context=context)


def table_item_user_guide(request): 
    data = request.GET
    table_id = data.get('table_id')

    queryset = None

    queryset =  helpers.Paginator(queryset).paginate(
        page=data.get('page',1), 
        limit=data.get('limit',5)
    )

    column_count = data.get('column_count',1)
    context = {
        'table_id': table_id,
        'data_lists': {
            'pages': queryset['page_details'],
            'column_count': column_count,
            'data': [],
            'empty': {
                'icon': 'bx bxs-user-detail',
                'message': 'No User Guide Available'
            }
        },
        'is_hide_pagination': data.get('is_hide_pagination', '') in ('true', 'True')  
    }
    
    for details in queryset.get('data', []):  
        context['data_lists']['data'].append([  
                {
                    'type': 'value',
                    'value': f"""
                        <a href="{details.file.url}">
                            {details.file_name}
                        </a>
                    """,
                },
                {
                    'type': 'value',
                    'value': details.date_created.strftime('%m-%d-%Y %I:%M %p'), 
                    'td_class': 'whitespace-nowrap'
                } 
                
            ])  
    return render(request, template_name='components/tables/table_data/table_item3.html', context=context)



def table_policy_procedure(request): 
    subpage_url = reverse('main:table_item_policy_procedure')
    context = {
        'table_id': 'table_policy_procedure',
        'subpage_url': subpage_url,
        'request_data': dict(zip(request.GET.keys(), request.GET.values())),
        'is_hide_pagination': False,
        'data_lists': {
            'column': [ 
                {
                    'name': 'Policies and Procedures',
                    'is_sorted': False
                }, 
                  {
                    'name': 'Effectivity date',
                    'is_sorted': False
                }, 
                 {
                    'name': 'Uploaded file (Downloadable)',
                    'is_sorted': False
                }, 
                {
                    'name': 'Date uploaded',
                    'is_sorted': False
                }
            ]
        }
    }
    
    if request.user.is_superuser:
        context['data_lists']['column'].append({
                    'name': 'Action',
                    'is_sorted': False
                })
    return render(request, template_name='components/tables/main_table1.html', context=context)


def table_item_policy_procedure(request): 
    data = request.GET
    table_id = data.get('table_id')

    queryset = None

    _search = data.get("search", "") 
    if _search != "":
        orm_lookups = ["name__icontains", "file_name__icontains"]
        queryset = helpers.search_result(queryset, _search, orm_lookups, 0, False)  

    queryset =  helpers.Paginator(queryset).paginate(
        page=data.get('page',1), 
        limit=data.get('limit',5)
    )

    column_count = data.get('column_count',1)
    context = {
        'table_id': table_id,
        'data_lists': {
            'pages': queryset['page_details'],
            'column_count': column_count,
            'data': [],
            'empty': {
                'icon': 'bx bxs-user-detail',
                'message': 'No Policy Available'
            }
        },
        'is_hide_pagination': data.get('is_hide_pagination', '') in ('true', 'True')  
    }
    
    for details in queryset.get('data', []): 

        remove_url = reverse(
        'user:delete_policy'
    ) 
        action =  f"""
                            <div class=" dropdown"> 
                                <button class="" type="button" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                    <i class="fas fa-ellipsis-h"></i>
                                </button>

                                <div class="dropdown-menu" aria-labelledby="dropdownMenuButton"> 
                                    <a class="dropdown-item table-drop"  href="{details.file.url}" target="_blank">
                                        Download
                                    </a>  
                                    <div class="cursor-pointer dropdown-item table-drop delete-url-btn" data-url="{remove_url}" data-id="{details.pk}" data-status="delete" >
                                        Delete 
                                    </div>  
                                </div>
                            </div>
                            """
        
            
        data_object = [  
                {
                    'type': 'value',
                    'value': details.name,
                },
                 {
                    'type': 'value',
                    'value':  details.effectivity_date.strftime('%m-%d-%Y'), 
                },
                {
                    'type': 'value',
                    'value': f"""
                        <a target="_blank" style="text-decoration:underline" href="{details.file.url}">
                            {details.file_name}
                        </a>
                    """,
                },
                {
                    'type': 'value',
                    'value': details.date_created.strftime('%m-%d-%Y'), 
                    'td_class': 'whitespace-nowrap'
                } 
                
            ] 
         
        if request.user.is_superuser:
            data_object.append({
                    'type': 'html',
                    'value': action
                })
        context['data_lists']['data'].append(data_object)
    return render(request, template_name='components/tables/table_data/table_item3.html', context=context)