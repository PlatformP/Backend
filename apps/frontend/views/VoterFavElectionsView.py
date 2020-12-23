from apps.frontend.serializers import VoterFavElectionsSerializer
from apps.frontend.models.VoterFavElections import VoterFavElections

from rest_framework import viewsets


class VoterFavElectionViewSet(viewsets.ModelViewSet):
    queryset = VoterFavElections.objects.all()
    serializer_class = VoterFavElectionsSerializer
