from django.db import models

class VoterCandidateMatch(models.Model):

    candidate = models.ForeignKey('frontend.Candidate', on_delete=models.CASCADE)
    voter = models.ForeignKey('frontend.Voter', on_delete=models.CASCADE)
    match_pct = models.FloatField(default=0.0, help_text='Match pct of the voter and candidate')

    class Meta:
        verbose_name_plural = 'Voter Candidate Matches'

    def __str__(self):
        return str(self.candidate)