

from .serializers import CreateUserSerializer, UpdateUserSelializer, ShortUserSerializer, GroupSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework import viewsets


from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

class CreateUserView(viewsets.ModelViewSet):
    """
    API endpoint for creating a User
    """
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny, )


from .models import User
from .permissions import IsSelf

class UserUpdate(viewsets.ModelViewSet):
    """
    API endpoint for retrieve, update, destroy a User
    """
    queryset = User.objects.all()
    serializer_class = UpdateUserSelializer
    #permission_classes = (IsAuthenticated, IsSelf,, TokenHasReadWriteScope)
    permission_classes = (AllowAny, )

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404


class UserDetail(APIView):
    """
    Retrieve a User
    """
    permission_classes = (AllowAny, )

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = ShortUserSerializer(user)
        return Response(serializer.data)


from django.contrib.auth.models import Group
from oauth2_provider.ext.rest_framework import OAuth2Authentication

class GroupViewSet(viewsets.ModelViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope]
    permission_classes = [IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserCurrent(APIView):
    """
    Retrieve
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        serializer = ShortUserSerializer(user)
        return Response(serializer.data)
