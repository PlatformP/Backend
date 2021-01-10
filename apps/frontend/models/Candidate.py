from django.db import models
from django.contrib.auth.models import User

from apps.frontend.models.VoterCandidateMatch import VoterCandidateMatch


class Candidate(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    political_party = models.ForeignKey('PoliticalParty', on_delete=models.SET_NULL, null=True)
    bio = models.TextField(default=None, null=True)
    popularity = models.FloatField(default=None, null=True, blank=True)
    supporters = models.IntegerField(default=None, null=True, blank=True)

    class Meta:
        verbose_name = 'Candidates'
        verbose_name_plural = 'Candidates'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def get_dict(self, user):

        try:
            voter_match, favorite = VoterCandidateMatch.objects.filter(voter__user=user, candidate__pk=self.id). \
                values_list('match_pct', 'favorite')[0]
        except VoterCandidateMatch.DoesNotExist:
            voter_match, favorite = [None, None]

        return {
            'id': self.id,
            'user': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'political_party': self.political_party.get_color_name(),
            'bio': self.bio,
            'voter_match': voter_match,
            'favorite': favorite,
            'popularity': self.popularity,
            'supporters': self.supporters
        }