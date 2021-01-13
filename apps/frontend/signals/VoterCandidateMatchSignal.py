from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.frontend.models.ElectionInLine import ElectionInLine


@receiver(post_save, sender=ElectionInLine)
def handler(sender, instance, created, **kwargs):
    if created:
        location = instance.location
        pass
