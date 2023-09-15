# from django.shortcuts import render
# from django.http import JsonResponse

# class customize_middleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # print("Before")
#         # response = self.get_response(request)
#         # print("After")
#         # return response


from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest
User = get_user_model()
class customize_middleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.user.is_authenticated:
            if not User.objects.filter(first_name=request.user.first_name, last_name=request.user.last_name).exists():
                return HttpResponseBadRequest("First name or last name do not exist in the database.")
        response = self.get_response(request)
        return response