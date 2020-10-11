from rest_framework import serializers

from .models.Candidate import Candidate
from .models.Election import Election
from .models.Location import Location
from .models.Policy import Policy
from .models.Election_InLine import Election_InLine
from .models.Voter import Voter
from .models.Voter_FavElections import Voter_FavElections

from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name', 'email', 'password']


class CandidateSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='user-detail',
        queryset=User.objects.all()
    )

    class Meta:
        model = Candidate
        fields = ['url', 'user', 'bio', 'location', 'is_verified']


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ['url', 'city', 'state']


class ElectionSerializer(serializers.HyperlinkedModelSerializer):
    location = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='location-detail',
        queryset=Location.objects.all()
    )

    class Meta:
        model = Election
        fields = ['url', 'name', 'location', 'status', 'date']


class PolicySerializer(serializers.HyperlinkedModelSerializer):
    candidate = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='candidate-detail',
        queryset=Candidate.objects.all()
    )

    class Meta:
        model = Policy
        fields = ['url', 'description', 'candidate']


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
        model = Election_InLine
        fields = ['url', 'election', 'candidate']


class VoterSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='user-detail',
        queryset=User.objects.all()
    )

    class Meta:
        model = Voter
        fields = ['user', ]

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
        model = Voter_FavElections
        fields = ['election', 'voter']