from django.db import models


class VoterFavElections(models.Model):
    voter = models.ForeignKey('Voter', on_delete=models.CASCADE)
    election = models.ForeignKey('Election', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.election)
