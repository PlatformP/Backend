from django.contrib.auth.models import User


def get_user():
    return User.objects.get(username='google-oauth2.102111345942287213137')
