from django.contrib.auth.models import User,Group
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from quickstart.serializers import UserSerializer,GroupSerializer
from rest_framework import serializers,generics,filters
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
import django_filters
from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(viewsets.ModelViewSet):
# class UserViewSet(viewsets.APIView):
    # pass
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    # filterset_class = UserFilter
    # filter_backends = [DjangoFilterBackend]

# class UserViewSet(generics.ListAPIView):
# # class UserViewSet(viewsets.APIView):
#     # pass
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     # filterset_class = UserFilter
#     filter_backends = [django_filters.rest_framework.DjangoFilterBackend]


    # def get_queryset(self):

    #     user = self.request.user
    #     return User.objects.filter(id=1)


    # queryset = User.objects.all()
    # renderer_classes = [TemplateHTMLRenderer]

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     return Response({'user': self.object}, template_name='user_detail.html')

    # renderer_classes = [JSONRenderer]

    # def get(self, request, format=None):
    #     user_count = User.objects.filter(active=True).count()
    #     content = {'user_count': user_count}
    #     return Response(content)

    # @api_view(['GET'])
    # @renderer_classes([JSONRenderer])
    # def user_count_view(request, format=None):
    #     user_count = User.objects.filter(active=True).count()
    #     content = {'user_count': user_count}
    #     return Response(content)

    # def has_permissions(self):
    #     if self.action == 'list':
    #         permission_classes = [IsAuthenticated]
    #     else:
    #         permission_classes = [IsAdminUser]
    #     return [permission() for permission in permission_classes]
    
    # def get(self, request, pk=None):
    #     queryset = User.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)
    # class CustomBrowsableAPIRenderer(BrowsableAPIRenderer):
    #     def get_default_renderer(self, view):
    #         return JSONRenderer()

    # @action(detail=True, methods=['post'])
    @action(detail=False,methods=['post'])
    def set_password(self, request):
        user = self.get_object()    
        serializer = request.data
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def recent_users(self, request):
        recent_users = User.objects.all().order_by('-id')
        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)
    

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]