from django.db import models
from django.contrib.auth.models import User


class Candidate(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    political_party = models.ForeignKey('PoliticalParty', on_delete=models.SET_NULL, null=True)

    profile_picture = models.ImageField(upload_to='candidate_pb', blank=True)
    bio = models.TextField(default=None, null=True)
    popularity = models.FloatField(default=None, null=True, blank=True)
    supporters = models.IntegerField(default=None, null=True, blank=True)

    class Meta:
        verbose_name = 'Candidates'
        verbose_name_plural = 'Candidates'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def get_image_path(self):
        return self.profile_picture.path