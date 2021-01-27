from apps.frontend.models.Survey import Survey
from apps.frontend.models.Candidate import Candidate
from apps.frontend.models.SurveyQuestionAnswers import SurveyQuestionAnswers

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response

from pandas import read_json

class SurveyViewSet(viewsets.ViewSet):
    queryset = Survey.objects.all()

    @action(detail=False, methods=['GET'], url_path='list')
    def get_surveys(self, request):
        candidate = Candidate.objects.filter(user=request.user).exists()
        df = Survey.get_list(request.user, candidate)
        return Response(data=df.to_json(orient='records'), status=HTTP_200_OK)

    @action(detail=False, methods=['POST'], url_path='submit_answers')
    def submit_answers(self, request):
        candidate = Candidate.objects.filter(user=request.user).exists()

        df_answers = read_json(request.data)

        SurveyQuestionAnswers.submit_answers_from_df(user=request.user, df_answers=df_answers, candidate=candidate)
