from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import os
import json
from app_profile.models import Role
from dateutil.relativedelta import relativedelta


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        import time 
        
        start = time.time()  

        roles = [
            {
                'name': 'System User',
                'role_code': 'SYSTMSR_1'
            },
            {
                'name': 'Branch',
                'role_code': 'BRNCH_1'
            },
            {
                'name': 'Admin',
                'role_code': 'DMN_1'
            }
        ]
        for role in roles:
            roleobj , is_created = Role.objects.get_or_create(role_code=role['role_code'])
            roleobj.name = role['name']
            roleobj.save()
            
        end = time.time()
        self.stdout.write(self.style.SUCCESS('%f seconds' % (end - start)))
        self.stdout.write(self.style.SUCCESS('Successfully setup'))

