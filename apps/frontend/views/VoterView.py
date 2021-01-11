from rest_framework import viewsets

from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.response import Response

from apps.frontend.models.Voter import Voter
from apps.frontend.models.VoterFavElections import VoterFavElections
from apps.frontend.models.VoterCandidateMatch import VoterCandidateMatch
from apps.frontend.models.Election import Election
from apps.frontend.models.Candidate import Candidate

from Scripts.HelperMethods import get_ballot_by_queryset, get_candidate_df
from pandas import DataFrame


class VoterViewSet(viewsets.ViewSet):
    queryset = Voter.objects.all().order_by('user__username')

    @action(detail=False, methods=['GET'], url_path='get_fav_election')
    def get_elections(self, request):

        voter_fav_election_id = VoterFavElections.objects.filter(
            voter__user=request.user). \
            values_list('election_id', flat=True)
        election_query = Election.objects.filter(pk__in=voter_fav_election_id)
        data = get_ballot_by_queryset(queryset=election_query, user=request.user)
        return Response(data=data, status=HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='get_fav_candidate')
    def get_candidates(self, request):

        #candidate_list = []

        candidate_pk = VoterCandidateMatch.objects.filter(voter__user=request.user, favorite=True).values_list(
            'candidate_id', flat=True)
        df_candidate = get_candidate_df(candidate_ids=candidate_pk, user=request.user)

        def get_election_name_id_from_cand(x):
            election_id = Candidate.objects.get(pk=x).electioninline_set.values_list('election_id', flat=True)[0]
            df_election = DataFrame.from_records(Election.objects.filter(pk=election_id).values('id', 'name'))
            return df_election.to_dict(orient='records')[0]

        df_candidate['election'] = df_candidate['id'].map(get_election_name_id_from_cand)
        '''
        for candidate in queryset:

            d = candidate.get_dict(request.user)
            election = candidate.electioninline_set.all()[0].election
            d['election_id'] = election.id
            d['election_name'] = election.name
            candidate_list.append(d)
        '''
        data = df_candidate.to_json(orient='records')

        return Response(data=data, status=HTTP_200_OK)

    @action(detail=False, methods=['PUT'], url_path='toggle_fav/(?P<primary_key>[0-9]+)')
    def toggle_fav(self, request, primary_key):
        try:
            voter_candidate_match_model = VoterCandidateMatch.objects.get(voter__user=request.user,
                                                                          candidate__pk=primary_key)
            voter_candidate_match_model.toggle_fav()
            return Response({}, status=HTTP_200_OK)
        except VoterCandidateMatch.DoesNotExist:
            return Response({}, status=HTTP_404_NOT_FOUND)
