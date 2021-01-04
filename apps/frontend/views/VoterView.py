from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response

from apps.frontend.models.Voter import Voter
from apps.frontend.models.VoterFavElections import VoterFavElections
from apps.frontend.models.Election import Election

from apps.frontend.serializers import VoterSerializer
from apps.frontend.serializers import ElectionSerializer


class VoterViewSet(viewsets.ModelViewSet):
    queryset = Voter.objects.all().order_by('user__username')
    serializer_class = VoterSerializer

    @action(detail=False, methods=['GET'], url_path='get_fav_election')
    def get_elections(self, request):
        voter_fav_election_id = VoterFavElections.objects.filter(
            voter__user=request.user). \
            values_list('election_id', flat=True)
        election_query = Election.objects.filter(pk__in=voter_fav_election_id)
        data = ElectionSerializer(election_query, many=True, context={'request': request}).data
        return Response(data=data, status=HTTP_200_OK)
