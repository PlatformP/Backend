from apps.frontend.models.Election import Election
from apps.frontend.models.Voter import Voter

from Backend.settings import US_GEO_CONFIG

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response

from Scripts.HelperMethods import get_ballot_by_queryset, get_key_from_state


class ElectionViewSet(viewsets.ViewSet):
    queryset = Election.objects.all().order_by('-date')


    @action(['GET'], detail=False, url_path='ballot')
    def get_ballot(self, request):
        voter_zip_code = Voter.objects.get(user=request.user).zipcode.zipcode

        location_df = US_GEO_CONFIG.query_postal_code(voter_zip_code)

        national_elections = Election.objects.filter(type=3).oder_by('-date')
        state_elections = Election.objects.filter(location__state=get_key_from_state(location_df.state_code), type=2).order_by('-date')
        county_elections = Election.objects.filter(location__county=location_df.county_name, type=1).order_by('-date')
        city_elections = Election.objects.filter(location__city=location_df.place_name, type=0).order_by('-date')
        instance_query = national_elections | state_elections | county_elections | city_elections

        data = get_ballot_by_queryset(queryset=instance_query, user=request.user)
        return Response(data=data, status=HTTP_200_OK)
