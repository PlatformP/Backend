from apps.frontend.serializers import PoliticalPartySerializer
from apps.frontend.models.PoliticalParty import PoliticalParty

from rest_framework import viewsets


class PoliticalPartyViewSet(viewsets.ModelViewSet):
    queryset = PoliticalParty.objects.all()
    serializer_class = PoliticalPartySerializer
