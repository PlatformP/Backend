from django.db import models

from pandas import DataFrame


class PoliticalParty(models.Model):
    NAME_CHOICES = [
        (0, 'Democrat'),
        (1, 'Republican'),
        (2, 'Independent'),
        (3, 'Constitutional Party'),
        (4, 'Libertarian'),
        (5, 'Green'),
        (6, 'No Affiliation'),
    ]

    COLOR_DICT = {
        0: 'blue',
        1: 'red',
        2: 'grey',
        3: 'orange',
        4: 'gold',
        5: 'green',
        6: 'silver'
    }

    name = models.SmallIntegerField(default=6, choices=NAME_CHOICES)
    logo = models.ImageField(upload_to='party_logo', null=True)

    class Meta:
        verbose_name_plural = 'Political Parties'

    def __str__(self):
        return self.NAME_CHOICES[self.name][1]

    def get_image_path(self):
        return self.logo.path

    def get_df(self) -> DataFrame:
        """
        gets the df
        :return:
        """
        df_political_party = DataFrame.from_dict(data={'id': self.id,
                                                       'party': self.NAME_CHOICES[self.name][-1],
                                                       'party_color': self.COLOR_DICT[self.name]}, orient='index').T
        df_political_party.set_index('id', inplace=True)
        return df_political_party
