from rest_framework import viewsets

from apps.frontend.models.Voter import Voter
from apps.frontend.serializers import VoterSerializer


class VoterViewSet(viewsets.ModelViewSet):
    queryset = Voter.objects.all().order_by('user__username')
    serializer_class = VoterSerializer
