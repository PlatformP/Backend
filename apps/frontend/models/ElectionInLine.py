from django.db import models


class ElectionInLine(models.Model):

    STATUS_CHOICE_FIELD = [
        (0, 'New'),
        (1, 'Current'),
        (2, 'Dropped')
    ]

    election = models.ForeignKey('frontend.Election', on_delete=models.CASCADE, null=False)
    candidate = models.ForeignKey('frontend.Candidate', on_delete=models.CASCADE, null=False)

    status = models.SmallIntegerField(default=1, choices=STATUS_CHOICE_FIELD)
