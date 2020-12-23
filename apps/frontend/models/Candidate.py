from django.db import models
from django.contrib.auth.models import User


class Candidate(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='candidate_picture', null=True)
    political_party = models.ForeignKey('PoliticalParty', on_delete=models.SET_NULL, null=True)
    bio = models.TextField(default=None, null=True)

    is_verified = models.BooleanField(default=None, null=False)

    class Meta:
        verbose_name = 'Candidates'
        verbose_name_plural = 'Candidates'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
