from apps.frontend.serializers import CandidateSerializer
from apps.frontend.models.Candidate import Candidate

from apps.frontend.models.Policy import Policy
from apps.frontend.serializers import PolicySerializer

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from ast import literal_eval


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all().order_by('user__username')
    serializer_class = CandidateSerializer

    @action(detail=False, methods=['get'])
    def get_policies(self, request):
        '''
        returns all policies registered under that candidate
        :param request:
        '''

        request_dict = literal_eval(request.body.decode('UTF-8'))
        candidate = Candidate.objects.get(**request_dict)

        policies = Policy.objects.filter(candidate=candidate)
        return Response(data=PolicySerializer(policies, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)
