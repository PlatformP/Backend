from apps.frontend.serializers import LocationSerializer, ElectionSerializer
from apps.frontend.models.Location import Location
from apps.frontend.models.Election import Election

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ast import literal_eval


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by('city')
    serializer_class = LocationSerializer

    @action(detail=False, methods=['GET'])
    def get_elections(self, request):
        request_dict = literal_eval(request.body.decode("UTF-8"))
        elections = Election.objects.filter(location__state=request_dict['state'])

        return Response(data=ElectionSerializer(elections, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)
