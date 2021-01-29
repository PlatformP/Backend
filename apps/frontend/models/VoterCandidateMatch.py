from django.db import models

from Scripts.HelperMethods import similarity


class VoterCandidateMatch(models.Model):

    voter = models.ForeignKey('frontend.Voter', on_delete=models.CASCADE)
    candidate = models.ForeignKey('frontend.Candidate', on_delete=models.CASCADE)

    match_pct = models.FloatField(default=None, help_text='Match pct of the voter and candidate', null=True, blank=True)
    match_0 = models.FloatField(default=None, null=True, blank=True)
    match_1 = models.FloatField(default=None, null=True, blank=True)
    match_2 = models.FloatField(default=None, null=True, blank=True)
    match_3 = models.FloatField(default=None, null=True, blank=True)
    match_4 = models.FloatField(default=None, null=True, blank=True)

    favorite = models.BooleanField(default=False)
    support = models.BooleanField(default=False)
    protest = models.BooleanField(default=False)

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

    #def get_matches(self):
    @classmethod
    def calculate_voter_match_score(cls, candidate_id, candidate_vector, voter_id, voter_vector):
        match = similarity(candidate_vector, voter_vector)
        obj = cls.objects.get(candidate_id=candidate_id, voter_id=voter_id)
        obj.match_pct = match
        return obj
