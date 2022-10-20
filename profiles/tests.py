from django.contrib.auth.models import User
from .models import Profile
from rest_framework.test import APITestCase


class ProfileCreatedTests(APITestCase):
    """
    Test to make sure that a profile is created everytime
    a new user is created
    """
    def setUp(self):
        ere = User.objects.create_user(username='ere', password='pass')
        dere = User.objects.create_user(username='dre', password='pass')
        dure = User.objects.create_user(username='dure', password='pass')

    def test_all_profiles_are_created(self):
        response = self.client.get('profiles')
        self.assertEqual(Profile.objects.count(), 3)
