from django.db import models


class PoliticalParty(models.Model):
    NAME_CHOICES = [
        (0, 'Democrat'),
        (1, 'Republican'),
        (2, 'Independent'),
        (3, 'Green'),
        (4, 'No Affiliation'),
    ]

    name = models.SmallIntegerField(choices=NAME_CHOICES)
    logo = models.ImageField(upload_to='party_logo', null=True)

    class Meta:
        verbose_name_plural = 'Political Parties'

    def __str__(self):
        return self.NAME_CHOICES[self.name][1]
