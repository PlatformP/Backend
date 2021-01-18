from django.db import models


class SurveyQuestion(models.Model):
    question = models.TextField()

    def __str__(self):
        return self.question
