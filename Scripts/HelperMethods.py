from datetime import date
from json import dumps
from apps.frontend.models.VoterCandidateMatch import VoterCandidateMatch


def date_time_converter(o):
    if isinstance(o, date):
        return o.__str__()


def get_ballot_by_queryset(queryset, user, voter_fav=False):
    """
    function that takes an election query set and returns a json of all the elections with their candiates
    :param queryset:
    :param user:
    :return:
    """
    instance_values = list(queryset.values())

    for i, instance in enumerate(queryset):
        candidate_list = []

        for candidate_q in instance.electioninline_set.all():
            d = candidate_q.candidate.get_dict(user=user)
            candidate_list.append(d)

        instance_values[i].update({'candidates': candidate_list})
    return dumps(instance_values, indent=4, default=date_time_converter)
