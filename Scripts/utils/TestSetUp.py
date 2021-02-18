from django.contrib.auth.models import User

from apps.frontend.models.Candidate import Candidate
from apps.frontend.models.SurveyQuestion import SurveyQuestion
from apps.frontend.models.Survey import Survey
from apps.frontend.models.ZipCode import ZipCode
from apps.frontend.models.PoliticalParty import PoliticalParty
from apps.frontend.models.Location import Location
from apps.frontend.models.Voter import Voter
from apps.frontend.models.VoterCandidateMatch import VoterCandidateMatch
from apps.frontend.models.Election import Election
from apps.frontend.models.ElectionInLine import ElectionInLine
from apps.frontend.models.SurveyQuestionAnswers import SurveyQuestionAnswers
from apps.frontend.models.VoterFavElections import VoterFavElections

from django.utils.timezone import now

from random import randint


def zipcode_set_up():
    ZipCode.objects.create(zipcode=84112)


def survey_set_up():
    Survey.objects.create(name='survey0', survey_type=0)


def survey_question_set_up():
    survey = Survey.objects.get(name='survey0')

    question_list = [
        'question1',
        'question2',
        'question3',
        'question4'
    ]

    for question in question_list:
        SurveyQuestion.objects.create(survey=survey, question=question)


def political_party_set_up():
    PoliticalParty.objects.create(name=0)


def location_set_up():
    Location.objects.create(city='Salt Lake City', state=44)


def candidate_set_up():
    # creating users for the candidates
    candidate_users = {
        'u1': {'username': 'u1', 'password': 'p1'},
        'u2': {'username': 'u2', 'password': 'p2'},
        'u3': {'username': 'u3', 'password': 'p3'},
    }

    for value in candidate_users.values():
        User.objects.create_user(**value)

    # creating the candidates
    candidate_kwargs = {
        'popularity': 0,
        'supporters': 0,
        'protesters': 0
    }
    for username in candidate_users.keys():
        user = User.objects.get(username=username)
        Candidate.objects.create(user=user, **candidate_kwargs)


def election_set_up():
    election_kwargs = {
        'name': 'elec1',
        'date': now().date(),
        'description': 'this is a description',
        'location': Location.objects.get(city='Salt Lake City'),
        'type': 0,
        'status': 0
    }

    election = Election.objects.create(**election_kwargs)

    # adding candidates to the election
    # for candidate in Candidate.objects.all():
    #    ElectionInLine.objects.create(election=election, candidate=candidate)


def voter_set_up():
    user = User.objects.create(username='v1', password='p1')

    zipcode = ZipCode.objects.get(zipcode=84112)

    voter = Voter.objects.create(user=user, zipcode=zipcode)

    for candidate in Candidate.objects.all():
        VoterCandidateMatch.objects.create(voter=voter, candidate=candidate)

    for election in Election.objects.all():
        VoterFavElections.objects.create(election=election, voter=voter)


def election_in_line_set_up():
    for election in Election.objects.all():
        for candidate in Candidate.objects.all():
            ElectionInLine.objects.create(election=election, candidate=candidate)


def survey_question_answer_set_up():
    for question in SurveyQuestion.objects.all():
        for candidate in Candidate.objects.all():
            SurveyQuestionAnswers.objects.create(candidate=candidate, question=question, answer=randint(0, 4))

        for voter in Voter.objects.all():
            SurveyQuestionAnswers.objects.create(voter=voter, question=question, answer=randint(0, 4))


def frontend_db_set_up():
    zipcode_set_up()
    location_set_up()
    survey_set_up()
    survey_question_set_up()
    political_party_set_up()
    candidate_set_up()
    voter_set_up()
    election_set_up()
    survey_question_answer_set_up()
