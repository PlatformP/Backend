from rest_framework import serializers

from .models.Candidate import Candidate
from .models.Election import Election
from .models.Location import Location
from .models.Policy import Policy
from .models.ElectionInLine import ElectionInLine
from .models.Voter import Voter
from .models.VoterFavElections import VoterFavElections
from .models.PoliticalParty import PoliticalParty

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'user', 'bio', 'political_party']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'city', 'state']


class ElectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Election
        fields = ['id', 'name', 'description', 'location', 'status', 'date']
        depth = 1


class PolicySerializer(serializers.ModelSerializer):

    class Meta:
        model = Policy
        fields = ['id', 'description', 'candidate']


class ElectionInLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = ElectionInLine
        fields = ['id', 'election_id', 'candidate']
        depth = 1


class VoterSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Voter
        fields = ['id', 'user']


class VoterFavElectionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = VoterFavElections
        fields = ['url', 'id', 'election', 'voter']


class PoliticalPartySerializer(serializers.ModelSerializer):

    class Meta:
        model = PoliticalParty
        fields = ['url', 'id', 'name']
