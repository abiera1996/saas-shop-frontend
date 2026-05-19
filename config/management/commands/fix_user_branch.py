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
        profiles = Profile.objects.all()
        for profile in profiles: 
            if not hasattr(profile,'userbranch'):
                branches = Branch.objects.all()
                user_branch = UserBranch.objects.create(
                    profile=profile
                )  
                user_branch.branches.add(*branches)
                user_branch.save()
        end = time.time()
        self.stdout.write(self.style.SUCCESS('%f seconds' % (end - start)))
        self.stdout.write(self.style.SUCCESS('Successfully setup'))

