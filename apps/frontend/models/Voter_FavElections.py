from django.db import models


class Voter_FavElections(models.Model):
    voter = models.ForeignKey('Voter', on_delete=models.CASCADE)
    election = models.ForeignKey('Election', on_delete=models.CASCADE)
