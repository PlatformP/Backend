from django.db import models

class SurveyQuestionInLine(models.Model):

    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE, null=True, blank=True)
    voter = models.ForeignKey('Voter', on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey('SurveyQuestion', on_delete=models.CASCADE, null=True)

    answer = models.PositiveSmallIntegerField()