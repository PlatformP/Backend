import django
import os
import sys
from django.utils import timezone

BASE_PATH = os.path.dirname('../CandidPoliticsBackend/')
sys.path.append(BASE_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'CandidPoliticsBackend.settings'
django.setup()


def retrieve_elections():
    """
    method for retrieving elections from the google civic API
    link to the API -> https://developers.google.com/civic-information
    :return: List of disctionaries with keys -> id, name, electionDay, ocdDividionId
    """
    from CandidPoliticsBackend.settings import GOOGLE_API_KEY
    import requests
    from ast import literal_eval
    from datetime import datetime

    r = requests.get(
        'https://www.googleapis.com/civicinfo/v2/elections?key=' + GOOGLE_API_KEY)  # requesting data from google
    e_str = r.content.decode("UTF-8")  # turning bytes data into string
    e_dict = literal_eval(e_str)['elections']  # list of elections stored as dictionaries
    for election in e_dict:
        election['electionDay'] = datetime.strptime(election['electionDay'], '%Y-%m-%d').date()  # str -> date

    return e_dict[1:]


def set_up_elections():
    """
    retrieves elections and sets up the models for it
    """
    from apps.frontend.models.Election import Election
    from apps.frontend.models.Location import Location

    election_list = retrieve_elections()

    for election in election_list:
        kwargs_location = {
            'state': election['ocdDivisionId'].split('/')[-1].split(':')[-1]
        }
        location = Location.objects.get_or_create(**kwargs_location)[0]

        kwargs_election = {
            'name': election['name'],
            'date': election['electionDay'],
            'location': location
        }
        Election.objects.get_or_create(**kwargs_election)


def election_status_update():
    """
    checks for election date and sets it to past if the election has passed
    """
    from apps.frontend.models.Election import Election

    for election in Election.objects.all():
        if election.date < timezone.now().date():
            election.set_status_past()


def run():
    """
    will be run as a chronjob
    """
    set_up_elections()
    election_status_update()


run()
