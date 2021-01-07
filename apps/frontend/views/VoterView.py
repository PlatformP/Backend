from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response

from apps.frontend.models.Voter import Voter
from apps.frontend.models.VoterFavElections import VoterFavElections
from apps.frontend.models.Election import Election

from apps.frontend.serializers import VoterSerializer

from json import dumps
from Scripts.HelperMethods import date_time_converter


class VoterViewSet(viewsets.ModelViewSet):
    queryset = Voter.objects.all().order_by('user__username')
    serializer_class = VoterSerializer

    @action(detail=False, methods=['GET'], url_path='get_fav_election')
    def get_elections(self, request):

        voter_fav_election_id = VoterFavElections.objects.filter(
            voter__user=request.user). \
            values_list('election_id', flat=True)
        election_query = Election.objects.filter(pk__in=voter_fav_election_id)
        election_list = list(election_query.values())

        for i, instance in enumerate(election_query):
            candidate_new = instance.electioninline_set.filter(status=0)
            candidate_curr = instance.electioninline_set.filter(status=1)
            candidate_dropped = instance.electioninline_set.filter(status=2)

            candidate_list = []
            for candidate in candidate_new:
                candidate_list.append(candidate.candidate.get_dict(request.user))
            election_list[i].update({'newCandidates': candidate_list})

            candidate_list = []
            for candidate in candidate_curr:
                candidate_list.append(candidate.candidate.get_dict(request.user))
            election_list[i].update({'candidates': candidate_list})

            candidate_list = []
            for candidate in candidate_dropped:
                candidate_list.append(candidate.candidate.get_dict(request.user))
            election_list[i].update({'droppedCandidates': candidate_list})
        data = dumps(election_list, indent=4, default=date_time_converter)

        return Response(data=data, status=HTTP_200_OK)
