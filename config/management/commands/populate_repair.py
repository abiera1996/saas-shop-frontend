from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import os
import json
from app_user.models import PermissionModule, UserRolePermissionMapping, UserPermission, UserRole
from dateutil.relativedelta import relativedelta

from app_vehicle.models import RepairClassification

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        import time 
        
        start = time.time()  
        data_list = [
            "Tire Replacement",
            "Body Repair",
            "Mechanical Repair",
            "Preventive Maintenance",
            "Battery Replacement",
            "Vehicle Registration"
        ]
        for details in data_list:
            RepairClassification.objects.get_or_create(
                name=details
            )
        end = time.time()
        self.stdout.write(self.style.SUCCESS('%f seconds' % (end - start)))
        self.stdout.write(self.style.SUCCESS('Successfully setup repair classification'))

