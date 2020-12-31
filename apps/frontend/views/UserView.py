from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from apps.frontend.serializers import UserSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer

    #TODO: DOUBLE CHECK THIS
    @action(['get'], detail=False, url_path='username/(?P<username>\w+)')
    def get_by_username(self, request, username):
        user = get_object_or_404(User, username=username)
        data = UserSerializer(user, context={'request': request}).data
        return Response(data=data, status=HTTP_200_OK)