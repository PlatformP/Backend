from django.db import models
from django.contrib.auth.models import User


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    political_party = models.ForeignKey('PoliticalParty', on_delete=models.SET_NULL, null=True)

    profile_picture = models.ImageField(upload_to='candidate_pb', blank=True)
    bio = models.TextField(default=None, null=True)
    popularity = models.FloatField(default=None, null=True, blank=True)
    supporters = models.IntegerField(default=None, null=True, blank=True)
    protesters = models.IntegerField(default=None, null=True, blank=True)

    #protestor_supporter_df = models.JSONField()

    class Meta:
        verbose_name = 'Candidates'
        verbose_name_plural = 'Candidates'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def get_image_path(self):
        try:
            return self.profile_picture.path
        except ValueError:
            return False

    def toggle_supporter(self, operation):
        self.supporters = self.supporters + 1 if operation == '+' else self.supporters - 1
        self.save()

    def toggle_protester(self, operation):
        self.protesters = self.protesters + 1 if operation == '+' else self.protesters - 1
        self.save()