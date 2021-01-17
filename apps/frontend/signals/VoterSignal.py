from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.frontend.models.Voter import Voter
from apps.frontend.models.Election import Election
from apps.frontend.models.VoterCandidateMatch import VoterCandidateMatch
from apps.frontend.models.Candidate import Candidate

from Backend.settings import US_GEO_CONFIG
from Scripts.HelperMethods import get_key_from_state

from numpy import array
from random import randint


@receiver(signal=post_save, sender=Voter)
def create_candidate_match_on_create(sender, instance, created, **kwargs):
    if created:
        zipcode_df = US_GEO_CONFIG.query_postal_code(instance.zipcode.zipcode)

        national_elections_candidate_ids = set(
            Election.objects.filter(type=3).values_list('electioninline__candidate_id', flat=True))
        state_elections_candidate_ids = set(
            Election.objects.filter(location__state=get_key_from_state(zipcode_df.state_code),
                                    type=2).values_list('electioninline__candidate_id', flat=True))
        county_elections_candidate_ids = set(
            Election.objects.filter(location__county=zipcode_df.county_name, type=1).values_list(
                'electioninline__candidate_id', flat=True))
        city_elections_candidate_ids = set(
            Election.objects.filter(location__city=zipcode_df.place_name, type=0).values_list(
                'electioninline__candidate_id', flat=True))

        candidate_id_union = national_elections_candidate_ids | state_elections_candidate_ids | \
                                county_elections_candidate_ids | city_elections_candidate_ids

        candidate_id_array = array(list(candidate_id_union))

        for pk in candidate_id_array:
            candidate = Candidate.objects.get(pk=pk)
            voter_candidate_match_instance = VoterCandidateMatch.objects.create(candidate=candidate, voter=instance)

            voter_candidate_match_instance.match_pct = randint(0, 100)
            voter_candidate_match_instance.save()
