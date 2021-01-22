from apps.frontend.models.Candidate import Candidate

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND


class CandidateView(viewsets.ViewSet):
    queryset = Candidate.objects.all()

    @action(methods=['GET'], detail=False, url_path='(?P<primary_key>[0-9]+)')
    def show_candidate(self, request, primary_key):
        try:
            candidate_df = Candidate.get_df(candidate_id=primary_key, voter_user=request.user)
        except ValueError:
            return Response({}, status=HTTP_404_NOT_FOUND)
        return Response(data=candidate_df.to_json(orient='records'), status=HTTP_200_OK)
