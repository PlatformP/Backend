from django.db import models


class Location(models.Model):
    STATE_CHOICES = [

    ]

    city = models.CharField(max_length=50, blank=True, default=None, null=True)
    state = models.CharField(max_length=20, blank=False, default=None)

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        if self.city is not None:
            return 'city: {}'.format(self.city)
        return 'state: {}'.format(self.state)