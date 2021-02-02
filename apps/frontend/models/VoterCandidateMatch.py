from django.db import models

from Scripts.HelperMethods import similarity

from numpy import array, append, mean


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

    def toggle_support(self) -> candidate:
        if self.protest:
            self.protest = False
            self.candidate.toggle_protester('-')
        self.support = not self.support
        self.candidate.toggle_supporter('+' if self.support else '-')
        self.save()

        return self.candidate

    def toggle_protest(self) -> candidate:
        if self.support:
            self.support = False
            self.candidate.toggle_supporter('-')
        self.protest = not self.protest
        self.candidate.toggle_protester('+' if self.protest else '-')
        self.save()

        return self.candidate

    def update_match_pct(self, save=False):
        survey_types = [0, 1, 2, 3, 4]
        match_arr = array([])
        for survey_type in survey_types:
            match = getattr(self, f'match_{survey_type}')
            if match is not None:
                match_arr = append(match_arr, match)

        print(f'candidate {str(self.candidate)} with {mean(match_arr)}, array {match_arr}')

        self.match_pct = mean(match_arr)

        if save:
            self.save()

    @classmethod
    def calculate_voter_match_score(cls, candidate_id, candidate_vector, voter_id, voter_vector, survey_type):
        match = similarity(candidate_vector, voter_vector)
        obj = cls.objects.get(candidate_id=candidate_id, voter_id=voter_id)
        setattr(obj, f'match_{survey_type}', match)
        obj.update_match_pct()
        return obj
