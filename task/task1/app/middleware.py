import logging
from typing import Any
from django.utils import timezone
from .models import CustomUser
from django.http import HttpResponseForbidden
from task1.settings import GOLD,SILVER,BRONZE,TIME_LIMIT

class LogUserIpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self,request, view_func, view_args, view_kwargs):
        if request.path == '/api/books/':
            logedin_user, is_created = CustomUser.objects.get_or_create(email=request.user.email)
            logedin_user.updated_time = timezone.now()
            
            count = logedin_user.count
            group = logedin_user.group_type
            time_now = logedin_user.date_joined
            user_ip = request.META.get('REMOTE_ADDR')

            with open('data.txt', 'a') as log_file:
                log_file.write(f"User IP: {user_ip}, Time: {timezone.now()} Count : {count} \n")
            
            present_time = timezone.now()
            time = present_time - time_now 
            _ , seconds = divmod(time.seconds,3600*60)
            status = False

            if seconds > TIME_LIMIT:
                logedin_user.count=0
                logedin_user.date_joined=timezone.now()
                logedin_user.save()

            new_count = logedin_user.count
            if group == 'GOLD' and new_count < GOLD:
                logedin_user.count+=1
                logedin_user.save()
                status = True
            elif group == 'SILVER' and new_count < SILVER:
                logedin_user.count+=1
                logedin_user.save()
                status = True
            elif group == 'BRONZE' and new_count < BRONZE:
                logedin_user.count+=1
                logedin_user.save()
                status = True
            if not status :
                return HttpResponseForbidden("You don't have access")
        else:
            pass
