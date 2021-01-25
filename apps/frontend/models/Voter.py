from django.db import models
from django.contrib.auth.models import User
from apps.frontend.models.ZipCode import ZipCode
from apps.frontend.models.SurveyQuestionAnswers import SurveyQuestionAnswers

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
                                                                                                         'answer'))
        df_survey_question_answers.set_index('question_id', inplace=True)
        return df_survey_question_answers
