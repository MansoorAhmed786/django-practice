from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import AbstractUser
from rest_framework.renderers import JSONRenderer,TemplateHTMLRenderer,StaticHTMLRenderer
from django.shortcuts import get_object_or_404
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination,CursorPagination


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']
    # def validate_username(self, value):
    #     # Custom email validation logic
    #     if "mansoor" in value:
    #         raise serializers.ValidationError("Mansoor is not allowed.")
    #     return value

class UserList(generics.ListCreateAPIView):
    # queryset = User.objects.filter(id=1)
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser]

class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })

    # throttle_classes = [UserRateThrottle]

    # def get(self, request, format=None):
    #     content = {
    #         'status': 'request was permitted'
    #     }
    #     return Response(content)

    # @api_view(['GET'])
    # @throttle_classes([UserRateThrottle])
    # def example_view(request, format=None):
    #     content = {
    #     'status': 'request was permitted'
    # }
    #     return Response(content)
    # @api_view(['GET'])
    # @renderer_classes([StaticHTMLRenderer])
    # def get(request):
    #     data = '<html><body><h1>Hello, world</h1></body></html>'
    #     return Response(data)

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

# class UserList(generics.RetrieveAPIView):
# # class UserViewSet(viewsets.APIView):
#     # pass
#     # queryset = User.objects.all()
#     # serializer_class = UserSerializer
#     queryset = User.objects.all()
#     renderer_classes = [TemplateHTMLRenderer]

#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return Response({'user': self.object})
# from rest_framework import serializers

# class CommentSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     content = serializers.CharField(max_length=200)
#     created = serializers.DateTimeField()