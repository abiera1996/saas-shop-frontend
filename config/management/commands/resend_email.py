from utils.helpers import (
    decode_request_body,
    id_generator,   
    search_result,
    Paginator, 
    force_logout_user,
    send_email
) 
from config import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import os
import json, datetime 
from dateutil.relativedelta import relativedelta
from django.template.loader import get_template 

from django.db.models import F, ExpressionWrapper, CharField, Value

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        import time 
        
        start = time.time()  
        users = User.objects.filter(
            date_joined__date=datetime.datetime.strptime('02-18-2024', "%m-%d-%Y").date()
        ).annotate(
            user_role_name=F('profile__user_role__name')
        )
        for user in users:
            user.set_password('password123')
            profile = user.profile
            profile.current_password = 'password123'
            profile.save()
            user.save()
            html = get_template('email_template/send_user_creation.html') 
            context = {
                'base_url': settings.BASE_URL,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'username':user.username,
                'userrole_name':user.user_role_name,
                'email':user.email
            }
            send_email(
                'WExpress Account Details', 
                html.render(context),
                [user.email]
            )
        end = time.time()
        self.stdout.write(self.style.SUCCESS('%f seconds' % (end - start)))
        self.stdout.write(self.style.SUCCESS('Successfully setup settings'))

