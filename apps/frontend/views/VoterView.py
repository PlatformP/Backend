from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_204_NO_CONTENT
from rest_framework.response import Response

from apps.frontend.models.Voter import Voter
from apps.frontend.models.VoterFavElections import VoterFavElections
from apps.frontend.models.VoterCandidateMatch import VoterCandidateMatch
from apps.frontend.models.Election import Election
from apps.frontend.models.Candidate import Candidate
from apps.frontend.models.ZipCode import ZipCode

from Scripts.HelperMethods import get_model_with_kwargs_else_false, get_model_df_with_kwargs_else_false
from pandas import DataFrame

from apps.frontend.APIdocu.VoterViewDocs import response_elections, response_get_profile


class VoterViewSet(viewsets.ViewSet):
    queryset = Voter.objects.all()

    @swagger_auto_schema(responses=response_elections)
    @action(['GET'], detail=False, url_path='ballot')
    def get_ballot(self, request):
        """
        returns the results for the ballot page. -> all the elections that are appropriate for the users zip code
        :param request:
        :return:
        """

        voter_zip_code = Voter.objects.get(user=request.user).zipcode

        national_elections = Election.objects.filter(type=3)
        state_elections = Election.objects.filter(location__state=voter_zip_code.state_key,
                                                  type=2)
        county_elections = Election.objects.filter(location__county=voter_zip_code.county_name, type=1)
        city_elections = Election.objects.filter(location__city=voter_zip_code.place_name, type=0)
        instance_query = national_elections | state_elections | county_elections | city_elections

        data = Election.get_ballot_df_by_queryset(queryset=instance_query, user=request.user).to_json(orient='records')
        return Response(data=data, status=HTTP_200_OK)

    @swagger_auto_schema(responses=response_elections)
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
        data = Election.get_ballot_df_by_queryset(queryset=election_query, user=request.user).to_json(orient='records')
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
        df_candidate = Candidate.get_multiple_df(candidate_ids=candidate_pk, user=request.user, election=True)

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
            return Response({}, status=HTTP_204_NO_CONTENT)
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
        if voter_fav_election := get_model_with_kwargs_else_false(VoterFavElections,
                                                                  voter__user=request.user,
                                                                  election__id=primary_key):
            voter_fav_election.delete()
            return Response({}, status=HTTP_200_OK)
        else:
            voter = Voter.objects.get(user=request.user)
            election = Election.objects.get(pk=primary_key)
            VoterFavElections.objects.create(voter=voter, election=election)

            return Response({}, status=HTTP_200_OK)
        return Response({}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['POST', 'PUT'], url_path='edit_profile')
    def edit_profile(self, request):
        '''
        Method for creating and editing profiles
        if editing then PUT must be used as a method
        :param request:
        :return:
        '''
        if voter := get_model_with_kwargs_else_false(Voter, user=request.user):
            data = dict(request.data)
            data['request_user'] = request.user
            voter.update_with_kwargs(**data)
            return Response({}, status=HTTP_204_NO_CONTENT)
        else:
            # TODO: HAS TO BE TESTED
            data = {}
            for key, value in request.data.items():
                data[key] = value
            print(data)
            data['user'] = request.user
            data['zipcode'] = ZipCode.objects.get_or_create(zipcode=request.data['zipcode'])[0]
            Voter.objects.create(**data)
            return Response({}, status=HTTP_204_NO_CONTENT)
        return Response({}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(responses=response_get_profile)
    @action(detail=False, methods=['GET'], url_path='get_profile')
    def get_profile(self, request):
        voter_df = get_model_df_with_kwargs_else_false(Voter, 'id', 'zipcode__zipcode', 'user__first_name',
                                                       'user__last_name', 'gender', 'dob', user=request.user)
        if type(voter_df) == DataFrame:
            voter_df.rename(columns={'zipcode__zipcode': 'zipcode', 'user__first_name': 'first_name',
                                     'user__last_name': 'last_name'}, inplace=True)
            return Response(voter_df.to_json(orient='records'), status=HTTP_200_OK)
        else:
            return Response({}, status=HTTP_404_NOT_FOUND)
        return Response({}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['PUT'], url_path='toggle_support_candidate/(?P<primary_key>[0-9]+)')
    def toggle_candidate_support(self, request, primary_key):
        """
        toggles the support
        :param request:
        :param primary_key: pk of the candidate
        :return: 204 if successfully
        """
        voter_candidate_match = VoterCandidateMatch.objects.get(voter__user=request.user, candidate__id=primary_key)
        voter_candidate_match.toggle_support()
        return Response({}, status=HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['PUT'], url_path='toggle_protest_candidate/(?P<primary_key>[0-9]+)')
    def toggle_candidate_protest(self, request, primary_key):
        """
        toggles the protest
        :param request:
        :param primary_key: pk of the candidate
        :return: 204 if successfully
        """
        voter_candidate_match = VoterCandidateMatch.objects.get(voter__user=request.user, candidate__id=primary_key)
        voter_candidate_match.toggle_protest()
        return Response({}, status=HTTP_204_NO_CONTENT)
