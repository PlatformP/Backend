from apps.frontend.serializers import ElectionInLineSerializer
from apps.frontend.models.Election_InLine import Election_InLine

from rest_framework import viewsets


class ElectionInLineViewSet(viewsets.ModelViewSet):
    queryset = Election_InLine.objects.all()
    serializer_class = ElectionInLineSerializer
