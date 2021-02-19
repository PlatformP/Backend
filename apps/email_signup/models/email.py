from django.db import models


class email(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email
