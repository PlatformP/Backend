from apps.frontend.serializers import PolicySerializer
from apps.frontend.models.Policy import Policy

from rest_framework import viewsets

class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all().order_by('candidate')
    serializer_class = PolicySerializer