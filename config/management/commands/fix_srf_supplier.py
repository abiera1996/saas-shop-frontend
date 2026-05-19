from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import os
import json
from app_user.models import PermissionModule, UserRolePermissionMapping, UserPermission, UserRole
from dateutil.relativedelta import relativedelta

from app_vehicle.models import Vehicle, VehicleStatusHistory, VehicleAssignmentHistory, ServiceProvider, VDF, Supplier, SRF

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        import time 
        
        start = time.time()  
        vdfs = SRF.objects.all()
        for vdf in vdfs:
            provider = Supplier.objects.filter(accreditation_no=vdf.accreditation_no_supplier).first()
            if provider:
                try:
                    vdf.supplier = provider
                    vdf.save()
                except:
                    vdf.actual_repair_ytd = 0
                    vdf.annual_repair_budget= 0
                    vdf.variance= 0
                    vdf.supplier = provider
                    vdf.save()
        end = time.time()
        self.stdout.write(self.style.SUCCESS('%f seconds' % (end - start)))
        self.stdout.write(self.style.SUCCESS('Successfully setup'))

