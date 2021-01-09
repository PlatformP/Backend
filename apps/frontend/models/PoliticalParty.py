from django.db import models


class PoliticalParty(models.Model):
    NAME_CHOICES = [
        (0, 'Democrat'),
        (1, 'Republican'),
        (2, 'Independent'),
        (3, 'Constitutional Party'),
        (4, 'Libertarian')
        (5, 'Green'),
        (6, 'No Affiliation'),
    ]

    name = models.SmallIntegerField(default= 6, choices=NAME_CHOICES)
    logo = models.ImageField(upload_to='party_logo', null=True)

    class Meta:
        verbose_name_plural = 'Political Parties'

    def __str__(self):
        return self.NAME_CHOICES[self.name][1]

    def get_color(self):
        if self.name == 0:
            return 'blue'
        elif self.name == 1:
            return 'red'
        elif self.name == 2:
            return 'grey'
        elif self.name == 3:
            return 'orange'
        elif self.name == 4:
            return 'gold'
        elif self.name == 5:
            return 'green'
        else:
            return None