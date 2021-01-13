from django.db import models


class ZipCode(models.Model):

    zipcode = models.IntegerField()

    def __str__(self):
        return str(self.zipcode)
