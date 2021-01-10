from django.db import models


class ElectionInLine(models.Model):
    STATUS_CHOICE_FIELD = [
        (0, 'New'),
        (1, 'Current'),
        (2, 'Dropped')
    ]

    election = models.ForeignKey('frontend.Election', on_delete=models.CASCADE, null=False)
    candidate = models.ForeignKey('frontend.Candidate', on_delete=models.CASCADE, null=False)

    date_joined = models.DateField(auto_now_add=True)
    date_dropped = models.DateField(default=None, blank=True, null=True)
    status = models.SmallIntegerField(default=1, choices=STATUS_CHOICE_FIELD)

    def __str__(self):
        return f'{str(self.election)} - {str(self.candidate)}'

    def set_status(self, status):
        self.status = status
        self.save()
