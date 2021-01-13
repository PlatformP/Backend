from django.db import models


class Location(models.Model):
    STATE_CHOICES = [
        (0, 'AL'), (1, 'AK'), (2, 'AZ'), (3, 'AR'), (4, 'CA'), (5, 'CO'), (6, 'CT'), (7, 'DE'), (8, 'FL'), (9, 'GA'),
        (10, 'HI'), (11, 'ID'), (12, 'IL'), (13, 'IN'), (14, 'IN'), (15, 'IA'), (16, 'KS'), (17, 'KY'), (18, 'LA'),
        (19, 'ME'), (20, 'MD'), (21, 'MA'), (22, 'MI'), (23, 'MN'), (24, 'MS'), (25, 'MO'), (26, 'MT'), (27, 'NE'),
        (28, 'NV'), (29, 'NH'), (30, 'NJ'), (31, 'NM'), (32, 'NY'), (33, 'NC'), (34, 'ND'), (35, 'OH'), (36, 'OK'),
        (37, 'OR'), (38, 'PA'), (39, 'RI'), (40, 'SC'),  (41, 'SD'), (42, 'TN'), (43, 'TX'), (44, 'UT'), (45, 'VT'),
        (46, 'VA'), (47, 'WA'), (48, 'WV'), (49, 'WI'), (50, 'WY')
    ]

    city = models.CharField(max_length=50, blank=True, default=None, null=True)
    state = models.SmallIntegerField(default=0, choices=STATE_CHOICES)

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        if self.city is not None:
            return 'city: {}'.format(self.city)
        return 'state: {}'.format(self.STATE_CHOICES[self.state][-1])