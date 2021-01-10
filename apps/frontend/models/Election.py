from django.db import models


class Election(models.Model):
    STATUS_CHOICE_FIELD = [
        (1, 'Future'),
        (0, 'Past')
    ]

    ELECTION_TYPE_CHOICES = [
        (0, 'City'),
        (1, 'State'),
        (2, 'National')
    ]

    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(max_length=250)
    location = models.ForeignKey('frontend.Location', on_delete=models.SET_NULL, blank=False, null=True)
    type = models.SmallIntegerField(default=0, choices=ELECTION_TYPE_CHOICES)
    status = models.SmallIntegerField(default=1, choices=STATUS_CHOICE_FIELD)

    # electionJSON = models.JSONField()

    class Meta:
        verbose_name = 'Election'
        verbose_name_plural = 'Elections'

    def __str__(self):
        return self.name

    def set_status_past(self):
        self.status = 0
        self.save()
