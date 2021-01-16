from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.frontend.models.ElectionInLine import ElectionInLine
from apps.frontend.models.VoterCandidateMatch import VoterCandidateMatch
from apps.frontend.models.Voter import Voter

from pandas import DataFrame

'''
@receiver(post_save, sender=ElectionInLine)
def handler(sender, instance, created, **kwargs):
    if created:
        if instance.election.type == 0:
            #Filter only city voter
            pass
        elif instance.election.type == 1:
            #Filter all Voters from the same county
            pass
        elif instance.election.type == 2:
            #All ELections on the state level
            pass
        else:
            #Filter all Voters on a national level
            voters = DataFrame.from_records(Voter.objects.all())
            voters['id'].map(lambda pk : VoterCandidateMatch.objects.create(voter=pk, candidate=instance.candidate_id))
'''