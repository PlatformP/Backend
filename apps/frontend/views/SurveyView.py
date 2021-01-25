from apps.frontend.models.Survey import Survey
from apps.frontend.models.Candidate import Candidate

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response


class SurveyViewSet(viewsets.ViewSet):
    queryset = Survey.objects.all()

    @action(detail=False, methods=['GET'], url_path='list')
    def get_surveys(self, request):
        if Candidate.objects.filter(user=request.user).exists():
            candidate = True
        else:
            candidate = False

        df = Survey.get_list(request.user, candidate)
        return Response(data=df.to_json(orient='records'), status=HTTP_200_OK)
