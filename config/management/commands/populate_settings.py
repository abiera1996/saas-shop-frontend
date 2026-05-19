from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import os
import json
from dateutil.relativedelta import relativedelta
  

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        import time 
        
        start = time.time()  
        obj, is_created = Settings.objects.get_or_create(
            key='srf_counter'
        )
        if is_created:
            obj.value = 0
            obj.save()
        obj, is_created = Settings.objects.get_or_create(
            key='vdf_counter'
        )
        if is_created:
            obj.value = 0
            obj.save()

        obj, is_created = Settings.objects.get_or_create(
            key='supplier_counter'
        )
        if is_created:
            obj.value = 0
            obj.save()

        obj, is_created = Settings.objects.get_or_create(
            key='provider_counter'
        )
        if is_created:
            obj.value = 0
            obj.save()

        obj, is_created = Settings.objects.get_or_create(
            key='disposal_counter'
        )
        if is_created:
            obj.value = 0
            obj.save()
        
        obj, is_created = Settings.objects.get_or_create(
            key='batch_upload_counter'
        )
        if is_created:
            obj.value = 0
            obj.save()

        end = time.time()
        self.stdout.write(self.style.SUCCESS('%f seconds' % (end - start)))
        self.stdout.write(self.style.SUCCESS('Successfully setup settings'))

