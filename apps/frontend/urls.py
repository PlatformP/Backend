from django.urls import include, path
from rest_framework import routers
from .views.CandidateView import CandidateViewSet
from .views.UserView import UserViewSet
from .views.ElectionView import ElectionViewSet
from .views.LocationView import LocationViewSet
from .views.PolicyView import PolicyViewSet
from .views.ElectionInLineView import ElectionInLineViewSet
from .views.VoterFavElectionsView import VoterFavElectionViewSet
from .views.VoterView import VoterViewSet
from .views.PoliticalPartyView import PoliticalPartyViewSet

router = routers.DefaultRouter()
router.register(r'Candidate', CandidateViewSet)
router.register(r'Election', ElectionViewSet)
router.register(r'Location', LocationViewSet)
router.register(r'Policies', PolicyViewSet)
router.register(r'User', UserViewSet)
router.register(r'ElectionInLine', ElectionInLineViewSet)
router.register(r'VoterFavElections', VoterFavElectionViewSet)
router.register(r'Voter', VoterViewSet)
router.register(r'PoliticalParty', PoliticalPartyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]