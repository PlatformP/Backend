from django.db import models


class Survey(models.Model):
    SURVEY_TYPE = [
        (0, 'general'),
        (1, 'city'),
        (2, 'county'),
        (3, 'state'),
        (4, 'national')
    ]

    name = models.CharField(default='__default__', max_length=50)
    survey_type = models.PositiveSmallIntegerField(default=0, choices=SURVEY_TYPE)

    def __str__(self):
        return self.name
