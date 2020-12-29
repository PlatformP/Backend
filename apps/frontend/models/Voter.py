from django.db import models


class Voter(models.Model):

    auth0_id = models.IntegerField(default=None, null=False, primary_key=True)

    def __str__(self):
        return f'{self.auth0_id}'