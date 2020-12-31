from django.contrib.auth.models import User

from rest_framework.viewsets import ModelViewSet

from apps.frontend.serializers import UserSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer