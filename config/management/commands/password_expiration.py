from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import os
import json
from app_profile.models import Profile
from dateutil.relativedelta import relativedelta
import datetime  

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        import time 
        
        start = time.time()  
        profiles = Profile.objects.all()
        for profile in profiles:
            if profile.password_expiration is None:
                profile.password_expiration = relativedelta(days=90) + datetime.date.today()
                profile.save()

        end = time.time()
        self.stdout.write(self.style.SUCCESS('%f seconds' % (end - start)))
        self.stdout.write(self.style.SUCCESS('Successfully setup'))

