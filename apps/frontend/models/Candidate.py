from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from apps.frontend.models.VoterCandidateMatch import VoterCandidateMatch
from apps.frontend.models.PoliticalParty import PoliticalParty

from pandas import DataFrame, read_json, Series
from json import dumps


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    political_party = models.ForeignKey('PoliticalParty', on_delete=models.SET_NULL, null=True)

    profile_picture = models.ImageField(upload_to='candidate_pb', blank=True)
    bio = models.TextField(default=None, null=True)
    popularity = models.FloatField(default=None, null=True, blank=True)
    supporters = models.IntegerField(default=None, null=True, blank=True)
    protesters = models.IntegerField(default=None, null=True, blank=True)

    protestor_supporter_json = models.JSONField()

    class Meta:
        verbose_name = 'Candidates'
        verbose_name_plural = 'Candidates'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def save(self, *args, **kwargs):
        df = DataFrame(columns=['date', 'supporters', 'protesters'])
        self.protestor_supporter_json = dumps(df.to_dict(orient='list'))
        super(Candidate, self).save(*args, **kwargs)

    def decode_json(self):
        return read_json(self.protestor_supporter_df)

    def encode_json(self, df):
        self.protestor_supporter_df = dumps(df.to_dict(orient='list'), indent=4)
        self.save()

    def get_image_path(self):
        try:
            return self.profile_picture.path
        except ValueError:
            return False

    def toggle_supporter(self, operation):
        if operation == '+':
            self.supporters += 1
            df = self.decode_json()
            series = Series({'date': timezone.now().timestamp(),
                             'supporters': self.supporters,
                             'protesters': self.protesters})
            df = df.append(series, ignore_index=True)
            self.encode_json(df)
        elif operation == '-':
            self.supporters -= 1
            df = self.decode_json()
            series = Series({'date': timezone.now().timestamp(),
                             'supporters': self.supporters,
                             'protesters': self.protesters})
            df = df.append(series, ignore_index=True)
            self.encode_json(df)
        self.save()

    def toggle_protester(self, operation):
        self.protesters = self.protesters + 1 if operation == '+' else self.protesters - 1
        self.save()

    @staticmethod
    def get_df(candidate_id, voter_user) -> DataFrame:
        """
        gets a DataFrame for the candidate
        :param candidate_id:
        :param voter_user:
        :return:
        """
        from time import perf_counter
        if Candidate.objects.filter(id=candidate_id).exists():
            df_candidate = DataFrame.from_records(Candidate.objects.filter(pk=candidate_id).values())
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
        else:
            raise ValueError

        return df_candidate

    @staticmethod
    def get_multiple_df(candidate_ids, user) -> DataFrame:
        """
            returns a DataFrame of all the Candidates with the appropriate coloumns filled in
            :param candidate_ids: list of candidate id's
            :param user: user instance with is used to find the the VoterCandidateMatch appropriate to the user
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

        df_candidates = DataFrame.from_records(Candidate.objects.filter(id__in=candidate_ids).values())
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

        return df_candidates
