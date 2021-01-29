from django.db import models

from apps.frontend.models.SurveyQuestion import SurveyQuestion
from apps.frontend.models.Voter import Voter

from pandas import DataFrame


class Survey(models.Model):
    SURVEY_TYPE = [
        (0, 'general'),
        (1, 'city'),
        (2, 'county'),
        (3, 'state'),
        (4, 'national')
    ]

    name = models.CharField(default='__default__', max_length=50)
    survey_type = models.PositiveSmallIntegerField(default=0, choices=SURVEY_TYPE)

    def __str__(self):
        return self.name

    def get_question_ids(self):
        return SurveyQuestion.objects.filter(survey=self).values_list('id', flat=True)

    @staticmethod
    def get_questions_with_answers(survey_id, user, candidate=False) -> DataFrame:
        df_survey_questions = DataFrame.from_records(SurveyQuestion.objects.filter(survey__pk__in=survey_id).values())
        questions_ids_set = set(df_survey_questions['id'])
        if candidate:
            # TODO Has to be implemented still
            pass
        else:
            df_answers = Voter.get_survey_answers(question_ids=questions_ids_set, user=user)

        df_survey_questions['answer'] = df_survey_questions['id'].map(df_answers.to_dict(orient='index'))

        df_survey_questions.set_index('survey_id', inplace=True)

        return df_survey_questions

    @classmethod
    def get_list(cls, user, candidate=False) -> DataFrame:

        df_surveys = DataFrame.from_records(Survey.objects.values())

        df_survey_answers = cls.get_questions_with_answers(set(df_surveys['id']), user=user, candidate=candidate)

        def get_question_for_survey(x):
            return df_survey_answers.loc[x].to_dict(orient='records')

        df_surveys['questions'] = df_surveys['id'].map(get_question_for_survey)

        return df_surveys
