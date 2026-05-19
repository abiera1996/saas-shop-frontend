from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import os
import json
from app_user.models import PermissionModule, UserRolePermissionMapping, UserPermission, UserRole
from dateutil.relativedelta import relativedelta

from app_vehicle.models import Vehicle, VehicleStatusHistory, VehicleAssignmentHistory

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        import time 
        
        start = time.time()  
        vehicles = Vehicle.objects.all()
        for vehicle in vehicles: 
            VehicleAssignmentHistory.objects.create(
                vehicle=vehicle,
                previous_branch=vehicle.branch,
                assignmet_date=vehicle.start_date_assignment,
                date_created=vehicle.date_created
            )
            VehicleStatusHistory.objects.create(
                vehicle=vehicle,
                branch=vehicle.branch,
                previous_status=vehicle.vehicle_status,
                date_created=vehicle.date_created
            )
        end = time.time()
        self.stdout.write(self.style.SUCCESS('%f seconds' % (end - start)))
        self.stdout.write(self.style.SUCCESS('Successfully setup'))

