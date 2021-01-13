from rest_framework import viewsets

from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.response import Response

from apps.frontend.models.Voter import Voter
from apps.frontend.models.VoterFavElections import VoterFavElections
from apps.frontend.models.VoterCandidateMatch import VoterCandidateMatch
from apps.frontend.models.Election import Election
from apps.frontend.models.Candidate import Candidate

from Scripts.HelperMethods import get_ballot_by_queryset, get_candidate_df, does_model_with_kwargs_exist_else_false
from pandas import DataFrame


class VoterViewSet(viewsets.ViewSet):
    queryset = Voter.objects.all().order_by('user__username')

    @action(detail=False, methods=['GET'], url_path='get_fav_election')
    def get_elections(self, request):
        """
        gets the favorite elections from the logged in voter
        :param request:
        :return:
        """
        voter_fav_election_id = VoterFavElections.objects.filter(
            voter__user=request.user). \
            values_list('election_id', flat=True)
        election_query = Election.objects.filter(pk__in=voter_fav_election_id)
        data = get_ballot_by_queryset(queryset=election_query, user=request.user)
        return Response(data=data, status=HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='get_fav_candidate')
    def get_candidates(self, request):
        """
        Getting the list of favorite elections stored in the VoterCandidateMatch model
        :param request:
        :return:
        """
        candidate_pk = VoterCandidateMatch.objects.filter(voter__user=request.user, favorite=True).values_list(
            'candidate_id', flat=True)
        df_candidate = get_candidate_df(candidate_ids=candidate_pk, user=request.user)

        def get_election_name_id_from_cand(x):
            election_id = Candidate.objects.get(pk=x).electioninline_set.values_list('election_id', flat=True)[0]
            df_election = DataFrame.from_records(Election.objects.filter(pk=election_id).values('id', 'name', 'type'))
            return df_election.to_dict(orient='records')[0]

        df_candidate['election'] = df_candidate['id'].map(get_election_name_id_from_cand)
        data = df_candidate.to_json(orient='records')

        return Response(data=data, status=HTTP_200_OK)

    @action(detail=False, methods=['PUT'], url_path='toggle_fav_candidate/(?P<primary_key>[0-9]+)')
    def toggle_fav_candidate(self, request, primary_key):
        """
        toggles the favorite tab in the VoterCandidateMatch model
        :param request:
        :param primary_key:
        :return:
        """
        try:
            voter_candidate_match_model = VoterCandidateMatch.objects.get(voter__user=request.user,
                                                                          candidate__pk=primary_key)
            voter_candidate_match_model.toggle_fav()
            return Response({}, status=HTTP_200_OK)
        except VoterCandidateMatch.DoesNotExist:
            return Response({}, status=HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['PUT'], url_path='toggle_fav_election/(?P<primary_key>[0-9]+)')
    def toggle_fav_election(self, request, primary_key):
        """
        creating or deleting a ElectionInLIne model with the primary key of the election
        :param request:
        :param primary_key:
        :return:
        """
        if voter_fav_election := does_model_with_kwargs_exist_else_false(VoterFavElections,
                                                                         voter__user=request.user,
                                                                         election__id=primary_key):
            voter_fav_election.delete()
            return Response({'deleted': True}, status=HTTP_200_OK)
        else:
            voter = Voter.objects.get(user=request.user)
            election = Election.objects.get(pk=primary_key)
            VoterFavElections.objects.create(voter=voter, election=election)

            return Response({'created': True}, status=HTTP_200_OK)
        return Response({}, status=HTTP_500_INTERNAL_SERVER_ERROR)