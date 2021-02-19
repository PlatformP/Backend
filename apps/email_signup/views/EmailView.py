from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from apps.email_signup.models.email import email
from apps.email_signup.serializer.EmailSerializer import EmailSerializer


class EmailViewSet(viewsets.ModelViewSet):
    queryset = email.objects.all()
    serializer_class = EmailSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
