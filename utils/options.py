category_option = [
        {
            'name': 'Select Category',
            'value': ''
        },
        {
            'name': '2 Wheels',
            'value': '2 wheels'
        },
        {
            'name': '3 Wheels',
            'value': '3 wheels'
        },
        {
            'name': '4 Wheels',
            'value': '4 wheels'
        },
        {
            'name': '6 Wheels',
            'value': '6 wheels'
        },
        {
            'name': '10 Wheels',
            'value': '10 wheels'
        }
    ] 

status_option = [
    {
        'name': 'Select Status',
        'value': ''
    }, 
    {
        'name': 'Active',
        'value': 'active'
    },
    {
        'name': 'Short-term breakdown',
        'value': 'short-term breakdown'
    },
    {
        'name': 'Permanent breakdown',
        'value': 'permanent breakdown'
    },
    {
        'name': 'For disposal',
        'value': 'for disposal'
    },
    {
        'name': 'Disposed',
        'value': 'disposed'
    }
] 

repair_status_option = [
    {
        'name': 'Select Status',
        'value': ''
    }, 
    {
        'name': 'Pending',
        'value': 'pending'
    },
    {
        'name': 'Done',
        'value': 'done'
    } 
] 

reason_for_rental_list = [
    {
        'value': '',
        'name': "Select Reason"
    },
    {
        'value': 'Additional vehicle for regular route or OTD',
        'name': 'Additional vehicle for regular route or OTD'
    },
    {
        'value': 'No assigned T-fleet vehicle',
        'name': 'No assigned T-fleet vehicle'
    },
    {
        'value': 'Replacement of breakdown T-fleet vehicle',
        'name': 'Replacement of breakdown T-fleet vehicle'
    },
    {
        'value': 'Other justification/request',
        'name': 'Other justification/request'
    }, 
]

classification_list = [
    {
        'value': '',
        'name': "Select"
    },
    {
        'value': 'Employee / on-call',
        'name': 'Employee / on-call'
    },
    {
        'value': '3rd party',
        'name': '3rd party'
    }, 
]


recommendation_list = [
    {
        'value': '',
        'name': "Select recommendation"
    },
    {
        'value': 'sell as junk',
        'name': 'Sell as junk'
    },
    {
        'value': 'sell as vehicle with OR/CR',
        'name': 'Sell as vehicle with OR/CR'
    },
    {
        'value': 'Other',
        'name': 'Other'
    },
]


lease_type_list = [
    {
        'value': '',
        'name': "Select Lease Type"
    },
    {
        'value': 'dry',
        'name': 'Dry'
    },
    {
        'value': 'wet',
        'name': 'Wet'
    }, 
]

MONTHS_OPTION = [
    {
        'name': 'Select Month',
        'value': ''
    },
    {
        'name': 'January',
        'value': '1'
    },
    {
        'name': 'February',
        'value': '2'
    },
    {
        'name': 'March',
        'value': '3'
    },
    {
        'name': 'April',
        'value': '4'
    },
    {
        'name': 'May',
        'value': '5'
    },
    {
        'name': 'June',
        'value': '6'
    },
    {
        'name': 'July',
        'value': '7'
    },
    {
        'name': 'August',
        'value': '8'
    },
    {
        'name': 'September',
        'value': '9'
    },
    {
        'name': 'October',
        'value': '10'
    },
    {
        'name': 'November',
        'value': '11'
    },
    {
        'name': 'December',
        'value': '12'
    },
] 


SRF_OPTION = [
            {"name": "FILTER BY STATUS", "isHeader":True},
            {"name": "Select All Status", "value": ""},
            {"name": "Draft", "class": "", "value": "pending"},
            {"name": "Queued to branch / dept manager	", "class": "", "value": "for branch manager endorsement"},
            {"name": "Queued to Group Head	", "class": "", "value": "for group head approval"}, 
            {"name": "Queued to Tfleet Personnel", "class": "", "value": "for Tfleet personnel endorsement"},
            {"name": "Queued to T-fleet Manager", "class": "", "value": "for Tfleet manager approval"},
            {"name": "Rejected", "class": "", "value": "rejected by Tfleet manager,rejected by group head"},
            {"name": "Approved", "class": "", "value": "approved"},
            {"name": "Complete", "class": "", "value": "complete"},
        ]


VDF_OPTIONS = [
            {"name": "FILTER BY STATUS", "isHeader":True},
            {"name": "Select All Status", "value": ""},
            {"name": "Draft", "class": "", "value": "pending"},
            {"name": "Queued to branch / dept manager", "class": "", "value": "for branch manager endorsement"},
            {"name": "Queued to Group Head", "class": "", "value": "for group head approval"}, 
            {"name": "Queued to Tfleet Personnel", "class": "", "value": "for Tfleet personnel approval"},
            {"name": "Queued to Tfleet manager", "class": "", "value": "for Tfleet manager approval"},
            {"name": "Rejected", "class": "", "value": "rejected by Tfleet personnel,rejected by group head,rejected by Tfleet manager"},
            {"name": "Approved", "class": "", "value": "approved"},
            # {"name": "Complete", "class": "", "value": "complete"},
        ]


DISPOSAL_OPTIONS = [
            {"name": "FILTER BY STATUS", "isHeader":True},
            {"name": "Select All Status", "value": ""},
            {"name": "Draft", "class": "", "value": "pending"},
            {"name": "Queued to branch / dept manager", "class": "", "value": "for branch manager recommendation"},
            {"name": "Queued to Tfleet manager", "class": "", "value": "for Tfleet manager approval"},
            {"name": "Queued to Purchasing Head", "class": "", "value": "for Purchasing manager approval"},
            {"name": "For actual details setup", "class": "", "value": "for actual details setup"},
            {"name": "Rejected", "class": "", "value": "rejected by branch manager,rejected by Tfleet manager,rejected by Purchasing manager"},
            {"name": "For disposal", "class": "", "value": "for disposal"},
        ]



def option_status_display(text):
    if text == 'pending':
        return 'Draft'
    if text == 'for branch manager endorsement':
        return 'Queued to branch / dept manager'
    if text == 'for group head approval':
        return 'Queued to Group Head'
    if text in ('rejected by group head', 'rejected by Tfleet manager', 'rejected by Purchasing manager') :
        return 'Rejected'
    if text == 'for Tfleet personnel endorsement':
        return 'Queued to Tfleet Personnel'
    if text == 'for Tfleet manager approval':
        return 'Queued to T-fleet Manager' 
    if text == 'for Tfleet manager approval':
        return 'Queued to T-fleet Manager' 
    if text == 'for Purchasing manager approval':
        return 'Queued to Purchasing Head'
    if text == 'for Tfleet personnel approval':
        return 'Queued to tfleet personnel'
    if text == 'approved':
        return 'Approved'
    return text


vdf_status_option = [
    {
        'name': 'Select Status',
        'value': ''
    }, 
    {
        'name': 'Active',
        'value': 'active'
    },
    {
        'name': 'Short-term breakdown',
        'value': 'short-term breakdown'
    },
    {
        'name': 'Permanent breakdown',
        'value': 'permanent breakdown'
    }
] 