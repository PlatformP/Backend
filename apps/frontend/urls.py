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

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'Candidate', CandidateViewSet)
router.register(r'Election', ElectionViewSet)
router.register(r'Location', LocationViewSet)
router.register(r'Policies', PolicyViewSet)
router.register(r'User', UserViewSet)
router.register(r'ElectionInLine', ElectionInLineViewSet)
router.register(r'VoterFavElections', VoterFavElectionViewSet)
router.register(r'Voter', VoterViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]