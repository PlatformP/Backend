from django.db import models

from pandas import DataFrame

class SurveyQuestionAnswers(models.Model):
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE, null=True, blank=True)
    voter = models.ForeignKey('Voter', on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey('SurveyQuestion', on_delete=models.CASCADE, null=True)

    answer = models.PositiveSmallIntegerField()

    @classmethod
    def submit_answers_from_df(cls, user, df_answers: DataFrame, candidate=False):
        from apps.frontend.models.Voter import Voter

        if candidate:
            #TODO: Has yet to be implemented
            pass
        else:
            Voter.submit_survey_answers(user=user, df_answers=df_answers)

    @classmethod
    def get_vector_per_user(cls, id, candidate=True):
        pass