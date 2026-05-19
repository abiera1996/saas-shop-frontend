from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import os
import json
from app_profile.models import Role
from dateutil.relativedelta import relativedelta


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        import time 
        
        start = time.time()  
        users = User.objects.filter(is_superuser=False)
        for user in users:
            user.username = user.first_name[0] + user.last_name
            user.save()

        end = time.time()
        self.stdout.write(self.style.SUCCESS('%f seconds' % (end - start)))
        self.stdout.write(self.style.SUCCESS('Successfully setup'))

