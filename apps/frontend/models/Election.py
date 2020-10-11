from django.db import models


class Election(models.Model):
    STATUS_CHOICE_FIELD = [
        (1, 'Future'),
        (0, 'Past')
    ]

    name = models.CharField(max_length=100)
    date = models.DateField()
    location = models.ForeignKey('frontend.Location', on_delete=models.SET_NULL, blank=False, null=True)
    status = models.SmallIntegerField(default=1, choices=STATUS_CHOICE_FIELD)

    class Meta:
        verbose_name = 'Election'
        verbose_name_plural = 'Elections'

    def __str__(self):
        return self.name

    def set_status_past(self):
        self.status = 0
        self.save()