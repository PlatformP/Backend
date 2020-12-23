from apps.frontend.serializers import ElectionInLineSerializer
from apps.frontend.models.ElectionInLine import ElectionInLine

from rest_framework import viewsets


class ElectionInLineViewSet(viewsets.ModelViewSet):
    queryset = ElectionInLine.objects.all()
    serializer_class = ElectionInLineSerializer
