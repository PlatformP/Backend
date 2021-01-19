from apps.frontend.models.Election import Election
from apps.frontend.models.Voter import Voter

from Backend.settings import US_GEO_CONFIG

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response

from Scripts.HelperMethods import get_ballot_by_queryset, get_key_from_state


class ElectionViewSet(viewsets.ViewSet):
    queryset = Election.objects.all()
