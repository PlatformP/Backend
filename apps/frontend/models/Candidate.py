from django.db import models
from django.contrib.auth.models import User

from apps.frontend.models.VoterCandidateMatch import VoterCandidateMatch


class Candidate(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    political_party = models.ForeignKey('PoliticalParty', on_delete=models.SET_NULL, null=True)
    bio = models.TextField(default=None, null=True)

    class Meta:
        verbose_name = 'Candidates'
        verbose_name_plural = 'Candidates'

    def __str__(self):
        return f'{self.user.username}'

    def get_dict(self, user):

        try:
            voter_match = VoterCandidateMatch.objects.filter(voter__user=user, candidate__pk=self.id). \
                values_list('match_pct', flat=True)[0]
        except VoterCandidateMatch.DoesNotExist:
            pass

        return {
            'id': self.id,
            'user': self.user.username,
            'political_party': self.political_party.name,
            'bio': self.bio,
            'voter_match': voter_match
        }