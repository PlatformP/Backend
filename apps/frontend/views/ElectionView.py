from apps.frontend.models.Election import Election
from apps.frontend.models.Voter import Voter

from Backend.settings import US_GEO_CONFIG

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response

from Scripts.HelperMethods import get_ballot_by_queryset, get_key_from_state


class ElectionViewSet(viewsets.ViewSet):
    queryset = Election.objects.all()

    @action(detail=False, methods=['GET'], url_path='(?P<primary_key>[0-9]+)')
    def show_election(self, request, primary_key):
        df_election = Election.get_df(primary_key, request.user)
        return Response(data=df_election.to_json(orient='records'), status=HTTP_200_OK)