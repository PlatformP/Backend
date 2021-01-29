from django.db import models


class Base(models.Model):
    class Meta:
        abstract = True

    def update_with_kwargs(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()
