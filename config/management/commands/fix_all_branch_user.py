from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import os
import json
from app_user.models import PermissionModule, UserRolePermissionMapping, UserPermission, UserRole
from dateutil.relativedelta import relativedelta

from app_profile.models import Profile
from app_branch.models import Branch

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        import time 
        
        start = time.time()  
        profiles = Profile.objects.filter(role__role_code='SYSTMSR_1')
        branch_count = Branch.objects.all().count()
        for profile in profiles: 
            if hasattr(profile, 'userbranch'):
                
                profile_branch = profile.userbranch.branches.all().count() 
                if profile_branch == branch_count:
                    profile.is_all_branch = True
                    profile.save()
        end = time.time()
        self.stdout.write(self.style.SUCCESS('%f seconds' % (end - start)))
        self.stdout.write(self.style.SUCCESS('Successfully setup'))

