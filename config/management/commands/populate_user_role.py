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

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        import time 
        
        start = time.time()  

        roles = [
            {
                'name': 'Branch Staff',
                'role_code': 'STFF_1',
                'permission': [
                    'CRT_SRF',
                    'CRTVDF', 
                    'VWBRNCHS',
                    'VWRPRNDMNTNNCHSTRY',
                    'VWSRFKP',
                    'VWSRF',
                    'VWVDF', 
                    'VWVHVLDSPTCHKP', 
                    'DDMDSRT',
                    'VWSRVCPRVDR'
                ]
            },
            {
                'name': 'Branch Manager',
                'role_code': 'BRNCH_MANAGER_1',
                'permission': [
                    'PPRVNDRJCTVDF',
                    'PPRVRJCTSRF', 
                    'VWVHCLS',
                    'VWRPRNDMNTNNCHSTRY',
                    'VWSRF',
                    'VWVDF', 
                    'VWVHVLDSPTCHKP',
                    'CRTDSPSLFVHCL',
                    'NDRSRCMMNDVHCLDSPSL',
                    'VWDSPSLFVHCL', 
                ]
            },
            {
                'name': 'Group Head',
                'role_code': 'GRP_HD',
                'permission': [
                    'PPRVRJCTSRF',
                    'PPRVNDRJCTVDF',
                    'VWRPRNDMNTNNCHSTRY',
                    'VWSRF',
                    'VWVDF', 
                    'VWVHVLDSPTCHKP',
                ]
            },
            {
                'name': 'Tfleet assigned personnel',
                'role_code': 'TFLT_PRSNNL',
                'permission': [ 
                    'PPRVNDRJCTVDF',
                    'PPRVRJCTSRF',
                    'CMPLTSRF',
                    'PPRVNDRJCTVDF',
                    'VWRPRNDMNTNNCHSTRY',
                    'VWSRF',
                    'VWVDF', 
                    'CRTMPRTVHCLE',
                    'VWVHCLS',
                    'VWVHVLDSPTCHKP',
                    'VWCTLVSBDGT',
                    'MPRTCTLVSBDGT',
                ]
            },
            {
                'name': 'Tfleet manager',
                'role_code': 'TFLT_MNGR',
                'permission': [
                    'PPRVRJCTSRF',
                    'VWVDF',
                    'PPRVNDRJCTVDF',
                    'VWRPRNDMNTNNCHSTRY',
                    'VWSRF',
                    'PPRVNDRJCTGSLN',
                    'VWGSLN',
                    'VWGSLNHSTRY',
                    'PPRVNDRJCTBLLNG',
                    'VWBLLNGS',
                    'VWBLLNGHSTRY',
                    'VWVHVLDSPTCHKP',
                    'VWDSPSLFVHCL',
                    'PPRVNDRJCTVHCLDSPSL',
                    'PPRVRJCTCTLVSBDGT',
                    'VWCTLVSBDGT',
                    'CMPLTSRF'
                ]
            },
            {
                'name': 'Tfleet staff',
                'role_code': 'TFLSTFF',
                'permission': [ 
                    'VWGSLN',
                    'VWGSLNHSTRY',
                    'CRTGSLNCNSMPTN',
                    'VWBLLNGS',
                    'VWBLLNGHSTRY',
                    'CRTBLLNG',
                    'VWNSRNC',
                    'VWNSRNC',
                    'CRNSRNC',
                    'VWVHVLDSPTCHKP',
                    'CRT_SRF',
                    'VWSRFKP',
                    'VWSRF',
                    'PPRVRJCTSRF',
                    'CMPLTSRF',
                ]
            }, 
            {
                'name': 'Purchasing Staff',
                'role_code': 'PRCHSNGSTFF',
                'permission': [ 
                    'VWNSRNC',
                    'VWNSRNC',
                    'CRNSRNC',
                    'VWSRVCPRVDR',
                    'CRTSRVCPRVDR',
                    'VWSSPPLR',
                    'CRTSSPPLR',
                    'VWVHVLDSPTCHKP',
                    'VWDSPSLFVHCL',
                    'CMPLTVHCLDSPSL',
                    'PDTNSRNCRMRKS',
                ]
            }, 
            {
                'name': 'Purchasing Manager',
                'role_code': 'PRCHSNGMNGR',
                'permission': [ 
                    'VWNSRNC',
                    'VWNSRNC',
                    'PPRVNDRJCTNSRNC',
                    'VWSRVCPRVDR',
                    'PPRVNDRJCTSRVCPRVDR',
                    'PPRVNDRJCTSSPPLR',
                    'VWSSPPLR',
                    'VWVHVLDSPTCHKP',
                    'VWDSPSLFVHCL',
                    'PPRVNDRJCTVHCLDSPSL',
                ]
            }, 
            {
                'name': 'Accounting Staff',
                'role_code': 'CCNTING_STFF',
                'permission': [  
                    'VWBLLNGS',
                    'VWBLLNGHSTRY',
                    'LCKDBLLNG'
                ]
            },
        ]
        for role in roles:
            roleobj, is_created = UserRole.objects.get_or_create(role_code=role['role_code'])
            
            roleobj.name = role['name']
            roleobj.save()
            UserRolePermissionMapping.objects.filter(user_role=roleobj).delete()
            profiles = Profile.objects.filter(user_role=roleobj) 
            for profile in profiles: 
                ProfilePermissionMapping.objects.filter(profile=profile).delete()

            for permission in role['permission']:
                perm = UserPermission.objects.get(code=permission)
                
                UserRolePermissionMapping.objects.create(
                    user_role=roleobj,
                    user_permission=perm,
                    has_permission=True
                )
                
                for profile in profiles: 
                    ProfilePermissionMapping.objects.create(
                        profile=profile,
                        user_permission=perm,
                        has_permission=True
                    )

                
        end = time.time()
        self.stdout.write(self.style.SUCCESS('%f seconds' % (end - start)))
        self.stdout.write(self.style.SUCCESS('Successfully setup'))

