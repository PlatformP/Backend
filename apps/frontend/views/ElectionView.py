from apps.frontend.serializers import ElectionSerializer
from apps.frontend.models.Election import Election
from apps.frontend.models.VoterCandidateMatch import VoterCandidateMatch

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response

from Scripts.HelperMethods import get_ballot_by_queryset


class ElectionViewSet(viewsets.ModelViewSet):
    queryset = Election.objects.all().order_by('name')
    serializer_class = ElectionSerializer

    @action(['GET'], detail=False, url_path='ballot')
    def get_ballot(self, request, *args, **kwargs):
        instance_query = self.get_queryset()
        data = get_ballot_by_queryset(queryset=instance_query, user=request.user)
        return Response(data=data, status=HTTP_200_OK)
