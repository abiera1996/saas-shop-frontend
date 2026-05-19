from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import os
import json
from app_user.models import PermissionModule, UserRolePermissionMapping, UserPermission, UserRole
from dateutil.relativedelta import relativedelta
from app_vehicle.models import VDF
from app_profile.models import Profile
from app_branch.models import Branch

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        import time 
        
        start = time.time()  
        vdfs = VDF.objects.filter(break_down_vehicle__isnull=False) 
        for vdf in vdfs: 
            vdf.break_down_vehicle_multiple.add(vdf.break_down_vehicle)
            vdf.save() 
        end = time.time()
        self.stdout.write(self.style.SUCCESS('%f seconds' % (end - start)))
        self.stdout.write(self.style.SUCCESS('Successfully setup'))

