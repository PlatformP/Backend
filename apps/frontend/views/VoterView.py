from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.response import Response

from apps.frontend.models.Voter import Voter
from apps.frontend.models.VoterFavElections import VoterFavElections
from apps.frontend.models.VoterCandidateMatch import VoterCandidateMatch
from apps.frontend.models.Election import Election
from apps.frontend.models.Candidate import Candidate

from apps.frontend.serializers import VoterSerializer

from json import dumps
from Scripts.HelperMethods import date_time_converter, get_ballot_by_queryset2


class VoterViewSet(viewsets.ModelViewSet):
    queryset = Voter.objects.all().order_by('user__username')
    serializer_class = VoterSerializer

    @action(detail=False, methods=['GET'], url_path='get_fav_election')
    def get_elections(self, request):

        voter_fav_election_id = VoterFavElections.objects.filter(
            voter__user=request.user). \
            values_list('election_id', flat=True)
        election_query = Election.objects.filter(pk__in=voter_fav_election_id)
        data = get_ballot_by_queryset2(queryset=election_query, user=request.user)
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

    @action(detail=False, methods=['POST', 'GET'], url_path='toggle_fav/(?P<primary_key>[0-9]+)')
    def toggle_fav(self, request, primary_key):
        try:
            voter_candidate_match_model = VoterCandidateMatch.objects.get(voter__user=request.user, candidate__pk=primary_key)
            voter_candidate_match_model.toggle_fav()
            return Response({}, status=HTTP_200_OK)
        except VoterCandidateMatch.DoesNotExist:
            return Response({}, status=HTTP_404_NOT_FOUND)