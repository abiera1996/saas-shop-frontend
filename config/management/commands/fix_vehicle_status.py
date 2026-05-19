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
            history_status = VehicleStatusHistory.objects.filter(
                vehicle=vehicle
            ).order_by('-date_created').first()
            vehicle.vehicle_status = history_status.previous_status if history_status else vehicle.vehicle_status
            vehicle.save()
        end = time.time()
        self.stdout.write(self.style.SUCCESS('%f seconds' % (end - start)))
        self.stdout.write(self.style.SUCCESS('Successfully setup'))

