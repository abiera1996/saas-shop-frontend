from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import os
import json
from app_user.models import PermissionModule, UserRolePermissionMapping, UserPermission, UserRole
from dateutil.relativedelta import relativedelta

from app_vehicle.models import Vehicle, VehicleStatusHistory, VehicleAssignmentHistory, ServiceProvider, VDF

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        import time 
        
        start = time.time()  
        vdfs = VDF.objects.all()
        for vdf in vdfs:
            provider = ServiceProvider.objects.filter(accreditation_no=vdf.accreditation_no_provider).first()
            if provider:
                vdf.provider = provider
                vdf.save()
        end = time.time()
        self.stdout.write(self.style.SUCCESS('%f seconds' % (end - start)))
        self.stdout.write(self.style.SUCCESS('Successfully setup'))

