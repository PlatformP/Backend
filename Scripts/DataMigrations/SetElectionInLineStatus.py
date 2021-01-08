import django
import os
import sys
from django.utils.timezone import now
BASE_PATH = os.path.dirname('../Backend/')
sys.path.append(BASE_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Backend.settings'
django.setup()

from apps.frontend.models.ElectionInLine import ElectionInLine


def set_status():
    election_inline_queryset = ElectionInLine.objects.filter(status__in=[0,2])

    for election_inline in election_inline_queryset:
        if election_inline.status == 0 and (now().date() - election_inline.date_joined).days > 7:
            print(f'setting current status for {str(election_inline.candidate)} for election {str(election_inline.election)}')
            election_inline.set_status(1)
        elif election_inline.status == 2 and (now().date() - election_inline.date_dropped).days > 3:
            print(f'dropping {str(election_inline.candidate)} from {str(election_inline.election)}')
            election_inline.delete()


set_status()