# Create a custom middleware in middleware.py

import logging
from django.utils import timezone
from .models import CustomUser
from django.http import HttpResponseForbidden

class LogUserIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        # count= CustomUser.objects.count()
        logedinUser = CustomUser.objects.get()
        timenow = logedinUser.date_joined
        presenttime = timezone.now()
        time = presenttime - timenow 
        minutes1,seconds = divmod(time.seconds,3600*60)
        print(f"Time Difference: hours,  minutes, {seconds} seconds")
        count = logedinUser.count
        group = logedinUser.group_type
        print(group)
        print(seconds)
        status = False
        if seconds > 60:
            logedinUser.count=0
            logedinUser.date_joined=timezone.now()
            logedinUser.save()
        newlogedinUser = CustomUser.objects.get()
        newcount = newlogedinUser.count
        newtimenow = newlogedinUser.date_joined
        presenttime = timezone.now()
        timenew = presenttime - newtimenow 
        minutes1,seconds = divmod(timenew.seconds,3600*60)
        print(f"Time Difference: hours,  minutes, {seconds} seconds")
        if group == 'gold' and newcount < 10 and seconds<60:
            logedinUser.count+=1
            logedinUser.save()
            status = True
            print("ok")
        elif group == 'silver' and newcount < 7 and seconds<60:
            logedinUser.count+=1
            logedinUser.save()
            status = True
            print("Silver")
        elif group == 'bronze' and newcount < 5 and seconds<60:
            logedinUser.count+=1
            logedinUser.save()
            status = True
            print("Bronze")

        afterlogedinUser = CustomUser.objects.get()
        newcount = afterlogedinUser.count
        user_ip = request.META.get('REMOTE_ADDR')
        data = f"User IP: {user_ip}, Time: {timezone.now()}"
        with open('data.txt', 'a') as log_file:
            log_file.write(f"{data} Count : {newcount} \n")
            print("Success")
        if status :
            self.logger.info(data)
            response = self.get_response(request)
            return response
        else :
            # raise Exception
            # response = self.get_response(request)
            response = HttpResponseForbidden("You don't have access")
            return response
