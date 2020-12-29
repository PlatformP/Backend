from django.db import models


class Candidate(models.Model):

    auth0_id = models.IntegerField(default=None, null=False, primary_key=True)
    political_party = models.ForeignKey('PoliticalParty', on_delete=models.SET_NULL, null=True)
    bio = models.TextField(default=None, null=True)

    class Meta:
        verbose_name = 'Candidates'
        verbose_name_plural = 'Candidates'

    def __str__(self):
        return f'{self.auth0_id}'