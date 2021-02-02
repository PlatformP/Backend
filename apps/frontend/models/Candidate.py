from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from apps.frontend.models.VoterCandidateMatch import VoterCandidateMatch
from apps.frontend.models.PoliticalParty import PoliticalParty
from apps.frontend.models.SurveyQuestionAnswers import SurveyQuestionAnswers

from pandas import DataFrame, read_json, Series
from json import dumps


class Candidate(models.Model):

    FIELDS_FOR_BALLOT = ['id', 'user_id', 'political_party_id', 'profile_picture', 'popularity', 'supporters',
                         'protesters']

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    political_party = models.ForeignKey('PoliticalParty', on_delete=models.SET_NULL, null=True)

    profile_picture = models.ImageField(upload_to='candidate_pb', blank=True)
    bio = models.TextField(default=None, null=True)
    popularity = models.FloatField(default=None, null=True, blank=True)
    supporters = models.IntegerField(default=None, null=True, blank=True)
    protesters = models.IntegerField(default=None, null=True, blank=True)

    protestor_supporter_json = models.JSONField()
    social_media_json = models.JSONField(default=dict)

    class Meta:
        verbose_name = 'Candidates'
        verbose_name_plural = 'Candidates'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def save(self, *args, **kwargs):
        if not self.pk:
            df = DataFrame(columns=['date', 'supporters', 'protesters'])
            self.protestor_supporter_json = dumps(df.to_dict(orient='list'))
        super(Candidate, self).save(*args, **kwargs)

    def decode_json(self) -> DataFrame:
        return read_json(self.protestor_supporter_json)

    def encode_json(self, df, save=False):
        """
        call witht the save method if method is not followed up with a self.save()
        :param df:
        :param save:
        :return:
        """
        df['date'] = df['date'].astype(str)
        self.protestor_supporter_json = dumps(df.to_dict(orient='list'), indent=4)
        if save:
            self.save()

    def update_support_protest(self, support, protest):
        '''
        updates the json with the new supporters and protesters
        :param support:
        :param protest:
        :return:
        '''
        df = self.decode_json()
        series = Series({'date': int(timezone.now().timestamp()),
                         'supporters': support,
                         'protesters': protest})
        df = df.append(series, ignore_index=True)
        self.encode_json(df)

    def toggle_supporter(self, operation):
        self.supporters = self.supporters + 1 if operation == '+' else self.supporters - 1
        self.update_support_protest(self.supporters, self.protesters)
        self.update_popularity()
        self.save()

    def toggle_protester(self, operation):
        self.protesters = self.protesters + 1 if operation == '+' else self.supporters - 1
        self.update_support_protest(self.supporters, self.protesters)
        self.update_popularity()
        self.save()

    def update_popularity(self, save=False):
        self.popularity = round(self.supporters / (self.supporters + self.protesters) * 100)
        if save:
            self.save()

    @classmethod
    def get_election_name_id_from_cand(cls, pk):
        """
        returns a dictionary of the election type and name for the candidate
        to be used when mapping through the candidate df
        :param pk: primary key of candidate
        :return:
        """
        from .Election import Election

        election_id = cls.objects.get(pk=pk).electioninline_set.values_list('election_id', flat=True)[0]
        df_election = DataFrame.from_records(Election.objects.filter(pk=election_id).values('id', 'name', 'type'))
        return df_election.to_dict(orient='records')[0]

    @classmethod
    def get_df(cls, candidate_id, voter_user, *args, **kwargs) -> DataFrame:
        """
        gets a DataFrame for the candidate
        :param candidate_id:
        :param voter_user:
        :param args: which fields to include with the candidate
        :return:
        """
        from time import perf_counter
        if cls.objects.filter(id=candidate_id).exists():
            df_candidate = DataFrame.from_records(cls.objects.filter(pk=candidate_id).values(*args))
            df_political_party = PoliticalParty.objects.get(pk=df_candidate['political_party_id']).get_df()

            df_voter_candidate_match = DataFrame.from_records(VoterCandidateMatch.objects.filter(voter__user=voter_user,
                                                                                                 candidate__pk=candidate_id
                                                                                                 ).values(
                'candidate_id',
                'match_pct',
                'favorite',
                'support',
                'protest'))

            df_user = DataFrame.from_records(User.objects.filter(id=df_candidate['user_id'])
                                             .values('id', 'first_name', 'last_name'))
            df_user.set_index('id', inplace=True)

            df_candidate['user_id'] = df_candidate['user_id'].map(df_user.to_dict(orient='index'))

            df_candidate['political_party_id'] = df_candidate['political_party_id'].map(df_political_party
                                                                                        .to_dict(orient='index'))
            df_candidate.rename(columns={'political_party_id': 'political_party', 'user_id': 'user'}, inplace=True)
            df_voter_candidate_match.set_index('candidate_id', inplace=True)

            df_candidate['voter_match'] = df_candidate['id'].map(df_voter_candidate_match.to_dict(orient='index'))

            df_candidate.rename(columns={'political_party_id': 'political_party', 'user_id': 'user'}, inplace=True)

            if 'election' in kwargs and kwargs['election']:
                df_candidate['election'] = df_candidate['id'].map(cls.get_election_name_id_from_cand)
        else:
            raise ValueError

        return df_candidate

    @classmethod
    def get_multiple_df(cls, candidate_ids, user, *args, **kwargs) -> DataFrame:
        """
            returns a DataFrame of all the Candidates with the appropriate coloumns filled in
            :param candidate_ids: list of candidate id's
            :param user: user instance with is used to find the the VoterCandidateMatch appropriate to the user
            :param args: fields to exclude form the candidate
            :return: DataFrame
            """

        # getting the political party DF
        # DataFrame has a name and color coloumn
        df_political_party_orig = DataFrame.from_records(PoliticalParty.objects.values())
        df_political_party = DataFrame(columns=['id', 'party', 'party_color'])
        df_political_party['id'] = df_political_party_orig['id']
        df_political_party['party'] = df_political_party_orig['name'].map(dict(PoliticalParty.NAME_CHOICES))
        df_political_party['party_color'] = df_political_party_orig['name'].map(PoliticalParty.COLOR_DICT)
        df_political_party.set_index('id', inplace=True)

        df_candidates = DataFrame.from_records(cls.objects.filter(id__in=candidate_ids).values(*cls.FIELDS_FOR_BALLOT))
        df_candidates['political_party_id'] = df_candidates['political_party_id'].map(df_political_party
                                                                                      .to_dict(orient='index'))

        # getting User DF
        # DataFrame with first_name and last_name as coloumns
        df_user = DataFrame.from_records(User.objects.filter(id__in=df_candidates['user_id'])
                                         .values('id', 'first_name', 'last_name'))
        df_user.set_index('id', inplace=True)

        # placing user info into candidate df
        df_candidates['user_id'] = df_candidates['user_id'].map(df_user.to_dict(orient='index'))
        df_candidates.rename(columns={'political_party_id': 'political_party', 'user_id': 'user'}, inplace=True)

        df_voter_candidate_match = DataFrame.from_records(VoterCandidateMatch.objects.filter(voter__user=user,
                                                                                             candidate__pk__in=candidate_ids
                                                                                             ).values('candidate_id',
                                                                                                      'match_pct',
                                                                                                      'favorite',
                                                                                                      'support',
                                                                                                      'protest'))
        df_voter_candidate_match.set_index('candidate_id', inplace=True)
        df_candidates['voter_match'] = df_candidates['id'].map(df_voter_candidate_match.to_dict(orient='index'))

        if 'election' in kwargs and kwargs['election']:
            df_candidates['election'] = df_candidates['id'].map(cls.get_election_name_id_from_cand)

        return df_candidates

    @classmethod
    def submit_survey_answers(cls, user, df_answers):
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

    def get_image_path(self):
        try:
            return self.profile_picture.path
        except ValueError:
            return False
