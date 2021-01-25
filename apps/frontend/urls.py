from django.urls import include, path
from rest_framework import routers
from .views.ElectionView import ElectionViewSet
from .views.CandidateView import CandidateViewSet
from .views.VoterView import VoterViewSet
from .views.SurveyView import SurveyViewSet

router = routers.DefaultRouter()
router.register(r'Election', ElectionViewSet)
router.register(r'Voter', VoterViewSet)
router.register(r'Candidate', CandidateViewSet)
router.register(r'Survey', SurveyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]