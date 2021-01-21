from django.db import models


class VoterCandidateMatch(models.Model):

    voter = models.ForeignKey('frontend.Voter', on_delete=models.CASCADE)
    candidate = models.ForeignKey('frontend.Candidate', on_delete=models.CASCADE)
    match_pct = models.FloatField(default=None, help_text='Match pct of the voter and candidate', null=True)
    favorite = models.BooleanField(default=False)
    support = models.BooleanField(default=False)
    protest = models.BooleanField(default=False)

    calculated_status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Voter Candidate Matches'

    def __str__(self):
        return str(self.candidate)

    def toggle_fav(self):
        self.favorite = not self.favorite
        self.save()

    def toggle_support(self):
        if self.protest:
            self.protest = not self.protest
        self.support = not self.support
        self.candidate.toggle_supporter('+' if self.support else '-')
        self.save()

    def toggle_protest(self):
        if self.support:
            self.support = not self.support
        self.protest = not self.protest
        self.candidate.toggle_protester('+' if self.protest else '-')
        self.save()

    @staticmethod
    def calculate_voter_match_score():
        pass