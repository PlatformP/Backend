from django.db import models


class Policy(models.Model):
    description = models.TextField(blank=False)
    candidate = models.ForeignKey('frontend.Candidate', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Policies'
