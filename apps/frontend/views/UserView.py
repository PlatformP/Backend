from rest_framework.decorators import action, api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from apps.frontend.serializers import UserSerializer

from apps.frontend.models.Candidate import Candidate

from ast import literal_eval


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
