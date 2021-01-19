from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.frontend.models.PoliticalParty import PoliticalParty
from apps.frontend.models.Candidate import Candidate

from Scripts.utils.MediaFiles import delete_picture


@receiver(signal=post_delete, sender=PoliticalParty)
@receiver(signal=post_delete, sender=Candidate)
def delete_photo_on_delete(instance, **kwargs):
    if path := instance.get_image_path:
        delete_picture(path)
