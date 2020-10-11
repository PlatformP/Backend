from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models.Candidate import Candidate
from os import remove

#@receiver(pre_delete)
#def delete_profile_pic(sender, instance, **kwargs):
#    print('sender: {}, instance: {}, kwagrs: {}'.format(sender, instance, kwargs))
