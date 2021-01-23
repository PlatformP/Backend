from django.db import models
from django.contrib.auth.models import User
from apps.frontend.models.VoterCandidateMatch import VoterCandidateMatch
from apps.frontend.models.PoliticalParty import PoliticalParty

from pandas import DataFrame


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    political_party = models.ForeignKey('PoliticalParty', on_delete=models.SET_NULL, null=True)

    profile_picture = models.ImageField(upload_to='candidate_pb', blank=True)
    bio = models.TextField(default=None, null=True)
    popularity = models.FloatField(default=None, null=True, blank=True)
    supporters = models.IntegerField(default=None, null=True, blank=True)
    protesters = models.IntegerField(default=None, null=True, blank=True)

    # protestor_supporter_df = models.JSONField()

    class Meta:
        verbose_name = 'Candidates'
        verbose_name_plural = 'Candidates'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def get_image_path(self):
        try:
            return self.profile_picture.path
        except ValueError:
            return False

    def toggle_supporter(self, operation):
        self.supporters = self.supporters + 1 if operation == '+' else self.supporters - 1
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
                                                                                                 ).values('candidate_id',
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
