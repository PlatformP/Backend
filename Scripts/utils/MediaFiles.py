from os import remove
from os.path import exists


def delete_picture(path):
    if exists(path):
        remove(path)
