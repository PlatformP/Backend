from django.db import models
from django.contrib.auth.models import User

from datetime import date as dt


class Voter(models.Model):
    GENDER_CHOICES = [
        (0, 'Male'),
        (1, 'Female'),
        (2, 'Other')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    zipcode = models.ForeignKey('ZipCode', on_delete=models.SET_NULL, null=True)
    gender = models.SmallIntegerField(default=0, choices=GENDER_CHOICES)

    dob = models.DateField(default=None, null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def save(self, *args, **kwargs):
        '''
        making sure the dob is the right format
        otherwise making it a datetime object
        '''
        self.dob = dt.fromtimestamp(self.dob / 1000)

        super(Voter, self).save(*args, **kwargs)
