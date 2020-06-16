from django.test import TestCase


class UserModelTestCase(TestCase):
    def test_project_setup(self):
        self.assertEqual("Hello World!", "Hello World!")
