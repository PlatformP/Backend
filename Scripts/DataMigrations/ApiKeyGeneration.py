from rest_framework_api_key.models import APIKey
from CandidPoliticsBackend.settings import BASE_DIR


def generate_store_key():
    '''
    creates and stores a key on in a text file
    will be run as a cronjob on the server
    :return: the API key
    '''
    try:
        file = open(str(BASE_DIR) + '\\api_key.txt', 'w')
        if APIKey.objects.filter(name='frontend_key'):
            APIKey.objects.filter(name='frontend_key').delete()
        _, key = APIKey.objects.create_key(name='frontend_key')
        file.write(key)
        file.close()

    except FileNotFoundError:
        print('File wasnt found')

    return key


generate_store_key()
