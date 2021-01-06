from apps.frontend.serializers import ElectionSerializer
from apps.frontend.models.Election import Election
from apps.frontend.models.Voter import Voter

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response

from Scripts.HelperMethods import get_ballot_by_queryset


class ElectionViewSet(viewsets.ModelViewSet):
    queryset = Election.objects.all().order_by('name')
    serializer_class = ElectionSerializer

    @action(['GET'], detail=False, url_path='ballot')
    def get_ballot(self, request):
        voter_location = Voter.objects.get(user=request.user).location
        national_elections = Election.objects.filter(type=2)
        state_elections = Election.objects.filter(location__state=voter_location.state, type=1)
        city_elections = Election.objects.filter(location__city=voter_location.city, type=0)
        instance_query = national_elections | state_elections | city_elections

        data = get_ballot_by_queryset(queryset=instance_query, user=request.user)
        return Response(data=data, status=HTTP_200_OK)
