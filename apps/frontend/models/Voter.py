from django.db import models
from django.contrib.auth.models import User
from apps.frontend.models.ZipCode import ZipCode
from apps.frontend.models.SurveyQuestionAnswers import SurveyQuestionAnswers
from apps.frontend.models.VoterCandidateMatch import VoterCandidateMatch
# from apps.frontend.models.Survey import Survey

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

    @classmethod
    def submit_survey_answers(cls, user, df_answers: DataFrame):
        """
        creates survey question answers in bulk from a dataframe
        dataframe format + -------------------- +
                         |question_id | answer  |
                         + -------------------- +
                         |            |         |
                         + -------------------- +
        :param user:
        :param df_answers:
        :return:
        """
        voter = cls.objects.get(user=user)

        def apply_method(x):
            question_id, answer = x
            SurveyQuestionAnswers.objects.update_or_create(voter=voter, question_id=question_id,
                                                           defaults={'answer': answer})

        df_answers.apply(lambda x: apply_method(x), axis=1)

    @classmethod
    def calculate_voter_matches(cls, question_ids, user):

        voter = cls.objects.get(user=user)
        candidate_ids = set(voter.votercandidatematch_set.values_list('candidate_id', flat=True))

        voter_vector = SurveyQuestionAnswers.get_survey_answers(question_ids, user, voter_match=True)

        voter_candidate_match_for_bulk_update = []
        for candidate_id in candidate_ids:
            candidate_vector = SurveyQuestionAnswers.get_survey_answers(question_ids, user=None,
                                                                        candidate_id=candidate_id, candidate=True,
                                                                        voter_match=True)
            voter_candidate_match_for_bulk_update.append(VoterCandidateMatch.
                                                         calculate_voter_match_score(candidate_id=candidate_id,
                                                                                     candidate_vector=candidate_vector,
                                                                                     voter_id=voter.pk,
                                                                                     voter_vector=voter_vector))

        VoterCandidateMatch.objects.bulk_update(voter_candidate_match_for_bulk_update, ['match_pct'])