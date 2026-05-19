from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import os
import json
from app_profile.models import Profile, UserBranch
from dateutil.relativedelta import relativedelta
from app_branch.models import Branch
from app_vehicle.models import Vehicle, VehicleStatusHistory, VehicleAssignmentHistory

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        import time 
        
        start = time.time()  
        profiles = Profile.objects.filter(current_password='password123')
        for profile in profiles: 
            user = profile.user
            user.set_password('password123')
            user.save()
        end = time.time()
        self.stdout.write(self.style.SUCCESS('%f seconds' % (end - start)))
        self.stdout.write(self.style.SUCCESS('Successfully setup'))

