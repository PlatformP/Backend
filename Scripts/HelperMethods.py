def initialize_request():
    """
    :return: a requests session with the FRONTEND_API_KEY stored in settings.py
    """
    from requests import Session
    # from CandidPoliticsBackend.settings import FRONTEND_API_KEY

    sess = Session()
    # sess.headers.update({'Api-Key': FRONTEND_API_KEY})

    return sess


def set_frontend_api_key():
    from CandidPoliticsBackend.settings import BASE_DIR

    try:
        FRONTEND_API_KEY = open(str(BASE_DIR) + '\\api_key.txt').read()
    except FileNotFoundError:
        from Scripts.DataMigrations.ApiKeyGeneration import generate_store_key
        FRONTEND_API_KEY = generate_store_key()

    return FRONTEND_API_KEY


def get_username(user):
    from django.contrib.auth.models import User
    is_email = '@' in user
    try:
        if is_email:
            return User.objects.filter(email=user)[0].username
        else:
            return user
    except:
        return False