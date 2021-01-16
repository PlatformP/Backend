from apps.frontend.models.Candidate import Candidate

from rest_framework import viewsets
from rest_framework.decorators import action


class CandidateView(viewsets.ViewSet):
    queryset = Candidate.objects.all()

    @action(methods=['GET'], detail=False, url_path='(?P<primary_key>[0-9]+)')
    def show_candidate(self):
        pass