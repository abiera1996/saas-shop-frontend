from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import os
import json
from app_user.models import PermissionModule, UserRolePermissionMapping, UserPermission, UserRole
from dateutil.relativedelta import relativedelta


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        import time 
        
        start = time.time()  

        roles = [ 
            {
                'name': 'DASHBOARD',
                'order': 0,
                'permission': [
                    {
                        'name': 'View Vehicles Information',
                        'code': 'VW_VHCLS_NFRMTN'
                    }, 
                    {
                        'name': 'View SRF Information',
                        'code': 'VW_SRF_NFRMTN'
                    }, 
                    {
                        'name': 'View VDF Information',
                        'code': 'VW_VDF_NFRMTN'
                    }, 
                    {
                        'name': 'View Insurance Information',
                        'code': 'VW_NSRNC_NFRMTN'
                    }, 
                     {
                        'name': 'View Vehicle Registration',
                        'code': 'VW_VHCL_RGSTRTN'
                    }, 
                ]
            },
            {
                'name': 'SRF CREATION',
                'order': 1,
                'permission': [
                    {
                        'name': 'Create SRF',
                        'code': 'CRT_SRF'
                    }, 
                ]
            },
            {
                'name': 'VDF CREATION',
                'order': 2,
                'permission': [
                    {
                        'name': 'Create VDF',
                        'code': 'CRTVDF'
                    }, 
                ]
            },
            {
                'name': 'Vehicle Disposal Creation',
                'order': 3,
                'permission': [
                    {
                        'name': 'Create Disposal of Vehicle',
                        'code': 'CRTDSPSLFVHCL'
                    }, 
                ]
            }, 
            {
                'name': 'BRANCH / DEPT',
                'order': 4,
                'permission': [
                    {
                        'name': 'Create and Edit Branch',
                        'code': 'CRT_BRNCH'
                    }, 
                    {
                        'name': 'View Branches',
                        'code': 'VWBRNCHS'
                    } 
                ]
            }, 
            {
                'name': 'MASTERLIST OF VEHICLES',
                'order': 5,
                'permission': [
                    {
                        'name': 'Create/Import and Edit Vehicle',
                        'code': 'CRTMPRTVHCLE'
                    }, 
                    {
                        'name': 'View Vehicles',
                        'code': 'VWVHCLS'
                    },
                    {
                        'name': 'Edit Vehicle Status',
                        'code': 'DTVHCLSTTS'
                    } 
                ]
            }, 
            {
                'name': 'SERVICE REQUEST MAINTENANCE FORM',
                'order': 6,
                'permission': [
                    {
                        'name': 'View SRF',
                        'code': 'VWSRF'
                    },
                    {
                        'name': 'View SRF KPI',
                        'code': 'VWSRFKP'
                    },
                    {
                        'name': 'View Repair and Maintenance History',
                        'code': 'VWRPRNDMNTNNCHSTRY'
                    }, 
                    {
                        'name': 'Batch Approval SRF',
                        'code': 'BTCHPPRVLSRF'
                    },
                    {
                        'name': 'Approve and Reject SRF',
                        'code': 'PPRVRJCTSRF'
                    },
                    {
                        'name': 'Complete SRF',
                        'code': 'CMPLTSRF'
                    }, 
                    {
                        'name': 'Reject for Completion SRF',
                        'code': 'RJCTCMPLTSRF'
                    }, 
                    {
                        'name': 'View Actual vs. Budget',
                        'code': 'VWCTLVSBDGT'
                    }, 
                    {
                        'name': 'Import Actual vs. Budget',
                        'code': 'MPRTCTLVSBDGT'
                    },
                    {
                        'name': 'Approve and Reject Actual vs. Budget',
                        'code': 'PPRVRJCTCTLVSBDGT'
                    },
                    {
                        'name': 'Import SRF',
                        'code': 'MPRTCRT_SRF'
                    }, 
                    {
                        'name': 'Import SRF Previous Data',
                        'code': 'MPRTCRT_SRF_PRVS_DT'
                    }, 
                ]
            },   
            {
                'name': 'VEHICLE DISPATCH FORM',
                'order': 7,
                'permission': [
                    {
                        'name': 'View VDF',
                        'code': 'VWVDF'
                    },
                    {
                        'name': 'View VDF approval KPI',
                        'code': 'VWVHVLDSPTCHKP'
                    }, 
                    {
                        'name': 'Batch Approval VDF',
                        'code': 'BTCHPPRVLVDF'
                    },
                    {
                        'name': 'Approve and Reject VDF',
                        'code': 'PPRVNDRJCTVDF'
                    }, 
                    {
                        'name': 'Import VDF',
                        'code': 'MPRTCRT_VDF'
                    }, 
                    {
                        'name': 'Import VDF Previous Data',
                        'code': 'MPRTCRT_VDF_PRVS_DT'
                    }, 
                ]
            }, 
            {
                'name': 'DISPOSAL OF VEHICLES',
                'order': 8,
                'permission': [
                    {
                        'name': 'View Disposal of Vehicle',
                        'code': 'VWDSPSLFVHCL'
                    },  
                    {
                        'name': 'Approve and Reject Vehicle Disposal',
                        'code': 'PPRVNDRJCTVHCLDSPSL'
                    },
                    {
                        'name': 'Endorse/Recommend Vehicle Disposal',
                        'code': 'NDRSRCMMNDVHCLDSPSL'
                    }, 
                    {
                        'name': 'Complete Vehicle Disposal',
                        'code': 'CMPLTVHCLDSPSL'
                    }, 
                ]
            }, 
            {
                'name': 'GASOLINE CONSUMPTION MONITORING',
                'order': 9,
                'permission': [
                    {
                        'name': 'Create Gasoline Consumption',
                        'code': 'CRTGSLNCNSMPTN'
                    }, 
                    {
                        'name': 'Approve and Reject Gasoline',
                        'code': 'PPRVNDRJCTGSLN'
                    },
                    {
                        'name': 'View Gasoline',
                        'code': 'VWGSLN'
                    },
                    {
                        'name': 'View Gasoline History',
                        'code': 'VWGSLNHSTRY'
                    },
                    
                ]
            }, 
            {
                'name': 'TFLEET VEHICLE RENTAL BILLINGS',
                'order': 10,
                'permission': [
                    {
                        'name': 'View Billings',
                        'code': 'VWBLLNGS'
                    },
                    {
                        'name': 'View Billing History',
                        'code': 'VWBLLNGHSTRY'
                    },
                    {
                        'name': 'Create Billing',
                        'code': 'CRTBLLNG'
                    }, 
                    {
                        'name': 'Approve and Reject Billing',
                        'code': 'PPRVNDRJCTBLLNG'
                    }, 
                    {
                        'name': 'Locked and Unlocked Billing',
                        'code': 'LCKDBLLNG'
                    } 
                ]
            }, 
            {
                'name': 'INSURANCE MONITORING',
                'order': 11,
                'permission': [
                    {
                        'name': 'View Insurance',
                        'code': 'VWNSRNC'
                    }, 
                    {
                        'name': 'Create Insurance',
                        'code': 'CRNSRNC'
                    }, 
                    {
                        'name': 'Approve and Reject Insurance',
                        'code': 'PPRVNDRJCTNSRNC'
                    },
                    {
                        'name': 'Update Remarks',
                        'code': 'PDTNSRNCRMRKS'
                    }, 
                ]
            }, 
             {
                'name': 'VEHICLE REGISTRATION MONITORING',
                'order': 11,
                'permission': [
                    {
                        'name': 'View Vehicle Registration',
                        'code': 'VWVHCLRGSTRTN'
                    }, 
                    {
                        'name': 'Batch Upload Vehicle Registration',
                        'code': 'CRVHCLRGSTRTN'
                    }, 
                    {
                        'name': 'Approve and Reject Vehicle Registration',
                        'code': 'PPRVNDRJCTVHCLRGSTRTN'
                    }, 
                        {
                        'name': 'Update Remarks',
                        'code': 'PDTVHCLRGSTRTNRMRKS'
                    }, 
                ]
            }, 
            {
                'name': 'MASTERLIST OF THIRD PARTY PROVIDERS',
                'order': 12,
                'permission': [
                    {
                        'name': 'View Service Provider',
                        'code': 'VWSRVCPRVDR'
                    }, 
                    {
                        'name': 'Create Service Provider',
                        'code': 'CRTSRVCPRVDR'
                    }, 
                    {
                        'name': 'Approve and Reject Service Provider',
                        'code': 'PPRVNDRJCTSRVCPRVDR'
                    }, 
                    {
                        'name': 'Setup MDS Route',
                        'code': 'DDMDSRT'
                    } 
                ]
            }, 
            {
                'name': 'MASTERLIST OF REPAIRS ACCREDITED SUPPLIERS',
                'order': 13,
                'permission': [
                    {
                        'name': 'View Supplier',
                        'code': 'VWSSPPLR'
                    }, 
                    {
                        'name': 'Create Supplier',
                        'code': 'CRTSSPPLR'
                    }, 
                    {
                        'name': 'Approve and Reject Supplier',
                        'code': 'PPRVNDRJCTSSPPLR'
                    } 
                ]
            }, 
            
            {
                'name': 'SETTINGS',
                'order': 14,
                'permission': [
                    {
                        'name': 'Add and Edit User',
                        'code': 'DDDTSR'
                    },
                    {
                        'name': 'View User',
                        'code': 'VWSR'
                    },
                    {
                        'name': 'Add and Edit User Role',
                        'code': 'DDDTSRRL'
                    },
                    {
                        'name': 'View User Role',
                        'code': 'VWSRRL'
                    },
                    {
                        'name': 'View Audit Logs',
                        'code': 'VWDTLGS'
                    },
                ]
            },
        ]
        for role in roles:
            roleobj , is_created = PermissionModule.objects.get_or_create(name=role['name'])
            roleobj.name = role['name']
            roleobj.order = role['order']
            roleobj.save() 
            for permission in role['permission']:
                permission_obj , is_created = UserPermission.objects.get_or_create(
                    code=permission['code'],
                    permission_module = roleobj
                ) 
                permission_obj.name = permission['name']
                permission_obj.save()
            
        end = time.time()
        self.stdout.write(self.style.SUCCESS('%f seconds' % (end - start)))
        self.stdout.write(self.style.SUCCESS('Successfully setup permission'))

