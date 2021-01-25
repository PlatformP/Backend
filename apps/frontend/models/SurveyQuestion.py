from django.db import models


class SurveyQuestion(models.Model):

    question = models.TextField()
    survey = models.ForeignKey('frontend.Survey', on_delete=models.CASCADE)

    def __str__(self):
        return self.question
