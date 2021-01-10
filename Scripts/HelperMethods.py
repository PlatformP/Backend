from datetime import date
from pandas import DataFrame

from django.contrib.auth.models import User
from apps.frontend.models.PoliticalParty import PoliticalParty
from apps.frontend.models.ElectionInLine import ElectionInLine
from apps.frontend.models.Election import Election
from apps.frontend.models.Candidate import Candidate
from apps.frontend.models.VoterCandidateMatch import VoterCandidateMatch
from apps.frontend.models.Location import Location


def date_time_converter(o):
    if isinstance(o, date):
        return o.__str__()


def get_candidate_df(candidate_ids, user):
    # getting the political party DF
    df_political_party_orig = DataFrame.from_records(PoliticalParty.objects.values())
    df_political_party = DataFrame(columns=['id', 'party', 'party_color'])
    df_political_party['id'] = df_political_party_orig['id']
    df_political_party['party'] = df_political_party_orig['name'].map(dict(PoliticalParty.NAME_CHOICES))
    df_political_party['party_color'] = df_political_party_orig['name'].map(PoliticalParty.COLOR_DICT)
    df_political_party.set_index('id', inplace=True)

    df_candidates = DataFrame.from_records(Candidate.objects.filter(id__in=candidate_ids).values())
    df_candidates['political_party_id'] = df_candidates['political_party_id'].map(df_political_party
                                                                                  .to_dict(orient='index'))

    # getting User DF
    df_user = DataFrame.from_records(User.objects.filter(id__in=df_candidates['user_id'])
                                     .values('id', 'first_name', 'last_name'))
    df_user.set_index('id', inplace=True)

    # placing user info into candidate df
    df_candidates['user_id'] = df_candidates['user_id'].map(df_user.to_dict(orient='index'))
    df_candidates.rename(columns={'political_party_id': 'political_party', 'user_id': 'user'}, inplace=True)

    df_voter_candidate_match = DataFrame.from_records(VoterCandidateMatch.objects.filter(voter__user=user,
                                                                                         candidate__pk__in=candidate_ids
                                                                                         ).values('candidate_id',
                                                                                                  'match_pct',
                                                                                                  'favorite'))
    df_voter_candidate_match.set_index('candidate_id', inplace=True)
    df_candidates['voter_match'] = df_candidates['id'].map(df_voter_candidate_match.to_dict(orient='index'))

    return df_candidates


def get_ballot_by_queryset2(queryset, user):
    '''
    function that gets a json of the ballot
    :param queryset:
    :param user:
    :return:
    '''
    candidate_ids = set(ElectionInLine.objects.filter(election__pk__in=set(queryset.values_list('id', flat=True)))
                        .values_list('candidate_id', flat=True))

    df_candidates = get_candidate_df(candidate_ids=candidate_ids, user=user)

    df_election = DataFrame.from_records(queryset.values())

    location_ids = set(df_election['location_id'])
    df_location = DataFrame.from_records(Location.objects.filter(pk__in=location_ids).values())
    df_location.set_index('id', inplace=True)

    df_election['location_id'] = df_election['location_id'].map(df_location.to_dict(orient='index'))

    df_election.rename(columns={'location_id': 'location'}, inplace=True)
    df_candidates.set_index('id', inplace=True, drop=False)

    def candidate_in_election(x):
        return df_candidates.loc[Election.objects.get(pk=x).
            electioninline_set.values_list('candidate_id', flat=True)].to_dict(orient='records')

    df_election['candidates'] = df_election['id'].map(candidate_in_election)

    return df_election.to_json(orient='records')
