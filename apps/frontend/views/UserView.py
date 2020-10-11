from rest_framework.decorators import action, api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from apps.frontend.serializers import UserSerializer

from apps.frontend.models.Candidate import Candidate

from ast import literal_eval


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def sign_up(self, request):
        """
        custom method to create candidates. Lives at the API/User/create_candidate
        :param request:
        :return:
        """
        request_dict = literal_eval(request.body.decode("UTF-8"))
        # checking if User exists
        if User.objects.filter(username=request_dict['username']):
            return Response(data='username used', status=status.HTTP_226_IM_USED)
        if User.objects.filter(email=request_dict['email']):
            return Response(data='email used', status=status.HTTP_226_IM_USED)

        user = User.objects.create_user(**request_dict)
        Candidate.objects.get_or_create(user=user)
        send_verification_email(user=user)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        custom method which checks user credentials for login
        :param request:
        :return:
        """
        from Scripts.HelperMethods import get_username

        request_dict = literal_eval(request.body.decode("UTF-8"))
        username = get_username(request_dict['username'])
        user = authenticate(username=username, password=request_dict['password'])
        if user is not None:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(data='username or password do not exist', status=status.HTTP_418_IM_A_TEAPOT)

    @action(detail=False, methods=['post'])
    def password_reset_request(self, request):
        """
        method for password reset
        :param request:
        :return:
        """
        from Scripts.HelperMethods import get_username
        from rest_framework_simplejwt.tokens import RefreshToken
        from json import dumps
        from CandidPoliticsBackend.settings import BASE_URL
        from django.utils.timezone import timedelta

        request_dict = literal_eval(request.body.decode)
        username = get_username(request_dict['username'])

        user = User.objects.get(username=username)
        token = RefreshToken.for_user(user)
        token.lifetime = timedelta(minutes=30)
        url_endpoint = '{}/passwordreset/{}'.format(BASE_URL, str(token.access_token))
        return Response(data=dumps(token), status=status.HTTP_200_OK)


@api_view(http_method_names=['post'])
def password_reset(request):
    pass

def send_verification_email(user):
    from django.core.mail import send_mail

    kwargs = {
        'subject': 'Candid-Politics Verification',
        'message': 'This is a test',
        'from_email': None,
        'recipient_list': [user.email]
    }
    send_mail(**kwargs)
