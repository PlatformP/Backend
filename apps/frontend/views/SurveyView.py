from apps.frontend.models.Survey import Survey
from apps.frontend.models.Candidate import Candidate
from apps.frontend.models.SurveyQuestionAnswers import SurveyQuestionAnswers
from apps.frontend.models.Voter import Voter

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.response import Response

from pandas import DataFrame


class SurveyViewSet(viewsets.ViewSet):
    queryset = Survey.objects.all()

    @action(detail=False, methods=['GET'], url_path='list')
    def get_surveys(self, request):
        candidate = Candidate.objects.filter(user=request.user).exists()
        df = Survey.get_list(request.user, candidate)
        return Response(data=df.to_json(orient='records'), status=HTTP_200_OK)

    @action(detail=False, methods=['POST'], url_path='submit_answers')
    def submit_answers(self, request):
        """
        submit one question in the format
        {
            survey_id: 1,
            question_id: [1],
            answer: [1]
        }
        if all the questions in the survey have been answered then the voter match gets calculated
        :param request:
        :return:
        """
        data = dict(request.data)
        survey_id = data['survey_id']
        del data['survey_id']
        candidate = Candidate.objects.filter(user=request.user).exists()
        df_answers = DataFrame(data)
        SurveyQuestionAnswers.submit_answers_from_df(user=request.user, df_answers=df_answers, candidate=candidate)

        all_questions, question_ids, survey_type = Survey.are_all_questions_answered(survey_id=survey_id, user=request.user)
        if all_questions:
            Voter.calculate_voter_matches(question_ids=question_ids, user=request.user, survey_type=survey_type)
        return Response({}, status=HTTP_204_NO_CONTENT)
