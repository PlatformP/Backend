from django.urls import include, path
from rest_framework import routers

from .views.EmailView import EmailViewSet

router = routers.DefaultRouter()
router.register(r'signup', EmailViewSet)

urlpatterns = [
    path('', include(router.urls))
]