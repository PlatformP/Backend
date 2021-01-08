from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response

from apps.frontend.models.Voter import Voter
from apps.frontend.models.VoterFavElections import VoterFavElections
from apps.frontend.models.VoterCandidateMatch import VoterCandidateMatch
from apps.frontend.models.Election import Election
from apps.frontend.models.Candidate import Candidate

from apps.frontend.serializers import VoterSerializer

from json import dumps
from Scripts.HelperMethods import date_time_converter, get_ballot_by_queryset


class VoterViewSet(viewsets.ModelViewSet):
    queryset = Voter.objects.all().order_by('user__username')
    serializer_class = VoterSerializer

    @action(detail=False, methods=['GET'], url_path='get_fav_election')
    def get_elections(self, request):

        voter_fav_election_id = VoterFavElections.objects.filter(
            voter__user=request.user). \
            values_list('election_id', flat=True)
        election_query = Election.objects.filter(pk__in=voter_fav_election_id)
        data = get_ballot_by_queryset(queryset=election_query, user=request.user, voter_fav=True)
        return Response(data=data, status=HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='get_fav_candidate')
    def get_candidates(self, request):

        candidate_list = []

        candidate_pk = VoterCandidateMatch.objects.filter(voter__user=request.user, favorite=True).values_list('candidate_id', flat=True)
        queryset = Candidate.objects.filter(pk__in=candidate_pk)
        for candidate in queryset:

            d = candidate.get_dict(request.user)
            election = candidate.electioninline_set.all()[0].election
            d['election_id'] = election.id
            d['election_name'] = election.name
            candidate_list.append(d)

        data = dumps(candidate_list, indent=4, default=date_time_converter)

        return Response(data=data, status=HTTP_200_OK)
