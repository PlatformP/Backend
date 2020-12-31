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


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username']


class CandidateSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='user-detail',
        queryset=User.objects.all()
    )
    political_party = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='politicalparty-detail',
        queryset=PoliticalParty.objects.all()
    )

    class Meta:
        model = Candidate
        fields = ['url', 'id', 'user', 'bio', 'political_party']


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ['url', 'id', 'city', 'state']


class ElectionSerializer(serializers.HyperlinkedModelSerializer):
    location = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='location-detail',
        queryset=Location.objects.all()
    )

    class Meta:
        model = Election
        fields = ['url', 'id', 'name', 'description', 'location', 'status', 'date']


class PolicySerializer(serializers.HyperlinkedModelSerializer):
    candidate = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='candidate-detail',
        queryset=Candidate.objects.all()
    )

    class Meta:
        model = Policy
        fields = ['url', 'id', 'description', 'candidate']


class ElectionInLineSerializer(serializers.HyperlinkedModelSerializer):
    election = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='election-detail',
        queryset=Election.objects.all()
    )
    candidate = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='candidate-detail',
        queryset=Candidate.objects.all()
    )

    class Meta:
        model = ElectionInLine
        fields = ['url', 'id', 'election', 'candidate']


class VoterSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='user-detail',
        queryset=User.objects.all()
    )

    class Meta:
        model = Voter
        fields = ['url', 'id', 'user']

class VoterFavElectionsSerializer(serializers.HyperlinkedModelSerializer):
    election = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='election-detail',
        queryset=Election.objects.all()
    )

    voter = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='voter-detail',
        queryset=Voter.objects.all()
    )

    class Meta:
        model = VoterFavElections
        fields = ['url', 'id', 'election', 'voter']


class PoliticalPartySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PoliticalParty
        fields = ['url', 'id', 'name']
