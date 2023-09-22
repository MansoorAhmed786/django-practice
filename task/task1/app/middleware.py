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
        print("hello")
        if request.path == '/api/books/':
            print("if")
            # print(request.user.email)
            logedin_user, _ = CustomUser.objects.get_or_create(email='admin@mail.com')
            # logedin_user, _ = CustomUser.objects.get_or_create(email=request.user.email)
            logedin_user.updated_time = timezone.now()
            count = logedin_user.count
            user_ip = request.META.get('REMOTE_ADDR')
            data = f"User IP: {user_ip}, Time: {timezone.now()}"
            with open('data.txt', 'a') as log_file:
                log_file.write(f"{data} Count : {count} \n")
            time_now = logedin_user.date_joined
            present_time = timezone.now()
            time = present_time - time_now 
            _ ,seconds = divmod(time.seconds,3600*60)
            group = logedin_user.group_type
            status = False
            print(seconds)
            print(logedin_user.count)
            if seconds > TIME_LIMIT:
                print("Success")  
                logedin_user.count=0
                logedin_user.date_joined=timezone.now()
                logedin_user.save()
            new_count = logedin_user.count
            new_time_now = logedin_user.date_joined
            new_present_time = timezone.now()
            timenew = new_present_time - new_time_now 
            _ ,seconds = divmod(timenew.seconds,3600*60)
            print(logedin_user.group_type)
            if group == 'GOLD' and new_count < GOLD and seconds < TIME_LIMIT:
                logedin_user.count+=1
                logedin_user.save()
                status = True
            elif group == 'SILVER' and new_count < SILVER and seconds < TIME_LIMIT:
                logedin_user.count+=1
                logedin_user.save()
                status = True
            elif group == 'BRONZE' and new_count < BRONZE and seconds < TIME_LIMIT:
                logedin_user.count+=1
                logedin_user.save()
                status = True
            if status :
                self.logger.info(data)
            else :
                response = HttpResponseForbidden("You don't have access")
                return response
        else:
            pass
