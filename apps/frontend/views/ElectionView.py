from apps.frontend.serializers import ElectionSerializer, ElectionInLineSerializer
from apps.frontend.models.Election import Election
from apps.frontend.models.Election_InLine import Election_InLine

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ast import literal_eval


class ElectionViewSet(viewsets.ModelViewSet):
    queryset = Election.objects.all().order_by('name')
    serializer_class = ElectionSerializer

    @action(detail=False, methods=['GET'])
    def get_candidates(self, request):
        request_dict = literal_eval(request.body.decode('UTF-8'))
        election_inlines = Election_InLine.objects.filter(election__name=request_dict['name'])

        return Response(data=ElectionInLineSerializer(election_inlines, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)