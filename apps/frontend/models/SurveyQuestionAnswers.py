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
            # TODO: Has yet to be implemented
            pass
        else:
            Voter.submit_survey_answers(user=user, df_answers=df_answers)

    @classmethod
    def get_survey_answers(cls, question_ids, user, candidate=False, candidate_id=None, voter_match=False) -> DataFrame:
        kwargs = {
            'question__pk__in': question_ids
        }
        if candidate:
            if candidate_id is not None:
                kwargs['candidate__id'] = candidate_id
            else:
                kwargs['candidate__user'] = user
        else:
            kwargs['voter__user'] = user

        df_survey_question_answers = DataFrame.from_records(
            cls.objects.filter(**kwargs).values('question_id', 'answer'), columns=['question_id', 'answer'])

        if voter_match:
            df_survey_question_answers.sort_values('question_id', inplace=True)
            return df_survey_question_answers['answer'].to_numpy()

        df_survey_question_answers.set_index('question_id', inplace=True)
        return df_survey_question_answers
