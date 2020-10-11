from django.db import models


class Election_InLine(models.Model):
    election = models.ForeignKey('frontend.Election', on_delete=models.CASCADE, null=False)
    candidate = models.ForeignKey('frontend.Candidate', on_delete=models.CASCADE, null=False)
