from django.urls import include, path
from rest_framework import routers
from .views.ElectionView import ElectionViewSet
from .views.VoterView import VoterViewSet

router = routers.DefaultRouter()
router.register(r'Election', ElectionViewSet)
router.register(r'Voter', VoterViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]