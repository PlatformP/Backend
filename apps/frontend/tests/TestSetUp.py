from Scripts.utils.TestSetUp import frontend_db_set_up
from django.test import TestCase


class TestSetUp(TestCase):
    def setUp(self) -> None:
        frontend_db_set_up()
