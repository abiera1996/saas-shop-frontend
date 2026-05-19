from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import os
import json
from app_user.models import PermissionModule, UserRolePermissionMapping, UserPermission, UserRole
from dateutil.relativedelta import relativedelta
from app_gas_consumption.models import GasConsumption
from app_profile.models import Profile
from app_branch.models import Branch

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        import time 
        
        start = time.time()  
        profiles = GasConsumption.objects.all() 
        for profile in profiles: 
            profile.km_liter = round((profile.km_run / profile.no_liters_consumed), 2)
            profile.save() 
        end = time.time()
        self.stdout.write(self.style.SUCCESS('%f seconds' % (end - start)))
        self.stdout.write(self.style.SUCCESS('Successfully setup'))

