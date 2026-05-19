from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import os
import json
from app_profile.models import Profile, ProfilePermissionMapping
from app_user.models import UserRolePermissionMapping, UserPermission, UserRole
from dateutil.relativedelta import relativedelta
from utils.helpers import (
    id_generator
)
from app_vehicle.models import Vehicle, VehicleStatusHistory, VehicleAssignmentHistory, ServiceProvider, VDF, Supplier, SRF, SRFApproveHistory, SRFApprover, VDFApproveHistory, VDFApprover


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        import time 
        
        start = time.time()  

        srf_approver = [
            {
                'name': 'Branch Manager',
                'status_name': 'Queued to Branch Manager',
                'type':'default',
                'sequence': 1,
                'user_role': [
                   'BRNCH_MANAGER_1'
                ]
            },
           {
                'name': 'Tfleet personnel',
                'status_name': 'Queued to Tfleet personnel',
                'type':'default',
                'sequence': 2,
                'user_role': [
                   'TFLT_PRSNNL'
                ]
            },
            {
                'name': 'Tfleet Manager',
                'status_name': 'For PR/PO',
                'type':'default',
                'sequence': 3,
                'user_role': [
                   'TFLT_MNGR'
                ]
            }, 
        ]

        srf_tfleet_approver = [ 
           {
                'name': 'Tfleet personnel',
                'status_name': 'Queued to Tfleet personnel',
                'type':'tfleet',
                'sequence': 1,
                'user_role': [
                   'TFLT_PRSNNL'
                ]
            },
            {
                'name': 'Tfleet Manager',
                'status_name': 'For PR/PO',
                'type':'tfleet',
                'sequence': 2,
                'user_role': [
                   'TFLT_MNGR'
                ]
            }, 
        ]

        srf_approver += srf_tfleet_approver
        vdf_approver = [
            {
                'name': 'Branch Manager',
                'status_name': 'Queued to Branch Manager',
                'type':'default',
                'sequence': 1,
                'user_role': [
                   'BRNCH_MANAGER_1'
                ]
            },
             {
                'name': 'Group Head',
                'status_name': 'Queued to Group Head',
                'type':'default',
                'sequence': 2,
                'user_role': [
                   'GRP_HD'
                ]
            },
           {
                'name': 'Tfleet personnel',
                'status_name': 'Queued to Tfleet personnel',
                'type':'default',
                'sequence': 3,
                'user_role': [
                   'TFLT_PRSNNL'
                ]
            },
            {
                'name': 'Tfleet Manager',
                'status_name': 'For PR/PO',
                'type':'default',
                'sequence': 4,
                'user_role': [
                   'TFLT_MNGR'
                ]
            }, 
        ]

        vdf_tfleet_approver = [
            {
                'name': 'Branch Manager',
                'status_name': 'Queued to Branch Manager',
                'type':'tfleet',
                'sequence': 1,
                'user_role': [
                   'BRNCH_MANAGER_1'
                ]
            }, 
            {
                'name': 'Tfleet personnel',
                'status_name': 'Queued to Tfleet personnel',
                'type':'tfleet',
                'sequence': 2,
                'user_role': [
                   'TFLT_PRSNNL'
                ]
            },
            {
                'name': 'Tfleet Manager',
                'status_name': 'Queued to Tfleet Manager',
                'type':'tfleet',
                'sequence': 3,
                'user_role': [
                   'TFLT_MNGR'
                ]
            }, 
        ]
        vdf_approver += vdf_tfleet_approver
        for approver in srf_approver:
            user_role = approver.pop('user_role')
            obj, is_created  = SRFApprover.objects.get_or_create(
                **approver
            )
            user_role = UserRole.objects.filter(
                role_code__in=user_role
            )
            obj.user_role.clear()
            obj.user_role.add(*user_role)
            obj.save()
        
        for approver in vdf_approver:
            user_role = approver.pop('user_role')
            obj, is_created  = VDFApprover.objects.get_or_create(
                **approver
            )
            user_role = UserRole.objects.filter(
                role_code__in=user_role
            )
            obj.user_role.clear()
            obj.user_role.add(*user_role)
            obj.save()
                
        end = time.time()
        self.stdout.write(self.style.SUCCESS('%f seconds' % (end - start)))
        self.stdout.write(self.style.SUCCESS('Successfully setup'))

