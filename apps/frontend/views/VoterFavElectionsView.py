from apps.frontend.serializers import VoterFavElectionsSerializer
from apps.frontend.models.Voter_FavElections import Voter_FavElections

from rest_framework import viewsets


class VoterFavElectionViewSet(viewsets.ModelViewSet):
    queryset = Voter_FavElections.objects.all()
    serializer_class = VoterFavElectionsSerializer
