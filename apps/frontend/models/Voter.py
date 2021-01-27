from django.db import models
from django.contrib.auth.models import User
from apps.frontend.models.ZipCode import ZipCode
from apps.frontend.models.SurveyQuestionAnswers import SurveyQuestionAnswers
from apps.frontend.models.SurveyQuestion import SurveyQuestion

from Scripts.utils.BaseClass import Base
from Scripts.HelperMethods import update_model_instance_from_post

from datetime import date as dt
from pandas import DataFrame


class Voter(Base):
    GENDER_CHOICES = [
        (0, 'Male'),
        (1, 'Female'),
        (2, 'Other')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    zipcode = models.ForeignKey('ZipCode', on_delete=models.SET_NULL, null=True)
    gender = models.SmallIntegerField(default=0, choices=GENDER_CHOICES)

    dob = models.DateField(default=None, null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def save(self, *args, **kwargs):
        '''
        making sure the dob is the right format
        otherwise making it a datetime object
        '''
        if type(self.dob) == int:
            self.dob = dt.fromtimestamp(self.dob / 1000)

        super(Voter, self).save(*args, **kwargs)

    def update_with_kwargs(self, **kwargs):
        if 'user' in kwargs:
            update_model_instance_from_post(kwargs['request_user'], kwargs['user'])
            del kwargs['user']
            del kwargs['request_user']

        if 'zipcode' in kwargs:
            kwargs['zipcode'] = ZipCode.objects.get_or_create(zipcode=kwargs['zipcode'])[0]

        super(Voter, self).update_with_kwargs(**kwargs)

    @staticmethod
    def get_survey_answers(question_ids, user) -> DataFrame:
        df_survey_question_answers = DataFrame.from_records(
            SurveyQuestionAnswers.objects.filter(question__pk__in=question_ids, voter__user=user).values('question_id',
                                                                                                         'answer'), columns=['question_id', 'answer'])
        df_survey_question_answers.set_index('question_id', inplace=True)
        return df_survey_question_answers

    @classmethod
    def submit_survey_answers(cls, user, df_answers: DataFrame):
        """
        creates survey question answers in bulk from a dataframe
        dataframe format + -------------------- +
                         |question_id | answer  |
                         + -------------------- +
                         |            |         |
                         |            |         |
                         + -------------------- +
        :param user:
        :param df_answers:
        :return:
        """
        voter = cls.objects.get(user=user)
        survey_question_answers_bulk = []

        def apply_method(x):
            question_id, answer = x
            survey_question_answers_bulk.append(SurveyQuestionAnswers(voter=voter, answer=answer,
                                                                      question_id=question_id))

        df_answers.apply(lambda x: apply_method(x))
        SurveyQuestionAnswers.objects.bulk_create(survey_question_answers_bulk)
