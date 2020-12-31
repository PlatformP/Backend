from rest_framework import viewsets
from rest_framework.decorators import action

from apps.frontend.models.Voter import Voter
from apps.frontend.serializers import VoterSerializer


class VoterViewSet(viewsets.ModelViewSet):
    queryset = Voter.objects.all().order_by('user__username')
    serializer_class = VoterSerializer

    @action(detail=False, methods=['GET'])
    def get_elections(self, request):
        pass