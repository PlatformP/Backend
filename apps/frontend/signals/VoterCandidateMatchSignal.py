from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.frontend.models.ElectionInLine import ElectionInLine
from apps.frontend.models.VoterCandidateMatch import VoterCandidateMatch
from apps.frontend.models.Voter import Voter

from pandas import DataFrame


@receiver(post_save, sender=ElectionInLine)
def handler(sender, instance, created, **kwargs):
    if created:
        if instance.election.type == 0:
            #City Level
            voters = DataFrame.from_records(
                Voter.objects.filter(zipcode__place_name=instance.election.location.city).values('id'))
            voters['id'].map(lambda pk : VoterCandidateMatch.objects.create(voter=pk, candidate=instance.candidate_id))
            pass
        elif instance.election.type == 1:
            #County Level
            voters = DataFrame.from_records(
                Voter.objects.filter(zipcode__county_name=instance.election.location.county).values('id'))
            voters['id'].map(lambda pk: VoterCandidateMatch.objects.create(voter=pk, candidate=instance.candidate_id))
            pass
        elif instance.election.type == 2:
            #State level
            voters = DataFrame.from_records(
                Voter.objects.filter(zipcode__state_key=instance.election.location.state).values('id'))
            voters['id'].map(lambda pk: VoterCandidateMatch.objects.create(voter=pk, candidate=instance.candidate_id))
            pass
        else:
            #Filter all Voters on a national level
            voters = DataFrame.from_records(Voter.objects.values('id'))
            voters['id'].map(lambda pk : VoterCandidateMatch.objects.create(voter=Voter.objects.get(pk=pk), candidate=instance.candidate))
