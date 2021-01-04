from django.db import models

class testinline(models.Model):

    v = models.ForeignKey('frontend.Voter', on_delete=models.CASCADE)
    c = models.ForeignKey('frontend.Candidate', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.c)