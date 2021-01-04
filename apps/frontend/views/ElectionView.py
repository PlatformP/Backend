from apps.frontend.serializers import ElectionSerializer
from apps.frontend.models.Election import Election
from apps.frontend.models.VoterCandidateMatch import VoterCandidateMatch

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response

from Scripts.HelperMethods import date_time_converter
from json import dumps


class ElectionViewSet(viewsets.ModelViewSet):
    queryset = Election.objects.all().order_by('name')
    serializer_class = ElectionSerializer

    @action(['GET'], detail=False, url_path='ballot')
    def get_ballot(self, request, *args, **kwargs):
        instance_query = self.get_queryset()
        instance_values = list(instance_query.values())

        for i, instance in enumerate(instance_query):
            candiate_list = []

            for candidate_q in instance.electioninline_set.all():
                d = candidate_q.candidate.get_dict()
                voter_match = VoterCandidateMatch.objects.filter(voter__user=request.user, candidate__pk=d['id']). \
                    values_list('match_pct', flat=True)[0]
                if voter_match is not None:
                    d['voter_match'] = voter_match

                candiate_list.append(d)

            instance_values[i].update({'Candidates': candiate_list})

        data = dumps(instance_values, indent=4, default=date_time_converter)
        # print(data)
        return Response(data=data, status=HTTP_200_OK)
