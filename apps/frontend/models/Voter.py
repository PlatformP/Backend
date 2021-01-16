from django.db import models
from django.contrib.auth.models import User


class Voter(models.Model):

    GENDER_CHOICES = [
        (0, 'Male'),
        (1, 'Female'),
        (2, 'Other')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    zipcode = models.ForeignKey('ZipCode', on_delete=models.SET_NULL, null=True)
    gender = models.SmallIntegerField(default=0, choices=GENDER_CHOICES)
    age = models.PositiveSmallIntegerField(default=None, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}'
